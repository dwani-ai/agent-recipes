"""Consultant (nutritionist) agent for the multi-agent nutrition app.

This file is extracted from the original Jupyter notebook
`multi_agent_nutrition-adk.ipynb` so it can be used directly with
`adk web` and other Python tooling.
"""

import os
import warnings
from typing import List, Dict, Any

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from tools_nutrition_local import reload_tsv, lookup_by_name_local


# ── Init nutrition TSV ─────────────────────────────────────────────────────────

_TSV_PATH = os.environ.get(
    "OPENNUTRITION_TSV_PATH",
    "./datasets/opennutrition_foods.tsv",
)

reload_tsv(_TSV_PATH)
print(f"Nutrition TSV loaded/reloaded for consultant from: {_TSV_PATH}")


# Ignore noisy warnings from ADK / Pydantic in dev environments
warnings.filterwarnings("ignore", category=UserWarning, module="google*")
warnings.filterwarnings("ignore", message=".*Pydantic serializer warnings.*")
warnings.filterwarnings(
    "ignore", category=RuntimeWarning, message="coroutine '.*' was never awaited"
)


# ── Tool definition ────────────────────────────────────────────────────────────

def local_lookup_by_name(name: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Lookup product by name (uses name + alternate_names).

    Returns a list of candidate products, or a single not_found record.
    """
    res = lookup_by_name_local(name, top_k=top_k)
    return res if res else [{"status": "not_found"}]


# ── Consultant / nutritionist agent ───────────────────────────────────────────

nutritionist_agent = Agent(
    model=LiteLlm(
        model="hosted_vllm/Qwen/Qwen3-30B-A3B-Instruct-2507-FP8",
        base_url="http://localhost:9000/v1",
    ),
    name="nutritionist_agent",
    description="Nutrition consultant that evaluates ingredients and recommends healthier alternatives.",
    instruction="""
You are a **Nutrition Consultant AI**.

### 1. Role
Evaluate food products or ingredient lists for a specific health goal.
Recommend healthier alternatives from your tool `local_lookup_by_name`
that taste similar and fit the same product type.

### 2. Input
You will receive either:
1) a product name, or
2) a list of ingredients,
and a goal in {general_health, low_sodium, low_sugar, high_protein}.

### 3. Process
- If a **product name** is provided, use `local_lookup_by_name` to retrieve
  a record and ingredients; then analyze.
- If only **ingredients** are provided, analyze using domain knowledge,
  infer product type (cookie, soup, rice dish, potato chips, etc.)
  and consider alternatives based on type.
- Find one healthier alternative by calling `local_lookup_by_name` for
  the same type (if the product is soup, suggest a healthier soup).
- Decide overall: ok | caution | avoid | uncertain. Keep reasons concise.

### 4. Rules
- If the alternative item you suggested is NOT found by `local_lookup_by_name`
  then keep trying until you find a healthier alternative that is found
  by this tool.

### 5. Output (JSON only)
You must respond with **only** a single JSON object in this exact shape:
{
  "product": "string | optional",
  "overall": "ok | caution | avoid | uncertain",
  "reasons": ["<=12 words each"],
  "warnings": ["<=12 words each"],
  "alternatives": [{"name": "string", "reason": "<=10 words"}],
  "notes": ["optional tip"],
  "disclaimer": "Educational only; not medical advice."
}
""",
    tools=[local_lookup_by_name],
)


__all__ = [
    "nutritionist_agent",
    "local_lookup_by_name",
]

