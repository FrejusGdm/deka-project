"""
Deka: A unified Python SDK for multiple translation providers.

Deka provides a simple, consistent interface to multiple translation services
including Google Translate, DeepL, OpenAI, and more. Users bring their own API keys.

Example:
    >>> import deka
    >>> deka.configure({'google_api_key': 'your-key'})
    >>> result = deka.translate("Hello world", "french", provider="google")
    >>> print(result.text)
    "Bonjour le monde"
"""

__version__ = "0.1.0"
__author__ = "Josue Godeme"
__email__ = "your.email@example.com"

from .config import configure, get_config, reset_config
from .core import translate, compare, translate_async, compare_async
from .providers import list_providers
from .language_mapper import list_languages, normalize_language
from .models import TranslationRequest, TranslationResponse, ComparisonResult
from .exceptions import DekaError, ProviderError, ConfigurationError, LanguageNotSupportedError
from .utils import get_supported_models, resolve_provider_and_model

# Main public API
__all__ = [
    # Core functions
    "translate",
    "compare", 
    "translate_async",
    "compare_async",
    
    # Configuration
    "configure",
    "get_config",
    "reset_config",
    
    # Information functions
    "list_providers",
    "list_languages",
    "normalize_language",
    "get_supported_models",
    
    # Models
    "TranslationRequest",
    "TranslationResponse", 
    "ComparisonResult",
    
    # Exceptions
    "DekaError",
    "ProviderError",
    "ConfigurationError",
    "LanguageNotSupportedError",
]
