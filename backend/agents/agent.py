import os
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from google import genai as genai_sdk
from google.genai import types
from config.config import Config

# Configure Gemini API Key
genai.configure(api_key=Config.GEMINI_API_KEY)
# Text Model
text_model = genai.GenerativeModel("gemini-2.5-flash")

# Image Model
image_model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")


# Agent 1: Generate Caption + Hashtags
def generate_caption_and_hashtags(topic, tone):
    prompt = f"""
    Generate an Instagram post for the topic: {topic}
    Tone: {tone}

    Requirements:
    - Caption max 150 words
    - Provide 5 to 10 hashtags
    - Return in this format:

    Caption:
    <caption>

    Hashtags:
    <comma separated hashtags>
    """

    response = text_model.generate_content(prompt)
    output = response.text

    caption = ""
    hashtags = []

    if "Caption:" in output and "Hashtags:" in output:
        parts = output.split("Hashtags:")
        caption = parts[0].replace("Caption:", "").strip()
        hashtags = [tag.strip() for tag in parts[1].split(",")]

    return caption, hashtags

client = genai_sdk.Client(api_key=Config.GEMINI_API_KEY)
# Agent 2: Generate Image
def generate_image(topic,content):
    prompt = f"Create an Instagram style image for {topic}, for the content: {content}"

    # 2. Use the new 'models.generate_content' method
    # This supports the response_modalities field
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",  # Also known as Nano Banana 2
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio="1:1",
                image_size="1K"
            )
        )
    )

    # 3. Extract and save the image
    for part in response.candidates[0].content.parts:
        if part.inline_data:
            # The new SDK provides a helper to convert bytes to a PIL Image
            img = Image.open(BytesIO(part.inline_data.data))
            img.save("insta_post.png")
            return "insta_post.png"
            
    return None