Database Tools for Agents


echo "DB_PASSWORD=techjobs-pwd-2025" >> .env
source .env

-- Create PostgreSQL instance -  

gcloud sql instances create jobs-instance \
  --database-version=POSTGRES_17 \
  --tier=db-custom-1-3840 \
  --edition=ENTERPRISE \
  --region=$REGION \
  --root-password=$DB_PASSWORD \
  --enable-google-ml-integration \
  --database-flags cloudsql.enable_google_ml_integration=on \
  --quiet &


-- Download and start toolboc

curl -O https://storage.googleapis.com/genai-toolbox/v0.27.0/linux/amd64/toolbox &

--

cd ~/build-agent-adk-toolbox-cloudsql
bash setup_verify_trial_project.sh && source .env


--

- Agentic RAG
    - https://codelabs.developers.google.com/agentic-rag-toolbox-cloudsql#0

- Travel Agent MCP
    - https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk#0

- ADK + MCP 
    - https://cloud.google.com/blog/topics/developers-practitioners/use-google-adk-and-mcp-with-an-external-server

- ADK Integrations
    - https://developers.googleblog.com/en/supercharge-your-ai-agents-adk-integrations-ecosystem/