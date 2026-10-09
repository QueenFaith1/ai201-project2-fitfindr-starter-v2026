# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings data for items matching keywords in a description, optionally filtered by size and a maximum price.
- **Inputs:** description (str, required), size (str, optional), max_price (float, optional)
- **Returns:** A list of listing dicts, best match first. Each dict has: id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform
- **When it has nothing:** Returns an empty list [] — never None, never an exception.

### `suggest_outfit`

- **What it does:** Given a thrifted item and the user's wardrobe, suggest one or two outfits.
- **Inputs:** new_item(dict, required),  wardrobe(dict, required)
- **Returns:** A non-empty string containing outfit suggestions.
- **When it has nothing:** With an empty wardrobe, returns general styling advice rather than raising an error or returning an empty string

### `create_fit_card`

- **What it does:** Writes a short caption someone would actually post about the find.
- **Inputs:** outfit (str, required), new_item (dict, required)
- **Returns:** A two-to-four sentence caption that reads like a real social post, mentioning the item, its price, and platform once each, and specific about the vibe.
- **When it has nothing:** if outfit is empty or whitespace, return a descriptive message instead of raising an error

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in the session and stop. Otherwise, take the first result and continue to suggest_outfit

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
 Regex / simple string splitting — looking for a `$` followed by digits to pull out `max_price`, and a "size X" pattern to pull out `size`; whatever text remains becomes the `description`. Chosen over asking the model because it's free, instant, and predictable, and the test queries follow a regular enough format for it to work reliably.

**What moves through the session:** <!-- which fields, in what order -->
query` (the raw user input) → `parsed` (description/size/max_price extracted from it) → `search_results` (everything `search_listings` returned) → `selected_item` (the one chosen to move forward) → `wardrobe` (passed in at the start) → `outfit_suggestion` (from `suggest_outfit`) → `fit_card` (from `create_fit_card`) → `error` (set if the run stopped early). 

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->
     ## Sample Run

**One full query**

```
$ python app.py ask "vintage graphic tee under $30"

  The planning loop isn't built yet — see the TODO in agent.py.

0 model calls this session
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'price': 24.0, 'platform': 'depop', ...}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'price': 18.0, 'platform': 'depop', ...}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'price': 26.0, 'platform': 'depop', ...}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'price': 19.0, 'platform': 'depop', ...}]
```
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two specific outfit suggestions incorporating the Vintage Levi's 501 Jeans into their existing wardrobe:

### Outfit 1: Casual & Classic
* Top: White ribbed tank top
* Outerwear: Vintage black denim jacket
* Bottoms: Vintage Levi's 501 Jeans (Medium Wash)
* Shoes: Chunky white sneakers
* Accessories: Black crossbody bag
[... full output ...]

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Still not over scoring these vintage Levi's 501 jeans on depop for just $38.0! They have that perfectly worn-in medium wash and the exact relaxed 90s vibe I've been hunting for. Honestly, I'm just living in these with my favorite white sneakers all spring.

```

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

Moment 1: Query Parsing Strategy, 
 *What I asked for* Should I parse the user's query with regex to extract price and size, or pass the whole thing to Claude and ask it to extract the fields? 
 *What came back:* Claude suggested regex would be faster and more predictable since the format is consistent ($30, size M, etc.), and I wouldn't want to burn a model call on something deterministic.
*What I changed* I went with simple regex splitting instead of LLM based parsing  saves time and tokens, works reliably for the expected input format.

Moment 2: Acceptance Criteria, the state criterion* 
*What I asked for:* I asked Claude to help me understand what "something about state" meant for criterion 3, since I didn't understand what I was being asked to check.  
*What came back:* Claude explained it as checking whether the item `search_listings` finds is the exact same item that reaches `suggest_outfit` comparing the `id` in `session["selected_item"]` against what the fit card actually references. 
 *What I changed:* I wrote the criterion as "for 5 matching queries, the id of session['selected_item'] matches the id referenced in the fit card 5 of 5 tries," and set the target to 5/5 since it's my own code passing a value, not something modeldriven that could vary.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

## Loop Trace

**Happy path**

```
$ python app.py ask "vintage graphic tee under $30" --trace

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Y2K Baby Tee — Butterfly Print, Vintage Graphic Hoodie — Faded Black … +7 more
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
      in:  dict with keys: item
      out: Here are two specific outfit combinations using the Graphic Tee...
[5] create_fit_card
      out: Still pinching myself over finding this sick 2003 tour bootleg tee...
```

**Empty search**

```
$ python app.py ask "designer ballgown size XXS under $5" --trace

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] branch
      →    empty results, stopping before suggest_outfit

      **On the MCP move:** "search_listings"  was moved onto an MCP server ("mcp_server.py"), registered with a typed schema and a description written for a caller who can't see the implementation. "run_agent()" now calls it through "mcp_client.call_tool("search_listings", {...})" instead of importing and calling the function directly. The results coming back are identical in shape to the direct call version. same listing dicts, same fields confirming the swap didn't change behavior, only how the call is routed.


## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
