"""Orchestrator agents for the multi-agent nutrition app.

This module defines:
* a basic ingredient-orchestrator agent, and
* the final `root_agent` that wraps the nutritionist agent as a tool and
  uses OpenFoodFacts (and optionally EXA MCP) for ingredient lookup.

These definitions are split out from the original notebook so they can be
used directly with `adk web`.
"""

from __future__ import annotations

from typing import List, Any

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.agent_tool import AgentTool

from consultant_agent import nutritionist_agent
from orchestrator_tools import (
    off_by_barcode_fn,
    off_search_by_name_fn,
    load_exa_tools_stdio,
)


# ── Phase 1 orchestrator (no tools, text-only) ────────────────────────────────

ORCHESTRATOR_INSTRUCTION_PHASE1 = """
You are an Ingredient Orchestrator.

Goal:
When the user names a packaged snack, a dish, or provides a picture,
return ONLY a cleaned ingredient list (bullets or comma-separated)
along with the product name. If ambiguous, state one brief assumption.

Keep response ≤ 5 lines. Educational only; not medical advice.
"""

orchestrator_agent_phase1 = Agent(
    model=LiteLlm(
        model="hosted_vllm/Qwen/Qwen3-VL-30B-A3B-Instruct-FP8",
        base_url="http://localhost:9001/v1",
    ),
    name="orchestrator_agent_phase1",
    instruction=ORCHESTRATOR_INSTRUCTION_PHASE1,
)


# ── Final root orchestrator (OFF + EXA + nutritionist_agent) ─────────────────

ROOT_ORCHESTRATOR_INSTRUCTION = """
You are an Ingredient Orchestrator with tool access.

Objective:
Derive an ingredient list (from OFF or EXA) or from an explicit
user‑provided list, then call `nutritionist_agent` with BOTH
ingredients (list) and product_name, and finally return the final
verdict and summary.

Data tools (priority):
1) off_by_barcode_fn(ean_13) - FIRST if a 13‑digit barcode is present.
2) off_search_by_name_fn(name) - If no barcode or lookup failed.
3) web_search_exa(query) - FALLBACK ONLY if OFF fails/ambiguous or if
   user explicitly asks for freshest data.

RULES:
- NEVER fabricate ingredients from memory.
- NEVER output an ingredients list unless it came from tools or the user.
- If all tools fail, ask the user to paste the ingredients.
- ALWAYS use nutritionist_agent when you have the ingredients.
- NEVER suggest your own alternative, always rely on the response from
  nutritionist_agent.
- NEVER repeat the exact same search query. If 'Product X ingredients'
  fails, pivot to 'Manufacturer site Product X' or 'Product X nutrition
  label'.
- After 2 unsuccessful searches, STOP and report exactly what you found
  to the user. Do not loop.
- When using EXA, always use text mode, limit 2000 chars, and at most
  3 results.

Goal:
Find the ingredient list and source link. Keep answers ≤ 6 lines.

Extraction rules:
- OFF: prefer ingredients fields; preserve order; trim/dedupe.
- Web: manufacturer > major retailer > reputable database.
  Ignore marketing blurbs and storage instructions.

Consultant call:
- After ingredients are ready, call nutritionist_agent with
  product_name and ingredients.
- Do NOT call until ingredients are confirmed.

Ambiguity:
- If OFF returns multiple variants (country/flavor), ask ONE concise
  clarifying question.

Final user answer format (≤ 6 lines):
1) Verdict: OK / Caution / Avoid / Uncertain
2–4) 1–3 short reasons
5) Healthier alternative (if available)
6) Educational only; not medical advice.
"""


async def build_root_agent(include_exa: bool = True) -> Agent:
    """Build the final root orchestrator agent.

    By default this tries to load EXA MCP tools if configured; set
    ``include_exa=False`` to rely only on OpenFoodFacts.
    """
    tools: List[Any] = [off_by_barcode_fn, off_search_by_name_fn]
    if include_exa:
        exa_tools = await load_exa_tools_stdio()
        tools.extend(exa_tools)

    wrapped_nutritionist = AgentTool(agent=nutritionist_agent)
    tools.insert(0, wrapped_nutritionist)

    root_agent = Agent(
        name="RootOrchestrator",
        model=LiteLlm(
            model="hosted_vllm/Qwen/Qwen3-VL-30B-A3B-Instruct-FP8",
            base_url="http://localhost:9001/v1",
        ),
        instruction=ROOT_ORCHESTRATOR_INSTRUCTION,
        tools=tools,
    )
    return root_agent


__all__ = [
    "orchestrator_agent_phase1",
    "build_root_agent",
]

