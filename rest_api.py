from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from typing import List
from post_manager import Post, PostCreate, create_database

# uvicorn rest_api:app --reload
# /docs# for SwaggerUI

engine = create_database()

app = FastAPI(title="Social Media API")

@app.get("/")
def root():
    return {"message": "Welcome to Social Media API"}

@app.get("/posts", response_model=List[Post])
def get_all_posts():
    with Session(engine) as session:
        posts = session.exec(select(Post).order_by(Post.id.desc())).all()
        return posts

@app.get("/posts/{post_id}", response_model=Post)
def get_post(post_id: int):
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

@app.post("/posts", response_model=Post, status_code=201)
def create_post(post: PostCreate):
    with Session(engine) as session:
        db_post = Post.model_validate(post)
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        return db_post

@app.get("/users/{username}/posts", response_model=List[Post])
def get_posts_by_user(username: str):
    with Session(engine) as session:
        posts = session.exec(select(Post).where(Post.user == username).order_by(Post.id.desc())).all()
        if not posts:
            raise HTTPException(status_code=404, detail="No posts found")
        return posts