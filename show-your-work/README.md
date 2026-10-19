# show-your-work

A [Claude Code](https://claude.com/claude-code) skill with eleven working rules for multi-step coding tasks. Every rule can be checked from the transcript: if Claude can't point to the tool call or output that satisfies it, the rule wasn't followed.

## The rules

1. **Locate before you plan.** Don't name a file in a plan until a search has found it, including where it's called from.
2. **Batch independent reads** into one step instead of one per turn.
3. **Use subagents for fan-out only.** If you can name the file, read it yourself.
4. **Reproduce before you fix.** The failing output appears before the first edit.
5. **Zero search hits means the pattern is wrong.** Try two more phrasings before saying something doesn't exist.
6. **At a fork, run the probe that kills one branch,** instead of fixing for both explanations.
7. **Iterate narrow, gate wide.** Run one test file while working, and the full quality gate before saying done.
8. **A failed edit means the mental model is stale.** Re-read before retrying.
9. **Every changed hunk must justify itself** in one sentence, or be reverted.
10. **Diagnose is not fix.** If the user asked why, report findings and don't edit.
11. **Say "untested."** Every claim either has observed output, or the word "untested" next to it.

## When it applies

Load it at the start of any task that will take more than a few tool calls. It sets no project-specific commands. The quality gate in rule 7 is whatever the project's CLAUDE.md, README or CI config says.

## Install

See the [collection README](../README.md).
