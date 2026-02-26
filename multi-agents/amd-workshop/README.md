AMD - Workshop

```bash
docker run --rm \
    --group-add=video \
    --cap-add=SYS_PTRACE \
    --security-opt seccomp=unconfined \
    --device /dev/kfd \
    --device /dev/dri \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    --env "HF_TOKEN=$HF_TOKEN" \
    -p 8000:8000 \
    --ipc=host \
    vllm/vllm-openai-rocm:v0.16.0 \
    --model Qwen/Qwen3-0.6B
```

### Orchestrator (`Qwen/Qwen3-VL-30B-A3B-Instruct-FP8`) on port **9001**


VLLM_USE_TRITON_FLASH_ATTN=0 \
vllm serve Qwen/Qwen3-VL-30B-A3B-Instruct-FP8 \
  --port 9001 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes \
  --trust-remote-code \
  --gpu-memory_utilization 0.45

### Consultant (`Qwen/Qwen3-30B-A3B-Instruct-2507-FP8`) on port **9000**


VLLM_ATTENTION_BACKEND=TORCH_SDPA \
VLLM_USE_TRITON_FLASH_ATTN=0 \
vllm serve Qwen/Qwen3-30B-A3B-Instruct-2507-FP8 \
  --port 9000 \
  --enable-auto-tool-choice \
  --tool-call-parser hermes \
  --trust-remote-code \
  --gpu-memory_utilization 0.45



  