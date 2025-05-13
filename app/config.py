import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# LLM Selection (gemini or deepseek)
ACTIVE_LLM = os.getenv("ACTIVE_LLM", "gemini")