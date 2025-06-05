"""
Basic usage examples for Deka.
"""

import deka

def main():
    # Configure Deka with your API keys
    # Note: Replace with your actual API keys
    deka.configure({
        'google_api_key': 'your-google-api-key-here',
        'deepl_api_key': 'your-deepl-api-key-here',
        'openai_api_key': 'your-openai-api-key-here',
    })
    
    print("🌍 Deka Translation Examples\n")
    
    # Example 1: Simple translation
    print("1. Simple Translation:")
    try:
        result = deka.translate("Hello world", "french", provider="google")
        print(f"   Original: Hello world")
        print(f"   French: {result.text}")
        print(f"   Provider: {result.provider}")
        print(f"   Response time: {result.response_time_ms}ms\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 2: Auto-detect source language
    print("2. Auto-detect Source Language:")
    try:
        result = deka.translate("Bonjour le monde", "english", provider="google")
        print(f"   Original: Bonjour le monde")
        print(f"   English: {result.text}")
        print(f"   Detected source: {result.source_language}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 3: Compare multiple providers
    print("3. Compare Multiple Providers:")
    try:
        comparison = deka.compare(
            text="Hello, how are you?",
            target_language="spanish",
            providers=["google", "openai"]  # Add more if you have keys
        )
        
        print(f"   Original: Hello, how are you?")
        print(f"   Target: Spanish")
        print("   Results:")
        
        for result in comparison.results:
            print(f"     {result.provider}: {result.text} ({result.response_time_ms}ms)")
        
        if comparison.fastest_provider:
            print(f"   Fastest: {comparison.fastest_provider}")
        
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 4: Different language formats
    print("4. Different Language Formats:")
    languages_to_try = ["french", "fr", "français", "Spanish", "es"]
    
    for lang in languages_to_try:
        try:
            normalized = deka.normalize_language(lang)
            print(f"   '{lang}' → '{normalized}'")
        except Exception as e:
            print(f"   '{lang}' → Error: {e}")
    
    print()
    
    # Example 5: List available providers and languages
    print("5. Available Providers:")
    providers = deka.list_providers()
    for provider in providers:
        print(f"   {provider['id']}: {provider['name']} ({provider['type']})")
    
    print("\n6. Supported Languages (first 10):")
    languages = deka.list_languages()
    for lang in languages[:10]:
        print(f"   {lang}")
    
    print(f"   ... and {len(languages) - 10} more")


if __name__ == "__main__":
    main()
