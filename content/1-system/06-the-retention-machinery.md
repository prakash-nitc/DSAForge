---
id: s6
numeral: §6
title: The retention machinery
---

Part II repairs. This section is what stops the decay from ever rebuilding. If you install nothing else from this document, install §6.1 and §6.5.

## 6.1 The four-touch schedule

Every problem you solve from today gets four scheduled touches. This is not extra work — it replaces solving a fourth new problem, and it produces strictly more interview value.

| Touch | When | What you do | Cost |
| --- | --- | --- | --- |
| T1 — Recall | Same evening | No code. Say the approach, the data structure and the complexity out loud. | 2 min |
| T2 — Skeleton | Day +2 | Write the code skeleton on paper. Loop shape and key lines only. Don't run it. | 5 min |
| T3 — Cold solve | Day +7 | Full re-solve in the IDE. Tab closed, timer on. This is the touch that decides L3. | 15 min |
| T4 — Timed | Day +21 | Cold re-solve inside the interview-ready bar. Two consecutive passes → interval doubles. | 10 min |

*Roughly 32 minutes per problem spread over three weeks. That sounds heavy until you notice it replaces re-learning the problem from scratch in October, which costs 45 minutes and produces less.*

## 6.2 Interval doubling

```text The interval ladder
PASS  ->  7d  ->  14d  ->  30d  ->  60d  ->  retired to anchor rotation only
FAIL  ->  reset to 3d, and the PATTERN goes to the top of the repair queue
```

One failure resets one problem. Two failures in the same pattern in a week means the pattern decayed, not the problem — run the Part II card rather than grinding the individual problems.

## 6.3 The three-line note (every problem, no exceptions)

```text Example note
PATTERN : Prefix Sum + HashMap (count form)
INSIGHT : count += seen[prefix - k]; seed the map with {0:1} for subarrays starting at index 0
MISS    : I'd have reached for sliding window, which silently breaks on negatives
```

**The third line is the only one about you rather than about the problem, and it is the only one worth re-reading in September. It is also the line everyone skips.**

## 6.4 The weekly interleaved test

- Every Sunday. 10 problems, ≥8 different patterns, all last touched 3+ weeks ago.
- Labels stripped, order shuffled, 90 minutes total for all ten — not per problem.
- You will not finish. That is correct; an OA is also a triage exercise.
- Score each: clean / slow / identified-but-failed / didn't-identify.
- "Didn't identify" is the only red category. Any pattern producing one jumps the repair queue.
- Log the weekly score. Four scores in a row is the only honest measure of improvement that exists.

## 6.5 The anchor set — 39 problems, permanent rotation

Three per pattern, listed in every Part II card and collected in Appendix C with date boxes. These never leave rotation — not in October, not during interview weeks. They are the load-bearing wall: as long as the anchors hold, the derived problems come back on demand.

**If any anchor has no tick in 30 days, that is a fire, not a to-do.**

## 6.6 What to do when you have interviews and no time

| Situation | What survives | What gets dropped |
| --- | --- | --- |
| Normal week | Everything | Nothing |
| One active interview process | Daily loop + anchor rotation + company-specific prep | New topics, weekly test moves to a rest day |
| Two+ active processes | Daily loop only, plus company-specific | All new problems, all repair sessions |
| Interview tomorrow | Appendix J night-before checklist | Everything else. Sleep 8 hours. |

> **The block-integrity rule**
>
> A missed daily loop ends at the day boundary. You do not do 50 minutes tomorrow. Two loops in one day is not twice the spacing benefit — it is one loop plus wasted time. Miss it, log it as missed, run tomorrow's on schedule. This is structural, not a willpower question.
