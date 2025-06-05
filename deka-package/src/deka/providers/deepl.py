"""
DeepL provider for Deka.
"""

import time
import requests
import aiohttp
from typing import Optional
from .base import BaseProvider
from ..models import TranslationRequest, TranslationResponse
from ..language_mapper import get_provider_code
from ..exceptions import ProviderError


class DeepLProvider(BaseProvider):
    """DeepL API provider."""
    
    display_name = "DeepL"
    description = "DeepL's high-quality neural translation service"
    provider_type = "api"
    
    @property
    def provider_name(self) -> str:
        return "deepl"
    
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using DeepL API."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Determine if using free or pro API
        is_free = api_key.endswith(':fx')
        base_url = "https://api-free.deepl.com" if is_free else "https://api.deepl.com"
        
        # Prepare language codes
        target_lang = get_provider_code(request.target_language, self.provider_name)
        source_lang = None
        if request.source_language:
            source_lang = get_provider_code(request.source_language, self.provider_name)
        
        # Prepare request
        url = f"{base_url}/v2/translate"
        headers = {
            'Authorization': f'DeepL-Auth-Key {api_key}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        data = {
            'text': request.text,
            'target_lang': target_lang,
        }
        
        if source_lang:
            data['source_lang'] = source_lang
        
        # Make request
        try:
            response = requests.post(url, headers=headers, data=data, timeout=30)
            self._handle_http_error(response)
            
            result = response.json()
            
            # Extract translation
            if 'translations' not in result or not result['translations']:
                raise ProviderError("Invalid response format from DeepL", self.provider_name)
            
            translation = result['translations'][0]
            translated_text = translation['text']
            detected_source = translation.get('detected_source_language', source_lang or 'auto')
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                detected_source_language=detected_source,
                characters_billed=len(request.text),
                api_type='free' if is_free else 'pro'
            )
            
        except requests.RequestException as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
    
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using DeepL API asynchronously."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Determine if using free or pro API
        is_free = api_key.endswith(':fx')
        base_url = "https://api-free.deepl.com" if is_free else "https://api.deepl.com"
        
        # Prepare language codes
        target_lang = get_provider_code(request.target_language, self.provider_name)
        source_lang = None
        if request.source_language:
            source_lang = get_provider_code(request.source_language, self.provider_name)
        
        # Prepare request
        url = f"{base_url}/v2/translate"
        headers = {
            'Authorization': f'DeepL-Auth-Key {api_key}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        
        data = {
            'text': request.text,
            'target_lang': target_lang,
        }
        
        if source_lang:
            data['source_lang'] = source_lang
        
        # Make async request
        session = await self._get_session()
        
        try:
            async with session.post(url, headers=headers, data=data) as response:
                await self._handle_aiohttp_error(response)
                
                result = await response.json()
                
                # Extract translation
                if 'translations' not in result or not result['translations']:
                    raise ProviderError("Invalid response format from DeepL", self.provider_name)
                
                translation = result['translations'][0]
                translated_text = translation['text']
                detected_source = translation.get('detected_source_language', source_lang or 'auto')
                
                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)
                
                return self._create_response(
                    translated_text=translated_text,
                    request=request,
                    response_time_ms=response_time_ms,
                    detected_source_language=detected_source,
                    characters_billed=len(request.text),
                    api_type='free' if is_free else 'pro'
                )
                
        except aiohttp.ClientError as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
