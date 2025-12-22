# AI Service Optimization for M1 Pro Apple Silicon

## Performance Optimizations Applied

### 1. Metal GPU Acceleration
- **Before**: `n_gpu_layers=0` (CPU only) - 8 minutes per query
- **After**: `n_gpu_layers=-1` (all layers on Metal GPU) - Expected: 2-5 seconds per query
- Automatically detects Apple Silicon and uses Metal backend

### 2. Model Loading Optimization
- **Singleton Pattern**: Model loaded only once, reused across all requests
- **Lazy Loading**: Model initialized on first use
- **Memory Mapping**: `use_mmap=True` for faster model loading
- **Memory Locking**: `use_mlock=True` prevents swapping to disk

### 3. Inference Speed Optimizations
- **Context Window**: Reduced from 2048 to 1024 tokens (faster processing)
- **Max Tokens**: Reduced from 512 to 256 (faster generation)
- **Threading**: Optimized to 6 threads for M1 Pro (better GPU utilization)
- **Batch Size**: Increased to 512 for better GPU throughput
- **Stop Tokens**: Added to terminate generation early when possible

### 4. Response Caching
- **LRU Cache**: Caches up to 32 similar queries
- **Hash-based Caching**: Similar spending patterns and KYC checks are cached
- **Faster Repeated Queries**: Cached responses return instantly

### 5. Prompt Optimization
- **Shorter Prompts**: Reduced prompt length for faster processing
- **Context Truncation**: Long context data truncated to 500 chars
- **Response Length Limits**: AI instructed to keep responses concise (80-150 words)

### 6. Database Query Optimization
- **Reduced Transaction Limit**: From 30 to 10 recent transactions
- **Description Truncation**: Transaction descriptions limited to 30 chars

## Installation Requirements

### For Metal GPU Support (M1 Pro):

```bash
# Uninstall existing llama-cpp-python
pip uninstall llama-cpp-python

# Install with Metal support
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --no-cache-dir
```

### Verify Metal Support:
```python
from llama_cpp import Llama
llm = Llama(model_path="models/mistral-7b-instruct-v0.2.Q4_K_M.gguf", n_gpu_layers=-1)
# Should print Metal device info if working
```

## Expected Performance

- **First Query**: 3-5 seconds (model loading + inference)
- **Subsequent Queries**: 2-4 seconds (inference only)
- **Cached Queries**: < 0.1 seconds (instant return)

## Configuration Tuning

If you need to adjust performance further, modify these parameters in `ai_service.py`:

```python
n_gpu_layers=-1,    # -1 = all layers, or specific number (35+ for 7B model)
n_ctx=1024,         # Context window (512-2048, lower = faster)
n_threads=6,        # CPU threads (4-8 for M1 Pro)
n_batch=512,        # Batch size (256-1024, higher = better GPU utilization)
max_tokens=256,     # Max response length (128-512, lower = faster)
```

## Troubleshooting

### If Metal GPU doesn't work:
1. Check if llama-cpp-python was installed with Metal support
2. Verify with: `python -c "from llama_cpp import Llama; print('Metal support available')"`
3. Falls back to optimized CPU mode automatically

### If still slow:
1. Reduce `n_ctx` to 512
2. Reduce `max_tokens` to 128
3. Check system memory (ensure enough RAM available)
4. Verify model file exists and is accessible

## Performance Monitoring

The code automatically detects Apple Silicon and prints:
- `✓ Using Metal GPU acceleration (Apple Silicon)` - GPU mode active
- `✓ Using CPU mode (optimized)` - CPU fallback active


