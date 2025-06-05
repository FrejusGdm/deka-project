"""
Base provider class for all translation providers.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
import time
import asyncio
import aiohttp
import requests
from ..models import TranslationRequest, TranslationResponse
from ..exceptions import ProviderError, APIKeyError, RateLimitError, QuotaExceededError
from ..config import get_api_key


class BaseProvider(ABC):
    """Abstract base class for all translation providers."""

    # Provider metadata (to be overridden by subclasses)
    display_name: str = "Unknown Provider"
    description: str = "A translation provider"
    provider_type: str = "api"  # 'api' or 'llm'
    default_model: Optional[str] = None  # Default model for this provider
    supported_models: List[str] = []     # List of supported models

    def __init__(self, model: Optional[str] = None):
        self.model = model or self.default_model
        self.api_key: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None

        # Validate model if provider supports models (now permissive)
        if self.supported_models and self.model:
            if self.model not in self.supported_models:
                # Just warn, don't fail - let provider API validate
                import difflib
                suggestions = difflib.get_close_matches(self.model, self.supported_models, n=3, cutoff=0.6)
                if suggestions:
                    print(f"⚠️  Warning: Model '{self.model}' not in known list for {self.provider_name}. Did you mean: {', '.join(suggestions)}? Trying anyway...")
                else:
                    print(f"⚠️  Warning: Model '{self.model}' not in known list for {self.provider_name}. Known models: {', '.join(self.supported_models)}. Trying anyway...")
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Unique identifier for this provider."""
        pass
    
    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text synchronously.
        
        Args:
            request: Translation request
            
        Returns:
            Translation response
        """
        pass
    
    @abstractmethod
    async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text asynchronously.
        
        Args:
            request: Translation request
            
        Returns:
            Translation response
        """
        pass
    
    def _get_api_key(self) -> str:
        """Get API key for this provider."""
        if not self.api_key:
            self.api_key = get_api_key(self.provider_name)
        return self.api_key
    
    def _handle_http_error(self, response: requests.Response) -> None:
        """Handle HTTP errors and convert to appropriate exceptions."""
        if response.status_code == 401:
            raise APIKeyError(self.provider_name)
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            retry_after = int(retry_after) if retry_after else None
            raise RateLimitError(self.provider_name, retry_after)
        elif response.status_code == 403:
            raise QuotaExceededError(self.provider_name)
        elif not response.ok:
            raise ProviderError(
                f"HTTP {response.status_code}: {response.text}",
                self.provider_name,
                response.status_code
            )
    
    async def _handle_aiohttp_error(self, response: aiohttp.ClientResponse) -> None:
        """Handle aiohttp errors and convert to appropriate exceptions."""
        if response.status == 401:
            raise APIKeyError(self.provider_name)
        elif response.status == 429:
            retry_after = response.headers.get('Retry-After')
            retry_after = int(retry_after) if retry_after else None
            raise RateLimitError(self.provider_name, retry_after)
        elif response.status == 403:
            raise QuotaExceededError(self.provider_name)
        elif not response.ok:
            text = await response.text()
            raise ProviderError(
                f"HTTP {response.status}: {text}",
                self.provider_name,
                response.status
            )
    
    def _create_response(
        self,
        translated_text: str,
        request: TranslationRequest,
        confidence: Optional[float] = None,
        response_time_ms: Optional[int] = None,
        **metadata
    ) -> TranslationResponse:
        """Create a standardized translation response."""
        response_metadata = {
            'response_time_ms': response_time_ms,
            **metadata
        }
        
        return TranslationResponse(
            text=translated_text,
            source_language=request.source_language or 'auto',
            target_language=request.target_language,
            provider=self.provider_name,
            confidence=confidence,
            metadata=response_metadata
        )
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    def __del__(self):
        """Cleanup when provider is destroyed."""
        if self._session and not self._session.closed:
            # Try to close the session, but don't fail if event loop is closed
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.close())
                else:
                    loop.run_until_complete(self.close())
            except:
                pass
