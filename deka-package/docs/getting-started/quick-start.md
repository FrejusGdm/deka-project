# Quick Start Guide

Get up and running with Deka in minutes!

## Installation

```bash
pip install deka
```

## Basic Setup

### 1. Get API Keys

You'll need API keys from the providers you want to use:

- **OpenAI**: [Get API key](https://platform.openai.com/api-keys)
- **Anthropic**: [Get API key](https://console.anthropic.com/)
- **Google Translate**: [Get API key](https://console.cloud.google.com/)
- **DeepL**: [Get API key](https://www.deepl.com/pro-api)
- **Gemini**: [Get API key](https://aistudio.google.com/)
- **GhanaNLP**: [Get API key](https://translation.ghananlp.org/)

### 2. Configure Deka

```python
import deka

# Configure with your API keys
deka.configure({
    'openai_api_key': 'your-openai-key',
    'anthropic_api_key': 'your-anthropic-key',
    'google_api_key': 'your-google-key',
    'deepl_api_key': 'your-deepl-key',
    'gemini_api_key': 'your-gemini-key',
    'ghananlp_api_key': 'your-ghananlp-key',
})
```

!!! tip "Start Small"
    You don't need all API keys to get started. Configure just one provider first!

## Basic Translation

### Simple Translation
```python
# Basic translation
result = deka.translate("Hello world", "french")
print(result.text)  # "Bonjour le monde"
print(result.provider)  # "google" (or your first configured provider)
```

### Choose a Provider
```python
# Use a specific provider
result = deka.translate("Hello world", "spanish", provider="deepl")
print(result.text)  # "Hola mundo"
```

### Model Selection (AI Providers)
```python
# Choose specific AI models
result = deka.translate("Hello", "french", provider="openai/gpt-4")
print(result.text)  # "Bonjour"
print(result.metadata['model'])  # "gpt-4"

# Use Claude 3.5 Sonnet
result = deka.translate("Hello", "german", provider="anthropic/claude-3-5-sonnet")
print(result.text)  # "Hallo"
```

## African Languages

### GhanaNLP Provider
```python
# Translate to Twi (Ghana)
result = deka.translate("Thank you", "twi", provider="ghananlp")
print(result.text)  # "Meda wo ase"

# Translate to Yoruba (Nigeria)
result = deka.translate("Good morning", "yoruba", provider="ghananlp")
print(result.text)  # "Ẹ káàárọ̀"

# Translate to Ga (Ghana)
result = deka.translate("How are you?", "ga", provider="ghananlp")
print(result.text)  # "Aleke nèwɔe?"
```

### Supported African Languages
- **Twi** (Ghana)
- **Ga** (Ghana)
- **Ewe** (Ghana/Togo)
- **Fante** (Ghana)
- **Dagbani** (Ghana)
- **Gurene** (Ghana)
- **Yoruba** (Nigeria/Benin)
- **Kikuyu** (Kenya)
- **Luo** (Kenya/Uganda)
- **Kimeru** (Kenya)

## Provider Comparison

### Compare Multiple Providers
```python
# Compare translations across providers
comparison = deka.compare("Hello world", "spanish", providers=[
    "google",
    "deepl", 
    "openai"
])

# See all results
for result in comparison.results:
    print(f"{result.provider}: {result.text} ({result.response_time_ms}ms)")

# Get the fastest result
fastest = comparison.fastest_provider
print(f"Fastest: {fastest}")
```

### Compare AI Models
```python
# Compare different AI models
comparison = deka.compare("Good evening", "italian", providers=[
    "openai/gpt-3.5-turbo",  # Fast, cheap
    "openai/gpt-4",          # High quality, slower
    "anthropic/claude-3-5-sonnet"  # Nuanced, creative
])

for result in comparison.results:
    model = result.metadata.get('model', 'default')
    print(f"{result.provider} ({model}): {result.text}")
```

## Async Usage

### Async Translation
```python
import asyncio

async def main():
    # Configure first
    deka.configure({'openai_api_key': 'your-key'})
    
    # Async translation
    result = await deka.translate_async("Hello", "japanese")
    print(result.text)

# Run async function
asyncio.run(main())
```

### Async Comparison (Concurrent)
```python
async def compare_providers():
    # This runs all providers concurrently for speed
    comparison = await deka.compare_async("Hello", "korean", providers=[
        "google", 
        "openai", 
        "anthropic"
    ])
    
    print(f"Fastest provider: {comparison.fastest_provider}")
    print(f"Total time: {comparison.total_time_ms}ms")

asyncio.run(compare_providers())
```

## Language Support

### Natural Language Names
```python
# Use natural language names
result = deka.translate("Hello", "french")
result = deka.translate("Hello", "spanish") 
result = deka.translate("Hello", "chinese")
result = deka.translate("Hello", "swahili")
```

### ISO Language Codes
```python
# Use ISO codes
result = deka.translate("Hello", "fr")  # French
result = deka.translate("Hello", "es")  # Spanish
result = deka.translate("Hello", "zh")  # Chinese
result = deka.translate("Hello", "sw")  # Swahili
```

### List Available Languages
```python
# See all supported languages
languages = deka.list_languages()
print(f"Supported languages: {len(languages)}")
print(languages[:10])  # First 10 languages
```

## Error Handling

```python
try:
    result = deka.translate("Hello", "french", provider="openai")
    print(result.text)
except deka.APIKeyError:
    print("API key not configured or invalid")
except deka.ProviderError as e:
    print(f"Provider error: {e}")
except deka.LanguageNotSupportedError as e:
    print(f"Language not supported: {e}")
```

## Next Steps

- **[Configuration Guide](configuration.md)** - Detailed configuration options
- **[Provider Overview](../providers/overview.md)** - Learn about each provider
- **[Model Selection](../features/model-selection.md)** - Advanced model selection
- **[African Languages](../features/african-languages.md)** - African language support
- **[API Reference](../api/core.md)** - Complete API documentation

## Tips for Success

!!! tip "Start with One Provider"
    Begin with just Google Translate or OpenAI to get familiar with the API.

!!! tip "Use Model Selection Wisely"
    - Use `gpt-3.5-turbo` for speed and cost
    - Use `gpt-4` for quality and accuracy
    - Use `claude-haiku` for fastest AI translation

!!! tip "African Languages"
    For African languages, GhanaNLP provides the most authentic translations.

!!! tip "Comparison for Quality"
    Use `deka.compare()` to find the best translation for important content.
