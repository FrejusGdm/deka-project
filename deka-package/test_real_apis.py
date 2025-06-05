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
