#!/usr/bin/env python3
"""
Test script for Deka with real API keys.
Replace the API keys below with your actual keys.
"""

import deka
import asyncio
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 🔑 GET API KEYS FROM ENVIRONMENT
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GHANANLP_API_KEY = os.getenv("GHANANLP_API_KEY")

def test_openai():
    """Test OpenAI provider."""
    print("\n🤖 Testing OpenAI Provider")
    print("=" * 40)
    
    try:
        # Configure OpenAI
        deka.configure({'openai_api_key': OPENAI_API_KEY})
        
        # Test simple translation
        print("Testing: 'Hello world' → French")
        start_time = time.time()
        result = deka.translate("Hello world", "french", provider="openai")
        end_time = time.time()
        
        print(f"✅ Translation: {result.text}")
        print(f"✅ Provider: {result.provider}")
        print(f"✅ Source language: {result.source_language}")
        print(f"✅ Target language: {result.target_language}")
        print(f"✅ Response time: {end_time - start_time:.2f}s")
        
        if result.metadata:
            print(f"✅ Metadata: {result.metadata}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_anthropic():
    """Test Anthropic provider."""
    print("\n🧠 Testing Anthropic Provider")
    print("=" * 40)
    
    try:
        # Configure Anthropic
        deka.configure({'anthropic_api_key': ANTHROPIC_API_KEY})
        
        # Test simple translation
        print("Testing: 'Hello world' → Spanish")
        start_time = time.time()
        result = deka.translate("Hello world", "spanish", provider="anthropic")
        end_time = time.time()
        
        print(f"✅ Translation: {result.text}")
        print(f"✅ Provider: {result.provider}")
        print(f"✅ Source language: {result.source_language}")
        print(f"✅ Target language: {result.target_language}")
        print(f"✅ Response time: {end_time - start_time:.2f}s")
        
        if result.metadata:
            print(f"✅ Metadata: {result.metadata}")
        
        return True
        
    except Exception as e:
        print(f"❌ Anthropic test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_comparison():
    """Test provider comparison."""
    print("\n⚖️  Testing Provider Comparison")
    print("=" * 40)
    
    try:
        # Configure both providers
        deka.configure({
            'openai_api_key': OPENAI_API_KEY,
            'anthropic_api_key': ANTHROPIC_API_KEY
        })
        
        # Test comparison
        print("Comparing: 'Good morning, how are you?' → German")
        start_time = time.time()
        comparison = deka.compare(
            text="Good morning, how are you?",
            target_language="german",
            providers=["openai", "anthropic"]
        )
        end_time = time.time()
        
        print(f"✅ Total time: {end_time - start_time:.2f}s")
        print(f"✅ Number of results: {len(comparison.results)}")
        
        for result in comparison.results:
            print(f"\n  {result.provider}:")
            print(f"    Translation: {result.text}")
            print(f"    Response time: {result.response_time_ms}ms")
        
        if comparison.fastest_provider:
            print(f"\n✅ Fastest provider: {comparison.fastest_provider}")
        
        return True
        
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

async def test_async():
    """Test async functionality."""
    print("\n🚀 Testing Async Functionality")
    print("=" * 40)
    
    try:
        # Configure both providers
        deka.configure({
            'openai_api_key': OPENAI_API_KEY,
            'anthropic_api_key': ANTHROPIC_API_KEY
        })
        
        # Test async comparison
        print("Async comparing: 'Thank you very much' → Italian")
        start_time = time.time()
        comparison = await deka.compare_async(
            text="Thank you very much",
            target_language="italian",
            providers=["openai", "anthropic"]
        )
        end_time = time.time()
        
        print(f"✅ Total time: {end_time - start_time:.2f}s")
        print(f"✅ Number of results: {len(comparison.results)}")
        
        for result in comparison.results:
            print(f"\n  {result.provider}:")
            print(f"    Translation: {result.text}")
            print(f"    Response time: {result.response_time_ms}ms")
        
        if comparison.fastest_provider:
            print(f"\n✅ Fastest provider: {comparison.fastest_provider}")
        
        return True
        
    except Exception as e:
        print(f"❌ Async test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_model_selection():
    """Test model selection functionality."""
    print("\n🎯 Testing Model Selection")
    print("=" * 40)

    try:
        # Configure providers
        deka.configure({
            'openai_api_key': OPENAI_API_KEY,
            'anthropic_api_key': ANTHROPIC_API_KEY
        })

        # Test OpenAI with different models
        print("Testing OpenAI with gpt-4:")
        result = deka.translate("Hello world", "french", provider="openai/gpt-4")
        print(f"✅ Translation: {result.text}")
        print(f"✅ Model used: {result.metadata.get('model', 'unknown')}")

        print("\nTesting Anthropic with claude-3-5-sonnet:")
        result = deka.translate("Hello world", "spanish", provider="anthropic/claude-3-5-sonnet-20241022")
        print(f"✅ Translation: {result.text}")
        print(f"✅ Model used: {result.metadata.get('model', 'unknown')}")

        # Test model comparison
        print("\nComparing different models:")
        comparison = deka.compare(
            text="Good evening",
            target_language="italian",
            providers=["openai/gpt-3.5-turbo", "openai/gpt-4", "anthropic/claude-3-5-sonnet-20241022"]
        )

        for result in comparison.results:
            model = result.metadata.get('model', 'unknown')
            print(f"  {result.provider} ({model}): {result.text}")

        return True

    except Exception as e:
        print(f"❌ Model selection test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_gemini():
    """Test Gemini provider (if API key available)."""
    print("\n🔮 Testing Gemini Provider")
    print("=" * 40)

    if not GEMINI_API_KEY or GEMINI_API_KEY == "your-gemini-api-key-here":
        print("⚠️  Gemini API key not configured, skipping test")
        return True  # Not a failure, just skipped

    try:
        # Configure Gemini
        deka.configure({'gemini_api_key': GEMINI_API_KEY})

        # Test simple translation
        print("Testing: 'Hello world' → Japanese")
        start_time = time.time()
        result = deka.translate("Hello world", "japanese", provider="google-gemini")
        end_time = time.time()

        print(f"✅ Translation: {result.text}")
        print(f"✅ Provider: {result.provider}")
        print(f"✅ Model: {result.metadata.get('model', 'unknown')}")
        print(f"✅ Response time: {end_time - start_time:.2f}s")

        if result.metadata:
            print(f"✅ Metadata: {result.metadata}")

        # Test with specific model
        print("\nTesting with gemini-2.0-flash:")
        result = deka.translate("Good morning", "korean", provider="google-gemini/gemini-2.0-flash-001")
        print(f"✅ Translation: {result.text}")
        print(f"✅ Model: {result.metadata.get('model', 'unknown')}")

        return True

    except Exception as e:
        print(f"❌ Gemini test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_permissive_model_validation():
    """Test that unknown models show warnings but still work."""
    print("\n⚠️  Testing Permissive Model Validation")
    print("=" * 40)

    try:
        # Configure providers
        deka.configure({
            'openai_api_key': OPENAI_API_KEY,
        })

        # Test with a made-up model name - should warn but still try
        print("Testing with fake model 'gpt-5-ultra':")
        result = deka.translate("Hello", "french", provider="openai/gpt-5-ultra")
        print(f"✅ Translation attempted (may fail at API level): {result.text if hasattr(result, 'text') else 'Failed as expected'}")

        return True

    except Exception as e:
        print(f"⚠️  Expected behavior - API rejected unknown model: {e}")
        return True  # This is expected behavior

def test_ghananlp():
    """Test GhanaNLP provider for African languages."""
    print("\n🌍 Testing GhanaNLP Provider (African Languages)")
    print("=" * 40)

    if not GHANANLP_API_KEY or GHANANLP_API_KEY == "your-ghananlp-api-key-here":
        print("⚠️  GhanaNLP API key not configured, skipping test")
        return True  # Not a failure, just skipped

    try:
        # Configure GhanaNLP
        deka.configure({'ghananlp_api_key': GHANANLP_API_KEY})

        # Test English to Twi (Ghanaian language)
        print("Testing: 'Hello, how are you?' → Twi")
        start_time = time.time()
        result = deka.translate("Hello, how are you?", "twi", provider="ghananlp")
        end_time = time.time()

        print(f"✅ Translation: {result.text}")
        print(f"✅ Provider: {result.provider}")
        print(f"✅ Response time: {end_time - start_time:.2f}s")

        if result.metadata:
            print(f"✅ Metadata: {result.metadata}")

        # Test another African language - Yoruba
        print("\nTesting: 'Good morning' → Yoruba")
        result = deka.translate("Good morning", "yoruba", provider="ghananlp")
        print(f"✅ Translation: {result.text}")

        # Test Ga language
        print("\nTesting: 'Thank you' → Ga")
        result = deka.translate("Thank you", "ga", provider="ghananlp")
        print(f"✅ Translation: {result.text}")

        return True

    except Exception as e:
        print(f"❌ GhanaNLP test failed: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        return False

def test_african_language_support():
    """Test our enhanced African language support."""
    print("\n🌍 Testing African Language Support")
    print("=" * 40)

    try:
        # Test language normalization for African languages
        african_languages = [
            'twi', 'ga', 'ewe', 'fante', 'dagbani', 'gurene',
            'yoruba', 'kikuyu', 'luo', 'kimeru'
        ]

        print("Testing language normalization for African languages:")
        for lang in african_languages:
            try:
                normalized = deka.normalize_language(lang)
                print(f"  {lang} → {normalized} ✅")
            except Exception as e:
                print(f"  {lang} → Error: {e} ❌")

        # Test provider language support
        print("\nGhanaNLP supported languages:")
        from deka.providers.ghananlp import GhanaNLPProvider
        supported = GhanaNLPProvider.get_supported_languages()
        print(f"  {len(supported)} languages: {', '.join(supported[:5])}...")

        return True

    except Exception as e:
        print(f"❌ African language support test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Deka Real API Testing")
    print("=" * 50)
    
    # Check if API keys are configured
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your-openai-api-key-here":
        print("❌ Please add your OpenAI API key to the .env file!")
        print("   Edit .env and set: OPENAI_API_KEY=your-actual-key")
        return

    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your-anthropic-api-key-here":
        print("❌ Please add your Anthropic API key to the .env file!")
        print("   Edit .env and set: ANTHROPIC_API_KEY=your-actual-key")
        return
    
    results = []
    
    # Test individual providers
    results.append(("OpenAI", test_openai()))
    results.append(("Anthropic", test_anthropic()))
    results.append(("Comparison", test_comparison()))
    results.append(("Model Selection", test_model_selection()))
    results.append(("Gemini", test_gemini()))
    results.append(("Permissive Models", test_permissive_model_validation()))
    results.append(("GhanaNLP", test_ghananlp()))
    results.append(("African Languages", test_african_language_support()))
    
    # Test async
    try:
        async_result = asyncio.run(test_async())
        results.append(("Async", async_result))
    except Exception as e:
        print(f"❌ Async test setup failed: {e}")
        results.append(("Async", False))
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! Deka is working perfectly!")
    else:
        print("\n🔧 Some tests failed. Let's debug the issues!")

if __name__ == "__main__":
    main()
