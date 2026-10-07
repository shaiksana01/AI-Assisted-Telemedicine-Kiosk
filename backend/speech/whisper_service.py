"""
Whisper Speech-to-Text Service for AI-Assisted Telemedicine Kiosk.
Uses OpenAI Whisper API for multilingual audio transcription with clean fallbacks.
"""

import os
import io
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Ensure .env is loaded from project root
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_env_path = os.path.join(_project_root, ".env")
if os.path.exists(_env_path):
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()

logger = logging.getLogger(__name__)


def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm", language: Optional[str] = None) -> Dict[str, Any]:
    """
    Transcribe recorded microphone audio using OpenAI Whisper API.
    Supports OpenAI SDK (1.x+) and direct HTTP request fallback.
    
    Returns:
        dict: {"success": bool, "transcript": str, "text": str, "error": str or None}
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return {
            "success": False,
            "transcript": "",
            "text": "",
            "error": "Speech-to-text service is not configured on the server. Please enter symptoms using text mode or configure OPENAI_API_KEY in .env."
        }

    if not audio_bytes or len(audio_bytes) < 64:
        return {
            "success": False,
            "transcript": "",
            "text": "",
            "error": "No valid audio data recorded. Please try recording again or use text input."
        }

    # Normalize filename extension
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".webm", ".wav", ".mp3", ".mp4", ".m4a", ".ogg"]:
        filename = f"audio_{int(os.times().elapsed)}.webm"
        ext = ".webm"

    # 1. Try official OpenAI SDK client
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = filename

        kwargs = {
            "model": "whisper-1",
            "file": audio_file
        }
        if language and language in ["en", "hi", "kn", "te"]:
            kwargs["language"] = language

        transcript_obj = client.audio.transcriptions.create(**kwargs)
        transcribed_text = getattr(transcript_obj, "text", str(transcript_obj)).strip()

        return {
            "success": True,
            "transcript": transcribed_text,
            "text": transcribed_text,
            "error": None
        }
    except Exception as sdk_err:
        logger.warning("OpenAI SDK transcription failed (%s), attempting HTTPS fallback.", sdk_err)

    # 2. Resilient HTTPS request fallback
    try:
        import requests
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        mime_map = {
            ".webm": "audio/webm",
            ".wav": "audio/wav",
            ".mp3": "audio/mpeg",
            ".mp4": "audio/mp4",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg"
        }
        content_type = mime_map.get(ext, "audio/webm")
        
        files = {
            "file": (filename, io.BytesIO(audio_bytes), content_type)
        }
        data = {
            "model": "whisper-1"
        }
        if language and language in ["en", "hi", "kn", "te"]:
            data["language"] = language

        response = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            transcribed_text = result.get("text", "").strip()
            return {
                "success": True,
                "transcript": transcribed_text,
                "text": transcribed_text,
                "error": None
            }
        else:
            err_msg = f"Whisper API error ({response.status_code}). Please try again or type symptoms."
            return {
                "success": False,
                "transcript": "",
                "text": "",
                "error": err_msg
            }
    except Exception as e:
        logger.error("Audio transcription fallback failed: %s", str(e))
        return {
            "success": False,
            "transcript": "",
            "text": "",
            "error": "Audio transcription service is currently unavailable. Please use text input."
        }

