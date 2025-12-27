import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
import uvicorn
from sqlmodel import Session, select
from typing import List, Optional
from class_manager import Post, User, PostCreate, UserCreate, create_database
import pika
import json
from ml import classify_text
from starlette.concurrency import run_in_threadpool
import logging

# uvicorn rest_api:app --reload
# /docs# for SwaggerUI

engine = create_database()

app = FastAPI(title="Social Media API")

frontend_directory = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/frontend", StaticFiles(directory=frontend_directory), name="frontend")

thumbs_dir = os.path.join(os.path.dirname(__file__), "..", "data", "thumbs")
os.makedirs(thumbs_dir, exist_ok=True)
app.mount("/thumbs", StaticFiles(directory=thumbs_dir), name="thumbs")

def send_resize_message(post_id: int, image_full: str) -> None:
    rabbit_host = os.getenv("RABBIT_HOST", "queue")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbit_host)
    )
    channel = connection.channel()
    channel.queue_declare(queue="resize")

    message = {
        "post_id": post_id,
        "image_full": image_full,
    }
    channel.basic_publish(
        exchange="",
        routing_key="resize",
        body=json.dumps(message),
    )
    connection.close()


@app.get("/")
def root():
    return RedirectResponse(url="/posts")

@app.get("/users/{username}")
def redirect_user(username: str):
    return RedirectResponse(url=f"/users/{username}/posts")

@app.get("/posts")
def posts_f():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "html", "posts.html")
    return FileResponse(file_path)

@app.get("/users/{username}/posts")
def get_posts_by_user(username: str):
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "html", "posts.html")
    return FileResponse(file_path)

@app.get("/login")
def login_f():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "html", "login.html")
    return FileResponse(file_path)

@app.get("/create_post")
def create_post():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "html", "create_post.html")
    return FileResponse(file_path)

@app.get("/users")
def create_post():
    file_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "html", "users.html")
    return FileResponse(file_path)



@app.get("/api/users", response_model=List[User])
def api_get_all_users():
    with Session(engine) as session:
        users = session.exec(select(User).order_by(User.id.desc())).all()
        return users
    
@app.get("/api/users/{username}", response_model=User)
def api_get_user_by_username(username: str):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.name == username)).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@app.get("/api/users/{username}/posts", response_model=List[Post])
def api_get_posts_by_user(username: str, 
                          country: Optional[str] = Query(None, alias="country"),
                          filter: Optional[str] = Query(None, alias="filter")
                          ):
    with Session(engine) as session:
        query = select(Post).where(Post.user == username).order_by(Post.id.desc())
        if country:
            countries = country.split(",")
            query = query.where(Post.country.in_(countries))
        if filter:
            filters = filter.split(",")
            query = query.where(Post.filter.in_(filters))

        posts = session.exec(query).all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found for this user")
        return posts

@app.get("/api/posts", response_model=List[Post])
def api_get_all_posts(  country: Optional[str] = Query(None, alias="country"),
                        filter: Optional[str] = Query(None, alias="filter")
                    ):
    with Session(engine) as session:
        query = select(Post).order_by(Post.id.desc())
        if country:
            countries = country.split(",")
            query = query.where(Post.country.in_(countries))
        if filter:
            filters = filter.split(",")
            query = query.where(Post.filter.in_(filters))

        posts = session.exec(query).all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found")
        return posts

@app.get("/api/posts/{post_id}", response_model=Post)
def api_get_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

@app.post("/api/posts", response_model=Post, status_code=201)
def api_create_post(post: PostCreate):
    db_post = Post.model_validate(post)

    with Session(engine) as session:
        session.add(db_post)
        session.commit()
        session.refresh(db_post)

        send_resize_message(db_post.id, db_post.image_full)

        return db_post
    
@app.post("/api/users", response_model=User, status_code=201)
def api_create_user(user: UserCreate):
    with Session(engine) as session:
        # check if user already exists
        existing_user = session.exec(select(User).where(User.name == user.name)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # create new user if not found
        db_user = User(name=user.name)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


@app.get("/api/posts/{post_id}/sentiment")
async def api_get_post_sentiment(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        if not post.text:
            raise HTTPException(status_code=400, detail="Post has no text to analyze")
        try:
            result = await run_in_threadpool(classify_text, post.text)
            label = max(result[0], key=lambda d: d["score"])["label"]
            page_result = f"The sentiment of this post is {label}."
            return {"post_id": post_id, "text": post.text, "sentiment": page_result}
        except Exception as e:
            logging.exception("Sentiment analysis failed for post %s", post_id)
            raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {e}")


if __name__ == "__main__":
    uvicorn.run("rest_api:app", host="127.0.0.1", port=8000, reload=True)
