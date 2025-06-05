"""
Configuration management for Deka.
"""

from typing import Dict, Any, Optional
from .exceptions import ConfigurationError

# Global configuration storage
_config: Dict[str, Any] = {}


def configure(config: Dict[str, Any]) -> None:
    """
    Configure Deka with API keys and settings.
    
    Args:
        config: Dictionary containing configuration options
        
    Example:
        >>> deka.configure({
        ...     'google_api_key': 'your-google-key',
        ...     'deepl_api_key': 'your-deepl-key',
        ...     'openai_api_key': 'your-openai-key',
        ...     'default_provider': 'google'
        ... })
    """
    global _config
    _config.update(config)


def get_config(key: str = None) -> Any:
    """
    Get configuration value(s).
    
    Args:
        key: Specific configuration key to retrieve. If None, returns all config.
        
    Returns:
        Configuration value or entire config dict
        
    Raises:
        ConfigurationError: If key is not found
    """
    if key is None:
        return _config.copy()
    
    if key not in _config:
        raise ConfigurationError(f"Configuration key '{key}' not found")
    
    return _config[key]


def get_api_key(provider: str) -> str:
    """
    Get API key for a specific provider.
    
    Args:
        provider: Provider name (e.g., 'google', 'deepl', 'openai')
        
    Returns:
        API key string
        
    Raises:
        ConfigurationError: If API key is not configured
    """
    key_name = f"{provider}_api_key"
    
    if key_name not in _config:
        raise ConfigurationError(
            f"API key for provider '{provider}' not configured. "
            f"Please set '{key_name}' in your configuration."
        )
    
    api_key = _config[key_name]
    if not api_key or not isinstance(api_key, str):
        raise ConfigurationError(f"Invalid API key for provider '{provider}'")
    
    return api_key


def is_provider_configured(provider: str) -> bool:
    """
    Check if a provider is properly configured.
    
    Args:
        provider: Provider name
        
    Returns:
        True if provider has valid API key configured
    """
    try:
        get_api_key(provider)
        return True
    except ConfigurationError:
        return False


def list_configured_providers() -> list:
    """
    List all providers that have API keys configured.
    
    Returns:
        List of provider names
    """
    providers = []
    for key in _config:
        if key.endswith('_api_key') and _config[key]:
            provider = key.replace('_api_key', '')
            providers.append(provider)
    return providers


def reset_config() -> None:
    """Reset all configuration. Useful for testing."""
    global _config
    _config.clear()
