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

def load_all_translations():
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

def get_text(key: str, language: str = "English", default: str = None) -> str:
    """
    Get localized string for a given key and language.
    Falls back to English if key is missing in target language, or default/key if not found.
    """
    translations = load_all_translations()
    lang_dict = translations.get(language, {})
    
    if key in lang_dict:
        return lang_dict[key]
    
    # Fallback to English
    en_dict = translations.get("English", {})
    if key in en_dict:
        return en_dict[key]
    
    return default if default is not None else key

def get_available_languages() -> List[str]:
    """Return supported language names."""
    return list(LANGUAGE_MAPPING.keys())

def get_language_code(language_name: str) -> str:
    """Return ISO language code."""
    return LANGUAGE_MAPPING.get(language_name, "en")
