"""
Text-to-Speech (TTS) Service for AI-Assisted Telemedicine Kiosk.
Uses OpenAI TTS API for high quality voice prompts with local audio caching.
"""

import os
import io
import hashlib
import logging
from typing import Optional, Tuple
from dotenv import load_dotenv
# Ensure .env is loaded from project root
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_env_path = os.path.join(_project_root, ".env")
if os.path.exists(_env_path):
    load_dotenv(dotenv_path=_env_path)
else:
    load_dotenv()

logger = logging.getLogger(__name__)

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "audio_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

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

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None, "OpenAI API key not configured on server. Text display is active."

    # 1. Try official OpenAI SDK client
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=clean_text
        )
        audio_bytes = response.read()
        if audio_bytes:
            try:
                with open(cache_path, "wb") as f:
                    f.write(audio_bytes)
            except Exception:
                pass
            return audio_bytes, None
    except Exception as sdk_err:
        logger.warning("OpenAI SDK TTS failed (%s), attempting HTTPS fallback.", sdk_err)

    # 2. Resilient HTTPS fallback
    try:
        import requests
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
            try:
                with open(cache_path, "wb") as f:
                    f.write(audio_bytes)
            except Exception:
                pass
            return audio_bytes, None
        else:
            return None, f"TTS API error ({response.status_code})."
    except Exception as e:
        return None, f"TTS service unavailable: {str(e)}"

