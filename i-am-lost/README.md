# i-am-lost

A [Claude Code](https://claude.com/claude-code) skill for when you've lost the thread of a long session. Say "I'm lost", "where are we" or "catch me up", and you get one complete picture of the work, without being asked questions back.

## What you get

It first runs read-only git commands (status, log, diffs against the base branch, stash list) for every repo touched in the session, so the summary comes from facts rather than memory. Then it writes:

| Section | What it covers |
|---|---|
| **Where you are** | Repos, branches, what they forked from, whether anything is uncommitted |
| **What the goal was** | The task as you framed it, including any change of direction and why |
| **What changed** | Each file or group of files: what was done and why, including changes that were later reverted |
| **What was verified** | The commands actually run and their actual results; anything unrun is labelled as such |
| **What's still open** | Remaining steps, known gaps, anything waiting on you |
| **Decisions made** | Choices approved or defaulted, one line each |
| **Anything surprising** | Bugs found, assumptions that turned out false, dead ends |

## Rules it follows

- Plain sentences, no shorthand.
- Honest about half-done or broken state.
- It reports only: no fixing, editing or committing.
- It never runs destructive git commands.

## Install

See the [collection README](../README.md).
