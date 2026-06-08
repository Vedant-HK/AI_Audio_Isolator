from pathlib import Path
from uuid import uuid4

from werkzeug.utils import secure_filename


class UploadValidationError(ValueError):
    """Raised when an uploaded file is missing, invalid, or cannot be saved."""


def ensure_directories(*directories):
    """Create application directories if they do not already exist."""
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def is_allowed_file(filename, allowed_extensions):
    """Return True when a filename has one of the allowed extensions."""
    if not filename or "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()
    return extension in allowed_extensions


def build_upload_path(filename, upload_dir):
    """Build a safe unique path for an uploaded file."""
    safe_name = secure_filename(filename)
    extension = Path(safe_name).suffix.lower()
    stem = Path(safe_name).stem or "audio"
    return Path(upload_dir) / f"{stem}-{uuid4().hex}{extension}"


def save_audio_upload(uploaded_file, upload_dir, allowed_extensions):
    """Validate and save an uploaded audio file."""
    if not uploaded_file or uploaded_file.filename == "":
        raise UploadValidationError("Please choose an MP3 or WAV file.")

    if not is_allowed_file(uploaded_file.filename, allowed_extensions):
        raise UploadValidationError("Invalid file type. Only MP3 and WAV files are supported.")

    upload_path = build_upload_path(uploaded_file.filename, upload_dir)

    try:
        uploaded_file.save(upload_path)
    except OSError as exc:
        raise UploadValidationError("The uploaded file could not be saved. Please try again.") from exc

    return upload_path
