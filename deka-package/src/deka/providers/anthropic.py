"""
Anthropic Claude provider for Deka.
"""

import time
import requests
import aiohttp
import json
from typing import Optional
from .base import BaseProvider
from ..models import TranslationRequest, TranslationResponse
from ..language_mapper import normalize_language
from ..exceptions import ProviderError


class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider for translation."""

    display_name = "Anthropic Claude"
    description = "Anthropic's Claude models for nuanced translation"
    provider_type = "llm"
    default_model = "claude-3-5-sonnet-20241022"
    supported_models = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-20240620",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "claude-3-opus-20240229",
    ]
    
    @property
    def provider_name(self) -> str:
        return "anthropic"
    
    def _create_translation_prompt(self, request: TranslationRequest) -> str:
        """Create a translation prompt for Claude."""
        target_lang = normalize_language(request.target_language)
        
        if request.source_language:
            source_lang = normalize_language(request.source_language)
            prompt = f"Translate the following text from {source_lang} to {target_lang}. Provide only the translation without any explanations or additional text:\n\n{request.text}"
        else:
            prompt = f"Translate the following text to {target_lang}. Provide only the translation without any explanations or additional text:\n\n{request.text}"
        
        return prompt
    
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Anthropic Claude."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Create prompt
        prompt = self._create_translation_prompt(request)
        
        # Prepare request
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01',
        }
        
        data = {
            'model': self.model,
            'max_tokens': len(request.text) * 3,  # Rough estimate for translation length
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'system': 'You are a professional translator. Translate text accurately while preserving meaning, tone, and cultural context.'
        }
        
        # Make request
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            self._handle_http_error(response)
            
            result = response.json()
            
            # Extract translation
            if 'content' not in result or not result['content']:
                raise ProviderError("Invalid response format from Anthropic", self.provider_name)
            
            translated_text = result['content'][0]['text'].strip()
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract usage information
            usage = result.get('usage', {})
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                model=self.model,
                input_tokens=usage.get('input_tokens'),
                output_tokens=usage.get('output_tokens')
            )
            
        except requests.RequestException as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
    
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Anthropic Claude asynchronously."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Create prompt
        prompt = self._create_translation_prompt(request)
        
        # Prepare request
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01',
        }
        
        data = {
            'model': self.model,
            'max_tokens': len(request.text) * 3,
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'system': 'You are a professional translator. Translate text accurately while preserving meaning, tone, and cultural context.'
        }
        
        # Make async request
        session = await self._get_session()
        
        try:
            async with session.post(url, headers=headers, json=data) as response:
                await self._handle_aiohttp_error(response)
                
                result = await response.json()
                
                # Extract translation
                if 'content' not in result or not result['content']:
                    raise ProviderError("Invalid response format from Anthropic", self.provider_name)
                
                translated_text = result['content'][0]['text'].strip()
                
                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)
                
                # Extract usage information
                usage = result.get('usage', {})
                
                return self._create_response(
                    translated_text=translated_text,
                    request=request,
                    response_time_ms=response_time_ms,
                    model=self.model,
                    input_tokens=usage.get('input_tokens'),
                    output_tokens=usage.get('output_tokens')
                )
                
        except aiohttp.ClientError as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
