# Provider System Deep Dive

## 🏗️ Provider Architecture Overview

The provider system is the **heart of Deka**. It's what makes adding new translation services easy and keeps the interface consistent.

```
┌─────────────────────────────────────┐
│            User Code                │
│    deka.translate("Hi", "french")   │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│         Provider Factory            │
│   create_provider_instance("google")│
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│        BaseProvider                 │
│    Abstract interface for all       │
└─────────────┬───────────────────────┘
              │
    ┌─────────┼─────────┬─────────┐
    │         │         │         │
┌───▼───┐ ┌──▼───┐ ┌───▼───┐ ┌───▼────┐
│Google │ │DeepL │ │OpenAI │ │Claude  │
│Provider│ │Provider│ │Provider│ │Provider│
└───────┘ └──────┘ └───────┘ └────────┘
```

## 📄 src/deka/providers/base.py - The Foundation

### Abstract Base Class Pattern

```python
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass
```

**Why ABC (Abstract Base Class)?**
- **Enforces contract**: All providers MUST implement `translate()`
- **Prevents instantiation**: Can't create `BaseProvider()` directly
- **Documentation**: Shows what methods providers need
- **Type safety**: IDE knows all providers have same interface

### Common Functionality

#### 1. **HTTP Error Handling**
```python
def _handle_http_error(self, response: requests.Response) -> None:
    if response.status_code == 401:
        raise APIKeyError(self.provider_name)
    elif response.status_code == 429:
        raise RateLimitError(self.provider_name)
```

**Why in base class?**
- **DRY principle**: Don't repeat error handling in every provider
- **Consistency**: All providers handle errors the same way
- **Maintainability**: Fix error handling in one place

#### 2. **Response Creation**
```python
def _create_response(self, translated_text: str, request: TranslationRequest, **metadata):
    return TranslationResponse(
        text=translated_text,
        source_language=request.source_language or 'auto',
        target_language=request.target_language,
        provider=self.provider_name,
        metadata=metadata
    )
```

**Benefits:**
- **Standardized responses**: All providers return same format
- **Metadata handling**: Easy to add provider-specific data
- **Less boilerplate**: Providers don't repeat response creation

#### 3. **Session Management**
```python
async def _get_session(self) -> aiohttp.ClientSession:
    if self._session is None or self._session.closed:
        self._session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30))
    return self._session
```

**Why session reuse?**
- **Performance**: Reusing connections is faster
- **Resource efficiency**: Don't create new connections every time
- **Proper cleanup**: Sessions are closed when provider is destroyed

## 📄 Provider Implementations

### Google Translate Provider

#### API Integration
```python
url = "https://translation.googleapis.com/language/translate/v2"
params = {
    'key': api_key,
    'q': request.text,
    'target': target_lang,
}
```

**Google Translate specifics:**
- **REST API**: Simple HTTP POST with parameters
- **API Key auth**: Key in URL parameters
- **Language codes**: Uses mostly ISO 639-1 codes
- **Response format**: JSON with nested structure

#### Error Handling
```python
if 'data' not in data or 'translations' not in data['data']:
    raise ProviderError("Invalid response format from Google Translate")
```

**Provider-specific validation:**
- **Response structure**: Google has specific JSON format
- **Error messages**: Convert Google errors to Deka errors
- **Graceful degradation**: Handle partial failures

### DeepL Provider

#### Free vs Pro API Detection
```python
is_free = api_key.endswith(':fx')
base_url = "https://api-free.deepl.com" if is_free else "https://api.deepl.com"
```

**Why this matters:**
- **Different endpoints**: Free and Pro use different URLs
- **Automatic detection**: Users don't need to specify
- **Transparent**: Same interface regardless of tier

#### Authentication
```python
headers = {
    'Authorization': f'DeepL-Auth-Key {api_key}',
    'Content-Type': 'application/x-www-form-urlencoded',
}
```

**DeepL specifics:**
- **Custom auth header**: Not standard Bearer token
- **Form encoding**: Uses form data, not JSON
- **High quality**: Known for better translations than Google

### OpenAI Provider (LLM-based)

#### Prompt Engineering
```python
def _create_translation_prompt(self, request: TranslationRequest) -> str:
    target_lang = normalize_language(request.target_language)
    return f"Translate the following text to {target_lang}. Return only the translation:\n\n{request.text}"
```

**LLM considerations:**
- **Clear instructions**: Tell model exactly what to do
- **Output format**: "Return only the translation" prevents explanations
- **Context preservation**: LLMs understand context better than traditional APIs

#### Model Configuration
```python
data = {
    'model': 'gpt-3.5-turbo',
    'temperature': 0.1,  # Low temperature for consistent translations
    'max_tokens': len(request.text) * 3,  # Rough estimate
}
```

**Parameter choices:**
- **Low temperature**: More deterministic, less creative
- **Token estimation**: Translations usually 1-3x original length
- **Model selection**: gpt-3.5-turbo is fast and cheap

### Anthropic Provider

#### Claude-specific Implementation
```python
headers = {
    'x-api-key': api_key,  # Different from OpenAI
    'anthropic-version': '2023-06-01',  # Required version header
}
```

**Anthropic differences:**
- **Custom headers**: Different auth and version headers
- **System prompts**: Separate system message field
- **Response format**: Different JSON structure than OpenAI

## 📄 src/deka/providers/__init__.py - Provider Registry

### Factory Pattern
```python
PROVIDERS: Dict[str, Type[BaseProvider]] = {
    'google': GoogleTranslateProvider,
    'deepl': DeepLProvider,
    'openai': OpenAIProvider,
    'anthropic': AnthropicProvider,
}

def get_provider(provider_name: str) -> Type[BaseProvider]:
    return PROVIDERS[provider_name]
```

**Benefits:**
- **Centralized registry**: All providers in one place
- **Dynamic loading**: Can add providers at runtime
- **Type safety**: Returns provider class, not instance

### Provider Aliases
```python
PROVIDER_ALIASES = {
    'google-translate': 'google',
    'gpt': 'openai',
    'chatgpt': 'openai',
    'claude': 'anthropic',
}
```

**User experience:**
- **Flexibility**: Users can use familiar names
- **Backwards compatibility**: Can change internal names
- **Discoverability**: Multiple ways to find same provider

## 🔧 Language Code Mapping

### The Problem
Different providers use different language codes:
- **Google**: `zh` for Chinese
- **DeepL**: `zh` for Chinese
- **Azure**: `zh-Hans` for Simplified Chinese
- **OpenAI**: "Chinese" in prompts

### The Solution
```python
def get_provider_code(language: str, provider: str) -> str:
    normalized = normalize_language(language)  # "chinese"
    
    if provider in PROVIDER_MAPPINGS:
        provider_map = PROVIDER_MAPPINGS[provider]
        if normalized in provider_map:
            return provider_map[normalized]
    
    # Fall back to ISO code
    return NAME_TO_ISO[normalized]  # "zh"
```

**Three-step process:**
1. **Normalize**: "Chinese" → "chinese"
2. **Provider mapping**: Check if provider has special code
3. **ISO fallback**: Use standard ISO code

## 🎯 Why This Provider System is Powerful

### 1. **Easy to Extend**
Adding a new provider is just:
```python
class NewProvider(BaseProvider):
    def translate(self, request):
        # Implementation here
        pass
```

### 2. **Consistent Interface**
All providers work the same way:
```python
provider = create_provider_instance("any-provider")
result = provider.translate(request)
```

### 3. **Error Handling**
Base class handles common errors, providers handle specific ones:
```python
# Base class handles 401, 429, 403
# Provider handles API-specific errors
```

### 4. **Performance**
- **Session reuse**: Faster HTTP requests
- **Async support**: Concurrent translations
- **Proper cleanup**: No resource leaks

### 5. **Testability**
- **Mock providers**: Easy to create fake providers for testing
- **Isolated testing**: Test each provider independently
- **Error simulation**: Test error handling paths

This provider system is **extensible**, **maintainable**, and **performant** - the foundation for a scalable translation SDK!
