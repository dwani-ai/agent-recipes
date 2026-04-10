"""Default router: delegates to sibling example agents."""

from __future__ import annotations

import importlib.util
import os
import re
from pathlib import Path

from dotenv import load_dotenv

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

_agents_root = Path(__file__).resolve().parent.parent
load_dotenv(_agents_root / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

MODEL = LiteLlm(
    model=os.getenv("LITELLM_MODEL_NAME"),
    api_base=os.getenv("LITELLM_API_BASE"),
    api_key=os.getenv("LITELLM_API_KEY"),
)

# (folder under agents root, unique sub_agent name, short description)
_SPECIALIST_SPECS: tuple[tuple[str, str, str], ...] = (
    (
        "custom-loan-processing",
        "specialist_loan",
        "Loan/credit demo (mock tools).",
    ),
    (
        "loop-agent",
        "specialist_loop",
        "Film loop agent demo (writers room with loop).",
    ),
    (
        "sequence-agents",
        "specialist_sequence",
        "Film sequence agents demo (linear pipeline).",
    ),
    (
        "simple-chatbot",
        "specialist_chat",
        "General conversational chat with no tools.",
    ),
    (
        "test_api",
        "specialist_time",
        "Mock get_current_time tool / API smoke test.",
    ),
    (
        "travel-planner-sub-agents",
        "specialist_travel",
        "Travel planning, countries, and attractions.",
    ),
)


def _load_sibling_agent_module(app_dir: str):
    path = _agents_root / app_dir / "agent.py"
    if not path.is_file():
        raise FileNotFoundError(
            f"Expected agent at {path} (project layout may have changed)."
        )
    safe = re.sub(r"[^0-9a-zA-Z_]", "_", app_dir)
    module_name = f"adk_router_{safe}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module spec for {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _clone_sub_agent(root: Agent, agent_name: str, description: str) -> Agent:
    return root.model_copy(update={"name": agent_name, "description": description})


def _build_sub_agents() -> list[Agent]:
    out: list[Agent] = []
    for folder, unique_name, desc in _SPECIALIST_SPECS:
        mod = _load_sibling_agent_module(folder)
        if not hasattr(mod, "root_agent"):
            raise AttributeError(
                f"{folder}/agent.py must define root_agent (got {dir(mod)})."
            )
        out.append(_clone_sub_agent(mod.root_agent, unique_name, desc))
    return out


_sub_agents = _build_sub_agents()

_ROUTER_INSTRUCTION = """You are the entry router for this workspace. Do not answer every topic yourself.

Delegate to exactly one specialist sub-agent by name:

- specialist_travel — travel, vacations, countries, attractions, itineraries, trip planning.
- specialist_chat — general conversation, Q&A, or when no specific demo fits.
- specialist_time — current time in a city, clocks, or exercising the mock get_current_time tool.
- specialist_loan — loan / credit demonstration (mock tools).
- specialist_sequence — sequence / film pipeline demo (linear multi-agent flow).
- specialist_loop — loop / writers room / iterative critique film demo.

If the user is unsure what they want, ask one short question or delegate to specialist_chat.
"""

root_agent = Agent(
    model=MODEL,
    name="default_router",
    description=(
        "Routes requests to specialized example agents (travel, demos, chat, tools)."
    ),
    instruction=_ROUTER_INSTRUCTION,
    sub_agents=_sub_agents,
)
