---
name: is-it-real
description: Check whether an experimental result is real before it becomes a claim. Traces the number back to the code, config, seeds and raw outputs that produced it, lists the ways it could be fake (noise, a broken judge or metric, a confound, a setup mismatch, a pipeline bug, picking the best run), and proposes the cheapest test to rule each one out. Keeps a ledger of claims, their evidence and what depends on them. Use when the user invokes /is-it-real, asks "is this real?", "could this be noise?", "check this result", or is about to write a result into a WRITEUP, README or report.
---

# Is it real?

Your job is to try to break a result before the researcher builds on it. You are not here to confirm it, summarise it or make it sound better. A result that survives your checks is worth more than one nobody tried to break.

Work from **artifacts, not prose**. Code, configs, logs, run records and raw model outputs count as evidence. The researcher's WRITEUP, notes, commit messages and your own earlier summaries do not. They are what is being checked.

Do not edit code, configs or results. Do not run anything that costs money or takes more than a couple of minutes without asking first. Proposing tests is the deliverable; running them is the researcher's call.

## Step 1: Pin the claim

Write the claim as one sentence that contains the number, what it is compared against, and the runs it comes from.

- Vague: "the new loss helps."
- Pinned: "Fine-tuning with the new loss raises exact-match accuracy on the 500-item test split from 61.2% (run 3, old loss) to 66.8% (run 7, new loss)."

If the user gave only a number or a vague sentence, pin it yourself from the artifacts and show them the pinned version. If you cannot tell which comparison or which runs it rests on, ask. Do not guess.

## Step 2: Trace where the number came from

Find, and cite as `file:line` or by path:

1. The script and function that computed the number.
2. The config or arguments of that run, including the seed and model name.
3. The raw outputs the number was computed from (predictions, judge replies, activations, logs).
4. The input data, and how many items it has.

Then **recompute the number from the raw outputs** if that is cheap (a few lines of Python, no model calls). Say whether it matches.

If you cannot trace the number to raw outputs, stop here and report that as the main finding. A number with no traceable source cannot be checked, and that is itself the problem to fix.

## Step 3: Mechanical checks

These need no judgment. Run every one that applies and report each as PASS, FAIL, or CAN'T CHECK with the reason.

For paired comparisons, AUROC with an interval, probe nulls (random and shuffled-label directions) or judge audits, import `checks.py` from this skill's folder instead of writing your own. Its docstring also lists the one-liners for Wilson intervals, McNemar, t-intervals, text baselines and leak checks.

- **Seeds.** How many independent seeds or reruns is the claim based on? One seed on anything trained, sampled or randomly split is a FAIL for any claim about a difference.
- **Sample size and interval.** How many items? Compute a 95% interval (Wilson for proportions, bootstrap otherwise). If the claim compares two numbers, do their intervals overlap?
- **Counts add up.** Does the number of items in the outputs match the number in the input? Silently dropped items (crashes, parse failures, timeouts, filtered rows) are a common hidden cause.
- **Selection.** Look in the logs, results folder and run history for *other* runs of the same experiment: other seeds, layers, prompts, thresholds, models. Was the reported one the best of several? If so, say how many were tried.
- **Decided before or after.** Look for a plan, hypothesis list or pre-registration dated before the run. Was this the comparison the researcher said in advance they would make, or was it chosen after seeing results? After is not wrong, but the claim must be labelled exploratory.
- **Baseline and control.** Is there a baseline that shows what "nothing going on" looks like (random directions, shuffled labels, a constant predictor, the untreated condition)? A number without one cannot be called large or small.
- **Ceiling and floor.** Is any condition at or near 0% or 100%, or is a judge or classifier giving the same answer to almost everything? If so, it is not measuring the difference.

## Step 4: Judgment checks

Go through every suspect in [suspects.md](suspects.md). For each one, decide whether it could plausibly explain this result **in this project**, and cite the file, line or output that made you think so. A suspect with no cited evidence is dismissed in one line.

Read raw outputs yourself. Pick at least 15 at random (not the first 15, which are often unrepresentative) from each condition being compared, and read them in full. Most of the worst problems in past projects were visible in raw outputs and invisible in the summary numbers.

## Step 5: Rank and cut

Every result has some conceivable alternative explanation. Listing many teaches the researcher to ignore you. Sort what you found into three bins:

- **Live suspects, at most three.** A suspect is live only if it passes both tests: (1) you can point to a specific file, line, number or output in *this* project that shows it could explain the result, and (2) if it turned out true, the claim would have to change. "Only one seed" is live only if you have a reason to think seeds would disagree here, such as a small effect, a result near a boundary, or other runs in the project that vary. Rank them by how likely they are times how cheap they are to rule out.
- **Caveats.** Limits on scope that don't threaten the claim as stated: "this is one model", "one dataset", "the numbers in a single run". Note them in one line each. They do not count against the verdict.
- **Considered and dismissed.** Everything else, one line each with the reason.

If you have more than three candidates for live suspect, keep the three strongest and move the rest to caveats or dismissed, saying which.

## Step 6: Propose the cheapest test for each live suspect

For each live suspect, give:

- **The test**, concretely: the command to run, the 15 outputs to read, the two extra seeds, the reworded prompt.
- **Cost**, roughly: minutes of compute, API spend if any, minutes of reading.
- **What would rule it in or out, stated now, before the test is run.** For example: "If the 3-seed mean stays above 0.85 with all seeds above 0.80, noise is ruled out. If any seed falls below 0.70, the claim is withdrawn."

Prefer tests that need no new code. Reading outputs and rerunning with a different seed beat building a new experiment.

## Step 7: Verdict and ledger

First, judge the claim **as written**, not a broader version of it. If the sentence is about one model, one run or one dataset, check that. If you think the researcher will be tempted to generalise it, say so under caveats instead of failing the narrow claim.

Then give one verdict:

- **SURVIVES SO FAR**: the number recomputes, the mechanical checks that matter pass, and no live suspect is left untested. Caveats are allowed. This is the expected verdict for a claim that was done carefully. Do not withhold it just because more seeds or more data would always be nice.
- **AT RISK**: at least one live suspect is still untested. Usable as an exploratory result only.
- **UNINFORMATIVE**: the claim is true as stated, but the test could not have come out any other way, so it shows less than it seems to. For example, a condition that is guaranteed by construction to produce the result, or a benchmark on which no variant of the method could differ. Say what test would actually be informative.
- **UNSUPPORTED**: the number may well be right, but a check already shows the evidence does not establish what the claim says it does. A simpler explanation fits equally well, for example a trivial baseline matches the method, or the comparison was not controlled the way the claim assumes. This says the claim is not shown, not that it is false. Say what narrower claim the evidence does support.
- **FAKE**: a check already shows the number itself is wrong, or is caused by something other than what the claim says: it does not recompute, a bug produced it, or a confirmed artifact accounts for it.

Choose UNSUPPORTED over FAKE whenever the check shows a rival explanation fits but does not show the claimed effect is absent. Most failed interpretations are UNSUPPORTED. Choose UNINFORMATIVE over UNSUPPORTED when the claim's literal sentence is true and your objection is that the test was too weak or too predetermined to tell anything apart.

In one sentence, also say whether your concern is about **the evidence available now** or about **whether the conclusion is true**. These come apart: a conclusion can turn out right even when the evidence for it at the time was not enough, and the verdict is about the evidence.

Then update `CLAIMS.md` at the project root, using the format in [ledger-template.md](ledger-template.md). Create it if it does not exist. Each claim gets an ID, its pinned sentence, the runs, the suspects with status, and the IDs of the claims it **depends on**.

When a claim's verdict becomes UNINFORMATIVE, UNSUPPORTED or FAKE, find every claim in the ledger that lists it under "Depends on", mark each one AT RISK, and tell the researcher which ones.

## Where the report goes

The ledger (`CLAIMS.md`) is the only file you write. Do not write the report to a file. Return it as your final message. If you are running as a subagent, the harness will refuse report files anyway, so the caller gets the report from your final message and saves it if they want it.

## Report format

```
## Claim C<n>: <pinned sentence>

Traced to: <script:line>, <config>, <raw outputs path> (recomputed: matches / differs / not checked)

Mechanical checks
- Seeds: FAIL. 1 seed (runs/r10/config.yaml:4).
- Interval: FAIL. 66.8% [62.6-70.8] vs 61.2% [56.9-65.4], the intervals overlap.
- ...

Live suspects (at most three, most worth checking first)
1. <suspect name>: <why it fits this project, with citation>
   Test: <what to do>. Cost: <time / money>.
   Rules out if: <...>. Confirms if: <...>.
2. ...

Caveats (do not count against the verdict)
- <scope limit, one line>

Considered and dismissed
- <suspect>: <one-line reason>

Verdict: AT RISK. <one sentence on what has to happen before this can be written as a finding>
Concern is about: the evidence available now / whether the conclusion is true.
```

Write the report in plain sentences. Say "untested" next to anything you could not check, and name the step you skipped.
