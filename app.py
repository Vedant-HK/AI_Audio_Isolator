import logging
from pathlib import Path

from flask import Flask, flash, redirect, render_template, request, send_file, url_for
from werkzeug.exceptions import RequestEntityTooLarge

from api_client import ElevenLabsAPIError, isolate_voice_elevenlabs
from config import Config
from storage import UploadValidationError, ensure_directories, save_audio_upload


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
ensure_directories(app.config["UPLOAD_DIR"], app.config["OUTPUT_DIR"])


@app.route("/", methods=["GET", "POST"])
def index():
    """Render the upload page and handle voice isolation requests."""
    if request.method == "GET":
        return render_template("index.html")

    try:
        upload_path = save_audio_upload(
            request.files.get("audio_file"),
            app.config["UPLOAD_DIR"],
            app.config["ALLOWED_EXTENSIONS"],
        )
        processed_path = isolate_voice_elevenlabs(upload_path, Config.output_file())
    except UploadValidationError as exc:
        flash(str(exc))
        return redirect(url_for("index"))
    except ElevenLabsAPIError as exc:
        app.logger.warning("Audio isolation failed: %s", exc)
        flash(str(exc))
        return redirect(url_for("index"))
    except Exception as exc:
        app.logger.exception("Unexpected error while processing upload: %s", exc)
        flash("An unexpected error occurred while processing the audio.")
        return redirect(url_for("index"))

    return render_template(
        "index.html",
        download_url=url_for("download_output"),
        output_name=Path(processed_path).name,
    )


@app.route("/download")
def download_output():
    """Return the processed output.wav file to the user as a download."""
    output_file = Config.output_file()

    if not output_file.exists():
        flash("No processed audio file is available yet.")
        return redirect(url_for("index"))

    return send_file(output_file, as_attachment=True, download_name=output_file.name)


@app.errorhandler(RequestEntityTooLarge)
def file_too_large(error):
    """Show a friendly message when the uploaded file exceeds the size limit."""
    flash("The uploaded file is too large. Please upload a file smaller than 100 MB.")
    return redirect(url_for("index"))


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """Prevent uncaught exceptions from exposing internals or crashing the response."""
    app.logger.exception("Unhandled application error: %s", error)
    flash("Something went wrong. Please try again.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
