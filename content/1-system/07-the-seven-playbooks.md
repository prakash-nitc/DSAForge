---
id: s7
numeral: §7
title: The seven playbooks
---

Pick by how much runway you have. Each is complete on its own and each assumes you run §7.7 alongside it.

| Playbook | For | Delivers |
| --- | --- | --- |
| §7.1 — 24 hours | OA tomorrow | Template recovery + identification drill. Nothing else. |
| §7.2 — 72 hours | OA in three days | All 19 templates reactivated, 18 anchors re-solved, interleaved rep |
| §7.3 — 7 days | One clear week | All patterns L1/L2 → L3, plus one measured interleaved test |
| §7.4 — 14 days | Two weeks to drives | Repair everything + Graphs built from zero + tree shapes closed |
| §7.5 — 28 days | Four weeks | The full rebuild: repair + Graphs + Trees + DP + four mock OAs |
| §7.6 — 8 weeks | A real runway | Everything above plus Tries, bit manipulation, hard-tier work, contests |
| §7.7 — Daily loop | Permanent | 25 minutes/day that stops decay from ever rebuilding |

## 7.1  The 24-Hour Protocol

You have an OA tomorrow. Rules: learn nothing. Zero new topics, zero new problems, zero editorials. Everything goes to reactivating what is already partly there.

| Block | Time | What |
| --- | --- | --- |
| Morning | 120 min | Blank-page all 19 templates back to back. Mark ✓ / partial / blank. Repair the blanks only. |
| Midday | 90 min | Six cold re-solves, drawn from your weakest four patterns. 15-min cap each, no exceptions. |
| Afternoon | 45 min | 40 reps of the 60-second identification drill (§8). Read, name, move on. Do not solve. |
| Late afternoon | 30 min | Read the mistake log end to end. Write the top ten cues on one sheet of paper. |
| Evening | 20 min | Environment check: IDE ready, Java imports automatic, ArrayDeque / PriorityQueue comparator syntax verified. |
| From 8 PM | — | Stop. Eat. Sleep 8 hours. This block is worth more than two extra problems and it is not negotiable. |

## 7.2  The 72-Hour Protocol

### Day 1 — Template recovery (5 hours)

- **A (120 min):** Blank-page all 19 templates. Ten minutes each, no notes. Mark ✓ / partial / blank.
- **B (60 min):** Repair blanks and partials only. Ignore the ✓ ones entirely today.
- **C (120 min):** Six anchor cold re-solves from your weakest four patterns. 20-min cap.
- **D (20 min):** Mistake log. Read it back out loud once.

### Day 2 — Interleaved firing (5 hours)

- **A (150 min):** Eight cold re-solves in RANDOM order across patterns. Shuffle before you start — do not let yourself know the pattern in advance. 20-min cap. This is the most OA-like activity available to you.
- **B (60 min):** Your two weakest patterns from Day 1 get a full second repair pass.
- **C (60 min):** Company-flavoured. Oracle → SQL joins, group-by/having, window functions. VISA/SAP → Java collections, complexity, concurrency vocabulary.
- **D (30 min):** Mistake log + tomorrow's shortlist.

### Day 3 — Recognition, then stop (3.5 hours)

- **A (60 min):** 40 reps of the 60-second drill (§8).
- **B (60 min):** Four re-solves of problems you failed on Day 1 or 2. Live wounds only.
- **C (40 min):** Mistake log end to end. Top-ten cue sheet.
- **D (30 min):** Environment + Appendix J checklist.
- **Then stop.** No DSA after 6 PM the night before.

> **What 72 hours explicitly does not include**
>
> Not starting Graphs. Not starting DP. Not attempting untouched HARDs. Not reading a new editorial. Three days out, breadth is a trap — the only winning move is making what you already have reliable.

## 7.3  The 7-Day Repair Sprint

Goal: all thirteen touched patterns moved from L1/L2 to L3, plus one measured interleaved test. This is the protocol I would run first given any choice — it converts 111 half-dead problems into roughly 90 usable ones in six days.

| Day | Morning (peak, 3h) | Afternoon (2h) | Evening (1h) |
| --- | --- | --- | --- |
| Mon | Cards 10 (Binary Search) + 1 (Two Pointers) | Spring Boot / project | Blank-page both again |
| Tue | Cards 3 (Sliding Window) + 5 (Prefix Sum) | Spring Boot / project | 5 identification reps + log |
| Wed | Cards 8 (Stack) + 4 (Kadane) | Spring Boot / project | Monotonic stack ×3 blank-page |
| Thu | Cards 11 (Heap) + 12 (Backtracking) | Spring Boot / project | Two-heaps + choose/explore/unchoose |
| Fri | Cards 2 (Fast & Slow) + 7 (LL Reversal) + 6 (Intervals) | Spring Boot / project | 5 identification reps |
| Sat | Card 13 (Trees, traversal set) + 6 mixed cold re-solves | Interleaved set — 6 random | Mistake log consolidation |
| Sun | INTERLEAVED TEST — 10 random, 90 min, no labels | Score + re-grade every pattern | Next week planned from the score |

### Why Binary Search first

It is your strongest asset — 20 of 23 solved, the broadest coverage on the board. Starting with a pattern that will mostly hold gives you a clean 3/3 on Monday morning and sets the week's tone. Starting with your weakest gives you a 0/3 and a reason to stop. Sequence for momentum on day one; sequence for need from day two.

## 7.4  The 14-Day Rebuild — the one that matches your situation

Week 1 restores what you have. Week 2 builds the hole that will actually fail you.

### Week 1 — Repair (as §7.3)

Identical to the 7-Day Sprint. Do not skip the Sunday test; it is the measurement that makes Week 2 targeted instead of generic.

### Week 2 — Build

| Day | Morning (3h) | Afternoon (2h) | Evening (1h) |
| --- | --- | --- | --- |
| Mon | Graphs Day 0 + 1: five templates, then grid BFS/DFS, Number of Islands, Rotting Oranges, Surrounded Regions | Project | Blank-page BFS + DFS |
| Tue | Graphs Day 2: Kahn, cycle detection ×2, Course Schedule I + II | Project | Blank-page topological sort |
| Wed | Graphs Day 3: DSU — Provinces, Redundant Connection, Accounts Merge | Project | Blank-page DSU + path compression |
| Thu | Graphs Day 4: Dijkstra, Network Delay, Cheapest Flights K Stops, Path With Minimum Effort | Project | Blank-page Dijkstra |
| Fri | Trees Shapes A + B (§12): depth family, diameter, balanced, max path sum, path sums | Project | Bottom-up vs top-down, out loud |
| Sat | Trees Shapes C + D: BST family, construction | DP entry: Climbing Stairs, House Robber, Coin Change, LIS | Mistake log |
| Sun | MOCK OA — 3 problems, 90 min, timed, no help | Score + re-grade | Week 3 planned from the score |

> [!TIP]
> **The trade you are explicitly making**
>
> Two weeks buys: thirteen repaired patterns, Graphs at OA-credible level, the four tree shapes closed, and a DP toehold. It does not buy the 22 scattered HARDs or deep DP.
>
> That is the correct trade. Graphs at L3 beats Median of Two Sorted Arrays at L4 by a wide margin in expected OA points, because Graphs appears in every September target's question band and that one Hard appears in almost none.

## 7.5  The 28-Day Full Rebuild

| Week | Primary | Secondary | Exit condition |
| --- | --- | --- | --- |
| 1 | Repair all 13 touched patterns (§7.3) | Spring Boot 2h/day — PaperTrail skeleton, entities, first endpoints | All templates blank-pageable; Sunday test ≥6/10 identified |
| 2 | Graphs from zero — 14 of 20 (§13) | Spring Boot — JPA, repositories, service layer, DTOs | Five graph templates cold; three graph problems cold-solved |
| 3 | Trees complete (§12) + DP core ten (§14) | Spring Boot — JWT auth, validation, exception handling | Tree shapes automatic; 1D/knapsack/LIS templates held |
| 4 | Four interleaved mock OAs + weak-topic strike + company-tagged sets | Spring Boot — Docker, deploy, README, defence doc | 3/4 mocks with 2+ clean; project live with a URL |

### Week 4 — the mock OA cycle in detail

- Four mocks: Mon, Wed, Fri, Sun. 90 minutes, 3 problems (one easy-medium, two medium), timed, no help, no algorithm autocomplete.
- Source from LeetCode company tags for Oracle / VISA / SAP / Flipkart, or contest problems in the right band.
- The 24 hours after each mock: repair only what the mock exposed. Nothing else. Highest signal-to-noise loop in prep.
- Track one number across all four: minutes to correct pattern identification. Above 5 means identification is your bottleneck, not implementation — go back to §8.

## 7.6  The 8-Week Complete Programme

If a genuine eight-week runway ever opens — a semester break, a gap between drive waves — this is the shape.

| Weeks | Focus | Output |
| --- | --- | --- |
| 1–2 | Repair all patterns to L3; close the 22 scattered gaps worth closing (Appendix D) | ~130 problems at L3, all templates cold |
| 3–4 | Graphs complete (20) + Trees complete (31) + interleaving begins | Two largest holes fully closed |
| 5–6 | DP proper: 1D, grid, knapsack, LIS, LCS, stocks, partition, DP-on-trees (~25 problems) | DP no longer a red topic |
| 7 | Tries, bit manipulation, advanced Union-Find, greedy proofs; Hard-tier attempts | Breadth complete for any product-company OA |
| 8 | Mock OAs ×6, contests ×2, company-tagged sets, full anchor rotation | Interview-ready across the board |

## 7.7  The 25-Minute Daily Loop — permanent

This runs every day from now until your last interview, regardless of which playbook you are on. It costs 25 minutes and it is the mechanism that stops decay from ever rebuilding. If you install nothing else, install this.

| Minutes | Activity | Why |
| --- | --- | --- |
| 0–3 | Blank-page ONE template, rotating through the 19. | Every template refreshes every 19 days automatically. |
| 3–8 | Five 60-second identification reps. Read, name, move on. Don't solve. | Trains the first five minutes of every OA problem. |
| 8–23 | One cold re-solve, last touched ≥7 days ago. 15-minute cap. | The spaced retrieval that holds the line. |
| 23–25 | Update the mistake log and the tracker grade. Schedule the next touch. | Keeps the system honest without ceremony. |

### The re-solve queue

One ordered list. Every problem you touch goes to the back with a due date. Pull from the front.

```text Example queue
DUE TODAY
  Subarray Sum Equals K          last 2026-08-28   L3   interval  7d
  Reorganize String              last 2026-08-28   L2   interval  7d
  Reverse every K-element Sub    last 2026-08-27   L3   interval  7d

PASSED TWICE — interval doubled
  Maximum Subarray Sum           next 2026-09-18   L4   interval 14d

FAILED — reset + pattern flagged
  Reorganize String              next 2026-09-07   L2   -> repair Card 11
```
