# Design Decisions and Rationale

## 🎯 High-Level Design Philosophy

### 1. **Simplicity Over Flexibility**
**Decision:** Simple, opinionated API over highly configurable one.

```python
# What we chose (simple):
deka.translate("Hello", "french", provider="google")

# What we could have done (complex):
translator = DekaTranslator(
    config=TranslationConfig(
        providers=[
            ProviderConfig(name="google", api_key="...", timeout=30),
            ProviderConfig(name="deepl", api_key="...", timeout=45)
        ],
        language_mapping=LanguageMapping(strategy="iso639"),
        error_handling=ErrorHandling(retry_count=3, backoff="exponential")
    )
)
result = translator.translate(
    TranslationRequest(text="Hello", target="french", provider="google")
)
```

**Why simple wins:**
- **Lower learning curve**: Users productive in minutes
- **Fewer bugs**: Less configuration = fewer ways to break
- **Better adoption**: Developers prefer simple tools
- **Easier maintenance**: Less code to maintain

### 2. **Convention Over Configuration**
**Decision:** Smart defaults instead of requiring configuration.

```python
# Auto-select provider if not specified
result = deka.translate("Hello", "french")  # Uses first configured provider

# Auto-detect source language
result = deka.translate("Bonjour", "english")  # Detects French automatically

# Smart language normalization
result = deka.translate("Hello", "français")  # Handles native names
```

**Benefits:**
- **Immediate productivity**: Works out of the box
- **Reduced cognitive load**: Fewer decisions to make
- **Graceful degradation**: Sensible fallbacks

### 3. **Fail Fast, Fail Clear**
**Decision:** Clear error messages over silent failures.

```python
# Clear, actionable error messages
try:
    deka.translate("Hello", "klingon")
except LanguageNotSupportedError as e:
    print(e)  # "Language 'klingon' not recognized. Did you mean: korean, mongolian?"

# Specific exception types
try:
    deka.translate("Hello", "french", provider="google")
except APIKeyError:
    print("Please configure your Google API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after} seconds")
```

**Why this matters:**
- **Better debugging**: Users know exactly what went wrong
- **Faster development**: Less time spent troubleshooting
- **Better user experience**: Actionable error messages

## 🏗️ Architectural Decisions

### 1. **Abstract Base Class vs Duck Typing**
**Decision:** Used ABC (Abstract Base Class) for providers.

```python
# What we chose:
class BaseProvider(ABC):
    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResponse:
        pass

# Alternative (duck typing):
class GoogleProvider:
    def translate(self, request):  # No enforcement
        pass
```

**Why ABC:**
- **Enforced contract**: All providers must implement required methods
- **IDE support**: Better autocomplete and error detection
- **Documentation**: Clear interface specification
- **Type safety**: mypy can verify implementations

### 2. **Dataclasses vs Dictionaries**
**Decision:** Used dataclasses for structured data.

```python
# What we chose:
@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str
    provider: str

# Alternative:
response = {
    'text': 'Bonjour',
    'source_language': 'english',
    'target_language': 'french',
    'provider': 'google'
}
```

**Why dataclasses:**
- **Type safety**: IDE knows field types
- **Validation**: Can validate data in `__post_init__`
- **Documentation**: Clear structure specification
- **Methods**: Can add computed properties and methods

### 3. **Global Configuration vs Dependency Injection**
**Decision:** Global configuration for simplicity.

```python
# What we chose (global):
deka.configure({'google_api_key': 'key'})
result = deka.translate("Hello", "french")

# Alternative (dependency injection):
config = DekaConfig({'google_api_key': 'key'})
translator = DekaTranslator(config)
result = translator.translate("Hello", "french")
```

**Why global configuration:**
- **Simpler API**: Configure once, use everywhere
- **Better for SDK**: Libraries should be easy to use
- **Familiar pattern**: Most Python libraries use global config
- **Testable**: Can reset config for tests

### 4. **Sync + Async vs Async Only**
**Decision:** Provide both sync and async versions.

```python
# Sync version for simple use cases
result = deka.translate("Hello", "french")

# Async version for performance
result = await deka.translate_async("Hello", "french")
```

**Why both:**
- **Accessibility**: Not everyone knows async
- **Use case fit**: Simple scripts don't need async
- **Performance option**: Async available when needed
- **Gradual adoption**: Users can migrate to async later

## 🔧 Implementation Decisions

### 1. **requests + aiohttp vs httpx**
**Decision:** Used separate libraries for sync/async.

**Why not httpx (unified HTTP library)?**
- **Maturity**: requests is battle-tested
- **Ecosystem**: More examples and documentation
- **Performance**: aiohttp is faster for async
- **Familiarity**: Most developers know requests

### 2. **Language Mapping Strategy**
**Decision:** Three-layer mapping system.

```
User Input → Normalized Name → ISO Code → Provider Code
"français" → "french"       → "fr"     → "fr-FR"
```

**Alternative approaches considered:**
- **Direct mapping**: User input directly to provider codes
- **ISO only**: Force users to use ISO codes
- **Provider-specific**: Each provider handles its own mapping

**Why three-layer:**
- **User-friendly**: Natural language input
- **Standardized**: ISO codes as common format
- **Provider-flexible**: Handle provider quirks
- **Extensible**: Easy to add new languages/providers

### 3. **Error Handling Strategy**
**Decision:** Custom exception hierarchy with context.

```python
class ProviderError(DekaError):
    def __init__(self, message: str, provider: str, status_code: int = None):
        self.provider = provider
        self.status_code = status_code
```

**Why custom exceptions:**
- **Specific handling**: Users can catch specific error types
- **Rich context**: Include provider, status code, etc.
- **Debugging**: Better error messages
- **API design**: Clear contract about what can fail

### 4. **Provider Registration**
**Decision:** Static registry with factory pattern.

```python
PROVIDERS = {
    'google': GoogleTranslateProvider,
    'deepl': DeepLProvider,
}

def create_provider_instance(name: str) -> BaseProvider:
    return PROVIDERS[name]()
```

**Alternative:** Dynamic plugin system with entry points.

**Why static registry:**
- **Simplicity**: Easy to understand and maintain
- **Performance**: No dynamic loading overhead
- **Reliability**: All providers are tested together
- **Control**: We control which providers are included

## 📦 Packaging Decisions

### 1. **pyproject.toml vs setup.py**
**Decision:** Used modern pyproject.toml.

**Why pyproject.toml:**
- **Modern standard**: PEP 518 specification
- **Declarative**: Configuration, not code
- **Tool agnostic**: Works with any build backend
- **Better tooling**: IDE support, validation

### 2. **src/ Layout vs Flat Layout**
**Decision:** Used src/ layout.

```
# What we chose:
src/deka/
    __init__.py
    core.py

# Alternative:
deka/
    __init__.py
    core.py
```

**Why src/ layout:**
- **Import safety**: Prevents accidental imports during development
- **Testing**: Forces proper installation testing
- **Best practice**: Recommended by Python packaging guide
- **Tool support**: Better support in modern tools

### 3. **Minimal Dependencies vs Rich Ecosystem**
**Decision:** Minimal, essential dependencies only.

**Dependencies chosen:**
- **requests**: Essential for HTTP
- **aiohttp**: Essential for async HTTP
- **pydantic**: Could be replaced with dataclasses

**Dependencies avoided:**
- **click**: For CLI (users can add if needed)
- **rich**: For pretty output (not essential)
- **tenacity**: For retries (can implement simply)

**Why minimal:**
- **Faster installation**: Fewer packages to download
- **Fewer conflicts**: Less chance of version conflicts
- **Smaller footprint**: Important for containers/lambdas
- **Easier maintenance**: Fewer dependencies to track

## 🎨 API Design Decisions

### 1. **Function-Based vs Class-Based API**
**Decision:** Function-based public API.

```python
# What we chose:
deka.translate("Hello", "french")
deka.compare("Hello", "french", providers=["google", "deepl"])

# Alternative:
translator = deka.Translator()
translator.translate("Hello", "french")
translator.compare("Hello", "french", providers=["google", "deepl"])
```

**Why function-based:**
- **Simpler**: No object creation needed
- **Stateless**: Each call is independent
- **Familiar**: Matches other Python libraries
- **Flexible**: Easy to add new functions

### 2. **Parameter Order and Naming**
**Decision:** Required parameters first, optional last.

```python
def translate(
    text: str,                    # Required, most important
    target_language: str,         # Required, second most important
    source_language: str = None,  # Optional
    provider: str = None          # Optional
):
```

**Why this order:**
- **Usability**: Most common parameters first
- **Readability**: Natural language order
- **Flexibility**: Optional parameters have defaults

### 3. **Return Types**
**Decision:** Rich objects instead of simple strings.

```python
# What we chose:
result = deka.translate("Hello", "french")
print(result.text)           # "Bonjour"
print(result.provider)       # "google"
print(result.response_time_ms)  # 245

# Alternative:
text = deka.translate("Hello", "french")  # Just returns "Bonjour"
```

**Why rich objects:**
- **More information**: Users get metadata
- **Extensibility**: Can add fields without breaking API
- **Debugging**: Users can see which provider was used
- **Analytics**: Response times, confidence scores, etc.

## 🔮 Future-Proofing Decisions

### 1. **Extensibility Points**
- **Provider system**: Easy to add new providers
- **Language mapping**: Easy to add new languages
- **Configuration**: Easy to add new settings
- **Response format**: Easy to add new metadata

### 2. **Backwards Compatibility**
- **Semantic versioning**: Clear versioning strategy
- **Deprecation warnings**: Gradual API changes
- **Optional parameters**: New features don't break existing code

### 3. **Performance Optimization**
- **Async support**: Ready for high-performance use cases
- **Session reuse**: Efficient HTTP connections
- **Concurrent execution**: Multiple providers simultaneously

These design decisions create a **professional, maintainable, and user-friendly** SDK that will scale with your users' needs!
