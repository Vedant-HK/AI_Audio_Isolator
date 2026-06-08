import os
from pathlib import Path

import requests


ELEVENLABS_AUDIO_ISOLATION_URL = "https://api.elevenlabs.io/v1/audio-isolation"
REQUEST_TIMEOUT_SECONDS = 120


class ElevenLabsAPIError(Exception):
    """Raised when the ElevenLabs Audio Isolation API request fails."""


class AudioIsolationError(ElevenLabsAPIError):
    """Raised when audio isolation fails."""


def user_friendly_api_message(status_code, detail):
    """Return a safe message for common ElevenLabs API failures."""
    messages = {
        400: "The audio file could not be processed. Please try a valid MP3 or WAV file.",
        401: "The ElevenLabs API key is missing or invalid.",
        403: "This ElevenLabs API key does not have permission to use audio isolation.",
        404: "The ElevenLabs audio isolation endpoint could not be found.",
        413: "The audio file is too large for the API.",
        429: "ElevenLabs rate limit reached. Please wait a moment and try again.",
        500: "ElevenLabs had a server error. Please try again shortly.",
        502: "ElevenLabs is temporarily unavailable. Please try again shortly.",
        503: "ElevenLabs is temporarily unavailable. Please try again shortly.",
        504: "ElevenLabs took too long to respond. Please try again shortly.",
    }

    base_message = messages.get(status_code, "ElevenLabs could not process the audio.")
    return f"{base_message} Details: {detail}" if detail else base_message


def get_api_key():
    """Read the ElevenLabs API key from the environment."""
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not api_key:
        raise AudioIsolationError("Missing ELEVENLABS_API_KEY. Add it to your .env file.")

    return api_key


def get_mime_type(input_path):
    """Return the multipart MIME type for a supported audio file."""
    extension = Path(input_path).suffix.lower()

    if extension == ".mp3":
        return "audio/mpeg"

    if extension == ".wav":
        return "audio/wav"

    raise AudioIsolationError("Unsupported audio format. Please upload an MP3 or WAV file.")


def parse_api_error(response):
    """Extract a useful error message from an ElevenLabs API response."""
    try:
        payload = response.json()
    except ValueError:
        return response.text.strip() or "The API returned an error without details."

    detail = payload.get("detail")

    if isinstance(detail, dict):
        return detail.get("message") or str(detail)

    if isinstance(detail, list):
        return "; ".join(str(item) for item in detail)

    return str(detail or payload)


class ElevenLabsAudioIsolationClient:
    """Reusable client for the ElevenLabs Audio Isolation API."""

    def __init__(
        self,
        api_key=None,
        api_url=ELEVENLABS_AUDIO_ISOLATION_URL,
        timeout=REQUEST_TIMEOUT_SECONDS,
        session=None,
    ):
        """Create a client with injectable credentials, endpoint, timeout, and HTTP session."""
        self.api_key = api_key or get_api_key()
        self.api_url = api_url
        self.timeout = timeout
        self.session = session or requests.Session()

    def isolate_voice(self, input_file_path, output_file_path):
        """Send audio to ElevenLabs, save the isolated WAV output, and return its path."""
        input_path = Path(input_file_path)
        output_path = Path(output_file_path)

        if not input_path.exists():
            raise AudioIsolationError(f"Input file not found: {input_path}")

        if not input_path.is_file():
            raise AudioIsolationError(f"Input path is not a file: {input_path}")

        headers = {"xi-api-key": self.api_key}

        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with input_path.open("rb") as audio_file:
                files = {
                    "audio": (
                        input_path.name,
                        audio_file,
                        get_mime_type(input_path),
                    )
                }
                response = self.session.post(
                    self.api_url,
                    headers=headers,
                    files=files,
                    timeout=self.timeout,
                )
        except OSError as exc:
            raise AudioIsolationError(f"File error: {exc}") from exc
        except requests.Timeout as exc:
            raise AudioIsolationError("The ElevenLabs request timed out. Try a shorter audio file.") from exc
        except requests.RequestException as exc:
            raise AudioIsolationError(f"Could not reach ElevenLabs: {exc}") from exc

        if response.status_code != 200:
            detail = parse_api_error(response)
            raise AudioIsolationError(user_friendly_api_message(response.status_code, detail))

        if not response.content:
            raise AudioIsolationError("ElevenLabs returned an empty audio file.")

        try:
            output_path.write_bytes(response.content)
        except OSError as exc:
            raise AudioIsolationError(f"File error: {exc}") from exc

        return str(output_path)


def isolate_voice_with_elevenlabs(
    input_file_path,
    output_file_path,
    api_key=None,
    timeout=REQUEST_TIMEOUT_SECONDS,
):
    """Create a default ElevenLabs client and isolate voice from an audio file."""
    client = ElevenLabsAudioIsolationClient(api_key=api_key, timeout=timeout)
    return client.isolate_voice(input_file_path, output_file_path)


def isolate_voice(input_path, output_path):
    """Run ElevenLabs voice isolation and save the result as output.wav."""
    return isolate_voice_with_elevenlabs(input_path, output_path)


def isolate_voice_elevenlabs(
    input_path,
    output_path,
    api_key=None,
    timeout=REQUEST_TIMEOUT_SECONDS,
):
    """Run ElevenLabs voice isolation with optional API key and timeout overrides."""
    return isolate_voice_with_elevenlabs(input_path, output_path, api_key=api_key, timeout=timeout)
