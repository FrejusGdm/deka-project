# Examples and Usage Patterns

## 📁 examples/ Directory Explained

I created two comprehensive example files that serve as both **documentation** and **testing tools** for users.

### 📄 examples/basic_usage.py - Getting Started

This file demonstrates **core functionality** in a beginner-friendly way:

#### Example 1: Simple Translation
```python
result = deka.translate("Hello world", "french", provider="google")
print(f"Original: Hello world")
print(f"French: {result.text}")
print(f"Provider: {result.provider}")
print(f"Response time: {result.response_time_ms}ms")
```

**What it teaches:**
- **Basic syntax**: How to call the main function
- **Response structure**: What data you get back
- **Performance awareness**: Response times matter
- **Provider selection**: How to choose specific providers

#### Example 2: Auto-detect Source Language
```python
result = deka.translate("Bonjour le monde", "english", provider="google")
print(f"Detected source: {result.source_language}")
```

**What it teaches:**
- **Language detection**: Don't need to specify source language
- **Bidirectional translation**: Can translate from any language to any language
- **Metadata access**: Response contains useful information

#### Example 3: Provider Comparison
```python
comparison = deka.compare(
    text="Hello, how are you?",
    target_language="spanish",
    providers=["google", "openai"]
)

for result in comparison.results:
    print(f"{result.provider}: {result.text} ({result.response_time_ms}ms)")

print(f"Fastest: {comparison.fastest_provider}")
```

**What it teaches:**
- **Comparison feature**: Deka's unique selling point
- **Performance comparison**: See which provider is fastest
- **Quality comparison**: Compare translation quality
- **Result iteration**: How to work with multiple results

#### Example 4: Language Format Flexibility
```python
languages_to_try = ["french", "fr", "français", "Spanish", "es"]

for lang in languages_to_try:
    normalized = deka.normalize_language(lang)
    print(f"'{lang}' → '{normalized}'")
```

**What it teaches:**
- **Input flexibility**: Many ways to specify languages
- **Normalization**: How Deka standardizes language names
- **Error handling**: What happens with invalid languages

### 📄 examples/async_example.py - Advanced Usage

This file demonstrates **high-performance patterns** for serious users:

#### Example 1: Basic Async
```python
result = await deka.translate_async("Hello world", "japanese", provider="openai")
```

**What it teaches:**
- **Async syntax**: Just add `async`/`await`
- **Same interface**: Async version works identically
- **Performance**: When to use async vs sync

#### Example 2: Concurrent Translations
```python
texts = ["Hello", "Good morning", "How are you?", "Thank you", "Goodbye"]

tasks = [
    deka.translate_async(text, "french", provider="google")
    for text in texts
]

results = await asyncio.gather(*tasks)
```

**What it teaches:**
- **Batch processing**: Translate multiple texts efficiently
- **Concurrency**: All translations happen simultaneously
- **Performance gains**: Much faster than sequential processing

#### Example 3: Async Provider Comparison
```python
comparison = await deka.compare_async(
    text="The weather is beautiful today",
    target_language="italian",
    providers=["google", "openai"]
)
```

**What it teaches:**
- **Concurrent comparison**: All providers called simultaneously
- **Maximum performance**: Fastest way to compare providers
- **Real-world usage**: How to use async in practice

#### Example 4: Batch Processing with Rate Limiting
```python
# Process in batches to avoid rate limits
batch_size = 2
for i in range(0, len(sentences), batch_size):
    batch = sentences[i:i + batch_size]
    
    tasks = [
        deka.translate_async(sentence, "german", provider="google")
        for sentence in batch
    ]
    
    batch_results = await asyncio.gather(*tasks)
    
    # Small delay between batches
    if i + batch_size < len(sentences):
        await asyncio.sleep(0.5)
```

**What it teaches:**
- **Rate limit management**: How to avoid hitting API limits
- **Production patterns**: Real-world batch processing
- **Error resilience**: Handle large workloads safely

## 🧪 tests/test_basic.py - Quality Assurance

### Test Categories

#### 1. Configuration Tests
```python
def test_configuration():
    configure({'test_key': 'test_value'})
    assert get_config('test_key') == 'test_value'
    
    with pytest.raises(ConfigurationError):
        get_config('missing_key')
```

**What it tests:**
- **Configuration storage**: Settings are saved correctly
- **Configuration retrieval**: Can get settings back
- **Error handling**: Missing keys raise appropriate errors

#### 2. Language Normalization Tests
```python
def test_language_normalization():
    assert normalize_language('french') == 'french'
    assert normalize_language('fr') == 'french'
    assert normalize_language('français') == 'french'
    
    with pytest.raises(LanguageNotSupportedError):
        normalize_language('klingon')
```

**What it tests:**
- **Basic normalization**: Standard cases work
- **Case insensitivity**: Uppercase/lowercase handled
- **Alias support**: Alternative names work
- **Error cases**: Invalid languages fail gracefully

#### 3. Data Model Tests
```python
def test_models():
    request = TranslationRequest(text="Hello", target_language="french")
    assert request.text == "Hello"
    
    with pytest.raises(ValueError):
        TranslationRequest(text="", target_language="french")
```

**What it tests:**
- **Model creation**: Objects can be created correctly
- **Validation**: Invalid data is rejected
- **Properties**: Computed properties work correctly

## 🎯 Usage Patterns Demonstrated

### Pattern 1: Simple One-off Translation
```python
# Quick translation for user interface
result = deka.translate(user_input, target_lang, provider="google")
display_translation(result.text)
```

**Use case:** Web app translating user messages

### Pattern 2: Quality Comparison
```python
# Compare providers to find best translation
comparison = deka.compare(content, target_lang, providers=["google", "deepl"])
best_result = max(comparison.results, key=lambda r: r.confidence or 0)
```

**Use case:** Content management system choosing best translation

### Pattern 3: Batch Processing
```python
# Translate large dataset efficiently
async def translate_dataset(items):
    tasks = [
        deka.translate_async(item.text, item.target_lang)
        for item in items
    ]
    return await asyncio.gather(*tasks)
```

**Use case:** Localizing app content or documentation

### Pattern 4: Fallback Strategy
```python
# Try multiple providers for reliability
providers = ["google", "deepl", "openai"]
for provider in providers:
    try:
        result = deka.translate(text, target_lang, provider=provider)
        return result
    except ProviderError:
        continue
raise Exception("All providers failed")
```

**Use case:** Mission-critical applications needing high availability

### Pattern 5: Cost Optimization
```python
# Use cheaper provider first, fallback to premium
try:
    result = deka.translate(text, target_lang, provider="google")  # Cheaper
except ProviderError:
    result = deka.translate(text, target_lang, provider="openai")  # More expensive
```

**Use case:** Budget-conscious applications

## 📊 Real-World Integration Examples

### Web Application Integration
```python
from flask import Flask, request, jsonify
import deka

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_endpoint():
    data = request.json
    
    try:
        result = deka.translate(
            text=data['text'],
            target_language=data['target_language'],
            provider=data.get('provider', 'google')
        )
        
        return jsonify({
            'translation': result.text,
            'provider': result.provider,
            'response_time': result.response_time_ms
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

### CLI Tool Integration
```python
import click
import deka

@click.command()
@click.argument('text')
@click.option('--target', '-t', required=True, help='Target language')
@click.option('--provider', '-p', default='google', help='Translation provider')
def translate_cli(text, target, provider):
    """Translate text using Deka."""
    try:
        result = deka.translate(text, target, provider=provider)
        click.echo(f"Translation: {result.text}")
        click.echo(f"Provider: {result.provider}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == '__main__':
    translate_cli()
```

### Data Processing Pipeline
```python
import pandas as pd
import asyncio
import deka

async def translate_dataframe(df, text_column, target_language):
    """Translate a pandas DataFrame column."""
    
    # Configure Deka
    deka.configure({'google_api_key': 'your-key'})
    
    # Create translation tasks
    tasks = [
        deka.translate_async(text, target_language)
        for text in df[text_column]
    ]
    
    # Execute all translations
    results = await asyncio.gather(*tasks)
    
    # Add translations to DataFrame
    df[f'{text_column}_{target_language}'] = [r.text for r in results]
    
    return df
```

## 🎓 Educational Value

### For Beginners
- **Simple examples**: Easy to understand and copy
- **Progressive complexity**: Start simple, build up
- **Error handling**: Shows what can go wrong
- **Best practices**: Demonstrates good patterns

### For Advanced Users
- **Async patterns**: High-performance techniques
- **Error resilience**: Production-ready error handling
- **Batch processing**: Efficient large-scale operations
- **Integration examples**: Real-world usage patterns

### For Contributors
- **Test structure**: How to test the package
- **Code organization**: How examples are structured
- **Documentation**: How to document features

These examples serve as **living documentation** that users can run, modify, and learn from - much more valuable than static documentation!
