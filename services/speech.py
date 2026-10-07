"""
Speech-to-Text (Whisper) Service for Flask Web App.
"""

from backend.speech.whisper_service import transcribe_audio

__all__ = ["transcribe_audio"]
