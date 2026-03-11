RAG + Embeds

- https://ai.google.dev/gemma/docs/get_started

- EmbeddedGemma
    - https://ai.google.dev/gemma/docs/embeddinggemma 

    - https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers

    - Prompt Instructions - 
        - https://ai.google.dev/gemma/docs/embeddinggemma/model_card#prompt_instructions

- Install and Run 

```bash
pip install -U sentence-transformers git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview accelerate datasets
```

```
python embedded-gemma-example.py
```

- Gemma RAG -example
    - https://github.com/google-gemini/gemma-cookbook/blob/main/Gemma/%5BGemma_3%5DRAG_with_EmbeddingGemma.ipynb
Models for RAG
    - Medium google/gemma-3-1b-it
    - Fast with Low Accuracy - google/gemma-3-270m-it
    - Slow with  High Accuracy -  google/gemma-3-4b-it