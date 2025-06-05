# Core Architecture Deep Dive

## 🏗️ Overall Architecture Pattern

Deka uses a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────┐
│           Public API Layer          │  ← What users see
│     translate(), compare()          │
├─────────────────────────────────────┤
│        Language Mapping Layer       │  ← Normalize languages
│    "french" → "fr" → "fr-FR"       │
├─────────────────────────────────────┤
│         Provider Layer              │  ← Abstract providers
│   Google, DeepL, OpenAI, Claude     │
├─────────────────────────────────────┤
│         HTTP/API Layer              │  ← Actual API calls
│    requests, aiohttp, error handling│
└─────────────────────────────────────┘
```

## 📄 src/deka/__init__.py - Public API Definition

This file defines **what users can import**. It's the contract between your package and the world.

### Key Concept: `__all__`
```python
__all__ = [
    "translate",
    "compare", 
    "configure",
    # ... etc
]
```
- **Controls imports**: Only these functions are available
- **Documentation**: Shows what's public vs internal
- **IDE support**: Better autocomplete

### Import Strategy
```python
from .config import configure, get_config
from .core import translate, compare
```
- **Relative imports**: `.config` means "from this package"
- **Selective imports**: Only import what we need
- **Flat namespace**: Users do `deka.translate()`, not `deka.core.translate()`

## 📄 src/deka/models.py - Data Structures

### Why Dataclasses?
```python
@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
```

**Benefits over dictionaries:**
- **Type safety**: IDE knows `request.text` is a string
- **Validation**: `__post_init__` can validate data
- **Auto-generated methods**: `__repr__`, `__eq__`, etc.
- **Documentation**: Clear what fields exist

### Design Patterns Used

#### 1. **Value Objects**
```python
@dataclass
class TranslationResponse:
    text: str
    source_language: str
    # ... immutable data
```
- **Immutable**: Once created, doesn't change
- **Self-contained**: Has all data it needs
- **Serializable**: Can be converted to JSON

#### 2. **Computed Properties**
```python
@property
def characters_used(self) -> int:
    return len(self.text)
```
- **Derived data**: Calculated from other fields
- **Consistent interface**: Looks like a field, but computed
- **No storage**: Doesn't take extra memory

#### 3. **Aggregate Root**
```python
@dataclass
class ComparisonResult:
    request: TranslationRequest
    results: List[TranslationResponse]
    
    def get_result_by_provider(self, provider: str):
        # Business logic here
```
- **Contains related objects**: Request + multiple responses
- **Business methods**: Logic for working with the data
- **Single entry point**: One object to rule them all

## 📄 src/deka/exceptions.py - Error Handling Strategy

### Exception Hierarchy
```
DekaError (base)
├── ConfigurationError
│   └── APIKeyError
├── ProviderError
│   ├── RateLimitError
│   └── QuotaExceededError
└── LanguageNotSupportedError
```

### Why Custom Exceptions?

#### 1. **Specific Error Handling**
```python
try:
    result = deka.translate("Hello", "french")
except APIKeyError:
    print("Please configure your API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after} seconds")
```

#### 2. **Context Information**
```python
class ProviderError(DekaError):
    def __init__(self, message: str, provider: str, status_code: int = None):
        self.provider = provider
        self.status_code = status_code
```
- **Rich context**: Not just "error occurred"
- **Actionable**: Users know which provider failed
- **Debugging**: Status codes help diagnose issues

#### 3. **Graceful Degradation**
```python
# In compare() function
for provider in providers:
    try:
        result = provider.translate(request)
        results.append(result)
    except ProviderError:
        # Skip failed provider, continue with others
        continue
```

## 📄 src/deka/config.py - Configuration Management

### Global State Pattern
```python
_config: Dict[str, Any] = {}

def configure(config: Dict[str, Any]) -> None:
    global _config
    _config.update(config)
```

**Why global state here?**
- **Convenience**: Users configure once, use everywhere
- **Simplicity**: No need to pass config around
- **Thread-safe**: Python's GIL protects dictionary updates
- **Testable**: `reset_config()` for clean tests

### API Key Management
```python
def get_api_key(provider: str) -> str:
    key_name = f"{provider}_api_key"
    if key_name not in _config:
        raise ConfigurationError(f"API key for '{provider}' not configured")
```

**Security considerations:**
- **No storage**: Keys only in memory
- **No logging**: Never log API keys
- **Validation**: Check keys exist before use

## 📄 src/deka/core.py - Main Business Logic

### Function Design Philosophy

#### 1. **Simple Interface, Complex Implementation**
```python
def translate(text: str, target_language: str, provider: str = None):
    # Simple for users, but handles:
    # - Language normalization
    # - Provider selection
    # - Error handling
    # - Response formatting
```

#### 2. **Sync and Async Versions**
```python
def translate(...) -> TranslationResponse:
    # Synchronous version

async def translate_async(...) -> TranslationResponse:
    # Asynchronous version
```
- **Same interface**: Only difference is `async`/`await`
- **Performance choice**: Users pick what they need
- **Implementation sharing**: Both use same providers

#### 3. **Smart Defaults**
```python
if not provider:
    configured = list_configured_providers()
    provider = configured[0]  # Use first configured
```
- **Convenience**: Don't force users to specify everything
- **Fail fast**: Error if no providers configured
- **Predictable**: Always uses same default logic

### Comparison Logic
```python
def compare(text, target_language, providers=None):
    results = []
    errors = []
    
    for provider in providers:
        try:
            result = translate_with_provider(provider)
            results.append(result)
        except Exception as e:
            errors.append(f"{provider}: {e}")
    
    if not results:
        raise DekaError(f"All providers failed: {errors}")
```

**Error handling strategy:**
- **Partial success**: If some providers work, return those
- **Complete failure**: Only fail if ALL providers fail
- **Error context**: Tell user which providers failed and why

### Async Implementation
```python
async def compare_async(...):
    tasks = [
        translate_with_provider(provider) 
        for provider in providers
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
```

**Concurrency benefits:**
- **Speed**: All providers called simultaneously
- **Efficiency**: Don't wait for slow providers
- **Resource management**: Proper cleanup with `finally`

## 🎯 Why This Architecture Works

### 1. **Separation of Concerns**
- **Models**: Data structures only
- **Config**: Configuration only  
- **Core**: Business logic only
- **Providers**: API integration only

### 2. **Dependency Inversion**
- **Core depends on abstractions**: Uses `BaseProvider` interface
- **Providers implement abstractions**: Each provider implements `BaseProvider`
- **Easy to extend**: Add new providers without changing core

### 3. **Single Responsibility**
- **Each file has one job**: Models define data, core has logic, etc.
- **Each function has one job**: `translate()` translates, `compare()` compares
- **Easy to test**: Small, focused functions

### 4. **Open/Closed Principle**
- **Open for extension**: Easy to add new providers
- **Closed for modification**: Don't need to change existing code

This architecture is **scalable**, **maintainable**, and **testable** - exactly what you want in a professional package!
