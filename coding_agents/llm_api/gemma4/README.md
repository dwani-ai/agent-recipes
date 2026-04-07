docker build -t vllm-gemma4-audio . 

docker run --gpus all \
    -v ~/.cache/huggingface:/root/.cache/huggingface \
    -p 8000:8000 \
    --ipc=host \
    vllm-gemma4-audio \
    --model google/gemma-4-E4B-it \
    --trust-remote-code \
    --max-model-len 32768 \
    --chat-template examples/template_gemma_4_audio.jinja