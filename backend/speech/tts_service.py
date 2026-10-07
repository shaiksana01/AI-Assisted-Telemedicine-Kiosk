"""
Text-to-Speech (TTS) Service for AI-Assisted Telemedicine Kiosk.
Uses OpenAI TTS API for high quality voice prompts with local audio caching.
"""

import os
import io
import hashlib
import requests
from typing import Optional, Tuple

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "audio_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def synthesize_speech(text: str, voice: str = "alloy", language_code: str = "en") -> Tuple[Optional[bytes], Optional[str]]:
    """
    Synthesize speech for important kiosk prompts using OpenAI TTS with local cache.
    Returns:
        (audio_bytes, error_message)
    """
    if not text or not text.strip():
        return None, "Empty text provided."

    clean_text = text.strip()
    # Cache key based on text and voice
    cache_hash = hashlib.md5(f"{clean_text}_{voice}".encode("utf-8")).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_hash}.mp3")

    # Return cached audio if available
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "rb") as f:
                return f.read(), None
        except Exception:
            pass

    api_key = os.getenv("OPENAI_API_KEY", OPENAI_API_KEY)
    if not api_key:
        return None, "OpenAI API key not configured. Text display is active."

    try:
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "tts-1",
            "input": clean_text,
            "voice": voice,
            "response_format": "mp3"
        }

        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            audio_bytes = response.content
            # Save to cache
            try:
                with open(cache_path, "wb") as f:
                    f.write(audio_bytes)
            except Exception:
                pass
            return audio_bytes, None
        else:
            return None, f"TTS API error ({response.status_code}): {response.text}"
    except Exception as e:
        return None, f"TTS service unavailable: {str(e)}"
