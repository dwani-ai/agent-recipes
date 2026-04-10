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
  --served-model-name gemma4 \
  --host 0.0.0.0 \
  --port 8000 \
  --gpu-memory-utilization 0.90 \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --max-num-seqs 16 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --enforce-eager \
  --chat-template-content-format openai \
  --trust-remote-code \
  --mm-encoder-tp-mode data \
  --limit-mm-per-prompt '{"image":2,"video":1,"audio":1}' \
  --reasoning-parser gemma4 \
  --enable-auto-tool-choice \
  --tool-call-parser gemma4


---


nohup vllm serve google/gemma-4-E2B-it \
  --served-model-name gemma4 \
  --host 0.0.0.0 \
  --port 8000 \
  --gpu-memory-utilization 0.90 \
  --tensor-parallel-size 1 \
  --max-model-len 8192 \
  --max-num-seqs 16 \
  --enable-chunked-prefill \
  --enable-prefix-caching \
  --enforce-eager \
  --chat-template-content-format openai \
  --trust-remote-code \
  --mm-encoder-tp-mode data \
  --limit-mm-per-prompt '{"image":2,"video":1,"audio":1}' \
  --reasoning-parser gemma4 \
  --enable-auto-tool-choice \
  --tool-call-parser gemma4 > vllm_gemma.log 2>&1 &

tail -f vllm_gemma.log

sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000

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
    "model": "gemma4",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "audio_url", 
            "audio_url": {"url": "https://github.com/dwani-ai/dwani-python-sdk/raw/refs/heads/main/examples/sample_data/kannada_sample.wav"}
          },
          {
            "type": "text", 
            "text": "Task: Detect language, transcribe, and solve.\n1. Identify the language.\n2. Transcribe the audio exactly in its native script.\n3. Provide a direct and factual answer to the question asked in the audio using the same language.\n\nFormat the output as follows:\nLanguage: [Name]\nTranscription: [Text]\nResponse: [Answer]"
          }
        ]
      }
    ],
    "temperature": 0.7,
    "max_tokens": 512
  }'


curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma4",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "audio_url", 
            "audio_url": {"url": "https://github.com/dwani-ai/dwani-python-sdk/raw/refs/heads/main/examples/sample_data/kannada_sample.wav"}
          },
          {
            "type": "text", 
            "text": "Instruction: Listen to the audio and provide ONLY the final answer in the native script of the language spoken. Do not transcribe or repeat the question.\n\nExample 1 (Kannada):\nAudio: [ಕರ್ನಾಟಕದ ರಾಜಧಾನಿ ಯಾವುದು?]\nAnswer: ಬೆಂಗಳೂರು\n\nExample 2 (Hindi):\nAudio: [भारत की राजधानी क्या है?]\nAnswer: नई दिल्ली\n\nAudio: [Current Audio]\nAnswer:"
          }
        ]
      }
    ],
    "temperature": 0.0,
    "max_tokens": 50
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