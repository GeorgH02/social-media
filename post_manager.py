from sqlmodel import Field, Session, SQLModel, create_engine, select
#from sqlalchemy import UniqueConstraint, Column, String

class Post(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    image: str
    text: str | None = None
    user: str
    
#for API input
class PostCreate(SQLModel):
    image: str
    text: str | None = None
    user: str

def create_database(db_url: str = "sqlite:///social-media-database.db"):
    engine = create_engine(db_url)
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
    post_1 = Post(image="https://example.com/sunset.jpg", text="A sunset :)", user="john01")
    post_2 = Post(image="https://example.com/coffee.jpg", text="I like coffee", user="_maria2")
    post_3 = Post(image="https://example.com/dog.jpg", text="Cute dog alert", user="jessica184")
    
    engine = create_database()
    add_posts(engine, [post_1, post_2, post_3])
    
    latest_post = get_latest_post(engine)
    
    if latest_post:
        print("Latest Post:")
        print(f"ID: {latest_post.id}")
        print(f"User: {latest_post.user}")
        print(f"Text: {latest_post.text}")
        print(f"Image: {latest_post.image}")
    else:
        print("No posts found")


if __name__ == "__main__":
    main()