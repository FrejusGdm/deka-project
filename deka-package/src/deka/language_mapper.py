"""
Language code normalization and mapping for different providers.
"""

from typing import Dict, List, Optional, Set
import difflib
from .exceptions import LanguageNotSupportedError

# ISO 639-1 language codes to common names mapping
ISO_TO_NAME = {
    'en': 'english',
    'es': 'spanish', 
    'fr': 'french',
    'de': 'german',
    'it': 'italian',
    'pt': 'portuguese',
    'ru': 'russian',
    'ja': 'japanese',
    'ko': 'korean',
    'zh': 'chinese',
    'ar': 'arabic',
    'hi': 'hindi',
    'tr': 'turkish',
    'pl': 'polish',
    'nl': 'dutch',
    'sv': 'swedish',
    'da': 'danish',
    'no': 'norwegian',
    'fi': 'finnish',
    'el': 'greek',
    'he': 'hebrew',
    'th': 'thai',
    'vi': 'vietnamese',
    'uk': 'ukrainian',
    'cs': 'czech',
    'hu': 'hungarian',
    'ro': 'romanian',
    'bg': 'bulgarian',
    'hr': 'croatian',
    'sk': 'slovak',
    'sl': 'slovenian',
    'et': 'estonian',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'mt': 'maltese',
    'ga': 'irish',
    'cy': 'welsh',
    'eu': 'basque',
    'ca': 'catalan',
    'gl': 'galician',
    'is': 'icelandic',
    'mk': 'macedonian',
    'sq': 'albanian',
    'sr': 'serbian',
    'bs': 'bosnian',
    'me': 'montenegrin',
    'yo': 'yoruba',
    'zu': 'zulu',
    'xh': 'xhosa',
    'af': 'afrikaans',
    'sw': 'swahili',
    'ha': 'hausa',
    'ig': 'igbo',
    'am': 'amharic',
    # GhanaNLP supported languages
    'tw': 'twi',
    'gaa': 'ga',  # Ga language (Ghana) - different from 'ga' (Irish)
    'ee': 'ewe',
    'fat': 'fante',
    'dag': 'dagbani',
    'gur': 'gurene',
    'ki': 'kikuyu',
    'luo': 'luo',
    'mer': 'kimeru',
    'or': 'oriya',
    'bn': 'bengali',
    'gu': 'gujarati',
    'kn': 'kannada',
    'ml': 'malayalam',
    'mr': 'marathi',
    'pa': 'punjabi',
    'ta': 'tamil',
    'te': 'telugu',
    'ur': 'urdu',
    'ne': 'nepali',
    'si': 'sinhala',
    'my': 'myanmar',
    'km': 'khmer',
    'lo': 'lao',
    'ka': 'georgian',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'kk': 'kazakh',
    'ky': 'kyrgyz',
    'tg': 'tajik',
    'tk': 'turkmen',
    'uz': 'uzbek',
    'mn': 'mongolian',
    'id': 'indonesian',
    'ms': 'malay',
    'tl': 'filipino',
}

# Reverse mapping: name to ISO code
NAME_TO_ISO = {name: code for code, name in ISO_TO_NAME.items()}

# Alternative names and variations
LANGUAGE_ALIASES = {
    'chinese': ['mandarin', 'zh-cn', 'zh-tw', 'simplified chinese', 'traditional chinese'],
    'spanish': ['castilian', 'español'],
    'portuguese': ['português'],
    'german': ['deutsch'],
    'french': ['français'],
    'arabic': ['عربي'],
    'russian': ['русский'],
    'japanese': ['日本語', 'nihongo'],
    'korean': ['한국어', 'hangul'],
    'hindi': ['हिन्दी'],
    'filipino': ['tagalog'],
    'myanmar': ['burmese'],
    # African languages - add explicit aliases to avoid confusion
    'ga': ['ga language', 'ga (ghana)', 'ga people'],  # Ga language from Ghana
    'irish': ['irish gaelic', 'gaeilge'],  # Irish language
}

# Provider-specific language code mappings
PROVIDER_MAPPINGS = {
    'google': {
        # Google Translate uses mostly ISO 639-1 codes
        'chinese': 'zh',
        'filipino': 'tl',
    },
    'deepl': {
        # DeepL uses specific codes
        'chinese': 'zh',
        'portuguese': 'pt-PT',  # European Portuguese by default
        'english': 'en-US',     # US English by default
    },
    'openai': {
        # OpenAI uses full language names in prompts
        # We'll use the normalized names directly
    },
    'anthropic': {
        # Claude uses full language names in prompts
        # We'll use the normalized names directly
    }
}


def normalize_language(language: str) -> str:
    """
    Normalize a language name or code to a standard form.
    
    Args:
        language: Language name or code (e.g., 'French', 'fr', 'français')
        
    Returns:
        Normalized language name (e.g., 'french')
        
    Raises:
        LanguageNotSupportedError: If language cannot be normalized
    """
    language = language.lower().strip()
    
    # Direct ISO code lookup
    if language in ISO_TO_NAME:
        return ISO_TO_NAME[language]
    
    # Direct name lookup
    if language in NAME_TO_ISO:
        return language
    
    # Check aliases
    for standard_name, aliases in LANGUAGE_ALIASES.items():
        if language in [alias.lower() for alias in aliases]:
            return standard_name
    
    # Fuzzy matching for typos
    all_names = list(NAME_TO_ISO.keys()) + list(ISO_TO_NAME.keys())
    matches = difflib.get_close_matches(language, all_names, n=1, cutoff=0.8)
    
    if matches:
        match = matches[0]
        if match in ISO_TO_NAME:
            return ISO_TO_NAME[match]
        return match
    
    # If no match found, suggest similar languages
    suggestions = difflib.get_close_matches(language, all_names, n=3, cutoff=0.6)
    suggestion_text = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
    
    raise LanguageNotSupportedError(
        f"Language '{language}' not recognized.{suggestion_text}", 
        "deka"
    )


def get_provider_code(language: str, provider: str) -> str:
    """
    Get the provider-specific language code.
    
    Args:
        language: Normalized language name
        provider: Provider name
        
    Returns:
        Provider-specific language code
    """
    # First normalize the language
    normalized = normalize_language(language)
    
    # Check if provider has specific mappings
    if provider in PROVIDER_MAPPINGS:
        provider_map = PROVIDER_MAPPINGS[provider]
        if normalized in provider_map:
            return provider_map[normalized]
    
    # Fall back to ISO code
    if normalized in NAME_TO_ISO:
        return NAME_TO_ISO[normalized]
    
    # This shouldn't happen if normalize_language worked
    raise LanguageNotSupportedError(normalized, provider)


def list_languages(provider: str = None) -> List[str]:
    """
    List all supported languages.
    
    Args:
        provider: Specific provider to check (optional)
        
    Returns:
        List of supported language names
    """
    # For now, return all languages we support
    # In the future, we could filter by provider capabilities
    return sorted(NAME_TO_ISO.keys())


def get_iso_code(language: str) -> str:
    """
    Get ISO 639-1 code for a language.
    
    Args:
        language: Language name or code
        
    Returns:
        ISO 639-1 code
    """
    normalized = normalize_language(language)
    return NAME_TO_ISO[normalized]
