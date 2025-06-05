"""
Google Translate provider for Deka.
"""

import time
import requests
import aiohttp
from typing import Optional
from .base import BaseProvider
from ..models import TranslationRequest, TranslationResponse
from ..language_mapper import get_provider_code
from ..exceptions import ProviderError


class GoogleTranslateProvider(BaseProvider):
    """Google Translate API provider."""
    
    display_name = "Google Translate"
    description = "Google's translation service with support for 100+ languages"
    provider_type = "api"
    
    @property
    def provider_name(self) -> str:
        return "google"
    
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Google Translate API."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Prepare language codes
        target_lang = get_provider_code(request.target_language, self.provider_name)
        source_lang = None
        if request.source_language:
            source_lang = get_provider_code(request.source_language, self.provider_name)
        
        # Prepare request
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            'key': api_key,
            'q': request.text,
            'target': target_lang,
        }
        
        if source_lang:
            params['source'] = source_lang
        
        # Make request
        try:
            response = requests.post(url, params=params, timeout=30)
            self._handle_http_error(response)
            
            data = response.json()
            
            # Extract translation
            if 'data' not in data or 'translations' not in data['data']:
                raise ProviderError("Invalid response format from Google Translate", self.provider_name)
            
            translation = data['data']['translations'][0]
            translated_text = translation['translatedText']
            detected_source = translation.get('detectedSourceLanguage', source_lang or 'auto')
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                detected_source_language=detected_source,
                characters_billed=len(request.text)
            )
            
        except requests.RequestException as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
    
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Google Translate API asynchronously."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Prepare language codes
        target_lang = get_provider_code(request.target_language, self.provider_name)
        source_lang = None
        if request.source_language:
            source_lang = get_provider_code(request.source_language, self.provider_name)
        
        # Prepare request
        url = "https://translation.googleapis.com/language/translate/v2"
        params = {
            'key': api_key,
            'q': request.text,
            'target': target_lang,
        }
        
        if source_lang:
            params['source'] = source_lang
        
        # Make async request
        session = await self._get_session()
        
        try:
            async with session.post(url, params=params) as response:
                await self._handle_aiohttp_error(response)
                
                data = await response.json()
                
                # Extract translation
                if 'data' not in data or 'translations' not in data['data']:
                    raise ProviderError("Invalid response format from Google Translate", self.provider_name)
                
                translation = data['data']['translations'][0]
                translated_text = translation['translatedText']
                detected_source = translation.get('detectedSourceLanguage', source_lang or 'auto')
                
                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)
                
                return self._create_response(
                    translated_text=translated_text,
                    request=request,
                    response_time_ms=response_time_ms,
                    detected_source_language=detected_source,
                    characters_billed=len(request.text)
                )
                
        except aiohttp.ClientError as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
