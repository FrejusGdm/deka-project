# Language Mapping System Deep Dive

## 🌍 The Language Problem

Different translation providers use different language codes for the same language:

| Language | Google | DeepL | Azure | OpenAI | User Input |
|----------|--------|-------|-------|--------|------------|
| French | `fr` | `fr` | `fr-FR` | "French" | "french", "français", "fr" |
| Chinese | `zh` | `zh` | `zh-Hans` | "Chinese" | "chinese", "mandarin", "zh-cn" |
| Portuguese | `pt` | `pt-PT` | `pt-BR` | "Portuguese" | "portuguese", "português" |

**The challenge:** Users think in natural language, but APIs need specific codes.

## 📄 src/deka/language_mapper.py - The Solution

### Three-Layer Mapping System

```
User Input → Normalized Name → ISO Code → Provider Code
"français" → "french"       → "fr"     → "fr-FR" (Azure)
```

### Layer 1: ISO Code Database
```python
ISO_TO_NAME = {
    'en': 'english',
    'fr': 'french', 
    'es': 'spanish',
    'de': 'german',
    # ... 70+ languages
}

NAME_TO_ISO = {name: code for code, name in ISO_TO_NAME.items()}
```

**Why ISO 639-1?**
- **Standard**: International standard for language codes
- **Widely supported**: Most APIs understand ISO codes
- **Compact**: Two-letter codes are short and memorable
- **Stable**: Codes don't change over time

### Layer 2: Language Aliases
```python
LANGUAGE_ALIASES = {
    'chinese': ['mandarin', 'zh-cn', 'zh-tw', 'simplified chinese'],
    'spanish': ['castilian', 'español'],
    'portuguese': ['português'],
    'arabic': ['عربي'],
    'japanese': ['日本語', 'nihongo'],
}
```

**Why aliases?**
- **User flexibility**: People use different names for same language
- **Cultural sensitivity**: Native names for languages
- **Regional variants**: "Simplified Chinese" vs "Chinese"
- **Common mistakes**: "Mandarin" is often used for "Chinese"

### Layer 3: Provider-Specific Mappings
```python
PROVIDER_MAPPINGS = {
    'deepl': {
        'portuguese': 'pt-PT',  # European Portuguese by default
        'english': 'en-US',     # US English by default
    },
    'google': {
        'chinese': 'zh',
        'filipino': 'tl',  # Google uses 'tl' for Tagalog
    }
}
```

**Provider quirks handled:**
- **Regional preferences**: DeepL defaults to European Portuguese
- **Different codes**: Google uses 'tl' for Filipino, others use 'fil'
- **API limitations**: Some providers don't support all variants

## 🧠 Core Algorithm: normalize_language()

### Step-by-Step Process

```python
def normalize_language(language: str) -> str:
    language = language.lower().strip()
    
    # Step 1: Direct ISO code lookup
    if language in ISO_TO_NAME:
        return ISO_TO_NAME[language]  # "fr" → "french"
    
    # Step 2: Direct name lookup  
    if language in NAME_TO_ISO:
        return language  # "french" → "french"
    
    # Step 3: Check aliases
    for standard_name, aliases in LANGUAGE_ALIASES.items():
        if language in [alias.lower() for alias in aliases]:
            return standard_name  # "mandarin" → "chinese"
    
    # Step 4: Fuzzy matching for typos
    matches = difflib.get_close_matches(language, all_names, cutoff=0.8)
    if matches:
        return normalize_match(matches[0])  # "frnch" → "french"
    
    # Step 5: Helpful error with suggestions
    suggestions = difflib.get_close_matches(language, all_names, cutoff=0.6)
    raise LanguageNotSupportedError(f"Did you mean: {suggestions}?")
```

### Why This Algorithm Works

#### 1. **Fast Common Cases**
- **O(1) lookups**: Hash table lookups for common cases
- **Early returns**: Most requests handled in first two steps
- **No computation**: Direct dictionary lookups

#### 2. **Handles Variations**
```python
# All of these work:
normalize_language("french")    # → "french"
normalize_language("fr")        # → "french" 
normalize_language("French")    # → "french"
normalize_language("FRENCH")    # → "french"
normalize_language("français")  # → "french"
```

#### 3. **Typo Tolerance**
```python
normalize_language("frnch")     # → "french" (fuzzy match)
normalize_language("spansh")    # → "spanish"
normalize_language("germn")     # → "german"
```

**Fuzzy matching parameters:**
- **cutoff=0.8**: High threshold for auto-correction
- **cutoff=0.6**: Lower threshold for suggestions
- **n=1**: Only return best match for auto-correction
- **n=3**: Return multiple suggestions for errors

#### 4. **Helpful Error Messages**
```python
# Instead of: "Language 'klingon' not supported"
# We show: "Language 'klingon' not recognized. Did you mean: korean, mongolian?"
```

## 🔧 Provider Code Resolution

### get_provider_code() Function
```python
def get_provider_code(language: str, provider: str) -> str:
    # First normalize: "français" → "french"
    normalized = normalize_language(language)
    
    # Check provider-specific mappings
    if provider in PROVIDER_MAPPINGS:
        provider_map = PROVIDER_MAPPINGS[provider]
        if normalized in provider_map:
            return provider_map[normalized]  # "french" → "fr-FR" for Azure
    
    # Fall back to ISO code
    return NAME_TO_ISO[normalized]  # "french" → "fr"
```

### Real-World Examples

#### Example 1: Google Translate
```python
get_provider_code("chinese", "google")
# "chinese" → "chinese" → "zh" (Google uses standard ISO)
```

#### Example 2: DeepL
```python
get_provider_code("portuguese", "deepl") 
# "portuguese" → "portuguese" → "pt-PT" (DeepL prefers European)
```

#### Example 3: OpenAI
```python
get_provider_code("français", "openai")
# "français" → "french" → "french" (OpenAI uses full names in prompts)
```

## 🎯 Advanced Features

### Language Support Detection
```python
def list_languages(provider: str = None) -> List[str]:
    if provider:
        # Could filter by provider capabilities
        return get_supported_languages_for_provider(provider)
    else:
        # Return all languages we know about
        return sorted(NAME_TO_ISO.keys())
```

**Future enhancement:** Each provider could declare supported languages.

### ISO Code Extraction
```python
def get_iso_code(language: str) -> str:
    normalized = normalize_language(language)
    return NAME_TO_ISO[normalized]
```

**Use cases:**
- **Metadata**: Store ISO codes in databases
- **Standardization**: Convert user input to standard format
- **Interoperability**: Exchange data with other systems

## 🌟 Why This System is Powerful

### 1. **User-Friendly**
```python
# All of these work the same way:
deka.translate("Hello", "french")
deka.translate("Hello", "fr") 
deka.translate("Hello", "français")
deka.translate("Hello", "French")
```

### 2. **Provider-Agnostic**
```python
# Same language input works with any provider:
deka.translate("Hello", "chinese", provider="google")    # → "zh"
deka.translate("Hello", "chinese", provider="azure")     # → "zh-Hans"
deka.translate("Hello", "chinese", provider="openai")    # → "Chinese"
```

### 3. **Error-Tolerant**
```python
# Handles typos gracefully:
deka.translate("Hello", "frnch")  # Works! Auto-corrects to "french"
```

### 4. **Extensible**
```python
# Easy to add new languages:
ISO_TO_NAME['yo'] = 'yoruba'
LANGUAGE_ALIASES['yoruba'] = ['yorùbá', 'yoruba language']
```

### 5. **Culturally Aware**
```python
# Supports native language names:
deka.translate("Hello", "日本語")  # Japanese in Japanese
deka.translate("Hello", "عربي")   # Arabic in Arabic
```

## 🔮 Future Enhancements

### 1. **Regional Variants**
```python
# Could support specific regions:
deka.translate("Hello", "portuguese-brazil")    # → "pt-BR"
deka.translate("Hello", "portuguese-portugal")  # → "pt-PT"
```

### 2. **Provider Capabilities**
```python
# Could check what each provider supports:
if not provider_supports_language("yoruba", "google"):
    suggest_alternative_provider()
```

### 3. **Language Detection**
```python
# Could auto-detect source language:
detected = deka.detect_language("Bonjour le monde")  # → "french"
```

This language mapping system makes Deka **incredibly user-friendly** while handling the complexity of multiple translation providers behind the scenes!
