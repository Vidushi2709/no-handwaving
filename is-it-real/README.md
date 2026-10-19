# is-it-real

A [Claude Code](https://claude.com/claude-code) skill that tries to break an experimental result before you build on it.

Most research mistakes aren't about missing papers. They're results believed too early: a gain that was one lucky seed, a judge that marks "I don't know" as correct, a probe that is really reading topic, test data that leaked into training. They usually get caught late, after other claims have been built on top.

`/is-it-real` checks a result at the moment you get it. It traces the number back to the code, config, seeds and raw outputs that produced it, asks how it could be fake, and proposes the cheapest test that would tell.

## What it does

Given a claim like *"system B beats A by 11.5 points (results/summary.json)"*, it:

1. **Pins the claim** down to one sentence: the number, what it's compared against, and which runs it comes from.
2. **Traces the number** to the script, config, seed and raw outputs, and recomputes it from the raw outputs where that's cheap.
3. **Runs mechanical checks:** how many seeds, whether the intervals overlap, whether item counts add up, whether this was the best of several runs, whether the comparison was planned before the results, whether there's a baseline, and whether anything is stuck at 0% or 100%.
4. **Reads raw outputs** and works through ten common ways a result can be fake: noise, a broken measuring tool, a confound, a setup mismatch, a pipeline bug or silent data loss, picking the best, an intervention that didn't happen, ceiling or floor effects, leakage, and parsing artifacts.
5. **Keeps at most three live suspects.** Each must point to something specific in your project, not a generic worry. Scope limits like "this is one model" go in a separate caveats list.
6. **Proposes the cheapest test** for each suspect, with its cost and what result would rule it in or out, stated before the test is run.
7. **Gives a verdict** and records it in `CLAIMS.md`, a ledger of your claims and which ones depend on which.

| Verdict | Meaning |
|---|---|
| **SURVIVES SO FAR** | Recomputes, the checks pass, and nothing plausible is left untested |
| **AT RISK** | A plausible problem is still untested; treat it as exploratory |
| **UNINFORMATIVE** | True as stated, but the test couldn't have come out any other way |
| **UNSUPPORTED** | The number may be right, but the evidence doesn't show what the claim says |
| **FAKE** | The number is wrong, or something other than the claim produces it |

When a claim becomes uninformative, unsupported or fake, every claim that depends on it in the ledger is marked at risk.

It never edits your code or results, and it asks before running anything slow or paid.

## Install

See the [collection README](../README.md). `checks.py` needs `numpy` and `scipy`. Some of the one-liners in its docstring use `scikit-learn`.

## Use

```
/is-it-real B beats A by 11.5 points on the 400-question set (results/summary.json)
```

Or just ask "is this result real?" or "could this be noise?", or have it check a result before it goes into a write-up.

## Files

| File | What it holds |
|---|---|
| `SKILL.md` | The procedure Claude follows |
| `suspects.md` | The ten ways a result can be fake: signs to look for, the cheapest test, and an example |
| `ledger-template.md` | The format of `CLAIMS.md` |
| `checks.py` | Helpers so reviews don't re-derive the same statistics each time: `paired` (two systems scored on the same items, with grouped bootstrap and McNemar), `auroc` / `auroc_ci`, `probe_nulls` (random and shuffled-label directions for a probe), and `judge_audit` (feeds a judge answers whose right verdict is known). Its docstring lists the one-liners that need no helper. |

## How well it works

It was tested in two ways, with each case given blind to a fresh agent that saw only the project and the claim:

- **Replay of past research.** 17 claims from earlier projects were rebuilt as they stood when each claim was made, hiding everything that came later. It caught the known flaw in 8 of 10 flawed claims. The 2 misses traced back to how the test claims were worded. Along the way it found several problems the original research had missed.
- **Built experiments with known answers.** 8 small experiments: 5 done properly, and 3 copies of them with one planted flaw. It caught all 3 flaws for the right reason. It said "survives" on 4 of the 5 sound ones and "uninformative" on the fifth, correctly: the generated data made that task solvable by a lookup table.

**Limits:**
- These are small tests: 25 cases, each run once.
- The test projects were built by the same person who wrote the skill.
- It is stronger at finding problems than at certifying that something is fine.
- Verdicts can vary between runs.

Treat its output as a careful second reader, not a referee.
