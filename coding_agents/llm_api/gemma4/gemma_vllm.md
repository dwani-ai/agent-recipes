Gemma4 with vllm

curl -LsSf https://astral.sh/uv/install.sh | sh


uv venv
source .venv/bin/activate
UV_HTTP_TIMEOUT=300 uv pip install -U vllm[audio] --pre \
  --extra-index-url https://wheels.vllm.ai/nightly/cu130 \
  --extra-index-url https://download.pytorch.org/whl/cu130 \
  --index-strategy unsafe-best-match --extra-index-url https://pypi.nvidia.com

uv pip install transformers==5.5.0


vllm serve google/gemma-4-E2B-it \
  --max-model-len 8192 \
  --limit-mm-per-prompt image=4,audio=1


vllm serve google/gemma-4-E2B-it  \
  --served-model-name gemma4  \
  --host 0.0.0.0  \
  --port 8000  \
  --gpu-memory-utilization 0.90  \
  --tensor-parallel-size 1  \
  --max-model-len 8192 \ 
  --max-num-seqs 16 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --generation-config auto \
  --enforce-eager \
  --chat-template-content-format openai \
  --trust-remote-code  \
  --mm-encoder-tp-mode data \       
  --limit-mm-per-prompt image=2,video=1,audio=1 \
  --reasoning-parser gemma4 \
  --enable-auto-tool-choice \
  --tool-call-parser gemma4


- Verification

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemma-4-E2B-it",
    "messages": [
      {"role": "user", "content": "Explain quantum entanglement in simple terms."}
    ],
    "max_tokens": 512,
    "temperature": 0.7
  }'

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemma-4-E2B-it",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "audio_url", "audio_url": {"url": "https://github.com/dwani-ai/dwani-python-sdk/raw/refs/heads/main/examples/sample_data/kannada_sample.wav"}},
          {"type": "text", "text": "Transcribe this audio."}
        ]
      }
    ],
    "max_tokens": 512
  }'

curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemma-4-E2B-it",
    "messages": [
      {"role": "user", "content": "What is the derivative of x^3 * ln(x)?"}
    ],
    "max_tokens": 4096,
    "chat_template_kwargs": {"enable_thinking": true}
  }'