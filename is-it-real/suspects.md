# Suspects: ways a result can be fake

Each suspect has what it is, the signs to look for in the artifacts, the cheapest test, and a short made-up example so the pattern is recognisable. The examples are illustrations, not rules to copy.

---

## 1. Noise

**What it is.** The difference is within what you would get by rerunning with a different seed or a different sample of items.

**Signs.** One seed. Small sample. A difference of a few points. Intervals that overlap. A result that appears in one condition and not in a near-identical one. A rate computed over so few units that one unit moves it by 20 or more points.

**Cheapest test.** Two or three more seeds, or bootstrap the items. Decide beforehand what spread would kill the claim.

**Example.** A method fails on 1 of 4 test cases in one run, reported as "a 25% failure rate". Two more seeds show 0 of 4 each time.

**Limit.** More seeds rule out noise and nothing else. A broken metric can give the same wrong answer to three decimal places on every seed. Agreement between seeds says nothing about whether the measuring tool works (suspect 2).

---

## 2. Broken measuring tool

**What it is.** The judge, metric, probe or parser producing the number does not measure what it is supposed to. The result describes the tool, not the thing being studied.

**Signs.** The tool was never tested on cases where the right answer is known. It gives the same answer to almost everything. Its scores do not change when the inputs obviously should change them. Its stated reasons are wrong when you read them.

**Cheapest test.** Feed the tool 10 to 20 cases where you already know the right verdict: a correct answer, a wrong answer, a refusal, an empty answer, a correct but hedged answer. Count how many it gets right.

**Example.** An LLM judge grades answers as correct or incorrect. It marks "I don't know" as correct because its prompt only tells it to fail answers that contradict the reference, so every refusal inflates the score.

---

## 3. Confound

**What it is.** The groups being compared differ in a second way besides the one the claim is about, and the second difference could explain the result.

**Signs.** The two groups come from different sources, were written by different people or models, were processed with different instructions, or cover different topics, lengths or formats. A random baseline already separates them well.

**Cheapest test.** Check whether a trivial method that cannot know about the claimed difference (a bag-of-words classifier, length alone, topic keywords) separates the groups as well as the method does. If it does, the claim is not supported. Then find or build a version where only the claimed difference changes and everything else is held fixed.

**Example.** A probe separates "questions from a test set" from "questions from real users" with high accuracy. The test-set questions are all about science and the user questions are all about everyday tasks, so the probe may be reading topic.

---

## 4. Setup mismatch

**What it is.** Some part of the setup (a prompt, a label, an instruction, a default) does not fit the data, or treats two groups differently, and the model or method reacts to that instead of to the thing being tested.

**Signs.** Prompts written for one dataset reused on another. Instructions that describe the data wrongly. Two groups generated or preprocessed with different instructions. Defaults left unchanged from an example script.

**Cheapest test.** Reread every prompt and config against a few real items from each group. Diff the instructions used for each group. Count simple surface features (slang, greetings, casing, length) per group to see whether processing added a difference. Rerun the suspicious condition with neutral or identical wording.

**Example.** Two groups of prompts are both rewritten by an LLM, but with different instructions. One instruction says "make it casual", so that group gains slang and lowercase text that the other group lacks.

---

## 5. Pipeline bug or silent data loss

**What it is.** Code between the raw data and the number does something other than intended: drops items, duplicates them, mixes up labels, reads the wrong file, or swallows errors.

**Signs.** Item counts that do not match between stages. `try/except` blocks that skip failures. Concurrency. A fix that "should have" solved an earlier problem. Results that change when nothing meaningful changed.

**Cheapest test.** Count items at every stage. Trace three individual items by hand from input to final score.

**Example.** Parallel writes to a database occasionally fail, the error is caught and logged at debug level, and 8% of sessions never reach the index. A config flag that sounds like it disables the cause does not.

---

## 6. Picking the best

**What it is.** Several variants were tried (layers, prompts, seeds, thresholds, models), and the reported one is the best of them. Some of its advantage is luck.

**Signs.** Many runs in the results folder with only one reported. A layer or threshold chosen after looking at results. A pre-registered setting that failed, followed by a different setting that worked.

**Cheapest test.** Report how many variants were tried. Re-test the chosen setting on held-out data or a fresh seed. Label the result exploratory.

**Example.** A method fails at the layer chosen in advance, then works at a different layer found by scanning all of them on the test set.

---

## 7. The intervention did not happen

**What it is.** The experiment changes something (a format, a prompt, a training condition) and measures the effect. But the change was weaker than intended, or did not register at all, so "no effect" or "small effect" says nothing.

**Signs.** No manipulation check (a direct measurement that the change took place). A manipulation check that failed.

**Cheapest test.** Measure the change directly before interpreting its effect.

**Example.** Prompts are wrapped in a template meant to look like an exam. A classifier trained to detect exam formatting labels almost none of the wrapped prompts as exams, so "the wrapper had no effect" is uninterpretable.

---

## 8. Ceiling, floor or saturation

**What it is.** One condition is at or near 0% or 100%, so a difference cannot show up, or an improvement looks large only because the baseline is broken.

**Signs.** Scores of 0%, 100% or full marks. A constant output from a judge or classifier.

**Cheapest test.** Add harder or easier items, or a condition known to land in the middle.

**Example.** A regression suite scores every version at full marks, so it can show that something broke but never what improved.

---

## 9. Leakage

**What it is.** Information about the answer reaches the model or method through a path it should not have: test items in training data, labels in prompts, future information in features, the answer in a file the agent can read.

**Signs.** Suspiciously high scores. Overlap between train and test. Prompts or inputs built from the same source as the labels.

**Cheapest test.** Check for overlap. Remove the suspected path and rerun on a small sample.

**Example.** Train and test splits are made by row, but the same underlying item appears in several rows, so near-copies of test items are in training.

---

## 10. Parsing and format artifacts

**What it is.** The number depends on how outputs were parsed (regex, keyword rules, JSON extraction), and the parser treats a change of wording as a change of meaning.

**Signs.** Keyword or regex scoring. Many "no verdict" or unparseable outputs. Different conditions producing differently styled outputs.

**Cheapest test.** Read 15 outputs per condition next to their parsed labels and count disagreements.

**Example.** A keyword rule counts a reply as a refusal only if it contains "I can't" or "I'm sorry". In one condition the model refuses in an impersonal lecturing voice, so the rule counts those refusals as compliance.
