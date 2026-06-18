import os
from pathlib import Path
from dotenv import load_dotenv

# .env file se variables load karne ke liye
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5"

if not API_KEY:
    raise ValueError("Critical Error: OPENWEATHER_API_KEY not found in environment variables. Check your .env file.")