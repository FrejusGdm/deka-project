# Deka 🌍

A unified Python SDK for multiple translation providers with advanced model selection and African language support.

## Overview

Deka provides a single, simple interface to work with multiple translation providers including Google Translate, DeepL, OpenAI, Anthropic, Gemini, and GhanaNLP. Compare translations, choose specific AI models, and access specialized African language support.

## Key Features

### 🎯 **Model Selection**
Choose specific AI models for your translations:
```python
# Use GPT-4 for high-quality translation
result = deka.translate("Hello", "french", provider="openai/gpt-4")

# Use Claude 3.5 Sonnet for nuanced translation  
result = deka.translate("Hello", "french", provider="anthropic/claude-3-5-sonnet")
```

### 🌍 **African Language Support**
Dedicated support for 11 African languages via GhanaNLP:
```python
# Translate to Twi (Ghana)
result = deka.translate("Thank you", "twi", provider="ghananlp")
# → "Meda wo ase"

# Translate to Yoruba (Nigeria)
result = deka.translate("Good morning", "yoruba", provider="ghananlp")  
# → "Ẹ káàárọ̀"
```

### 🔄 **Provider Comparison**
Compare translations across multiple providers and models:
```python
comparison = deka.compare("Hello world", "spanish", providers=[
    "google",
    "openai/gpt-4", 
    "anthropic/claude-3-5-sonnet",
    "ghananlp"
])

for result in comparison.results:
    print(f"{result.provider}: {result.text}")
```

### ⚡ **Async Support**
Full async/await support for better performance:
```python
# Async translation
result = await deka.translate_async("Hello", "french", provider="openai")

# Async comparison (runs providers concurrently)
comparison = await deka.compare_async("Hello", "spanish", providers=["google", "openai"])
```

## Supported Providers

| Provider | Type | Languages | Models | Specialization |
|----------|------|-----------|--------|----------------|
| **Google Translate** | API | 100+ | - | Fast, reliable, auto-detection |
| **DeepL** | API | 30+ | - | High quality, European languages |
| **OpenAI** | LLM | Any | 5 models | Context-aware, creative |
| **Anthropic** | LLM | Any | 5 models | Nuanced, culturally-aware |
| **Google Gemini** | LLM | Any | 5 models | Latest Google AI, multimodal |
| **GhanaNLP** | API | 11 African | - | African language specialist |

## Quick Start

### Installation
```bash
pip install deka
```

### Basic Usage
```python
import deka

# Configure with your API keys
deka.configure({
    'openai_api_key': 'your-openai-key',
    'ghananlp_api_key': 'your-ghananlp-key'
})

# Simple translation
result = deka.translate("Hello world", "french")
print(result.text)  # "Bonjour le monde"

# African language translation
result = deka.translate("Hello", "twi", provider="ghananlp")
print(result.text)  # "Hello na ɔkyerɛwee"
```

## What Makes Deka Special

### 🎯 **First SDK with Model Selection**
No other translation library lets you choose specific AI models. With Deka, you can optimize for speed (gpt-3.5-turbo), quality (gpt-4), or cost (claude-haiku).

### 🌍 **Dedicated African Language Support**
Built-in integration with GhanaNLP provides authentic translations for Ghanaian and other African languages that other providers don't support well.

### ⚠️ **Future-Proof Design**
Permissive model validation means you can try new models as soon as providers release them, without waiting for SDK updates.

### 🔄 **Professional Comparison Tools**
Compare quality, speed, and cost across different providers and models to find the best solution for your use case.

## Use Cases

- **🌍 Multilingual Applications**: Support users in their native languages
- **📊 Translation Quality Assessment**: Compare providers to find the best translations
- **🚀 Performance Optimization**: Choose fast models for real-time chat, quality models for documents
- **💰 Cost Optimization**: Use cheaper models for simple content, premium models for important content
- **🌍 African Market Expansion**: Reach African audiences with authentic language support
- **🔄 Fallback Systems**: Try multiple providers for reliability

## Getting Started

Ready to start translating? Check out our [Quick Start Guide](getting-started/quick-start.md) or explore specific [Provider Documentation](providers/overview.md).

For African language support, see our [African Languages Guide](features/african-languages.md).

For advanced features like model selection, see our [Model Selection Guide](features/model-selection.md).
