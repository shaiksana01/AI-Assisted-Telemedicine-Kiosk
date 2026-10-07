"""
Utils package for AI-Assisted Telemedicine Kiosk.
"""

from utils.translations import (
    get_text,
    get_available_languages,
    get_language_code,
    load_all_translations,
    LANGUAGE_MAPPING
)

__all__ = [
    "get_text",
    "get_available_languages",
    "get_language_code",
    "load_all_translations",
    "LANGUAGE_MAPPING"
]
