import os
import base64
from io import BytesIO
from PIL import Image
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Text Model
text_model = genai.GenerativeModel("gemini-3-flash")

# Image Model
image_model = genai.GenerativeModel("gemini-3-flash")


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


# Agent 2: Generate Image
def generate_image(topic):
    prompt = f"Create an Instagram style image for {topic}"

    response = image_model.generate_content(
        prompt,
        generation_config={"response_modalities": ["IMAGE"]}
    )

    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data"):
            image_bytes = base64.b64decode(part.inline_data.data)
            image = Image.open(BytesIO(image_bytes))

            image_path = f"generated_{topic.replace(' ', '_')}.png"
            image.save(image_path)

            return image_path

    return None