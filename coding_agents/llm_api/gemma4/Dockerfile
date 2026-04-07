# Use NVIDIA CUDA 12.9 base for Ubuntu 24.04
FROM nvidia/cuda:12.9.1-cudnn-devel-ubuntu24.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    # Bypasses the "externally-managed-environment" error (PEP 668)
    PIP_BREAK_SYSTEM_PACKAGES=1 \
    HF_HOME=/root/.cache/huggingface

# Install system dependencies for audio and Python 3.12
RUN apt-get update && apt-get install -y \
    python3.12 \
    python3-pip \
    python3-venv \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Ensure we are using Python 3.12 as the default 'python'
RUN ln -s /usr/bin/python3.12 /usr/bin/python

# Update build tools
RUN pip install --upgrade pip setuptools wheel

# Install PyTorch with CUDA 12.9 support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu129

# Install Transformers 5.50.0 and vLLM with audio extensions
# Note: Gemma 4 requires these specific versions for native audio support
RUN pip install --no-cache-dir \
    transformers==5.50.0 \
    "vllm[audio]>=0.19.0" \
    accelerate \
    sentencepiece

# Create workspace
WORKDIR /app

# Expose the port for the OpenAI-compatible API
EXPOSE 8000

# Default command to run Gemma 4 E4B (Audio-capable version)
# Adjust the --model flag if using a different variant
ENTRYPOINT ["python", "-m", "vllm.entrypoints.openai.api_server"]

#CMD ["--model", "google/gemma-4-E4B-it", "--trust-remote-code", "--max-model-len", "32768"]