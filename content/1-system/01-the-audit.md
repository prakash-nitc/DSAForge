---
id: s1
numeral: §1
title: The audit
---

Counted row by row from your tracker, 4 September 2026. Your header reads 171; I count 176 visible rows. The discrepancy changes nothing.

| Pattern | Solved | Total | Left | Mastery | Verdict |
| --- | --- | --- | --- | --- | --- |
| Two Pointers | 9 | 12 | 3 | 20% (Revised) | Repair |
| Fast & Slow Pointers | 7 | 8 | 1 | 20% | Repair |
| Sliding Window | 7 | 11 | 4 | 20% | Repair + fill |
| Kadane's Algorithm | 6 | 6 | 0 | 20% | Repair |
| Prefix Sum | 4 | 6 | 2 | 20% | Repair + fill |
| Merge Intervals | 5 | 7 | 2 | 20% | Repair |
| In-place LL Reversal | 5 | 6 | 1 | 20% | Repair |
| Stack / Monotonic | 8 | 11 | 3 | 20% | Repair + fill |
| Hash Maps | 4 | 4 | 0 | 20% | Fold into others |
| Binary Search | 20 | 23 | 3 | 20% | [Strongest — protect]{.green} |
| Heap / Priority Queue | 14 | 17 | 3 | 20% | Repair + 2 gaps |
| Recursion & Backtracking | 11 | 11 | 0 | 20–30% | Repair + Subsets gap |
| Trees | 11 | 31 | 20 | 30% (traversal only) | [**HALF-BUILT**]{.red} |
| Graphs | 0 | 20 | 20 | 0% | [**ZERO**]{.red} |
| Dynamic Programming | 0 | 3 | 3 | 0% | [**ZERO**]{.red} |
| **TOTAL** | **111** | **176** | **65** | **~22%** |  |

## 1.1 The 65 unsolved, sorted by what they actually are

- **43 are structural holes —** Trees 20, Graphs 20, DP 3. These are missing capabilities. They need building (Part III), not revising.
- **22 are scattered HARDs —** spread thinly across nine patterns you otherwise own. Most are skippable; six are not. Appendix D marks each one.

## 1.2 What the 111 are worth

| Encoding level | Approx. count | Usable in an OA? |
| --- | --- | --- |
| Solved with editorial or hint, never revisited | ~60 | [No]{.red} |
| Solved unaided once, never re-solved | ~35 | [Coin flip]{.amber} |
| Two Pointers set marked 'Revised' | 9 | [Probably]{.green} |
| Cold re-solved after ≥7 days, under time | ~0 | [Yes — and you have none]{.red} |

*This is an estimate. §3.1 shows you how to replace it with a measurement in twenty minutes.*

## 1.3 The progress that is real

Mid-June: 15 solved. Today: 111. Ninety-six problems in eleven weeks, sustained through a semester, at roughly 1.2 per day. That is genuine work and it is the reason a one-week repair sprint can produce a transformation — the raw material exists. Most candidates four weeks out do not have it.

**What went wrong is narrow and fixable:** you optimised for first-solve throughput and never scheduled a second touch. Volume without consolidation produces exactly the tracker you are looking at — a long list of 20% rows and a felt sense of having forgotten everything, which is accurate.

## 1.4 The clock

| Company | Window | OA shape | Your exposure |
| --- | --- | --- | --- |
| Oracle | September | DSA + SQL + aptitude | [Graphs/DP gap; SQL is separately gated]{.red} |
| VISA | September | 2 DSA problems in Java | [Graphs gap; project gap is worse]{.red} |
| SAP Labs | September | DSA + aptitude | [Project round is the risk]{.red} |
| IBM India | September | Mixed, multiple tracks | [Reachable now]{.green} |
| Flipkart / MathWorks / Qualcomm | August (passed or passing) | Medium-hard DSA | [Graphs + DP heavy]{.red} |

> [!WARNING]
> **Reverse-engineered from the deadline**
>
> First OA plausibly lands in 7–21 days.
>
> Graphs is 20 problems at zero and appears in every target's question band. At 4/day with templates learned first, that is five working days to OA-credible.
>
> Trees-past-traversal is 20 problems that decompose into four recursion shapes. Four days.
>
> Everything else on this board is repair, and repair runs at two patterns per morning.
>
> Total to a defensible position: nine working days. You have them, but only if the sprint starts before the reading does.
