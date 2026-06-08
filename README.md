# Voice Isolation Web Application

## Overview

Voice Isolation Web Application is a Flask-based web platform that allows users to upload audio files and isolate vocals using the ElevenLabs Audio Isolation API.

The application provides a simple drag-and-drop interface for uploading audio files, securely processes the audio through ElevenLabs, and allows users to download the isolated voice output.

---

## Features

* Upload MP3 and WAV audio files
* Drag-and-drop file upload interface
* Voice isolation using ElevenLabs AI
* Secure file validation
* Error handling and user-friendly messages
* Download processed audio output
* Reentrancy-safe backend processing
* Configurable environment variables

---

## Project Structure

```text
.
├── app.py
├── api_client.py
├── config.py
├── storage.py
├── requirements.txt
├── .env.example
│
├── templates/
│   └── index.html
│
├── static/
│   ├── uploads/
│   └── output/
│
└── README.md
```

---

## How It Works

```text
User Uploads Audio
          │
          ▼
 File Validation
          │
          ▼
 Secure Storage
          │
          ▼
 ElevenLabs Audio Isolation API
          │
          ▼
 Processed Voice Output
          │
          ▼
 Download Isolated Audio
```

---

## Technologies Used

### Backend

* Python
* Flask
* Requests
* Python Dotenv

### Frontend

* HTML5
* CSS3
* JavaScript

### AI Service

* ElevenLabs Audio Isolation API

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/voice-isolation-app.git
cd voice-isolation-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
ELEVENLABS_API_KEY=your_api_key_here

FLASK_SECRET_KEY=your_secret_key

MAX_UPLOAD_BYTES=104857600
```

### Required Variable

| Variable           | Description        |
| ------------------ | ------------------ |
| ELEVENLABS_API_KEY | ElevenLabs API Key |

### Optional Variables

| Variable         | Description            |
| ---------------- | ---------------------- |
| FLASK_SECRET_KEY | Flask session secret   |
| MAX_UPLOAD_BYTES | Maximum upload size    |
| OUTPUT_FILENAME  | Name of generated file |

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Application will be available at:

```text
http://127.0.0.1:5000
```

---

## Usage

### Upload Audio

1. Open the application.
2. Drag and drop an MP3 or WAV file.
3. Click **Process Audio**.
4. Wait for processing to complete.

### Download Output

After successful processing:

1. Click **Download Output**.
2. Save the isolated voice file.

---

## Supported Formats

| Format | Supported |
| ------ | --------- |
| MP3    | ✅         |
| WAV    | ✅         |
| FLAC   | ❌         |
| AAC    | ❌         |
| OGG    | ❌         |

---

## Error Handling

The application handles:

* Missing files
* Invalid file types
* Large uploads
* API authentication errors
* Rate limit errors
* Network failures
* Server-side exceptions

---

## Security Features

* Secure filename handling
* Unique upload naming
* File type validation
* Upload size restrictions
* Protected API key management
* Graceful exception handling

---

## API Integration

The application integrates with:

**ElevenLabs Audio Isolation API**

Capabilities:

* Vocal extraction
* Instrumental separation
* Audio enhancement
* High-quality voice isolation

---

## Future Enhancements

* Multiple audio format support
* Batch audio processing
* User authentication
* Audio preview before download
* Progress tracking
* Cloud storage integration
* Docker deployment
* REST API endpoints

---

## Screenshots

Add screenshots here:

```text
screenshots/
├── home.png
├── upload.png
└── result.png
```

---

## Author

**Vedant Khadye**

Artificial Intelligence & Data Science Engineer

---

## License

This project is licensed under the MIT License.

---

## Acknowledgements

* Flask Framework
* ElevenLabs API
* Python Requests Library
* Open Source Community
