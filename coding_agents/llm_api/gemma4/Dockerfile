# Use a modern CUDA-enabled base
FROM nvidia/cuda:12.9.1-cudnn-devel-ubuntu24.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/root/.cache/huggingface

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    python3.12 python3-pip git ffmpeg libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Update pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Install Transformers 5.50.0 and vLLM with Audio support
# Note: Gemma 4 support is currently in the vLLM 'gemma4' branch or latest nightlies
RUN pip install --no-cache-dir \
    transformers==5.50.0 \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129 \
    "vllm[audio]>=0.19.0" \
    accelerate \
    sentencepiece

# Expose the OpenAI-compatible server port
EXPOSE 8000

# Set the entrypoint to launch the vLLM server
ENTRYPOINT ["python3", "-m", "vllm.entrypoints.openai.api_server"]