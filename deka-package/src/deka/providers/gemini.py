"""
Google Gemini provider for Deka.
"""

import time
import asyncio
from typing import Optional
from .base import BaseProvider
from ..models import TranslationRequest, TranslationResponse
from ..language_mapper import normalize_language
from ..exceptions import ProviderError, APIKeyError

try:
    import google.genai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiProvider(BaseProvider):
    """Google Gemini provider for translation."""
    
    display_name = "Google Gemini"
    description = "Google's Gemini models for advanced AI translation"
    provider_type = "llm"
    default_model = "gemini-2.0-flash-001"
    supported_models = [
        "gemini-2.0-flash-001",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.5-pro-002",
        "gemini-1.5-flash-002",
    ]
    
    @property
    def provider_name(self) -> str:
        return "google-gemini"
    
    def __init__(self, model: Optional[str] = None):
        if not GENAI_AVAILABLE:
            raise ImportError(
                "google-genai package is required for Gemini provider. "
                "Install with: pip install google-genai"
            )
        super().__init__(model)
        self._client = None
    
    def _get_client(self):
        """Get or create Gemini client."""
        if self._client is None:
            api_key = self._get_api_key()
            genai.configure(api_key=api_key)
            self._client = genai.GenerativeModel(self.model)
        return self._client
    
    def _create_translation_prompt(self, request: TranslationRequest) -> str:
        """Create a translation prompt for Gemini."""
        target_lang = normalize_language(request.target_language)
        
        if request.source_language:
            source_lang = normalize_language(request.source_language)
            prompt = (
                f"Translate the following text from {source_lang} to {target_lang}. "
                f"Provide only the translation without any explanations or additional text:\n\n"
                f"{request.text}"
            )
        else:
            prompt = (
                f"Translate the following text to {target_lang}. "
                f"Provide only the translation without any explanations or additional text:\n\n"
                f"{request.text}"
            )
        
        return prompt
    
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Google Gemini."""
        start_time = time.time()
        
        try:
            # Get client
            client = self._get_client()
            
            # Create prompt
            prompt = self._create_translation_prompt(request)
            
            # Generate response
            response = client.generate_content(prompt)
            
            # Extract translation
            if not response.text:
                raise ProviderError("Empty response from Gemini", self.provider_name)
            
            translated_text = response.text.strip()
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract usage information if available
            usage_metadata = {}
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                usage_metadata = {
                    'prompt_token_count': getattr(response.usage_metadata, 'prompt_token_count', None),
                    'candidates_token_count': getattr(response.usage_metadata, 'candidates_token_count', None),
                    'total_token_count': getattr(response.usage_metadata, 'total_token_count', None),
                }
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                model=self.model,
                **usage_metadata
            )
            
        except Exception as e:
            if "API_KEY_INVALID" in str(e) or "authentication" in str(e).lower():
                raise APIKeyError(self.provider_name)
            else:
                raise ProviderError(f"Gemini request failed: {str(e)}", self.provider_name)
    
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Google Gemini asynchronously."""
        start_time = time.time()
        
        try:
            # Get client
            client = self._get_client()
            
            # Create prompt
            prompt = self._create_translation_prompt(request)
            
            # Generate response asynchronously
            # Note: google-genai doesn't have native async support yet,
            # so we run in a thread pool
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                client.generate_content, 
                prompt
            )
            
            # Extract translation
            if not response.text:
                raise ProviderError("Empty response from Gemini", self.provider_name)
            
            translated_text = response.text.strip()
            
            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Extract usage information if available
            usage_metadata = {}
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                usage_metadata = {
                    'prompt_token_count': getattr(response.usage_metadata, 'prompt_token_count', None),
                    'candidates_token_count': getattr(response.usage_metadata, 'candidates_token_count', None),
                    'total_token_count': getattr(response.usage_metadata, 'total_token_count', None),
                }
            
            return self._create_response(
                translated_text=translated_text,
                request=request,
                response_time_ms=response_time_ms,
                model=self.model,
                **usage_metadata
            )
            
        except Exception as e:
            if "API_KEY_INVALID" in str(e) or "authentication" in str(e).lower():
                raise APIKeyError(self.provider_name)
            else:
                raise ProviderError(f"Gemini async request failed: {str(e)}", self.provider_name)
