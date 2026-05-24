import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")
ENV = os.getenv("ENV", "local")


allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200")
ALLOWED_ORIGINS = [origin.strip() for origin in allowed_origins_raw.split(",")]