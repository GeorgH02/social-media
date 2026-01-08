import unittest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

import rest_api as rest_api  

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  
)

rest_api.engine = test_engine

SQLModel.metadata.create_all(test_engine)

client = TestClient(rest_api.app)

def reset_db():
    """Drop and recreate all tables before each test."""
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)


class TestRestAPI(unittest.TestCase):

    def setUp(self):
        reset_db()

    def test_create_post_and_get_by_id(self):
        payload = {
            "user": "alice",
            "text": "Hello from API test",
            "image_full": "https://example.com/image.jpg",
            "country": "Austria",
            "filter": "City"
        }
        resp = client.post("/api/posts", json=payload)
        self.assertEqual(resp.status_code, 201)

        created = resp.json()
        self.assertIn("id", created)
        self.assertEqual(created["user"], "alice")
        self.assertEqual(created["text"], "Hello from API test")

        post_id = created["id"]

        resp2 = client.get(f"/api/posts/{post_id}")
        self.assertEqual(resp2.status_code, 200)
        fetched = resp2.json()
        self.assertEqual(fetched["id"], post_id)
        self.assertEqual(fetched["user"], "alice")

    def test_get_all_posts_and_filtering(self):
        client.post("/api/users", json={"name": "alice"})
        client.post("/api/users", json={"name": "bob"})
        
        p1 = {
            "user": "alice",
            "text": "I love pizza",
            "image_full": "https://example.com/a.jpg",
            "country": "Austria",
            "filter": "City"
        }
        p2 = {
            "user": "bob",
            "text": "I love pasta",
            "image_full": "https://example.com/b.jpg",
            "country": "Italy",
            "filter": "Nature"
        }
        client.post("/api/posts", json=p1)
        client.post("/api/posts", json=p2)

        resp_all = client.get("/api/posts")
        self.assertEqual(resp_all.status_code, 200)
        all_posts = resp_all.json()
        self.assertEqual(len(all_posts), 2)

    def test_get_posts_by_user_endpoint(self):
        client.post("/api/users", json={"name": "alice"})
        
        p1 = {
            "user": "alice",
            "text": "First",
            "image_full": "https://example.com/1.jpg",
            "country": "Austria",
            "filter": "City"
        }
        p2 = {
            "user": "alice",
            "text": "Second",
            "image_full": "https://example.com/2.jpg",
            "country": "Italy",
            "filter": "Nature"
        }
        client.post("/api/posts", json=p1)
        client.post("/api/posts", json=p2)

        resp = client.get("/api/users/alice/posts")
        self.assertEqual(resp.status_code, 200)
        posts = resp.json()
        self.assertEqual(len(posts), 2)
        self.assertTrue(all(p["user"] == "alice" for p in posts))

    def test_get_nonexistent_post_returns_404(self):
        resp = client.get("/api/posts/999999")
        self.assertEqual(resp.status_code, 404)
        data = resp.json()
        self.assertEqual(data["detail"], "Post not found")

    def test_get_posts_by_user_404_when_none(self):
        resp = client.get("/api/users/ghost/posts")
        self.assertEqual(resp.status_code, 404)
        data = resp.json()
        self.assertEqual(data["detail"], "User not found")


if __name__ == "__main__":
    unittest.main()
