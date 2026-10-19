# no-handwaving  ( •_•)>⌐■-■

[Claude Code](https://claude.com/claude-code) skills for doing AI research and coding without handwaving. Every result gets checked, every claim gets backed by something Claude actually ran, and nothing gets called "done" on vibes.

| Skill | What it does |
|---|---|
| [`deep-dive`](deep-dive/)  `\(^o^)/` | A one-week research mentor: explore a topic, pass a novelty gate, run a small experiment nobody has published, and ship a repo |
| [`is-it-real`](is-it-real/)  `(¬_¬)` | Tries to break a result before you build on it: traces the number to its raw outputs, lists how it could be fake, and proposes the cheapest test for each |
| [`show-your-work`](show-your-work/)  `φ(..)` | Eleven checkable working rules for multi-step coding tasks: locate before planning, reproduce before fixing, run the full gate before saying done, say "untested" |
| [`i-am-lost`](i-am-lost/)  `(@_@)` | Catches you up on a long session: where you are, what changed, what was verified, what's still open |

## How they fit together  ᕕ( ᐛ )ᕗ

```
  deep-dive        plan the week, run the experiment
      |
  is-it-real       is that result real, or noise / a bug / a leak?
      |
  show-your-work   keep the code changes honest while you fix it
      |
  i-am-lost        come back after a break and know where you are
```

## The skills, a bit more

### `deep-dive`  \(^o^)/

A research mentor for one week on one AI topic. It proposes 3–4 topics from different areas, each with a concrete experiment that runs on a laptop GPU or CPU and one anchor paper. Then it writes a day-by-day plan with a verified reading list.

The key rule is the **novelty gate**: after two days of reading, it searches recent work for each candidate question. You only build an experiment for a question nobody has answered yet. If nothing passes, the week becomes an honest write-up of what's known and what's open, and that counts too.

On later days, `/deep-dive` reads your notes and code and gives you one next step. `/deep-dive done` walks you through shipping the repo.

The topic bank refreshes every week. Follow-up questions from a finished week are saved, and the next week's options include a continuation of past work. That way each week builds on the last.
→ [more](deep-dive/)

### `is-it-real`  (¬_¬)

Give it a result, like "B beats A by 11.5 points", and it tries to break it. It traces the number back to the code, seed and raw outputs, recomputes it, and runs the mechanical checks: how many seeds, whether the error bars overlap, whether the item counts add up, whether this was the best of several runs.

Then it reads raw outputs and works through ten ways results go wrong: noise, a broken judge or metric, a confound, leakage, a pipeline bug, picking the best, and more. It keeps at most three real suspects and proposes the cheapest test for each. The verdict is one of: survives, at risk, uninformative, unsupported, or fake.

It also keeps a `CLAIMS.md` ledger. When one claim falls, everything built on it gets flagged.

Tested on 17 real past claims and 8 built experiments: it caught the known flaws, and said "survives" when the work was actually sound.
→ [more](is-it-real/)

### `show-your-work`  φ(..)

Eleven rules for coding tasks, each one checkable from what Claude actually ran:
- find the code before planning;
- reproduce a bug before fixing it;
- run two more searches before saying something doesn't exist;
- at a fork, run the one probe that rules out an explanation;
- run the full quality gate before saying "done";
- revert any change you can't justify in a sentence;
- if the user asked "why", explain instead of editing;
- say "untested" out loud when something wasn't run.

→ [more](show-your-work/)

### `i-am-lost`  (@_@)

Say "I'm lost" or "where are we" after a long session or a break. It checks git for the real state of every repo touched, then gives one complete summary:
- where you are;
- what the goal was, including any change of direction;
- what changed;
- what was actually verified;
- what's still open;
- which decisions were made;
- anything surprising.

It only reports. It never edits, commits or runs anything destructive.
→ [more](i-am-lost/)

## Install  ┬─┬ノ( º _ ºノ)

Copy the skills you want into your Claude Code skills folder:

```bash
git clone https://github.com/Vidushi2709/no-handwaving.git
cp -r no-handwaving/deep-dive no-handwaving/is-it-real no-handwaving/show-your-work no-handwaving/i-am-lost ~/.claude/skills/
```

To use a skill in one project only, copy it into that project's `.claude/skills/` instead. Start a new Claude Code session afterwards, then type `/deep-dive`, `/is-it-real`, `/show-your-work` or `/i-am-lost`.

`is-it-real/checks.py` needs `numpy` and `scipy`.

## License  ¯\\\_(ツ)\_/¯

[MIT](LICENSE)
