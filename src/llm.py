"""LLM-generated, user-facing recommendation blurb.

Uses an Anthropic model when LLM_API_KEY is set, otherwise composes a clear template
summary so the feature works offline. This is the project's 'how LLMs were used'
element on the recommendation side (ideation/explanation, not the numeric scoring).
"""
from __future__ import annotations
import pandas as pd

from .config import SETTINGS


def recommend_blurb(ranked: pd.DataFrame, top_n: int = 3) -> str:
    """Return a short natural-language recommendation for the top destinations."""
    top = ranked.head(top_n)
    facts = "\n".join(
        f"- {r.city}, {r.country}: score {r.adventure_score:.0f}, {int(r.night_clubs)} clubs, "
        f"~{r.temp_max:.0f}C, ~£{int(r.total_cost)} total" for r in top.itertuples()
    )
    if SETTINGS.has_llm:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=SETTINGS.llm_api_key)
            prompt = ("You are a friendly travel adviser. In 3-4 sentences, recommend the best "
                      "adventurous tropical destination for someone who loves nightlife, using these "
                      f"options:\n{facts}\nBe specific and upbeat.")
            msg = client.messages.create(model=SETTINGS.llm_model, max_tokens=220,
                                          messages=[{"role": "user", "content": prompt}])
            return msg.content[0].text.strip()
        except Exception:
            pass
    best = top.iloc[0]
    return (f"Top pick: {best.city}, {best.country}. With around {int(best.night_clubs)} clubs and "
            f"{int(best.bars)} bars nearby, warm {best.temp_max:.0f}°C weather and a competitive "
            f"~£{int(best.total_cost)} total trip cost, it offers the best balance of nightlife, "
            f"climate and value among the options. {top.iloc[1].city} and {top.iloc[2].city} are "
            f"strong runners-up if you want alternatives.")
