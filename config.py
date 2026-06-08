import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Application configuration loaded from environment variables."""

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_BYTES", 100 * 1024 * 1024))
    STATIC_DIR = BASE_DIR / "static"
    UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", STATIC_DIR / "uploads"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", STATIC_DIR / "output"))
    OUTPUT_FILENAME = os.getenv("OUTPUT_FILENAME", "output.wav")
    ALLOWED_EXTENSIONS = {"mp3", "wav"}

    @classmethod
    def output_file(cls):
        """Return the configured output file path."""
        return cls.OUTPUT_DIR / cls.OUTPUT_FILENAME
