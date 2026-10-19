# Ledger format

The ledger lives at `CLAIMS.md` in the root of the project being checked. One section per claim, newest at the bottom. Never delete a claim; change its verdict and add a dated line under History.

```markdown
# Claims ledger

## C1: Fine-tuning with the new loss raises exact-match accuracy on the 500-item test split from 61.2% (run 3, old loss) to 66.8% (run 7, new loss).

- Verdict: AT RISK
- Runs: runs/r3, runs/r7
- Depends on: none
- Suspects:
  - Noise (1 seed each): OPEN. Test: 2 more seeds of each. Rules out if every new-loss seed beats every old-loss seed.
  - Parsing artifact (new loss changes answer format): RULED OUT. Read 15 outputs per run; the parser agreed with a manual reading on all 30.
- History:
  - 2026-10-17: added, AT RISK.

## C2: The gain from the new loss is largest on multi-step problems.

- Verdict: AT RISK
- Runs: runs/r7
- Depends on: C1
- Suspects:
  - Picking the best (the split by problem type was chosen after looking at results): OPEN. Test: check the split on a fresh seed.
- History:
  - 2026-10-18: added, AT RISK.
```

Status values for a suspect: OPEN (not tested), RULED OUT (a test shows it does not explain the result), CONFIRMED (a test shows it does).

Status values for a claim: SURVIVES SO FAR, AT RISK, UNINFORMATIVE, UNSUPPORTED, FAKE.

When a claim becomes UNINFORMATIVE, UNSUPPORTED or FAKE, every claim listing it under "Depends on" becomes AT RISK, with a History line naming the claim that caused it.
