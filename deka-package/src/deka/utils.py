"""
Utility functions for Deka.
"""

from typing import Tuple, Optional, Dict, List


# Model definitions for each provider
PROVIDER_MODELS: Dict[str, List[str]] = {
    'openai': [
        'gpt-4',
        'gpt-4-turbo', 
        'gpt-4o',
        'gpt-3.5-turbo',
        'gpt-4o-mini',
    ],
    'anthropic': [
        'claude-3-5-sonnet-20241022',
        'claude-3-5-sonnet-20240620', 
        'claude-3-sonnet-20240229',
        'claude-3-haiku-20240307',
        'claude-3-opus-20240229',
    ],
    'google-gemini': [
        'gemini-2.0-flash-001',
        'gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-1.5-pro-002',
        'gemini-1.5-flash-002',
    ],
    'google': [
        # Google Translate doesn't have models, just the service
    ],
    'deepl': [
        # DeepL doesn't have models, just the service
    ],
    'ghananlp': [
        # GhanaNLP doesn't have models, just the service
    ]
}

# Default models for each provider
DEFAULT_MODELS: Dict[str, str] = {
    'openai': 'gpt-3.5-turbo',
    'anthropic': 'claude-3-5-sonnet-20241022',
    'google-gemini': 'gemini-2.0-flash-001',
    'google': None,  # No models for Google Translate
    'deepl': None,   # No models for DeepL
    'ghananlp': None,  # No models for GhanaNLP
}

# Provider aliases for convenience
PROVIDER_ALIASES: Dict[str, str] = {
    # Existing aliases
    'google-translate': 'google',
    'gpt': 'openai',
    'chatgpt': 'openai',
    'claude': 'anthropic',
    
    # New aliases
    'gemini': 'google-gemini',
    'google-gemini': 'google-gemini',
    
    # Model-specific aliases
    'gpt-4': 'openai/gpt-4',
    'gpt-3.5': 'openai/gpt-3.5-turbo',
    'claude-3-5': 'anthropic/claude-3-5-sonnet-20241022',
    'gemini-2': 'google-gemini/gemini-2.0-flash-001',
}


def parse_provider_name(provider_name: str) -> Tuple[str, Optional[str]]:
    """
    Parse provider name that may include model specification.
    
    Args:
        provider_name: Provider name, optionally with model (e.g., "openai/gpt-4")
        
    Returns:
        Tuple of (provider, model). Model is None if not specified.
        
    Examples:
        >>> parse_provider_name("openai")
        ("openai", None)
        >>> parse_provider_name("openai/gpt-4")
        ("openai", "gpt-4")
        >>> parse_provider_name("anthropic/claude-3-5-sonnet")
        ("anthropic", "claude-3-5-sonnet-20241022")
    """
    # Check aliases first
    if provider_name in PROVIDER_ALIASES:
        provider_name = PROVIDER_ALIASES[provider_name]
    
    # Parse provider/model format
    if '/' in provider_name:
        provider, model = provider_name.split('/', 1)
        
        # Normalize provider name through aliases
        if provider in PROVIDER_ALIASES:
            provider = PROVIDER_ALIASES[provider]
            
        return provider, model
    else:
        # Just provider name, no model specified
        return provider_name, None


def get_default_model(provider: str) -> Optional[str]:
    """
    Get the default model for a provider.
    
    Args:
        provider: Provider name
        
    Returns:
        Default model name, or None if provider doesn't use models
    """
    return DEFAULT_MODELS.get(provider)


def validate_provider_model(provider: str, model: str) -> bool:
    """
    Validate that a provider supports a specific model.
    Now uses permissive validation - warns about unknown models but allows them.

    Args:
        provider: Provider name
        model: Model name

    Returns:
        Always True (let provider APIs validate)
    """
    if provider not in PROVIDER_MODELS:
        print(f"⚠️  Warning: Unknown provider '{provider}', trying anyway...")
        return True

    supported_models = PROVIDER_MODELS[provider]

    # If provider doesn't use models (like Google Translate), any model is invalid
    if not supported_models:
        if model is not None:
            print(f"⚠️  Warning: Provider '{provider}' doesn't support model selection, ignoring model '{model}'")
        return True

    # Check if model is in our known list
    if model not in supported_models:
        # Suggest similar models
        import difflib
        suggestions = difflib.get_close_matches(model, supported_models, n=3, cutoff=0.6)
        if suggestions:
            print(f"⚠️  Warning: Model '{model}' not in known list for '{provider}'. Did you mean: {', '.join(suggestions)}? Trying anyway...")
        else:
            print(f"⚠️  Warning: Model '{model}' not in known list for '{provider}'. Known models: {', '.join(supported_models)}. Trying anyway...")

    return True  # Always allow - let provider API validate


def get_supported_models(provider: str) -> List[str]:
    """
    Get list of supported models for a provider.
    
    Args:
        provider: Provider name
        
    Returns:
        List of supported model names
    """
    return PROVIDER_MODELS.get(provider, [])


def normalize_model_name(provider: str, model: str) -> str:
    """
    Normalize model name for a provider (handle aliases, etc.).
    
    Args:
        provider: Provider name
        model: Model name (may be alias)
        
    Returns:
        Normalized model name
    """
    # Handle model aliases per provider
    model_aliases = {
        'anthropic': {
            'claude-3-5-sonnet': 'claude-3-5-sonnet-20241022',
            'claude-3-sonnet': 'claude-3-sonnet-20240229',
            'claude-3-haiku': 'claude-3-haiku-20240307',
            'claude-3-opus': 'claude-3-opus-20240229',
        },
        'google-gemini': {
            'gemini-2.0-flash': 'gemini-2.0-flash-001',
            'gemini-1.5-pro': 'gemini-1.5-pro',
            'gemini-1.5-flash': 'gemini-1.5-flash',
        }
    }
    
    if provider in model_aliases and model in model_aliases[provider]:
        return model_aliases[provider][model]
    
    return model


def resolve_provider_and_model(provider_name: str) -> Tuple[str, Optional[str]]:
    """
    Resolve provider name and model, handling all aliases and defaults.
    
    Args:
        provider_name: Provider specification (e.g., "openai", "openai/gpt-4", "gpt-4")
        
    Returns:
        Tuple of (provider, model) with all aliases resolved
        
    Raises:
        ValueError: If provider or model is not supported
    """
    provider, model = parse_provider_name(provider_name)
    
    # Validate provider exists
    if provider not in PROVIDER_MODELS:
        available_providers = list(PROVIDER_MODELS.keys())
        raise ValueError(
            f"Provider '{provider}' not supported. "
            f"Available providers: {', '.join(available_providers)}"
        )
    
    # If no model specified, use default
    if model is None:
        model = get_default_model(provider)
    else:
        # Normalize model name
        model = normalize_model_name(provider, model)
        
        # Validate model is supported
        if not validate_provider_model(provider, model):
            supported_models = get_supported_models(provider)
            if supported_models:
                raise ValueError(
                    f"Model '{model}' not supported by provider '{provider}'. "
                    f"Supported models: {', '.join(supported_models)}"
                )
            else:
                raise ValueError(
                    f"Provider '{provider}' does not support model selection"
                )
    
    return provider, model
