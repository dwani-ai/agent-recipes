"""Root app wiring for ADK Web.

This module exposes a concrete `root_agent` instance that can be discovered
and used by `adk web`. It builds the full orchestrator agent which:

- Uses OpenFoodFacts tools (barcode + name search)
- Optionally uses EXA MCP tools (when EXA_API_KEY is set)
- Delegates nutrition analysis to the `nutritionist_agent` via AgentTool
"""

import asyncio

from orchestrator_agents import build_root_agent


def _build_root_agent():
    # By default, try to include EXA tools when configured.
    return asyncio.run(build_root_agent(include_exa=True))


# This is the main agent that ADK Web can attach to.
root_agent = _build_root_agent()

__all__ = ["root_agent"]

