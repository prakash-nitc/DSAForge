---
id: s5
numeral: §5
title: The engine — the 90-minute Pattern Repair session
---

This is the atomic unit of everything that follows. One session repairs one pattern — meaning it restores 6–20 previously-solved problems to usable state, because they were all instances of one template. This is why repair is roughly ten times more efficient than re-solving problem by problem, and it is the most important operational idea in this document.

## 5.1 The five phases

| Phase | Time | What you do | The rule |
| --- | --- | --- | --- |
| 1. Blank page | 10 min | Write the pattern's template from memory. No notes, no IDE autocomplete. Then the trigger signals and the complexity. | If you can't, that IS the finding. Write down what you couldn't produce. |
| 2. Repair | 15 min | Open the card. Fix your blank page. Annotate only the differences. | Do not re-read everything. Only the deltas. |
| 3. Cold anchors | 45 min | Cold re-solve the card's three anchors. 15-minute hard cap each. Tab closed, timer visible. | No editorial during. Failure is data. |
| 4. Gap note | 10 min | One line per failure in the mistake log: what you missed and why. | The clause 'I would have missed this because…' is mandatory. |
| 5. Re-grade | 10 min | Update mastery levels honestly. Schedule the next touch at +7 days. | Grade down freely. Never up on a feeling. |

## 5.2 Reading the outcome

| Result | Meaning | Next action |
| --- | --- | --- |
| 3/3 clean, inside time | L4. It held. | Next touch in 14 days. Move on. |
| 2/3 clean | Normal. L3. | Next touch in 7 days. Add one new problem in the family. |
| 1/3 clean | Genuine decay. | Repeat the entire card in 48 hours before moving on. |
| 0/3 clean | Never encoded past L1. | Treat as a new topic. Re-learn from the template up, two sessions. |

## 5.3 The mistake log

One file. Append-only. Four lines per entry. By October this is the highest-value document you own — it is what you read the night before every OA, and nothing else.

```text Example log entry
[2026-09-05]  Triplet Sum to Zero  |  Two Pointers  |  FAILED cold (18 min, dup output)
  MISSED : the dedup for l and r AFTER recording a match.
  WHY    : I remember the outer-loop dedup and assume it covers the inner. It doesn't.
  CUE    : 'dedup fires three times in 3Sum — outer i, inner l, inner r.'
```

*Do not log successes here. A log of things you got right is a comfort object. This file exists to be short and uncomfortable.*

## 5.4 The time bars

| Difficulty | First solve | Cold re-solve | Interview-ready | OA target |
| --- | --- | --- | --- | --- |
| Easy | 20 min | 10 min | ≤ 6 min | ≤ 8 min incl. edge cases |
| Medium | 45 min | 20 min | ≤ 15 min | ≤ 22 min incl. edge cases |
| Hard | 60 min | 35 min | ≤ 30 min | Flag and return |

**Hit the cap, stop. Log the failure, take the learning, move to the next anchor. Overrunning to "finally get it" turns a 90-minute session into four hours that repairs one pattern instead of two. The cap is the point.**

## 5.5 Session hygiene

- Phone in another room. Not face-down — another room.
- One file open: the card. Not the tracker, not LeetCode's editorial tab, not YouTube.
- Paper and pen on the desk. The blank-page phase is on paper, not in an editor.
- Timer visible and audible. A silent timer you have to check is a distraction.
- Java only. Switching languages mid-prep costs you the exact muscle memory you're building.
