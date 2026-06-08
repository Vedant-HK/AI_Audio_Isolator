# ElevenLabs Voice Isolation Flask App

A mini Flask backend that accepts an MP3 or WAV upload, sends it to the ElevenLabs Audio Isolation API, saves the cleaned result as `static/output/output.wav`, and returns it for download.

## Project Structure

```text
AI Audio/
├── app.py
├── api_client.py
├── .env.example
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── uploads/
    │   └── .gitkeep
    └── output/
        └── .gitkeep
```

## Setup

1. Create and activate a virtual environment.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies.

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`, then add your ElevenLabs API key.

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
FLASK_SECRET_KEY=replace_this_with_a_random_secret
```

4. Run the Flask app.

```powershell
python app.py
```

5. Open the app.

```text
http://127.0.0.1:5000
```

## Notes

- This project uses only the ElevenLabs API. It does not run local ML models.
- Uploaded files are saved in `static/uploads/`.
- Processed audio is always saved as `static/output/output.wav`.
- The app handles invalid file types, missing API keys, API failures, empty responses, oversized files, and request timeouts.
