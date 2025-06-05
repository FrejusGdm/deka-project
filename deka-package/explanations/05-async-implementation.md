# Async Implementation Deep Dive

## 🚀 Why Async Matters for Translation

Translation APIs are **slow**:
- **Google Translate**: 500ms - 2 seconds
- **DeepL**: 1-3 seconds  
- **OpenAI**: 2-5 seconds (LLM processing)
- **Network latency**: +100-500ms

**Without async:**
```python
# Sequential - takes 6-10 seconds total!
google_result = translate_with_google("Hello")      # 2 seconds
deepl_result = translate_with_deepl("Hello")        # 3 seconds  
openai_result = translate_with_openai("Hello")      # 4 seconds
```

**With async:**
```python
# Concurrent - takes 4 seconds total (slowest provider)
results = await asyncio.gather(
    translate_with_google("Hello"),    # All run
    translate_with_deepl("Hello"),     # at the
    translate_with_openai("Hello")     # same time!
)
```

## 🏗️ Async Architecture Overview

```
┌─────────────────────────────────────┐
│         User Code                   │
│  await deka.compare_async(...)      │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│      Core Async Functions           │
│   compare_async(), translate_async()│
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│     Provider Async Methods          │
│  provider.translate_async(request)  │
└─────────────┬───────────────────────┘
              │
┌─────────────▼───────────────────────┐
│       aiohttp Sessions              │
│    Actual HTTP requests             │
└─────────────────────────────────────┘
```

## 📄 Base Provider Async Implementation

### Session Management
```python
class BaseProvider:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
```

**Why session reuse?**
- **Performance**: TCP connection reuse is much faster
- **Resource efficiency**: Don't create new connections every time
- **Connection pooling**: aiohttp manages connection pool automatically

### Proper Cleanup
```python
async def close(self) -> None:
    if self._session and not self._session.closed:
        await self._session.close()

def __del__(self):
    # Cleanup when provider is destroyed
    if self._session and not self._session.closed:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
        except:
            pass  # Don't fail if event loop is closed
```

**Resource management:**
- **Explicit cleanup**: `close()` method for manual cleanup
- **Automatic cleanup**: `__del__` tries to clean up automatically
- **Error tolerance**: Won't crash if event loop is already closed

## 🔧 Provider-Specific Async Implementation

### Google Translate Async
```python
async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
    session = await self._get_session()
    
    try:
        async with session.post(url, params=params) as response:
            await self._handle_aiohttp_error(response)
            data = await response.json()
            # Process response...
    except aiohttp.ClientError as e:
        raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
```

**Key patterns:**
- **Context manager**: `async with` ensures proper cleanup
- **Error handling**: Convert aiohttp errors to Deka errors
- **JSON parsing**: `await response.json()` for async parsing

### OpenAI Async (More Complex)
```python
async def translate_async(self, request: TranslationRequest) -> TranslationResponse:
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [...],
        'max_tokens': len(request.text) * 3,
        'temperature': 0.1,
    }
    
    session = await self._get_session()
    
    try:
        async with session.post(url, headers=headers, json=data) as response:
            await self._handle_aiohttp_error(response)
            result = await response.json()
            
            translated_text = result['choices'][0]['message']['content'].strip()
            # Create response...
    except aiohttp.ClientError as e:
        raise ProviderError(f"Request failed: {str(e)}", self.provider_name)
```

**LLM-specific considerations:**
- **Longer timeouts**: LLMs take more time to process
- **Token management**: Track token usage for cost estimation
- **Response parsing**: Extract text from complex JSON structure

## 📄 Core Async Functions

### translate_async() - Single Provider
```python
async def translate_async(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    provider: Optional[str] = None
) -> TranslationResponse:
    # Normalize languages
    target_language = normalize_language(target_language)
    
    # Create request
    request = TranslationRequest(...)
    
    # Get provider and translate
    provider_instance = create_provider_instance(provider)
    try:
        return await provider_instance.translate_async(request)
    finally:
        await provider_instance.close()  # Always cleanup!
```

**Key points:**
- **Same interface**: Only difference from sync version is `async`/`await`
- **Resource cleanup**: Always close provider session
- **Error propagation**: Let provider errors bubble up

### compare_async() - Multiple Providers (The Complex One)
```python
async def compare_async(
    text: str,
    target_language: str,
    providers: Optional[List[str]] = None
) -> ComparisonResult:
    # Create provider instances
    provider_instances = []
    for provider in providers:
        instance = create_provider_instance(provider)
        provider_instances.append((provider, instance))
    
    # Define async translation function
    async def translate_with_provider(provider_name, provider_instance):
        try:
            return await provider_instance.translate_async(request)
        except Exception:
            return None  # Return None for failed translations
        finally:
            await provider_instance.close()  # Always cleanup
    
    # Run all translations concurrently
    tasks = [
        translate_with_provider(name, instance) 
        for name, instance in provider_instances
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Filter successful results
    successful_results = [r for r in results if isinstance(r, TranslationResponse)]
    
    return ComparisonResult(request=request, results=successful_results)
```

**Concurrency patterns:**
- **asyncio.gather()**: Run all tasks concurrently
- **return_exceptions=True**: Don't fail if one provider fails
- **Resource cleanup**: Each task cleans up its own session
- **Error tolerance**: Partial success is still success

## ⚡ Performance Benefits

### Benchmark Example
```python
import time
import asyncio

# Sync version - Sequential
def sync_compare():
    start = time.time()
    results = []
    for provider in ["google", "deepl", "openai"]:
        result = deka.translate("Hello world", "french", provider=provider)
        results.append(result)
    end = time.time()
    print(f"Sync: {end - start:.2f} seconds")  # ~8 seconds

# Async version - Concurrent  
async def async_compare():
    start = time.time()
    comparison = await deka.compare_async(
        "Hello world", 
        "french", 
        providers=["google", "deepl", "openai"]
    )
    end = time.time()
    print(f"Async: {end - start:.2f} seconds")  # ~3 seconds
```

**Real-world improvements:**
- **3x faster**: For 3 providers
- **10x faster**: For 10 providers
- **Scales linearly**: More providers = more benefit

## 🛡️ Error Handling in Async

### Partial Failure Strategy
```python
# If Google fails but DeepL works, still return DeepL result
results = await asyncio.gather(*tasks, return_exceptions=True)

successful_results = []
for result in results:
    if isinstance(result, TranslationResponse):
        successful_results.append(result)
    elif isinstance(result, Exception):
        # Log error but continue
        logger.warning(f"Provider failed: {result}")

if not successful_results:
    raise DekaError("All providers failed")
```

**Benefits:**
- **Resilience**: One failed provider doesn't break everything
- **User experience**: Users get partial results quickly
- **Debugging**: Failed providers are logged for investigation

### Timeout Handling
```python
async def translate_with_timeout(provider, request, timeout=30):
    try:
        return await asyncio.wait_for(
            provider.translate_async(request),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise ProviderError(f"Provider {provider.provider_name} timed out")
```

**Timeout strategy:**
- **Per-provider timeouts**: Don't let slow providers block others
- **Configurable**: Different timeouts for different provider types
- **Graceful degradation**: Timeout = failed provider, not failed request

## 🎯 Best Practices Implemented

### 1. **Resource Management**
```python
# Always use try/finally for cleanup
try:
    result = await provider.translate_async(request)
finally:
    await provider.close()
```

### 2. **Error Isolation**
```python
# Don't let one provider's error affect others
async def safe_translate(provider):
    try:
        return await provider.translate_async(request)
    except Exception as e:
        logger.warning(f"Provider {provider.provider_name} failed: {e}")
        return None
```

### 3. **Concurrent Execution**
```python
# Use asyncio.gather() for concurrent execution
results = await asyncio.gather(*tasks, return_exceptions=True)
```

### 4. **Session Reuse**
```python
# Reuse HTTP sessions for better performance
if self._session is None or self._session.closed:
    self._session = aiohttp.ClientSession()
```

## 🔮 Advanced Async Patterns

### Rate Limiting
```python
import asyncio

class RateLimiter:
    def __init__(self, max_requests_per_second):
        self.semaphore = asyncio.Semaphore(max_requests_per_second)
        
    async def acquire(self):
        await self.semaphore.acquire()
        # Release after 1 second
        asyncio.create_task(self._release_after_delay())
    
    async def _release_after_delay(self):
        await asyncio.sleep(1)
        self.semaphore.release()
```

### Batch Processing
```python
async def translate_batch(texts, target_language, batch_size=5):
    results = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        # Process batch concurrently
        tasks = [
            deka.translate_async(text, target_language)
            for text in batch
        ]
        
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
        
        # Small delay between batches to respect rate limits
        if i + batch_size < len(texts):
            await asyncio.sleep(0.1)
    
    return results
```

This async implementation makes Deka **incredibly fast** for multi-provider comparisons and batch operations - a huge competitive advantage!
