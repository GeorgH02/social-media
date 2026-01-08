import os
import json
import time
from io import BytesIO

import pika
import requests
from PIL import Image

from sqlmodel import Session, select
from sqlalchemy import create_engine

RABBIT_HOST = os.getenv("RABBIT_HOST", "queue")
QUEUE_NAME = os.getenv("RESIZE_QUEUE", "resize")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test.db")

THUMB_DIR = os.getenv("THUMB_DIR", "/data/thumbs")
PUBLIC_PREFIX = os.getenv("THUMB_PUBLIC_PREFIX", "/thumbs")  

THUMB_SIZE = int(os.getenv("THUMB_SIZE", "256")) 

engine = create_engine(DATABASE_URL, echo=False)

from class_manager import Post 


def ensure_dirs() -> None:
    os.makedirs(THUMB_DIR, exist_ok=True)


def download_image(url: str) -> Image.Image:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    img = Image.open(BytesIO(r.content))
    return img.convert("RGB")


def make_thumbnail(img: Image.Image, size: int) -> Image.Image:
    img_copy = img.copy()
    img_copy.thumbnail((size, size))
    return img_copy


def save_thumbnail(img: Image.Image, post_id: int) -> str:
    filename = f"post_{post_id}_{THUMB_SIZE}.jpg"
    path = os.path.join(THUMB_DIR, filename)
    img.save(path, format="JPEG", quality=85)
    return f"{PUBLIC_PREFIX}/{filename}"


def update_post_thumb(post_id: int, thumb_path: str) -> None:
    with Session(engine) as session:
        post = session.get(Post, post_id)
        if not post:
            print(f"[worker] Post {post_id} not found, skipping")
            return
        post.image_thumb = thumb_path
        session.add(post)
        session.commit()
        print(f"[worker] Updated post {post_id} image_thumb={thumb_path}")


def process_message(body: bytes) -> None:
    payload = json.loads(body.decode("utf-8"))
    post_id = int(payload["post_id"])
    image_full = payload["image_full"]

    print(f"[worker] Resize job received: post_id={post_id}, image_full={image_full}")

    img = download_image(image_full)
    thumb = make_thumbnail(img, THUMB_SIZE)
    thumb_path = save_thumbnail(thumb, post_id)
    update_post_thumb(post_id, thumb_path)


def main() -> None:
    ensure_dirs()

    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_HOST)
            )
            channel = connection.channel()
            channel.queue_declare(queue=QUEUE_NAME, durable=False)

            def callback(ch, method, properties, body):
                try:
                    process_message(body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as e:
                    print(f"[worker] Error: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
            print(f"[worker] Waiting for messages on queue='{QUEUE_NAME}'...")
            channel.start_consuming()

        except Exception as e:
            print(f"[worker] Connection error: {e}. Reconnecting in 3s...")
            time.sleep(3)


if __name__ == "__main__":
    main()
