# Multi-Agent System with Google ADK

This directory contains examples and runnable agents built with [Google's Agent Development Kit (ADK)](https://github.com/GoogleCloudPlatform/devrel-demos), using LiteLLM for model inference (e.g. local or custom endpoints).

## Prerequisites

- **Python 3.10**
- An AI inference endpoint (local or remote) compatible with LiteLLM

## Setup

1. **Create and activate a virtual environment:**

   ```bash
   python3.10 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** — create a `.env` file in this directory (or in each agent subdirectory as needed) with your model settings:

   ```env
   LITELLM_MODEL_NAME="openai/gemma3"
   LITELLM_API_BASE="https://qwen-api"
   LITELLM_API_KEY="sk-dummy"
   ```

   Adjust `LITELLM_MODEL_NAME`, `LITELLM_API_BASE`, and `LITELLM_API_KEY` for your inference server.

## Verify AI inference

From this directory (with `venv` activated):

```bash
adk run test_api
```

This runs the `test_api` agent and confirms that the ADK can reach your model via LiteLLM.

## Example agents

Each example corresponds to a section in the [Google codelab: Build a multi-agent system with ADK](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/3-developing-agents/build-a-multi-agent-system-with-adk#0).

| Example | Command | Codelab section |
|--------|--------|------------------|
| **Travel planner (sub-agents)** | `adk run travel-planner-sub-agents` | [§6 – Sub-agents](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/3-developing-agents/build-a-multi-agent-system-with-adk#6) |
| **Sequence agents** | `adk run sequence_agents` | [§9 – Sequence](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/3-developing-agents/build-a-multi-agent-system-with-adk#9) |
| **Loop agent** | `adk run loop-agent` | [§10 – Loop](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/3-developing-agents/build-a-multi-agent-system-with-adk#10) |

Run any of the above from this directory after setup.

## Web UI

To use the ADK web interface for running and inspecting agents:

```bash
adk web
```

## Docker (ADK web only)

The stack runs **ADK web** in a container. There is **no LiteLLM proxy** here: agents use the **LiteLLM library** with `LITELLM_*` environment variables, same as local development.

1. Start your OpenAI-compatible model server first. For the Sarvam llama.cpp setup in this repo, use [coding_agents/llm_api/llama-cpp-sarvam.yml](../../coding_agents/llm_api/llama-cpp-sarvam.yml) (`--alias gemma3`, published on host port **80**).
2. Copy [.env.example](.env.example) to `.env` with `LITELLM_MODEL_NAME`, `LITELLM_API_BASE`, and `LITELLM_API_KEY`. [docker-compose.yml](docker-compose.yml) passes only those three variables into `adk-web` (no separate LiteLLM config file).
3. From this directory:

   ```bash
   docker compose up --build
   ```

4. Open [http://localhost:8000](http://localhost:8000).

`docker-compose.yml` sets `host.docker.internal` → host gateway so the container can call `http://host.docker.internal:80/v1` on Linux when you set that in `.env`. If the llama server runs in another Docker network, point `LITELLM_API_BASE` at that service URL instead.

**Note:** The ADK loader lists every subdirectory under this folder; `database-tools` is documentation-only and may error if selected in the UI.

### Integrated: llama.cpp + ADK web

[docker-compose.integrated.yml](docker-compose.integrated.yml) runs **llama-server** (same image, model, and GPU settings as [llama-cpp-sarvam.yml](../../coding_agents/llm_api/llama-cpp-sarvam.yml)) and **adk-web** on one Compose network. In `.env`, set **`LITELLM_API_BASE=http://llama-server:8080/v1`** (plus `LITELLM_MODEL_NAME` and `LITELLM_API_KEY`); compose passes those three variables into `adk-web` only.

1. Ensure GGUF shards exist under `coding_agents/llm_api/models/` (same layout as the standalone Sarvam compose).
2. Copy [.env.example](.env.example) to `.env` and set the three `LITELLM_*` values (see example comments for integrated vs host llama).
3. From **this directory**:

   ```bash
   docker compose -f docker-compose.integrated.yml up --build
   ```

4. ADK web: [http://localhost:8000](http://localhost:8000). Llama HTTP API (host): [http://localhost:80](http://localhost:80) (same as the standalone Sarvam stack).

## References

- **Codelab:** [Production-ready AI with Google Cloud – Build a multi-agent system with ADK](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/3-developing-agents/build-a-multi-agent-system-with-adk#0)
- **Source repo (Google DevRel demos):**

  ```bash
  git clone --depth 1 https://github.com/GoogleCloudPlatform/devrel-demos.git devrel-demos-multiagent-lab
  ```
