"""
Data models for Deka translation requests and responses.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class TranslationRequest:
    """Request model for translation operations."""
    text: str
    target_language: str
    source_language: Optional[str] = None
    provider: Optional[str] = None
    
    def __post_init__(self):
        if not self.text.strip():
            raise ValueError("Text cannot be empty")
        if not self.target_language.strip():
            raise ValueError("Target language cannot be empty")


@dataclass
class TranslationResponse:
    """Response model for translation operations."""
    text: str
    source_language: str
    target_language: str
    provider: str
    confidence: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @property
    def characters_used(self) -> int:
        """Number of characters in the original text."""
        return len(self.text)
    
    @property
    def response_time_ms(self) -> Optional[int]:
        """Response time in milliseconds if available in metadata."""
        if self.metadata:
            return self.metadata.get('response_time_ms')
        return None


@dataclass
class ComparisonResult:
    """Result model for comparing multiple providers."""
    request: TranslationRequest
    results: List[TranslationResponse]
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def fastest_provider(self) -> Optional[str]:
        """Provider with the fastest response time."""
        fastest = None
        fastest_time = float('inf')
        
        for result in self.results:
            if result.response_time_ms and result.response_time_ms < fastest_time:
                fastest_time = result.response_time_ms
                fastest = result.provider
        
        return fastest
    
    @property
    def highest_confidence(self) -> Optional[str]:
        """Provider with the highest confidence score."""
        highest = None
        highest_score = 0.0
        
        for result in self.results:
            if result.confidence and result.confidence > highest_score:
                highest_score = result.confidence
                highest = result.provider
        
        return highest
    
    def get_result_by_provider(self, provider: str) -> Optional[TranslationResponse]:
        """Get translation result for a specific provider."""
        for result in self.results:
            if result.provider == provider:
                return result
        return None
