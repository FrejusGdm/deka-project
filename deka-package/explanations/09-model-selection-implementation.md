# Model Selection & Gemini Provider Implementation

## 🎯 **What We're Adding:**

### **1. Model Selection Syntax**
```python
# Current (still works):
deka.translate("Hello", "french", provider="openai")

# New model selection:
deka.translate("Hello", "french", provider="openai/gpt-4")
deka.translate("Hello", "french", provider="anthropic/claude-3-5-sonnet")
deka.translate("Hello", "french", provider="google/gemini-2.0-flash")
```

### **2. Gemini Provider**
- **New provider**: `google-gemini` or `google/gemini-*`
- **Multiple models**: gemini-2.0-flash, gemini-1.5-pro, gemini-1.5-flash
- **Official SDK**: Uses Google's `google-genai` library
- **API Key**: Gemini Developer API key

## 🏗️ **Architecture Changes:**

### **Provider Name Parsing**
```python
# Before:
provider_name = "openai"  # Simple name

# After:
provider_name = "openai/gpt-4"  # Provider/model format
provider, model = parse_provider_name(provider_name)
# provider = "openai", model = "gpt-4"
```

### **Provider Registry Enhancement**
```python
# Before:
PROVIDERS = {
    'openai': OpenAIProvider,
    'anthropic': AnthropicProvider,
}

# After:
PROVIDERS = {
    'openai': OpenAIProvider,
    'anthropic': AnthropicProvider,
    'google-gemini': GeminiProvider,  # New!
}

# Model mappings per provider:
PROVIDER_MODELS = {
    'openai': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-4o'],
    'anthropic': ['claude-3-5-sonnet', 'claude-3-sonnet', 'claude-3-haiku'],
    'google-gemini': ['gemini-2.0-flash-001', 'gemini-1.5-pro', 'gemini-1.5-flash'],
}
```

## 📚 **Provider Documentation Research:**

### **OpenAI Models (Current)**
- **gpt-4**: Most capable, slower, more expensive
- **gpt-4-turbo**: Faster than gpt-4, good balance
- **gpt-4o**: Optimized for speed and cost
- **gpt-3.5-turbo**: Fast, cheap, good for simple tasks

### **Anthropic Models (Current)**
- **claude-3-5-sonnet**: Latest, most capable
- **claude-3-sonnet**: Balanced performance
- **claude-3-haiku**: Fastest, cheapest
- **claude-3-opus**: Most capable (older generation)

### **Gemini Models (New)**
- **gemini-2.0-flash-001**: Latest, fastest, multimodal
- **gemini-1.5-pro**: High capability, longer context
- **gemini-1.5-flash**: Fast, efficient

## 🔧 **Implementation Steps:**

### **Step 1: Provider Name Parsing**
```python
def parse_provider_name(provider_name: str) -> tuple[str, str]:
    """Parse provider/model format."""
    if '/' in provider_name:
        provider, model = provider_name.split('/', 1)
        return provider, model
    else:
        # Backward compatibility - use default model
        return provider_name, None
```

### **Step 2: Enhanced Provider Base Class**
```python
class BaseProvider(ABC):
    default_model: str = None  # Each provider sets default
    supported_models: List[str] = []  # List of supported models
    
    def __init__(self, model: str = None):
        self.model = model or self.default_model
        if self.model not in self.supported_models:
            raise ValueError(f"Model {self.model} not supported")
```

### **Step 3: Gemini Provider Implementation**
```python
class GeminiProvider(BaseProvider):
    display_name = "Google Gemini"
    description = "Google's Gemini models for advanced AI capabilities"
    provider_type = "llm"
    default_model = "gemini-2.0-flash-001"
    supported_models = [
        "gemini-2.0-flash-001",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
    
    def __init__(self, model: str = None):
        super().__init__(model)
        self.client = None  # Will be created when needed
```

### **Step 4: Model Validation**
```python
def validate_provider_model(provider: str, model: str) -> bool:
    """Validate that provider supports the model."""
    if provider not in PROVIDER_MODELS:
        return False
    return model in PROVIDER_MODELS[provider]
```

## 🎯 **Backward Compatibility:**

### **All existing code continues to work:**
```python
# These still work exactly the same:
deka.translate("Hello", "french", provider="openai")      # Uses gpt-3.5-turbo
deka.translate("Hello", "french", provider="anthropic")   # Uses claude-3-sonnet
```

### **New capabilities:**
```python
# Now you can specify exact models:
deka.translate("Hello", "french", provider="openai/gpt-4")
deka.translate("Hello", "french", provider="anthropic/claude-3-5-sonnet")
deka.translate("Hello", "french", provider="google-gemini/gemini-2.0-flash")
```

## 🔍 **Provider Aliases:**
```python
PROVIDER_ALIASES = {
    # Existing:
    'google-translate': 'google',
    'gpt': 'openai',
    'claude': 'anthropic',
    
    # New:
    'gemini': 'google-gemini',
    'google-gemini': 'google-gemini',
    'gpt-4': 'openai/gpt-4',
    'claude-3-5': 'anthropic/claude-3-5-sonnet',
}
```

## 📦 **Dependencies:**

### **New Dependency: google-genai**
```toml
dependencies = [
    "requests>=2.25.0",
    "aiohttp>=3.8.0", 
    "pydantic>=1.8.0",
    "python-dotenv>=0.19.0",
    "google-genai>=0.8.0",  # New for Gemini
]
```

## 🧪 **Testing Strategy:**

### **Test Cases:**
1. **Backward compatibility**: All existing tests still pass
2. **Model selection**: New provider/model syntax works
3. **Gemini integration**: Real API calls with Gemini
4. **Error handling**: Invalid models are rejected
5. **Comparison**: Compare across different models

### **Example Tests:**
```python
# Test model selection
result = deka.translate("Hello", "french", provider="openai/gpt-4")
assert result.metadata['model'] == 'gpt-4'

# Test Gemini
result = deka.translate("Hello", "french", provider="google-gemini")
assert result.provider == 'google-gemini'

# Test comparison with models
comparison = deka.compare("Hello", "french", providers=[
    "openai/gpt-4",
    "anthropic/claude-3-5-sonnet", 
    "google-gemini/gemini-2.0-flash"
])
```

## 🎉 **Benefits:**

1. **More Control**: Users can choose exact models
2. **Performance Tuning**: Pick fast vs accurate models
3. **Cost Optimization**: Choose cheaper models when appropriate
4. **Latest Models**: Easy to add new models as they're released
5. **Comparison**: Compare different model generations

This implementation maintains full backward compatibility while adding powerful new capabilities!

## 🚨 **Current Limitations & Future Improvements:**

### **Model Validation Issue:**
**Problem**: We currently use hardcoded model lists that become outdated when providers release new models.

**Current Behavior**:
```python
# This fails if OpenAI releases a new model:
deka.translate("Hello", "french", provider="openai/gpt-5")  # ❌ Error: Model not supported
```

**Better Approach** (Future):
```python
# Should work - let provider API validate:
deka.translate("Hello", "french", provider="openai/gpt-5")  # ✅ Try with API
```

### **Language Coverage Issue:**
**Problem**: Manual language list missing many African and indigenous languages.

**Current Coverage**: ~70 languages (mostly European/Asian)
**Missing**: Many African languages, regional variants, indigenous languages

**Better Approach** (Future):
- Use official ISO 639-1/639-3 data (7,000+ languages)
- Download from Library of Congress
- Include comprehensive African language support

## 🔧 **Recommended Improvements:**

1. **Permissive Model Validation**: Remove strict model checking, let APIs validate
2. **Official Language Data**: Use ISO 639 standard data files
3. **Dynamic Provider Discovery**: Auto-detect what models/languages providers support
4. **Warning System**: Warn about unknown models but still try them
