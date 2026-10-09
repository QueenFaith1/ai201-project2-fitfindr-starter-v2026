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

FitFindr takes a plain language thrifting query  like "vintage graphic tee under $30" and searches a mock Depop/Poshmark/thredUp listings dataset for a match. If something matches, it picks the best result, suggests one or two outfits combining it with the user's existing wardrobe, and writes a short social media style caption for the find. If nothing matches, it stops before the later steps and tells the user what to change the price, size, or keywords instead of guessing.

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

 
Moment 3: Diagnosing the trace not printing
*What I asked for:* Why `--trace` kept saying "You haven't added trace.step() calls yet" even after I'd added them to `agent.py`.
*What came back:* Claude had me add a plain `print()` statement directly inside `run_agent()` to confirm the function was actually being reached with my edits, which revealed the file had an old, unsaved/stale version running.
*What I changed:* Once I saved properly and the print confirmed the real code was executing, the trace worked. I also used this same moment to find and remove duplicate dead code left over from an earlier edit, in the same file.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

## Run Log — Before

Produced by `run_eval.py::main`, loop in `agent.py::run_agent`, tools in
`tools.py`. 5 tries per scenario, caching off. Full output in
`results/run_2026-10-09_1010_before.md`.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Full three-tool run returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before tool 2 | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item matches fit card reference | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions price | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Price ceiling respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, produced by `run_eval.py::main` →
`agent.py::run_agent` → `tools.py::create_fit_card`:

```
Query: vintage graphic tee under $30 (example wardrobe)

selected_item: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)

Fit card: Finally found the ultimate Y2K tour bootleg tee on depop for just $24.0. The fade on this thing is unreal and it instantly gives off that effortless, lived-in grunge vibe. Can't wait to style it with baggy denim and an open hoodie!
```


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
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All 5 tries completed every tool call and returned a non-empty fit card. Checked the trace for each try — no early stops, all 5 steps present. |
| 2 | Impossible query stops before suggest_outfit | 5 of 5 | MET (5/5) | All 5 tries stopped after `search_listings` returned empty, with `selected_item` staying None and a specific message naming what to change (price, size, keywords). Verified via the trace's 3-step branch path. |
| 3 | Item in session matches item passed to suggest_outfit | 5 of 5 | MET (5/5) | Checked the `selected_item` field against the fit card text for all 5 tries — same title, same price, same platform referenced every time. |
| 4 | Fit card mentions the item's price | 4 of 5 | MET (5/5)* | Read all 5 fit cards individually — each one named the price exactly once. *See caveat below — this verdict is real but incomplete. |
| 5 | Search results never exceed the price ceiling | 5 of 5 | MET (5/5) | Pulled raw prices directly from `search_listings` output (not the model's summary) — all 10 results across checks stayed at or under $30. |

**Diagnoses**
Nothing missed, all five criteria held at or above their targets across all five tries. Rather than fabricate a failure, here's an honest check on
whether my targets, and my tests of them, were actually rigorous.

**Criterion 4's result is real but weaker evidence than it looks.** My criterion says "for 5 **different items**." My scenario in `scenarios.py`
ran the same item (the $24 Graphic Tee) 5 times, not 5 different ones. The criterion itself was measurable as written. I built a scenario that
tested something narrower: repeatability on one easy, clean input (a round price, no missing fields) rather than reliability across varied items. This isn't a flaw in the criterion I'm correcting, it's a gap in my test coverage, and I'm leaving it as an honest limitation rather than dressing it up as a criterion revision, since the criterion itself didn't need fixing.

**Criteria 1, 2, 3, and 5 held up as genuinely meaningful, not just easy.** Criterion 2's target had real room to fail if my branch logic had a bug, it didn't. Criterion 5's check came from raw tool output, not the model's paraphrase, so there was no room for a price to quietly slip through uncaught. Criterion 3 compares actual IDs/titles across two pipeline stages, which would have caught a real state bug if one existed. I'm confident these four were tested properly, not just set easy.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

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
```

**On the MCP move:** `search_listings` was moved onto an MCP server (`mcp_server.py`), registered with a typed schema and a description written
for a caller who can't see the implementation. `run_agent()` now calls it through `mcp_client.call_tool("search_listings", {...})` instead of
importing and calling the function directly. The results coming back are identical in shape to the direct-call version — same listing dicts, same
fields, confirming the swap didn't change behavior, only how the call is routed.

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:** My diagnosis found that criterion 4's "before" test only ran the same item (the $24 Graphic Tee) 5 times, even though the criterion itself says "for 5 **different items**." I rewrote `scenarios.py` to replace
that one repeated scenario with 5 separate scenarios, each targeting a different real listing: the Graphic Tee ($24, no brand), Vintage Levi's 501
Jeans ($38, brand: Levi's), a cropped Denim Jacket ($42, brand: Wrangler), a Y2K Baby Tee ($18, no brand), and a Knit Cardigan ($35, no brand), a real mix of prices and brand presence, not just repeating one easy input.


**Which failure it was meant to fix:** Not a failure exactly,  my diagnosis flagged that criterion 4's original "MET" result was weaker evidence than it looked, since it only proved the model could repeat itself on one clean item, not that it reliably handles price-mentioning across varied items and data shapes (including items with a missing `brand` field, which the tool's docstring explicitly warns is common).


### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 4. Fit card mentions price — item 1 (Graphic Tee, $24) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions price — item 2 (Levi's 501, $38) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions price — item 3 (Denim Jacket, $42) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions price — item 4 (Y2K Baby Tee, $18) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card mentions price — item 5 (Knit Cardigan, $35) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

All other criteria (1, 2, 3, 5) were re-run in the same `--label after` pass and held at their previous results unaffected, since the only change was to criterion 4's test scenarios, not the agent itself.

**Real output, item 2 (Levi's 501 Jeans), try 1**, produced by `run_eval.py::main` → `agent.py::run_agent` → `tools.py::create_fit_card`:

```
Query: vintage Levi's 501 jeans (example wardrobe)

selected_item: Vintage Levi's 501 Jeans — Medium Wash ($38.0, depop).

Fit card: scored these vintage levi's 501 jeans on depop for $38 and i'm never taking them off. the medium wash gives them the exact relaxed 90s vibe I've been looking for.
```

**Did it help, and how do I know:**  Yes, this wasn't a case of fixing a bug, but of closing a real gap between what my criterion claimed to test and what my scenario actually tested. Across 5 genuinely different items (varied prices, varied brand presence), the fit card mentioned the price correctly 25 out of 25 times. The "MET (5/5)" verdict for criterion 4 is now backed by real variety, not one easy repeated case, so I trust this result more than the "before" one, even though both say the same thing on paper.


---

## What's Still Broken

## What's Still Broken

Nothing was missed against any target, so there's no failed criterion to fix,  but a few honest gaps remain, worth naming rather than pretending
everything is airtight.

**Criterion 1's target (4 of 5) was never actually tested against a hardcase.** Every scenario I ran used clean, wellformed queries that matched
easily. I never tried a deliberately awkward phrasing (a misspelled item name, unusual word order) to see if the 4-of-5 buffer is doing real work or if it's untested slack. I'd want to add a few messier queries to find out.

**The `>>> TRACE TEST` debug line is still in `agent.py`.** I added it while debugging why `--trace` wasn't printing anything, and never removed it. It's harmless and it doesn't affect correctness but it clutters every run's output and shouldn't be in submitted code. 

**I only moved one tool (`search_listings`) onto MCP, not more.** The stretch feature for a second MCP tool wasn't attempted . I focused my time
on testing rigor instead (the criterion 4 fix) rather than adding more surface area.

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
