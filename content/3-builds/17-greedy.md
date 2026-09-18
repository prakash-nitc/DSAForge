---
id: s17
numeral: §17
title: Greedy
card: 18
---

You already use greedy inside Cards 6, 8 and 11 without naming it. Naming it matters, because the interview question is never "write the greedy" — it is "why is the greedy correct?"

## 17.1 The two proof techniques you should be able to state

- **Exchange argument —** take any optimal solution; show that swapping in your greedy choice does not make it worse. Therefore an optimal solution exists that contains your greedy choice. This is how you justify sorting by end time in interval scheduling.
- **Greedy stays ahead —** show that after every step, your partial solution is at least as good as any other partial solution of the same size. Used for shortest-path and scheduling arguments.

**You do not need a formal proof in an interview. You need two sentences that show you know why it works rather than that it happened to pass the samples.**

## 17.2 The recognisable greedy families

| Family | The greedy choice | Examples |
| --- | --- | --- |
| Interval scheduling | Always take the interval that ENDS earliest | Non-overlapping Intervals · Minimum Arrows to Burst Balloons |
| Interval merging | Sort by START and sweep | Merge Intervals · Insert Interval (Card 6) |
| Jump / reach | Track the furthest reachable index | Jump Game · Jump Game II |
| Heap greedy | Always serve the current extreme | Task Scheduler · IPO · Refuelling Stops (Card 11) |
| Monotonic-stack greedy | Pop anything that can be improved upon | Remove K Digits · Create Maximum Number (Card 8) |
| Assignment / two pointers | Sort both sides and match | Assign Cookies · Boats to Save People |
| Frequency greedy | Place the most frequent item first | Reorganize String · Task Scheduler |

## 17.3 The discriminator — greedy or DP?

- If a locally optimal choice can be shown never to hurt the global optimum, greedy. Otherwise DP.
- The standard counterexample to keep in your pocket: Coin Change with coins {1, 3, 4} and target 6. Greedy takes 4+1+1 = three coins; optimal is 3+3 = two. This one example answers "why not greedy?" for the entire DP topic.
- If the problem asks for the NUMBER of ways, it is almost never greedy — counting needs DP.
- If a wrong early choice can be repaired later at no cost, greedy is likely safe. If it locks you out of a better future, it is DP.

## 17.4 Problems worth doing

- **Jump Game and Jump Game II —** the reachability greedy. Both are quick and both are asked.
- **Non-overlapping Intervals —** the sort-by-end greedy you are currently missing entirely (Card 6, Template 6B).
- **Gas Station —** the classic 'one pass with a running deficit' argument. Very common.
- **Partition Labels —** last-occurrence map plus a sweep. Elegant and asked.
- **Task Scheduler —** you have it as CPU Task Scheduler; make sure you can explain the formula-based solution as well as the heap one.
