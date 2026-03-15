OpenClaw

--
setup AI inference
  - docker compose -f vllm-qwen-3_5.yml up -d

--

git clone https://github.com/openclaw/openclaw.git

git checkout 70d7a0854c54c489eaefd56bb406ad885f2b3ea2
cd openclaw
chmod +x docker-setup.sh
./docker-setup.sh


docker compose run --rm openclaw-cli \
  config set gateway.controlUi.allowedOrigins '["http://localhost:18789","http://127.0.0.1:18789"]' --strict-json

docker compose up -d openclaw-gateway


--

docker compose run --rm openclaw-cli dashboard --no-open


docker exec -it openclaw-openclaw-gateway-1 bash

openclaw devices list

openclaw devices approve <requestId>



openclaw devices approve asds
openclaw devices approve asdasd

----


docker compose run --rm openclaw-cli config set gateway.mode local


docker compose run --rm openclaw-cli devices list --url ws://127.0.0.1:18789


   docker compose run --rm openclaw-cli devices list


---

---

OPENCLAW_SANDBOX=1


nano ~/.openclaw/.env


ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
OPENCLAW_GATEWAY_TOKEN=your-generated-token


--- 
Adding to Whatsapp

nano ~/.openclaw/config.json

Add/update the channels section:

{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "dmPolicy": "pairing",
      "allowFrom": ["+YOUR_PHONE_NUMBER"],
      "groupPolicy": "allowlist",
      "groupAllowFrom": ["+YOUR_PHONE_NUMBER"]
    }
  }
}



docker exec -it openclaw-gateway bash
    - openclaw channels login --channel whatsapp

cd ~/code/openclaw

# Set allowed origins via the CLI container
docker compose run --rm openclaw-cli \
  config set gateway.controlUi.allowedOrigins '["http://127.0.0.1:18789"]' --strict-json

# Then restart the gateway
docker compose up -d openclaw-gateway



docker compose run --rm openclaw-cli \
  config set gateway.controlUi.allowedOrigins '["http://localhost:18789","http://127.0.0.1:18789"]' --strict-json


--

  docker compose run --rm openclaw-cli dashboard --no-open
  docker compose run --rm openclaw-cli devices list

