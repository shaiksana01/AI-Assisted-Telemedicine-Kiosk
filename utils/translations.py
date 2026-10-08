"""
Central Translations Module for AI-Assisted Telemedicine Kiosk.
Loads multilingual dictionaries for English, Hindi, Kannada, and Telugu.
Supports both JSON files in translations/ and built-in dictionary fallbacks.
"""

import os
import json
from typing import Dict, Any, List

TRANSLATIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "translations")

LANGUAGE_MAPPING = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Telugu": "te"
}

_loaded_translations: Dict[str, Dict[str, str]] = {}

def load_all_translations() -> Dict[str, Dict[str, str]]:
    """Load translation JSON files from translations/ directory."""
    global _loaded_translations
    if _loaded_translations:
        return _loaded_translations

    for lang_name, code in LANGUAGE_MAPPING.items():
        file_path = os.path.join(TRANSLATIONS_DIR, f"{code}.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    _loaded_translations[lang_name] = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load {file_path}: {e}")
                _loaded_translations[lang_name] = {}
        else:
            _loaded_translations[lang_name] = {}

    return _loaded_translations

def get_language_name(code_or_name: str) -> str:
    """
    Return canonical full language name (e.g., 'English', 'Hindi', 'Kannada', 'Telugu').
    """
    if not code_or_name:
        return "English"
    code = get_language_code(code_or_name)
    reverse_map = {v: k for k, v in LANGUAGE_MAPPING.items()}
    return reverse_map.get(code, "English")

def get_text(key: str, language: str = "English", default: str = None) -> str:
    """
    Get localized string for a given key and language (accepts code or full name).
    Falls back to English if key is missing in target language, or default/key if not found.
    """
    canonical_name = get_language_name(language)
    translations = load_all_translations()
    lang_dict = translations.get(canonical_name, {})
    
    if key in lang_dict and lang_dict[key]:
        return lang_dict[key]
    
    # Fallback to English
    en_dict = translations.get("English", {})
    if key in en_dict and en_dict[key]:
        return en_dict[key]
    
    return default if default is not None else key

def get_available_languages() -> List[str]:
    """Return supported language names."""
    return list(LANGUAGE_MAPPING.keys())

def get_language_code(language_name: str) -> str:
    """
    Return 2-letter ISO language code (e.g., 'en', 'hi', 'kn', 'te').
    Handles language names, localized labels, or existing codes gracefully.
    """
    if not language_name:
        return "en"
    
    clean = str(language_name).strip().lower()
    
    # Direct mapping
    lookup = {
        "english": "en",
        "en": "en",
        "hindi": "hi",
        "hi": "hi",
        "hindi (हिंदी)": "hi",
        "हिंदी": "hi",
        "kannada": "kn",
        "kn": "kn",
        "kannada (ಕನ್ನಡ)": "kn",
        "ಕನ್ನಡ": "kn",
        "telugu": "te",
        "te": "te",
        "telugu (తెలుగు)": "te",
        "తెలుగు": "te"
    }
    
    if clean in lookup:
        return lookup[clean]
    
    # Substring matching fallback
    for name, code in LANGUAGE_MAPPING.items():
        if name.lower() in clean or code in clean:
            return code
            
    return "en"

__all__ = [
    "get_text",
    "get_available_languages",
    "get_language_code",
    "get_language_name",
    "load_all_translations",
    "LANGUAGE_MAPPING"
]

