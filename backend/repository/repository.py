import sqlite3
import uuid
from datetime import datetime

DB_NAME = "posts.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            topic TEXT,
            tone TEXT,
            caption TEXT,
            hashtags TEXT,
            image_url TEXT,
            posted INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_post(topic, tone, caption, hashtags, image_url):
    conn = get_connection()
    cursor = conn.cursor()

    post_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO posts (id, topic, tone, caption, hashtags, image_url, posted, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        post_id,
        topic,
        tone,
        caption,
        ",".join(hashtags),
        image_url,
        0,
        created_at
    ))

    conn.commit()
    conn.close()

    return post_id


def get_post_by_id(post_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cursor.fetchone()

    conn.close()

    if not post:
        return None

    return {
        "id": post[0],
        "topic": post[1],
        "tone": post[2],
        "caption": post[3],
        "hashtags": post[4].split(","),
        "image_url": post[5],
        "posted": bool(post[6]),
        "created_at": post[7]
    }


def get_all_posts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    conn.close()

    result = []
    for post in posts:
        result.append({
            "id": post[0],
            "topic": post[1],
            "tone": post[2],
            "caption": post[3],
            "hashtags": post[4].split(","),
            "image_url": post[5],
            "posted": bool(post[6]),
            "created_at": post[7]
        })

    return result


def mark_post_as_posted(post_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE posts
        SET posted = 1
        WHERE id = ?
    """, (post_id,))

    conn.commit()
    conn.close()