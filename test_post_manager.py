import unittest
import os
from sqlmodel import Session, select, SQLModel
from post_manager import Post, create_database, add_posts, get_latest_post


class TestPostManager(unittest.TestCase):
    
    def setUp(self):
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")
        
        self.test_db = "sqlite:///test_database.db"
        self.engine = create_database(self.test_db)
    
    def tearDown(self):
        self.engine.dispose()
        if os.path.exists("test_database.db"):
            os.remove("test_database.db")
    
    def test_post_creation(self):
        post = Post(image="test.jpg", text="Test post", user="testuser")
        self.assertEqual(post.image, "test.jpg")
        self.assertEqual(post.text, "Test post")
        self.assertEqual(post.user, "testuser")
        self.assertIsNone(post.id)  
    
    def test_add_posts_to_database(self):
        posts = [Post(image="img1.jpg", text="Post 1", user="user1"),
                Post(image="img2.jpg", text="Post 2", user="user2"),
                Post(image="img3.jpg", text="Post 3", user="user3")]
        add_posts(self.engine, posts)
        
        with Session(self.engine) as session:
            result = session.exec(select(Post)).all()
            self.assertEqual(len(result), 3)
    
    def test_get_latest_post(self):
        posts = [Post(image="img1.jpg", text="First post", user="user1"),
                Post(image="img2.jpg", text="Second post", user="user2"),
                Post(image="img3.jpg", text="Third post", user="user3")]
        
        add_posts(self.engine, posts)
        latest_post = get_latest_post(self.engine)
        
        self.assertIsNotNone(latest_post)
        self.assertEqual(latest_post.text, "Third post")
        self.assertEqual(latest_post.user, "user3")
    
    def test_get_latest_post_empty_database(self):
        latest_post = get_latest_post(self.engine)
        self.assertIsNone(latest_post)


if __name__ == '__main__':
    unittest.main()
