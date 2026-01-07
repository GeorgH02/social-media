import unittest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import StaticPool

import rest_api as rest_api  


# Shared in-memory SQLite DB for all connections
test_engine = create_engine(
    "sqlite://",  # in-memory
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

    """
    def test_root_endpoint(self):
        resp = client.get("/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["message"], "Welcome to Social Media API")
    """

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
        p1 = {
            "user": "alice",
            "text": "I love pizza",
            "image": "https://example.com/a.jpg",
        }
        p2 = {
            "user": "bob",
            "text": "I love pasta",
            "image": "https://example.com/b.jpg",
        }
        client.post("/api/posts", json=p1)
        client.post("/api/posts", json=p2)

        resp_all = client.get("/api/posts")
        self.assertEqual(resp_all.status_code, 200)
        all_posts = resp_all.json()
        self.assertEqual(len(all_posts), 2)

        """
        # filter by user
        resp_alice = client.get("/api/posts", params={"user": "alice"})
        self.assertEqual(resp_alice.status_code, 200)
        posts_alice = resp_alice.json()
        self.assertEqual(len(posts_alice), 1)
        self.assertEqual(posts_alice[0]["user"], "alice")

        
        # filter by search text
        resp_search = client.get("/posts", params={"search": "pasta"})
        self.assertEqual(resp_search.status_code, 200)
        posts_search = resp_search.json()
        self.assertEqual(len(posts_search), 1)
        self.assertEqual(posts_search[0]["user"], "bob")
        """

    def test_get_posts_by_user_endpoint(self):
        p1 = {
            "user": "alice",
            "text": "First",
            "image": "https://example.com/1.jpg",
        }
        p2 = {
            "user": "alice",
            "text": "Second",
            "image": "https://example.com/2.jpg",
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
        self.assertEqual(data["detail"], "No posts found")


if __name__ == "__main__":
    unittest.main()
