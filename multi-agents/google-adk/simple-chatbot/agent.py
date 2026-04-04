import os

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

# Same LiteLLM wiring as test_api — uses LITELLM_* from the environment.
model = LiteLlm(
    model=os.getenv("LITELLM_MODEL_NAME"),
    api_base=os.getenv("LITELLM_API_BASE"),
    api_key=os.getenv("LITELLM_API_KEY"),
)

root_agent = Agent(
    model=model,
    name="root_agent",
    description="A simple conversational chatbot with no tools.",
    instruction=(
        "You are a helpful, friendly assistant. Have natural conversations, "
        "answer questions clearly, and admit when you do not know something."
    ),
)
