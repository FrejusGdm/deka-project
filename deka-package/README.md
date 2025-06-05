# Deka 🌍

A unified Python SDK for multiple translation providers with advanced model selection and African language support. Compare translations from Google Translate, DeepL, OpenAI, Anthropic, Gemini, and GhanaNLP with a single, simple interface.

## ✨ Features

- **🎯 Model Selection**: Choose specific AI models (gpt-4, claude-3-5-sonnet, gemini-2.0-flash)
- **🌍 African Languages**: Dedicated support for 11 African languages via GhanaNLP
- **🔄 Provider Comparison**: Compare translations side-by-side across providers and models
- **🚀 6 Providers**: Google Translate, DeepL, OpenAI, Anthropic, Gemini, GhanaNLP
- **📝 Language Normalization**: Use natural language names ("french") or ISO codes ("fr")
- **⚡ Async Support**: Full async/await support for better performance
- **🔒 Type Safety**: Complete type hints for better development experience
- **🔑 Bring Your Own Keys**: Use your own API keys, no vendor lock-in
- **⚠️ Permissive Validation**: Try new models without SDK updates

## 🚀 Quick Start

### Installation

```bash
pip install deka
```

### Basic Usage

```python
import deka

# Configure with your API keys
deka.configure({
    'google_api_key': 'your-google-key',
    'deepl_api_key': 'your-deepl-key',
    'openai_api_key': 'your-openai-key',
    'anthropic_api_key': 'your-anthropic-key',
    'gemini_api_key': 'your-gemini-key',
    'ghananlp_api_key': 'your-ghananlp-key',
})

# Simple translation
result = deka.translate("Hello world", "french", provider="google")
print(result.text)  # "Bonjour le monde"

# Model selection - choose specific AI models
result = deka.translate("Hello", "spanish", provider="openai/gpt-4")
print(result.text)  # "Hola"

# African languages with GhanaNLP
result = deka.translate("Thank you", "twi", provider="ghananlp")
print(result.text)  # "Meda wo ase"

# Compare multiple providers and models
comparison = deka.compare("Hello world", "spanish", providers=[
    "google",
    "openai/gpt-4",
    "anthropic/claude-3-5-sonnet"
])
for result in comparison.results:
    print(f"{result.provider}: {result.text}")
```

### Async Usage

```python
import asyncio
import deka

async def main():
    # Configure first
    deka.configure({'openai_api_key': 'your-key'})
    
    # Async translation
    result = await deka.translate_async("Hello", "japanese", provider="openai")
    print(result.text)
    
    # Async comparison (runs providers concurrently)
    comparison = await deka.compare_async("Hello", "korean", providers=["google", "openai"])
    print(f"Fastest: {comparison.fastest_provider}")

asyncio.run(main())
```

## 🔧 Supported Providers

| Provider | Type | Languages | Models | Features |
|----------|------|-----------|--------|----------|
| **Google Translate** | API | 100+ | - | Fast, reliable, auto-detection |
| **DeepL** | API | 30+ | - | High quality, European languages |
| **OpenAI** | LLM | Any | 5 models | Context-aware, creative translations |
| **Anthropic Claude** | LLM | Any | 5 models | Nuanced, culturally-aware translations |
| **Google Gemini** | LLM | Any | 5 models | Latest Google AI, multimodal |
| **GhanaNLP** | API | 11 African | - | Specialized African languages |

### 🤖 Available Models

#### OpenAI Models:
- `gpt-4` - Most capable, slower
- `gpt-4-turbo` - Faster than gpt-4
- `gpt-4o` - Optimized for speed and cost
- `gpt-3.5-turbo` - Fast, cheap (default)
- `gpt-4o-mini` - Smallest, fastest

#### Anthropic Models:
- `claude-3-5-sonnet-20241022` - Latest, most capable (default)
- `claude-3-sonnet-20240229` - Balanced performance
- `claude-3-haiku-20240307` - Fastest, cheapest
- `claude-3-opus-20240229` - Most capable (older)

#### Gemini Models:
- `gemini-2.0-flash-001` - Latest, fastest (default)
- `gemini-1.5-pro` - High capability, longer context
- `gemini-1.5-flash` - Fast, efficient

#### GhanaNLP Languages:
- **Ghanaian**: Twi, Ga, Ewe, Fante, Dagbani, Gurene
- **Other African**: Yoruba, Kikuyu, Luo, Kimeru

## 📖 Documentation

### Configuration

```python
import deka

# Configure all providers at once
deka.configure({
    'google_api_key': 'your-google-translate-api-key',
    'deepl_api_key': 'your-deepl-api-key',
    'openai_api_key': 'your-openai-api-key',
    'anthropic_api_key': 'your-anthropic-api-key',
})

# Or configure individual providers
deka.configure({'google_api_key': 'your-key'})
```

### Translation

```python
# Basic translation
result = deka.translate(
    text="Hello world",
    target_language="french",
    provider="google"
)

# Model selection - choose specific AI models
result = deka.translate(
    text="Hello world",
    target_language="french",
    provider="openai/gpt-4"  # Use GPT-4 specifically
)

result = deka.translate(
    text="Hello world",
    target_language="french",
    provider="anthropic/claude-3-5-sonnet-20241022"  # Use latest Claude
)

# African languages with GhanaNLP
result = deka.translate(
    text="Good morning",
    target_language="twi",  # Ghanaian language
    provider="ghananlp"
)

# With source language specified
result = deka.translate(
    text="Bonjour",
    target_language="english",
    source_language="french",
    provider="deepl"
)

# Auto-select provider (uses first configured)
result = deka.translate("Hello", "spanish")
```

### Comparison

```python
# Compare specific providers
comparison = deka.compare(
    text="Hello world",
    target_language="german",
    providers=["google", "deepl", "openai"]
)

# Access results
for result in comparison.results:
    print(f"{result.provider}: {result.text} ({result.response_time_ms}ms)")

# Get fastest/best result
fastest = comparison.fastest_provider
best_confidence = comparison.highest_confidence
google_result = comparison.get_result_by_provider("google")
```

### Language Support

```python
# List all supported languages
languages = deka.list_languages()
print(languages[:5])  # ['english', 'french', 'spanish', 'german', 'italian']

# Normalize language names
normalized = deka.normalize_language("français")  # returns "french"
normalized = deka.normalize_language("zh")        # returns "chinese"

# List configured providers
providers = deka.list_providers()
```

## 🔑 API Keys Setup

### Google Translate
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Cloud Translation API
3. Create credentials and get your API key

### DeepL
1. Sign up at [DeepL API](https://www.deepl.com/pro-api)
2. Get your authentication key
3. Note: Free tier keys end with `:fx`

### OpenAI
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Go to API Keys section
3. Create a new API key

### Anthropic
1. Sign up at [Anthropic](https://console.anthropic.com/)
2. Go to API Keys section
3. Create a new API key

### Google Gemini
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key
3. Note: Different from Google Translate API

### GhanaNLP
1. Visit [GhanaNLP Translation API](https://translation.ghananlp.org/)
2. Sign up for an API key
3. Specialized for African languages

## 🎯 Use Cases

- **A/B Testing Translations**: Compare quality across providers
- **Fallback Systems**: Try multiple providers for reliability
- **Cost Optimization**: Compare pricing and choose best value
- **Quality Assessment**: Find the best translation for your content
- **Multi-Provider Apps**: Let users choose their preferred provider

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/FrejusGdm/deka-project)
- [Documentation](https://deka.readthedocs.io)
- [PyPI Package](https://pypi.org/project/deka/)
- [Issue Tracker](https://github.com/josuegodeme/deka/issues)

---

Made with ❤️ by [Josue Godeme](https://github.com/FrejusGdm)
