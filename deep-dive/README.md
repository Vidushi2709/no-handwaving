# deep-dive

A [Claude Code](https://claude.com/claude-code) skill that turns Claude into a research mentor for a one-week deep dive into a single AI topic. The week ends with a GitHub repo of notes, code, results and a README that teaches the topic.

## The idea

Most "learning projects" end up as reproductions of a paper someone already wrote. This skill pushes each week toward something new:

1. **Explore first.** Read the primary papers, map what is known, and list candidate questions.
2. **Novelty gate.** Before writing code, search 2024+ work for each candidate question. Only build an experiment for a question that isn't already answered. If none passes, the week becomes an exploration write-up, and that counts as a valid outcome.
3. **Build small.** Experiments must run on one consumer GPU or a CPU. Toy settings, done carefully, teach more than big runs.
4. **Ship.** Every week ends with a repo whose README answers the week's questions, including what failed and what surprised you.

## Commands

| Command | What it does |
|---|---|
| `/deep-dive` | Resumes the active week, or proposes new topics if none is active |
| `/deep-dive new` | Proposes 3–4 topics from different areas, each with a concrete experiment and an anchor paper |
| `/deep-dive <topic>` | Skips proposals and plans a week on that topic |
| `/deep-dive status` | Summarises progress against the day of the week |
| `/deep-dive done` | Wrap-up: README checklist, retrospective, log update |

## What a week looks like

Planning writes a `PLAN.md` with:
- the week's question;
- 3–5 verified papers with real arXiv links;
- candidate questions, each with the closest existing work;
- a provisional experiment;
- a day-by-day checklist;
- 4–6 questions the README must answer;
- one genuinely open research question, checked against recent work, with a small probe you could run.

| Days | Plan |
|---|---|
| 1–2 | Read and summarise the papers; list candidate questions |
| End of 2 | Novelty gate: search, record the verdict for each candidate, pick one or stop |
| 3–5 | Build and run the experiment; every day ends with a result or a documented dead end |
| 6 | One extension of your choice |
| 7 | README, clean repo, push, retrospective |

On later days the skill reads your notes and code and gives you **one** next concrete step, then offers to help with it.

## State

Everything lives in `~/ai-deep-dives/`: a `LOG.md` index of weeks, plus one folder per week with `PLAN.md`, `NOTES.md` and the code. Change the path at the top of `SKILL.md` if you want it elsewhere.

`topics.md` is the topic bank, grouped by area: interpretability, training dynamics, architectures, systems, post-training, evaluation, classics, and agents.

**It refreshes itself every week.**
- **At wrap-up,** any follow-up questions the week raised get added to its "Seeded ideas" section.
- **Next time you ask for topics,** one of the options is a continuation of a past week, and it says which week it builds on.
- **When you pick a seeded idea,** it gets marked as taken so it isn't offered again.

Over time, your weeks build on each other instead of being isolated one-offs.

## Install

See the [collection README](../README.md).

The skill never runs git commands without asking. Pair it with [`is-it-real`](../is-it-real/) to check each result before it goes into the week's README.
