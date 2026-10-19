---
name: i-am-lost
description: "Catch the user up on the current branch and session: what changed, what was verified, what's still open. Use whenever the user says 'i am lost', 'im lost', 'i'm lost', 'lost track', 'where are we', 'where was i', 'catch me up', 'what have we done', 'recap', 'remind me what we did', or otherwise signals they have lost the thread of the work. Also use when returning to a session after a long gap and the user asks what state things are in."
---

# I Am Lost

The user has lost the thread. Give them one complete picture of this branch in this session — no questions back, no "what would you like to know". They ask once, they get everything.

## Step 1: Gather facts before writing

Never summarize from memory alone. Memory drifts, and files change outside the session. Run these first, in one batch:

```
git status --short --branch
git log --oneline <base>..HEAD        # base is usually main; check what the branch forked from
git diff --stat <base>...HEAD          # committed work
git diff --stat                        # uncommitted work
git stash list
```

In a monorepo or multi-repo task, do this for **every repo touched this session**, not just the working directory. Name each repo and its branch separately — a summary that silently blends two repos is worse than none.

If a claim in your summary cannot be traced to a command output, a tool result, or a message in this session, either verify it now or mark it explicitly as unverified.

## Step 2: Write the summary

Lead with orientation, then detail. Use these sections, dropping any that are genuinely empty:

**Where you are** — repo(s), branch(es), what they forked from, whether the tree is clean, and whether anything is committed yet. One short paragraph.

**What the goal was** — the task in the user's own framing, including any mid-session change of direction. If the approach changed, say what it was before and why it changed. This is the part people lose first.

**What changed** — per file or per group of files, what was done and why, in plain sentences. Cite `path:line` for anything specific, and say in words what's there. Include changes that were made and then reverted, and say they were reverted.

**What was verified** — the actual commands run and their actual results: test counts, lint status, real output. Anything not run, or run but not passing, goes here too and is labelled as such. Never let "should work" pass as verified.

**What's still open** — remaining steps, known gaps, deliberate omissions (with the reason), and anything blocked waiting on the user.

**Decisions made** — choices the user approved or you defaulted to, with the reason in one line each. These are the things most expensive to re-derive.

**Anything surprising** — findings that changed the shape of the work: a bug discovered, an assumption that turned out false, a file that changed outside the session. If the session hit a dead end, say so; a failed attempt is worth as much as a successful one and costs the most to rediscover.

## Rules

- Write in full sentences and plain language. Define any term the first time it appears. No arrow chains, no fragments, no invented shorthand.
- Be honest about state. If something is half-done, broken, or uncertain, that is the most useful line in the summary.
- Do not perform new work while summarizing. This skill reports; it does not fix, edit, or commit. If the obvious next step is clear, name it in one line and stop.
- Do not pad. If the session did three things, the summary has three things in it.
- Never run destructive git commands to answer this — no `stash`, `checkout`, `reset`, `clean`. Read-only inspection only.
