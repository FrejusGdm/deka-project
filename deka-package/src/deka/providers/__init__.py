"""
Translation providers for Deka.
"""

from typing import Dict, List, Type
from .base import BaseProvider
from .google import GoogleTranslateProvider
from .deepl import DeepLProvider
from .openai import OpenAIProvider
from .anthropic import AnthropicProvider
from .gemini import GeminiProvider
from .ghananlp import GhanaNLPProvider

# Registry of all available providers
PROVIDERS: Dict[str, Type[BaseProvider]] = {
    'google': GoogleTranslateProvider,
    'deepl': DeepLProvider,
    'openai': OpenAIProvider,
    'anthropic': AnthropicProvider,
    'google-gemini': GeminiProvider,
    'ghananlp': GhanaNLPProvider,
}

# Provider aliases for convenience
PROVIDER_ALIASES = {
    'google-translate': 'google',
    'gpt': 'openai',
    'chatgpt': 'openai',
    'claude': 'anthropic',
    'gemini': 'google-gemini',
    'ghana': 'ghananlp',
    'ghana-nlp': 'ghananlp',
}


def get_provider(provider_name: str) -> Type[BaseProvider]:
    """
    Get a provider class by name.
    
    Args:
        provider_name: Name of the provider
        
    Returns:
        Provider class
        
    Raises:
        ValueError: If provider is not found
    """
    # Check aliases first
    if provider_name in PROVIDER_ALIASES:
        provider_name = PROVIDER_ALIASES[provider_name]
    
    if provider_name not in PROVIDERS:
        available = list(PROVIDERS.keys()) + list(PROVIDER_ALIASES.keys())
        raise ValueError(
            f"Provider '{provider_name}' not found. "
            f"Available providers: {', '.join(available)}"
        )
    
    return PROVIDERS[provider_name]


def list_providers() -> List[Dict[str, str]]:
    """
    List all available providers.
    
    Returns:
        List of provider information dictionaries
    """
    providers = []
    for name, provider_class in PROVIDERS.items():
        providers.append({
            'id': name,
            'name': provider_class.display_name,
            'description': provider_class.description,
            'type': provider_class.provider_type,
        })
    return providers


def create_provider_instance(provider_name: str, model: str = None) -> BaseProvider:
    """
    Create an instance of a provider.

    Args:
        provider_name: Name of the provider
        model: Optional model name

    Returns:
        Provider instance
    """
    provider_class = get_provider(provider_name)
    return provider_class(model=model)
