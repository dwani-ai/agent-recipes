OpenClaw

git clone --depth 1 https://github.com/openclaw/openclaw.git
cd openclaw
chmod +x docker-setup.sh
./docker-setup.sh


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

