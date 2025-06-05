"""
Custom exceptions for Deka.
"""


class DekaError(Exception):
    """Base exception for all Deka errors."""
    pass


class ConfigurationError(DekaError):
    """Raised when there's an issue with configuration."""
    pass


class ProviderError(DekaError):
    """Raised when a translation provider encounters an error."""
    
    def __init__(self, message: str, provider: str, status_code: int = None):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code


class LanguageNotSupportedError(DekaError):
    """Raised when a language is not supported by a provider."""
    
    def __init__(self, language: str, provider: str):
        message = f"Language '{language}' is not supported by provider '{provider}'"
        super().__init__(message)
        self.language = language
        self.provider = provider


class APIKeyError(ConfigurationError):
    """Raised when API key is missing or invalid."""
    
    def __init__(self, provider: str):
        message = f"API key for provider '{provider}' is missing or invalid"
        super().__init__(message)
        self.provider = provider


class RateLimitError(ProviderError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, provider: str, retry_after: int = None):
        message = f"Rate limit exceeded for provider '{provider}'"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message, provider, 429)
        self.retry_after = retry_after


class QuotaExceededError(ProviderError):
    """Raised when API quota is exceeded."""
    
    def __init__(self, provider: str):
        message = f"API quota exceeded for provider '{provider}'"
        super().__init__(message, provider, 403)
