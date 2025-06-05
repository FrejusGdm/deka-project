# Deka 🌍

A unified Python SDK for multiple translation providers. Compare translations from Google Translate, DeepL, OpenAI, and more with a single, simple interface.

## ✨ Features

- **Unified Interface**: One API for multiple translation providers
- **Provider Comparison**: Compare translations side-by-side
- **Language Normalization**: Use natural language names ("french") or ISO codes ("fr")
- **Async Support**: Full async/await support for better performance
- **Type Safety**: Complete type hints for better development experience
- **Bring Your Own Keys**: Use your own API keys, no vendor lock-in

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
})

# Simple translation
result = deka.translate("Hello world", "french", provider="google")
print(result.text)  # "Bonjour le monde"

# Compare multiple providers
comparison = deka.compare("Hello world", "spanish", providers=["google", "deepl"])
for result in comparison.results:
    print(f"{result.provider}: {result.text}")
# google: Hola mundo
# deepl: Hola mundo
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

| Provider | Type | Languages | Features |
|----------|------|-----------|----------|
| **Google Translate** | API | 100+ | Fast, reliable, auto-detection |
| **DeepL** | API | 30+ | High quality, European languages |
| **OpenAI** | LLM | Any | Context-aware, creative translations |
| **Anthropic Claude** | LLM | Any | Nuanced, culturally-aware translations |

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

- [GitHub Repository](https://github.com/josuegodeme/deka)
- [Documentation](https://deka.readthedocs.io)
- [PyPI Package](https://pypi.org/project/deka/)
- [Issue Tracker](https://github.com/josuegodeme/deka/issues)

---

Made with ❤️ by [Josue Godeme](https://github.com/josuegodeme)
