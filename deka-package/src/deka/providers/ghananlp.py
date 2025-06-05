"""
GhanaNLP provider for Deka.
Specializes in Ghanaian and African languages.
"""

import time
import requests
import aiohttp
from typing import Optional
from .base import BaseProvider
from ..models import TranslationRequest, TranslationResponse
from ..language_mapper import get_provider_code
from ..exceptions import ProviderError, APIKeyError


class GhanaNLPProvider(BaseProvider):
    """GhanaNLP provider for African language translation."""
    
    display_name = "GhanaNLP"
    description = "GhanaNLP's translation service for Ghanaian and African languages"
    provider_type = "api"
    
    # GhanaNLP doesn't use models, just the service
    default_model = None
    supported_models = []
    
    # Language mappings specific to GhanaNLP
    # Based on their API: English - en, Twi - tw, Ga - gaa, Ewe - ee, Fante - fat, 
    # Dagbani - dag, Gurene - gur, Yoruba - yo, Kikuyu - ki, Luo - luo, Kimeru - mer
    GHANANLP_LANGUAGES = {
        'english': 'en',
        'twi': 'tw',
        'ga': 'gaa',
        'ewe': 'ee', 
        'fante': 'fat',
        'dagbani': 'dag',
        'gurene': 'gur',
        'yoruba': 'yo',
        'kikuyu': 'ki',
        'luo': 'luo',
        'kimeru': 'mer',
    }
    
    @property
    def provider_name(self) -> str:
        return "ghananlp"
    
    def _get_language_code(self, language: str) -> str:
        """
        Get GhanaNLP language code for a language.

        Args:
            language: Normalized language name

        Returns:
            GhanaNLP language code

        Raises:
            ProviderError: If language not supported by GhanaNLP
        """
        # Handle special case for Ga language (Ghana) vs Irish
        # When using GhanaNLP, 'ga' should refer to Ga language (Ghana), not Irish
        if language.lower() in ['ga', 'ga language', 'ga (ghana)', 'ga people', 'irish']:
            # For GhanaNLP, if someone says 'ga' or even 'irish', assume they mean Ga language
            if language.lower() == 'irish':
                # This is likely a mistake - user probably meant Ga language when using GhanaNLP
                print(f"⚠️  Note: GhanaNLP doesn't support Irish. Assuming you meant Ga language (Ghana).")
            return 'gaa'  # GhanaNLP code for Ga language

        if language in self.GHANANLP_LANGUAGES:
            return self.GHANANLP_LANGUAGES[language]

        # Check if it's already a GhanaNLP code
        if language in self.GHANANLP_LANGUAGES.values():
            return language

        # Language not supported
        supported = list(self.GHANANLP_LANGUAGES.keys())
        raise ProviderError(
            f"Language '{language}' not supported by GhanaNLP. "
            f"Supported languages: {', '.join(supported)}",
            self.provider_name
        )
    
    def _create_language_pair(self, source_lang: str, target_lang: str) -> str:
        """
        Create GhanaNLP language pair format (from-to).
        
        Args:
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            Language pair string (e.g., "en-tw")
        """
        return f"{source_lang}-{target_lang}"
    
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using GhanaNLP API."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Get language codes
        try:
            target_lang_code = self._get_language_code(request.target_language)
            
            # For source language, default to English if not specified
            if request.source_language:
                source_lang_code = self._get_language_code(request.source_language)
            else:
                source_lang_code = 'en'  # Default to English
            
            # Create language pair
            lang_pair = self._create_language_pair(source_lang_code, target_lang_code)
            
        except ProviderError:
            # Re-raise provider errors as-is
            raise
        except Exception as e:
            raise ProviderError(f"Language mapping error: {str(e)}", self.provider_name)
        
        # Prepare request
        url = "https://translation-api.ghananlp.org/v1/translate"
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': api_key,  # Azure API Management style
        }
        
        data = {
            'in': request.text,
            'lang': lang_pair
        }
        
        # Make request
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            self._handle_http_error(response)
            
            # GhanaNLP returns the translated text directly as a string
            translated_text = response.text.strip().strip('"')  # Remove quotes if present
            
            if not translated_text:
                raise ProviderError("Empty response from GhanaNLP", self.provider_name)
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                language_pair=lang_pair,
                characters_billed=len(request.text)
            )
            
        except requests.RequestException as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
    
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using GhanaNLP API asynchronously."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Get language codes
        try:
            target_lang_code = self._get_language_code(request.target_language)
            
            # For source language, default to English if not specified
            if request.source_language:
                source_lang_code = self._get_language_code(request.source_language)
            else:
                source_lang_code = 'en'  # Default to English
            
            # Create language pair
            lang_pair = self._create_language_pair(source_lang_code, target_lang_code)
            
        except ProviderError:
            # Re-raise provider errors as-is
            raise
        except Exception as e:
            raise ProviderError(f"Language mapping error: {str(e)}", self.provider_name)
        
        # Prepare request
        url = "https://translation-api.ghananlp.org/v1/translate"
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': api_key,  # Azure API Management style
        }
        
        data = {
            'in': request.text,
            'lang': lang_pair
        }
        
        # Make async request
        session = await self._get_session()
        
        try:
            async with session.post(url, headers=headers, json=data) as response:
                await self._handle_aiohttp_error(response)
                
                # GhanaNLP returns the translated text directly as a string
                translated_text = await response.text()
                translated_text = translated_text.strip().strip('"')  # Remove quotes if present
                
                if not translated_text:
                    raise ProviderError("Empty response from GhanaNLP", self.provider_name)
                
                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)
                
                return self._create_response(
                    translated_text=translated_text,
                    request=request,
                    response_time_ms=response_time_ms,
                    language_pair=lang_pair,
                    characters_billed=len(request.text)
                )
                
        except aiohttp.ClientError as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of languages supported by GhanaNLP."""
        return list(cls.GHANANLP_LANGUAGES.keys())
    
    @classmethod
    def get_language_pairs(cls) -> list:
        """Get list of supported language pairs."""
        languages = list(cls.GHANANLP_LANGUAGES.values())
        pairs = []
        
        # Generate all possible pairs
        for source in languages:
            for target in languages:
                if source != target:
                    pairs.append(f"{source}-{target}")
        
        return pairs
