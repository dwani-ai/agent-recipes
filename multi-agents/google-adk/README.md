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

The loader lists each agent subdirectory **in alphabetical order**. **`0-default-router`** is the default entry app: it sorts first and routes the user to the other example agents (travel, sequence/loop demos, simple chat, loan stub, time tool). You can still pick any other app from the ADK UI.

## Docker (ADK web only)

The stack runs **ADK web** behind **nginx** on **port 80**. The ADK process is **not** published on the host; only nginx listens on `80`. There is **no LiteLLM proxy** here: agents use the **LiteLLM library** with `LITELLM_*` environment variables, same as local development.

1. Start your OpenAI-compatible model server first. For the Sarvam llama.cpp setup in this repo, use [coding_agents/llm_api/llama-cpp-sarvam.yml](../../coding_agents/llm_api/llama-cpp-sarvam.yml) (`--alias gemma3`, published on host port **80**).
2. Copy [.env.example](.env.example) to `.env` and set `LITELLM_MODEL_NAME`, `LITELLM_API_BASE`, `LITELLM_API_KEY`, and **`BASIC_AUTH_PASSWORD`** (plus optional `BASIC_AUTH_USER`). HTTP Basic Auth is enforced by nginx unless you set **`ALLOW_UNAUTHENTICATED_ACCESS=true`** (development only — do not use on a public internet-facing VM).
3. From this directory:

   ```bash
   docker compose up --build
   ```

4. Open `http://localhost` (port **80**). Sign in with the basic-auth user and password from `.env`. The **`0-default-router`** app should appear first in the app list and open as the default session entry point.

**Local development without nginx** (ADK exposed on `8000` only, no basic auth at the proxy):

```bash
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

`docker-compose.yml` sets `host.docker.internal` → host gateway so the container can call `http://host.docker.internal:80/v1` on Linux when you set that in `.env`. If the llama server runs in another Docker network, point `LITELLM_API_BASE` at that service URL instead.

**Note:** The ADK loader lists every subdirectory under this folder; `database-tools` is documentation-only and may error if selected in the UI.

### Securing deployment on a GCP VM (port 80)

- **Access control:** Prefer **HTTPS** in front of this stack (Google Cloud Load Balancer with managed certificates, or Caddy / Certbot on the VM) so credentials and traffic are not sent in cleartext. Port 80 alone is convenient but not encrypted.
- **Firewall:** In [VPC firewall rules](https://cloud.google.com/vpc/docs/firewalls), restrict **tcp:80** (and **tcp:443** if you terminate TLS) to trusted CIDR ranges, [Identity-Aware Proxy](https://cloud.google.com/iap/docs/concepts-overview) TCP forwarding, or a known bastion — avoid `0.0.0.0/0` unless you must and have other controls (Cloud Armor, OAuth proxy, etc.).
- **Secrets:** Store `BASIC_AUTH_PASSWORD` and `LITELLM_API_KEY` in [Secret Manager](https://cloud.google.com/secret-manager) or another secret store; inject at runtime — do not commit real `.env` files.
- **SSH:** Use OS Login or key-based SSH; keep port **22** restricted similarly.
- **Updates:** Keep the VM image, Docker, and base images patched.

### Integrated: llama.cpp + ADK web

[docker-compose.integrated.yml](docker-compose.integrated.yml) runs **llama-server** (same image, model, and GPU settings as [llama-cpp-sarvam.yml](../../coding_agents/llm_api/llama-cpp-sarvam.yml)) and **adk-web** behind **nginx** on one Compose network. In `.env`, set **`LITELLM_API_BASE=http://llama-server:8080/v1`** (plus `LITELLM_MODEL_NAME` and `LITELLM_API_KEY`), and the same **`BASIC_AUTH_*`** (or dev-only **`ALLOW_UNAUTHENTICATED_ACCESS`**) as the main compose file.

1. Ensure GGUF shards exist under `coding_agents/llm_api/models/` (same layout as the standalone Sarvam compose).
2. Copy [.env.example](.env.example) to `.env` and set the three `LITELLM_*` values (see example comments for integrated vs host llama).
3. From **this directory**:

   ```bash
   docker compose -f docker-compose.integrated.yml up --build
   ```

4. ADK web (behind nginx, with the same `BASIC_AUTH_*` / `ALLOW_UNAUTHENTICATED_ACCESS` rules as above): [http://localhost:8081](http://localhost:8081). Llama HTTP API (host): [http://localhost:80](http://localhost:80) (same as the standalone Sarvam stack).

## References

- **Codelab:** [Production-ready AI with Google Cloud – Build a multi-agent system with ADK](https://codelabs.developers.google.com/codelabs/production-ready-ai-with-gc/3-developing-agents/build-a-multi-agent-system-with-adk#0)
- **Source repo (Google DevRel demos):**

  ```bash
  git clone --depth 1 https://github.com/GoogleCloudPlatform/devrel-demos.git devrel-demos-multiagent-lab
  ```
