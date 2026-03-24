from agents.agent import generate_caption_and_hashtags, generate_image
from repository.repository import (
    save_post,
    get_post_by_id,
    get_all_posts,
    mark_post_as_posted
)


# 1. Generate Post
def generate_post_handler(topic, tone):
    try:
        # Call AI Content Agent
        caption, hashtags = generate_caption_and_hashtags(topic, tone)

        # Call AI Image Agent
        image_url = generate_image(topic)

        # Save to DB
        post_id = save_post(topic, tone, caption, hashtags, image_url)

        return {
            "status": "success",
            "post_id": post_id,
            "topic": topic,
            "tone": tone,
            "caption": caption,
            "hashtags": hashtags,
            "image_url": image_url
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 2. Simulate Posting to Instagram
def post_handler(post_id):
    try:
        post = get_post_by_id(post_id)

        if not post:
            return {
                "status": "error",
                "message": "Post not found"
            }

        # Mark as posted
        mark_post_as_posted(post_id)

        return {
            "status": "success",
            "message": "Post published successfully (simulated)",
            "post": post
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


# 3. Get All Posts History
def history_handler():
    try:
        posts = get_all_posts()

        return {
            "status": "success",
            "total_posts": len(posts),
            "posts": posts
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }