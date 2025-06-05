"""
Core translation functions for Deka.
"""

import asyncio
from typing import List, Optional, Union
from .models import TranslationRequest, TranslationResponse, ComparisonResult
from .providers import create_provider_instance, list_providers as get_available_providers
from .language_mapper import normalize_language
from .config import list_configured_providers
from .exceptions import DekaError, ConfigurationError
from .utils import resolve_provider_and_model


def translate(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    provider: Optional[str] = None
) -> TranslationResponse:
    """
    Translate text using a single provider.
    
    Args:
        text: Text to translate
        target_language: Target language (e.g., 'french', 'fr', 'español')
        source_language: Source language (optional, auto-detected if not provided)
        provider: Provider to use (e.g., 'google', 'deepl', 'openai')
        
    Returns:
        Translation response
        
    Raises:
        ConfigurationError: If provider is not configured
        ProviderError: If translation fails
        
    Example:
        >>> result = deka.translate("Hello world", "french", provider="google")
        >>> print(result.text)
        "Bonjour le monde"
    """
    # Normalize languages
    target_language = normalize_language(target_language)
    if source_language:
        source_language = normalize_language(source_language)
    
    # Determine provider and model
    if not provider:
        configured = list_configured_providers()
        if not configured:
            raise ConfigurationError("No providers configured. Please run deka.configure() first.")
        provider = configured[0]  # Use first configured provider

    # Resolve provider and model
    provider_name, model = resolve_provider_and_model(provider)

    # Create request
    request = TranslationRequest(
        text=text,
        target_language=target_language,
        source_language=source_language,
        provider=provider_name
    )

    # Get provider and translate
    provider_instance = create_provider_instance(provider_name, model)
    return provider_instance.translate(request)


async def translate_async(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    provider: Optional[str] = None
) -> TranslationResponse:
    """
    Translate text using a single provider asynchronously.
    
    Args:
        text: Text to translate
        target_language: Target language
        source_language: Source language (optional)
        provider: Provider to use
        
    Returns:
        Translation response
    """
    # Normalize languages
    target_language = normalize_language(target_language)
    if source_language:
        source_language = normalize_language(source_language)
    
    # Determine provider and model
    if not provider:
        configured = list_configured_providers()
        if not configured:
            raise ConfigurationError("No providers configured. Please run deka.configure() first.")
        provider = configured[0]

    # Resolve provider and model
    provider_name, model = resolve_provider_and_model(provider)

    # Create request
    request = TranslationRequest(
        text=text,
        target_language=target_language,
        source_language=source_language,
        provider=provider_name
    )

    # Get provider and translate
    provider_instance = create_provider_instance(provider_name, model)
    try:
        return await provider_instance.translate_async(request)
    finally:
        await provider_instance.close()


def compare(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    providers: Optional[List[str]] = None
) -> ComparisonResult:
    """
    Compare translations from multiple providers.
    
    Args:
        text: Text to translate
        target_language: Target language
        source_language: Source language (optional)
        providers: List of providers to compare (uses all configured if not specified)
        
    Returns:
        Comparison result with translations from all providers
        
    Example:
        >>> comparison = deka.compare("Hello", "french", providers=["google", "deepl"])
        >>> for result in comparison.results:
        ...     print(f"{result.provider}: {result.text}")
        google: Bonjour
        deepl: Bonjour
    """
    # Normalize languages
    target_language = normalize_language(target_language)
    if source_language:
        source_language = normalize_language(source_language)
    
    # Determine providers
    if not providers:
        providers = list_configured_providers()
        if not providers:
            raise ConfigurationError("No providers configured. Please run deka.configure() first.")
    
    # Create request
    request = TranslationRequest(
        text=text,
        target_language=target_language,
        source_language=source_language
    )
    
    # Translate with each provider
    results = []
    errors = []

    for provider in providers:
        try:
            # Resolve provider and model
            provider_name, model = resolve_provider_and_model(provider)
            provider_instance = create_provider_instance(provider_name, model)
            result = provider_instance.translate(request)
            results.append(result)
        except Exception as e:
            errors.append(f"{provider}: {str(e)}")
    
    if not results:
        raise DekaError(f"All providers failed. Errors: {'; '.join(errors)}")
    
    return ComparisonResult(request=request, results=results)


async def compare_async(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    providers: Optional[List[str]] = None
) -> ComparisonResult:
    """
    Compare translations from multiple providers asynchronously.
    
    Args:
        text: Text to translate
        target_language: Target language
        source_language: Source language (optional)
        providers: List of providers to compare
        
    Returns:
        Comparison result with translations from all providers
    """
    # Normalize languages
    target_language = normalize_language(target_language)
    if source_language:
        source_language = normalize_language(source_language)
    
    # Determine providers
    if not providers:
        providers = list_configured_providers()
        if not providers:
            raise ConfigurationError("No providers configured. Please run deka.configure() first.")
    
    # Create request
    request = TranslationRequest(
        text=text,
        target_language=target_language,
        source_language=source_language
    )
    
    # Create provider instances
    provider_instances = []
    for provider in providers:
        try:
            # Resolve provider and model
            provider_name, model = resolve_provider_and_model(provider)
            instance = create_provider_instance(provider_name, model)
            provider_instances.append((provider, instance))
        except Exception as e:
            # Skip providers that can't be created
            continue
    
    if not provider_instances:
        raise ConfigurationError("No valid providers available")
    
    # Translate with all providers concurrently
    async def translate_with_provider(provider_name, provider_instance):
        try:
            return await provider_instance.translate_async(request)
        except Exception as e:
            return None  # Return None for failed translations
        finally:
            await provider_instance.close()
    
    # Run all translations concurrently
    tasks = [
        translate_with_provider(name, instance) 
        for name, instance in provider_instances
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter out failed translations
    successful_results = [r for r in results if isinstance(r, TranslationResponse)]
    
    if not successful_results:
        raise DekaError("All providers failed during async comparison")
    
    return ComparisonResult(request=request, results=successful_results)
