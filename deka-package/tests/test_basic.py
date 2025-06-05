"""
Basic tests for Deka package.
"""

import pytest
from deka import configure, reset_config, normalize_language, list_languages, list_providers
from deka.exceptions import ConfigurationError, LanguageNotSupportedError


def test_configuration():
    """Test configuration functionality."""
    # Reset config first
    reset_config()
    
    # Test configuration
    configure({'test_key': 'test_value'})
    
    # Test getting config
    from deka.config import get_config
    assert get_config('test_key') == 'test_value'
    
    # Test missing key
    with pytest.raises(ConfigurationError):
        get_config('missing_key')


def test_language_normalization():
    """Test language normalization."""
    # Test basic normalization
    assert normalize_language('french') == 'french'
    assert normalize_language('fr') == 'french'
    assert normalize_language('French') == 'french'
    assert normalize_language('FRENCH') == 'french'
    
    # Test aliases
    assert normalize_language('mandarin') == 'chinese'
    assert normalize_language('zh') == 'chinese'
    
    # Test invalid language
    with pytest.raises(LanguageNotSupportedError):
        normalize_language('klingon')


def test_list_functions():
    """Test list functions."""
    # Test list languages
    languages = list_languages()
    assert isinstance(languages, list)
    assert 'english' in languages
    assert 'french' in languages
    assert len(languages) > 50  # Should have many languages
    
    # Test list providers
    providers = list_providers()
    assert isinstance(providers, list)
    assert len(providers) > 0
    
    # Check provider structure
    for provider in providers:
        assert 'id' in provider
        assert 'name' in provider
        assert 'description' in provider
        assert 'type' in provider


def test_models():
    """Test data models."""
    from deka.models import TranslationRequest, TranslationResponse
    
    # Test TranslationRequest
    request = TranslationRequest(
        text="Hello",
        target_language="french"
    )
    assert request.text == "Hello"
    assert request.target_language == "french"
    
    # Test empty text validation
    with pytest.raises(ValueError):
        TranslationRequest(text="", target_language="french")
    
    # Test TranslationResponse
    response = TranslationResponse(
        text="Bonjour",
        source_language="english",
        target_language="french",
        provider="google"
    )
    assert response.text == "Bonjour"
    assert response.characters_used == 7  # "Bonjour"


if __name__ == "__main__":
    pytest.main([__file__])
