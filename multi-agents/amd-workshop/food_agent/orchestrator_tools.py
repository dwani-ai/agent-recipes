"""Tools used by the orchestrator agent (OpenFoodFacts + optional EXA MCP).

This is a notebook-free version of the tooling code so it can be imported
from normal Python modules and used with `adk web`.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List

import openfoodfacts

try:
    from google.adk.tools.mcp_tool import McpToolset
    from google.adk.tools.mcp_tool.mcp_session_manager import (
        StdioConnectionParams,
        StreamableHTTPConnectionParams,
    )
    from mcp import StdioServerParameters

    _HAS_MCP = True
except ImportError:  # Optional dependency
    McpToolset = None  # type: ignore
    StdioConnectionParams = None  # type: ignore
    StreamableHTTPConnectionParams = None  # type: ignore
    StdioServerParameters = None  # type: ignore
    _HAS_MCP = False


# ── OpenFoodFacts tools ────────────────────────────────────────────────────────

api = openfoodfacts.API(
    user_agent="IngredientOrchestrator/1.0 (you@example.com)", timeout=30
)


def off_by_barcode_fn(ean_13: str) -> Dict[str, Any]:
    """OpenFoodFacts API: lookup by EAN‑13 barcode."""
    try:
        # code,product_name,brands,ingredients_text,last_modified_t,countries_tags
        return api.product.get(
            ean_13,
            fields=[
                "code",
                "product_name",
                "brands",
                "ingredients_text",
                "last_modified_t",
                "countries_tags",
            ],
        ) or {"status": "not_found"}
    except Exception as e:  # pragma: no cover - best-effort logging
        return {"status": "error", "error": str(e)}


def off_search_by_name_fn(
    query: str, limit: int = 10, retries: int = 3
) -> List[Dict[str, Any]]:
    """OpenFoodFacts API: search by product name."""
    try:
        return (
            api.product.text_search(query, page_size=limit)
            or [{"status": "not_found"}]
        )
    except Exception as e:  # pragma: no cover - best-effort logging
        return [{"status": "error", "error": str(e)}]


# ── Optional EXA MCP tools (loaded lazily) ────────────────────────────────────

EXA_API_KEY = os.environ.get("EXA_API_KEY")


async def load_exa_tools_stdio() -> List[Any]:
    """Load EXA MCP tools using stdio connection.

    Returns an empty list if EXA is not configured or MCP is unavailable.
    """
    if not (_HAS_MCP and EXA_API_KEY):
        return []

    exa_provider = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "mcp-remote",
                    f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}",
                ],
                env={"EXA_API_KEY": EXA_API_KEY},
            ),
            timeout=20,
        )
    )

    tools = await exa_provider.get_tools()
    return list(tools or [])


async def load_exa_tools_http() -> List[Any]:
    """Alternative HTTP-based EXA MCP loader (not used by default)."""
    if not (_HAS_MCP and EXA_API_KEY):
        return []

    exa_provider = McpToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}&tools=web_search_exa",
            timeout=20,
        )
    )
    tools = await exa_provider.get_tools()
    return list(tools or [])


__all__ = [
    "off_by_barcode_fn",
    "off_search_by_name_fn",
    "load_exa_tools_stdio",
    "load_exa_tools_http",
]

