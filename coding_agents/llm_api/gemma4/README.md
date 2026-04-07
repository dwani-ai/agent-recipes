docker build -t vllm-gemma4-audio . 

docker compose -f vllm-gemma-4-audio.yml up -d

# Use the latest CUDA 13.0 base (ensure your host driver supports this!)
FROM nvidia/cuda:13.0.0-devel-ubuntu24.04

# Set system environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    UV_HTTP_TIMEOUT=300 \
    HF_HOME=/root/.cache/huggingface \
    PATH="/root/.cargo/bin:$PATH"

# 1. Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.12 python3-pip curl git ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# 2. Install 'uv' directly from the official script
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create a workspace and virtual environment
WORKDIR /app
RUN uv venv /app/.venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# 4. Install vLLM [audio] nightlies and Transformers 5.5.0
# Using the specific nightly index you provided
RUN uv pip install -U vllm[audio] --pre \
    --extra-index-url https://wheels.vllm.ai/nightly/cu130 \
    --extra-index-url https://download.pytorch.org/whl/cu130 \
    --extra-index-url https://pypi.nvidia.com \
    --index-strategy unsafe-best-match

RUN uv pip install transformers==5.5.0

# 5. Expose ports
EXPOSE 8000

# 6. Default Entrypoint (OpenAI API Server)
# We use 'uv run' or path to venv to ensure we use the correct environment
ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]

# 7. Optimized Gemma 4 Launch Arguments
CMD [ \
    "--model", "google/gemma-4-E2B-it", \
    "--served-model-name", "gemma4", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--gpu-memory-utilization", "0.90", \
    "--tensor-parallel-size", "1", \
    "--max-model-len", "8192", \
    "--max-num-seqs", "16", \
    "--enable-chunked-prefill", \
    "--enable-prefix-caching", \
    "--enforce-eager", \
    "--chat-template-content-format", "openai", \
    "--trust-remote-code", \
    "--mm-encoder-tp-mode", "data", \
    "--limit-mm-per-prompt", "image=2,video=1,audio=1", \
    "--reasoning-parser", "gemma4", \
    "--tool-call-parser", "gemma4" \
]