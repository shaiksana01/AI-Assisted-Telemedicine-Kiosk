"""
Whisper Speech-to-Text Service for AI-Assisted Telemedicine Kiosk.
Uses OpenAI Whisper API for multilingual audio transcription with clean fallbacks.
"""

import os
import io
import requests
from typing import Dict, Any, Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav", language: Optional[str] = None) -> Dict[str, Any]:
    """
    Transcribe recorded microphone audio using OpenAI Whisper API.
    Returns:
        dict: {"success": bool, "text": str, "error": str or None}
    """
    api_key = os.getenv("OPENAI_API_KEY", OPENAI_API_KEY)
    if not api_key:
        return {
            "success": False,
            "text": "",
            "error": "OpenAI API key not configured. Please enter symptoms using text mode or configure OPENAI_API_KEY in .env."
        }

    if not audio_bytes or len(audio_bytes) < 100:
        return {
            "success": False,
            "text": "",
            "error": "No valid audio data recorded. Please try recording again or use text input."
        }

    try:
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        files = {
            "file": (filename, io.BytesIO(audio_bytes), "audio/wav")
        }
        data = {
            "model": "whisper-1"
        }
        if language and language in ["en", "hi", "kn", "te"]:
            data["language"] = language

        response = requests.post(url, headers=headers, files=files, data=data, timeout=25)
        
        if response.status_code == 200:
            result = response.json()
            transcribed_text = result.get("text", "").strip()
            return {
                "success": True,
                "text": transcribed_text,
                "error": None
            }
        else:
            err_msg = f"Whisper API error ({response.status_code}): {response.text}"
            return {
                "success": False,
                "text": "",
                "error": err_msg
            }
    except Exception as e:
        return {
            "success": False,
            "text": "",
            "error": f"Audio transcription service unavailable: {str(e)}. Please use text input."
        }
