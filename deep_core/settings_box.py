import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
    S3_BUCKET = os.getenv("S3_BUCKET", "")
    S3_PREFIX = os.getenv("S3_PREFIX", "deep-bot-downloads")

    TEMP_FOLDER = Path(os.getenv("TEMP_FOLDER", "temp_jobs"))

    LINK_EXPIRES_SECONDS = int(os.getenv("LINK_EXPIRES_SECONDS", "3600"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "500"))


settings = Settings()