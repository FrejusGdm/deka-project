"""
OpenAI provider for Deka.
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


class OpenAIProvider(BaseProvider):
    """OpenAI ChatGPT provider for translation."""

    display_name = "OpenAI ChatGPT"
    description = "OpenAI's ChatGPT models for high-quality translation"
    provider_type = "llm"
    default_model = "gpt-3.5-turbo"
    supported_models = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4o",
        "gpt-3.5-turbo",
        "gpt-4o-mini",
    ]
    
    @property
    def provider_name(self) -> str:
        return "openai"
    
    def _create_translation_prompt(self, request: TranslationRequest) -> str:
        """Create a translation prompt for ChatGPT."""
        target_lang = normalize_language(request.target_language)
        
        if request.source_language:
            source_lang = normalize_language(request.source_language)
            prompt = f"Translate the following text from {source_lang} to {target_lang}. Return only the translation, no explanations:\n\n{request.text}"
        else:
            prompt = f"Translate the following text to {target_lang}. Return only the translation, no explanations:\n\n{request.text}"
        
        return prompt
    
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using OpenAI ChatGPT."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Create prompt
        prompt = self._create_translation_prompt(request)
        
        # Prepare request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a professional translator. Translate text accurately while preserving meaning and tone.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': len(request.text) * 3,  # Rough estimate for translation length
            'temperature': 0.1,  # Low temperature for consistent translations
        }
        
        # Make request
        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            self._handle_http_error(response)
            
            result = response.json()
            
            # Extract translation
            if 'choices' not in result or not result['choices']:
                raise ProviderError("Invalid response format from OpenAI", self.provider_name)
            
            translated_text = result['choices'][0]['message']['content'].strip()
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract usage information
            usage = result.get('usage', {})
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                model=self.model,
                prompt_tokens=usage.get('prompt_tokens'),
                completion_tokens=usage.get('completion_tokens'),
                total_tokens=usage.get('total_tokens')
            )
            
        except requests.RequestException as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
    
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using OpenAI ChatGPT asynchronously."""
        start_time = time.time()
        
        # Get API key
        api_key = self._get_api_key()
        
        # Create prompt
        prompt = self._create_translation_prompt(request)
        
        # Prepare request
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        
        data = {
            'model': self.model,
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a professional translator. Translate text accurately while preserving meaning and tone.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': len(request.text) * 3,
            'temperature': 0.1,
        }
        
        # Make async request
        session = await self._get_session()
        
        try:
            async with session.post(url, headers=headers, json=data) as response:
                await self._handle_aiohttp_error(response)
                
                result = await response.json()
                
                # Extract translation
                if 'choices' not in result or not result['choices']:
                    raise ProviderError("Invalid response format from OpenAI", self.provider_name)
                
                translated_text = result['choices'][0]['message']['content'].strip()
                
                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)
                
                # Extract usage information
                usage = result.get('usage', {})
                
                return self._create_response(
                    translated_text=translated_text,
                    request=request,
                    response_time_ms=response_time_ms,
                    model=self.model,
                    prompt_tokens=usage.get('prompt_tokens'),
                    completion_tokens=usage.get('completion_tokens'),
                    total_tokens=usage.get('total_tokens')
                )
                
        except aiohttp.ClientError as e:
            raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
