---
name: show-your-work
description: Working method for multi-step coding tasks — how to break work down, when to delegate to subagents, which probes to run at decision forks, and the concrete checks that must pass before claiming done. Load at the start of any task that will take more than two or three tool calls.
---

# Show Your Work

Every rule here is checkable from the transcript. If you can't point to the tool call or output that satisfies a rule, you didn't follow it.

## 1. Locate before you plan

**Never name a file in a plan that hasn't appeared in a search result first.**

Why: plans built from assumed file layouts produce edits in the wrong layer, and you only find out after writing code.

Rule: before proposing an approach, your transcript must contain the Grep/Glob/Read calls that confirmed where the behavior actually lives — including the *call site*, not just the definition.

Example: asked to "fix the discount not being applied," don't open `pricing/discounts.py` and start editing. First grep for where discounts are applied (`checkout/total.py`) and read that path. The bug is as likely in how checkout calls the discount code as in the discount code itself.

## 2. Batch reads that don't depend on each other

**If the input to call B doesn't come from the output of call A, issue A and B in the same block.**

Why: sequential single reads double or triple wall-clock time for zero information gain.

Rule: a chain of one-at-a-time tool calls is only justified when each call's arguments were derived from the previous result. Reading `models.py`, `pricing/base.py`, and `pricing/discounts.py` to understand one feature is one block of three Reads, not three turns.

## 3. Subagents are for fan-out, not for files you can name

**If you can name the file that answers the question, Read it; spawn Explore only when the answer is a conclusion synthesized across many files whose contents you don't need.**

Why: a subagent starts cold and re-derives context you already hold; for a known target it is strictly slower and lossier than reading the file yourself.

Rule: before spawning, write the question as one sentence. If it names a specific file or symbol ("how does `cache.py` expire entries?"), read it directly. If it names a *pattern across the codebase* ("which of the API handlers swallow exceptions?"), that's a fan-out — delegate it and ask for the conclusion plus `file:line` citations, not file dumps.

Corollary: never spawn an agent to re-examine code already read in this conversation.

## 4. Reproduce before you fix

**The failing output must appear in your transcript before your first Edit.**

Why: bug reports paraphrase. Fixing the paraphrase produces a plausible patch for a bug that isn't there, and the real one survives.

Rule: run the narrowest command that shows the failure (`pytest tests/test_discounts.py -q`, or a three-line reproduction script in a scratch folder) and read the actual assertion text — not the issue's description of it. If the failure won't reproduce, that *is* the finding; report it instead of patching blind.

## 5. Zero search hits means your pattern is wrong

**Run two more searches with different vocabulary before concluding a thing doesn't exist.**

Why: "the client has no retry logic" and "I grepped the wrong word" look identical after one search, and the first conclusion changes what you build.

Rule: after a zero-hit Grep, try (a) a broader regex and (b) the domain's alternate naming before stating absence. `retry` finds nothing → try `backoff|attempt|max_retries|tenacity`. Only after all three miss may you write "there is no retry logic."

## 6. At a fork, run the probe that kills one branch

**When two explanations both fit the evidence, don't fix for both — run the cheapest command that only one explanation survives.**

Why: fixing both causes ships an unnecessary change and leaves you not knowing what the bug was.

Example: a string-comparison test fails on Windows only. Path separators or line endings? Don't normalize both. Print `repr()` of the two strings — one probe, one surviving hypothesis, one fix.

## 7. Iterate narrow, gate wide

**While iterating, run only the test file covering your change; before claiming done, run the full quality gate and show its exit status.**

Why: the full suite is too slow for an edit loop, and the narrow test is too weak for a done-claim — using either for the other's job wastes time or ships breakage.

Rule: iterate with the single test file covering the change (e.g. `pytest tests/test_discounts.py -q`). Done requires the project's documented quality gate — the commands its CLAUDE.md, README or CI config says to run before every commit — with pass/fail stated in the final report. For a typical Python project that might be:

```
ruff format --check .
ruff check .
pytest -q
```

A done-claim without the gate's results in the transcript is false. If the project documents no gate, run the full test suite and name the command you used.

## 8. A failed Edit means your mental model is stale

**Never retry a failed Edit with guessed whitespace; Read the actual region first.**

Why: `old_string` mismatches mean the file differs from what you remember — retrying from the same wrong memory fails again or, worse, matches somewhere you didn't intend.

Rule: two consecutive failed Edits on the same location with no Read between them is a violation. One failure → Read the surrounding 20 lines → edit from what's actually there.

## 9. Every hunk must justify itself in one sentence

**Before finishing, view the working diff; revert any hunk you cannot tie to the task in a single sentence.**

Why: drive-by changes (a type annotation a linter nudged you into, a renamed variable, reordered imports in a file you only read) are where review time goes and where unrelated regressions hide.

Rule: check the diff of your changes before the final report. "The task was fixing the discount calculation, so why does `utils.py` have a new docstring?" — if the answer starts with "while I was in there," revert it.

## 10. Distinguish "diagnose" from "fix" before touching code

**If the user described a problem or asked why, the deliverable is findings — a turn answering "why does X happen?" contains zero Edit calls.**

Why: an unrequested patch pre-empts the user's decision about *whether* and *how* to fix, and that decision is theirs.

Example: "why is the sync job hammering the API?" → trace the code path, name the root cause with `file:line`, state what a fix would touch — then stop. Edit only when asked.

## 11. Untested is a word you must say

**The final message either contains observed output for every claim, or the explicit word "untested" next to the claim it couldn't verify.**

Why: "this should work" and "I ran it and it passed" read almost identically to a user skimming, but only one of them is information.

Rule: banned phrasings for unverified changes: "should now work," "this fixes," "the tests will pass." Allowed: "passes `pytest tests/ -q` (output above)" or "untested — this environment has no network access, so `test_live_api.py` needs a live run." If a step was skipped, name the step.
