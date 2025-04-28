from dotenv import load_dotenv
import os

load_dotenv()  # reads .env into os.environ
DATABASE_URL = os.getenv("DATABASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")