import os
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    image_full: str                     # path or URL to the full-size image
    image_thumb: str | None = None      # path or URL to the reduced-size image
    text: str | None = None
    user: str
    country: str
    filter: str
    
class PostCreate(SQLModel):
    image_full: str                     # client sends full-size image URL (for now)
    text: str | None = None
    user: str
    country: str
    filter: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str

class UserCreate(SQLModel):
    name: str

def create_database():
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if not DATABASE_URL:
        print("DATABASE_URL not set — skipping database initialization")
        return None
    engine = create_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)
    return engine

def add_posts(engine, posts: list[Post]):
    with Session(engine) as session:
        for post in posts:
            session.add(post)
        session.commit()

def get_latest_post(engine):
    with Session(engine) as session:
        statement = select(Post).order_by(Post.id.desc()).limit(1)
        latest_post = session.exec(statement).first()
        return latest_post


def main():
    post_1 = Post(image_full="https://example.com/sunset.jpg", text="A sunset :)", user="john01", country="Austria", filter="Nature")
    post_2 = Post(image_full="https://example.com/coffee.jpg", text="I like coffee", user="_maria2", country="Italy", filter="City")
    post_3 = Post(image_full="https://example.com/dog.jpg", text="Cute dog alert", user="jessica184", country="United Kingdom", filter="Nature")
    
    engine = create_database()
    add_posts(engine, [post_1, post_2, post_3])
    
    latest_post = get_latest_post(engine)
    
    if latest_post:
        print("Latest Post:")
        print(f"ID: {latest_post.id}")
        print(f"User: {latest_post.user}")
        print(f"Text: {latest_post.text}")
        print(f"Image: {latest_post.image_full}")
    else:
        print("No posts found")


if __name__ == "__main__":
    main()