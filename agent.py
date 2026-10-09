"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────


def run_agent(query: str, wardrobe: dict) -> dict:
    from trace import step, start_trace

    start_trace()
    print(">>> TRACE TEST: inside run_agent, about to call step()")
    session = new_session(query, wardrobe)

    # Parse the query: pull out max_price and size, rest becomes description
    import re

    price_match = re.search(r"\$(\d+(?:\.\d+)?)", query)
    max_price = float(price_match.group(1)) if price_match else None

    size_match = re.search(r"\bsize\s+(\w+)\b", query, re.IGNORECASE)
    size = size_match.group(1) if size_match else None

    description = query
    if price_match:
        description = description.replace(price_match.group(0), "")
    if size_match:
        description = description.replace(size_match.group(0), "")
    description = description.replace("under", "").strip()

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }
    step("parse_query", inputs={"query": query}, returned=session["parsed"])

    # Step 1: search
    from mcp_client import call_tool

    results = call_tool("search_listings", {
        "description": description,
        "size": size,
        "max_price": max_price,
    })

    session["search_results"] = results
    step("search_listings (via MCP)", inputs=session["parsed"], returned=results)

    # THE BRANCH
    if not results:
        session["error"] = (
            f"No listings matched '{description}'"
            f"{f' under ${max_price}' if max_price else ''}"
            f"{f' in size {size}' if size else ''}. "
            f"Try a higher price, a different size, or fewer/different "
            f"keywords in your description."
        )
        step("branch", note="empty results, stopping before suggest_outfit")
        return session

    # Step 2: pick the top match
    session["selected_item"] = results[0]
    step("select_item", returned=session["selected_item"])

    # Step 3: suggest an outfit
    try:
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"], wardrobe
        )
        step("suggest_outfit", inputs={"item": session["selected_item"]["title"]},
             returned=session["outfit_suggestion"])
    except ModelUnavailable as exc:
        session["error"] = (
            f"Couldn't reach the model to suggest an outfit: {exc} "
            f"Try again in a moment, or check your API key."
        )
        step("suggest_outfit", note=f"ModelUnavailable: {exc}")
        return session

    # Step 4: write the caption
    try:
        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"], session["selected_item"]
        )
        step("create_fit_card", returned=session["fit_card"])
    except ModelUnavailable as exc:
        session["error"] = (
            f"Couldn't reach the model to write the caption: {exc} "
            f"Try again in a moment, or check your API key."
        )
        step("create_fit_card", note=f"ModelUnavailable: {exc}")
        return session

    return session
   

# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
