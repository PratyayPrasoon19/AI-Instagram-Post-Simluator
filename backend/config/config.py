# config/config.py

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """
    Configuration for Instagram Post Generator backend using Gemini API.
    """
    # Gemini API key
    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
