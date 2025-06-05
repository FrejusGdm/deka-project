"""
Async usage examples for Deka.
"""

import asyncio
import time
import deka


async def main():
    # Configure Deka with your API keys
    deka.configure({
        'google_api_key': 'your-google-api-key-here',
        'openai_api_key': 'your-openai-api-key-here',
    })
    
    print("🚀 Deka Async Examples\n")
    
    # Example 1: Simple async translation
    print("1. Async Translation:")
    try:
        start_time = time.time()
        result = await deka.translate_async("Hello world", "japanese", provider="openai")
        end_time = time.time()
        
        print(f"   Original: Hello world")
        print(f"   Japanese: {result.text}")
        print(f"   Total time: {(end_time - start_time) * 1000:.0f}ms\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 2: Concurrent translations
    print("2. Concurrent Translations:")
    try:
        texts = [
            "Hello",
            "Good morning", 
            "How are you?",
            "Thank you",
            "Goodbye"
        ]
        
        start_time = time.time()
        
        # Translate all texts concurrently
        tasks = [
            deka.translate_async(text, "french", provider="google")
            for text in texts
        ]
        
        results = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f"   Translated {len(texts)} phrases in {(end_time - start_time) * 1000:.0f}ms:")
        for original, result in zip(texts, results):
            print(f"     {original} → {result.text}")
        
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 3: Async comparison (fastest!)
    print("3. Async Provider Comparison:")
    try:
        start_time = time.time()
        
        comparison = await deka.compare_async(
            text="The weather is beautiful today",
            target_language="italian",
            providers=["google", "openai"]
        )
        
        end_time = time.time()
        
        print(f"   Original: The weather is beautiful today")
        print(f"   Target: Italian")
        print(f"   Total time: {(end_time - start_time) * 1000:.0f}ms")
        print("   Results:")
        
        for result in comparison.results:
            print(f"     {result.provider}: {result.text}")
            print(f"       Response time: {result.response_time_ms}ms")
        
        if comparison.fastest_provider:
            print(f"   Fastest provider: {comparison.fastest_provider}")
        
        print()
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # Example 4: Batch processing with rate limiting
    print("4. Batch Processing with Rate Limiting:")
    try:
        sentences = [
            "Machine learning is fascinating",
            "Python is a great programming language",
            "Translation technology has improved significantly",
            "Artificial intelligence is changing the world",
            "Open source software benefits everyone"
        ]
        
        print(f"   Processing {len(sentences)} sentences...")
        
        # Process in batches to avoid rate limits
        batch_size = 2
        all_results = []
        
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i + batch_size]
            print(f"   Processing batch {i//batch_size + 1}...")
            
            # Process batch concurrently
            tasks = [
                deka.translate_async(sentence, "german", provider="google")
                for sentence in batch
            ]
            
            batch_results = await asyncio.gather(*tasks)
            all_results.extend(batch_results)
            
            # Small delay between batches
            if i + batch_size < len(sentences):
                await asyncio.sleep(0.5)
        
        print("   Results:")
        for i, (original, result) in enumerate(zip(sentences, all_results), 1):
            print(f"     {i}. {original}")
            print(f"        → {result.text}")
        
    except Exception as e:
        print(f"   Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
