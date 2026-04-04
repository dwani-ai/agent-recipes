Gemma4 with vllm

curl -LsSf https://astral.sh/uv/install.sh | sh


uv venv
source .venv/bin/activate
uv pip install -U vllm --pre \
  --extra-index-url https://wheels.vllm.ai/nightly/cu130 \
  --extra-index-url https://download.pytorch.org/whl/cu130 \
  --index-strategy unsafe-best-match
uv pip install transformers==5.5.0

uv pip install "vllm[audio]"

vllm serve google/gemma-4-E2B-it \
  --max-model-len 8192 \
  --limit-mm-per-prompt image=4,audio=1