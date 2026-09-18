---
id: s9
numeral: §9
title: The stuck protocol
---

Being stuck is not a state to endure; it is a state with a procedure. Run the procedure in order. Most of the time you exit at step 2 or 3.

## 9.1 The nine questions, in order

| # | Question | What it unlocks |
| --- | --- | --- |
| 1 | What are the constraints? What complexity do they permit? | The constraint names the algorithm class before you know the algorithm. See §9.2. |
| 2 | What is the brute force, and what is its complexity? | You always have a brute force. Say it out loud. It is also the interview answer if you run out of time. |
| 3 | Can I solve n = 1, 2, 3 by hand? | Small cases expose the recurrence, the invariant, or the pattern almost every time. |
| 4 | What am I recomputing? | Recomputation → memoisation, prefix sums, or a cached map. |
| 5 | Does sorting help? What sort key? | Sorting is free at O(n log n) and converts many problems into two-pointer or greedy. |
| 6 | Is there a monotone property? | Monotone → binary search, possibly on the answer. |
| 7 | What is the state? What changes between steps? | Naming the state is the whole of DP. If the state is small, DP. If greedy is provable, greedy. |
| 8 | What data structure gives me the operation I keep needing? | Need the extreme repeatedly → heap. Need nearest-greater → monotonic stack. Need order statistics → TreeMap. |
| 9 | Have I seen a problem with this SHAPE before? | Not the same problem — the same shape. This is the question the 60-second drill trains. |

## 9.2 The constraint → complexity table

This is the single highest-leverage table in competitive and interview programming. Memorise it. Roughly 10⁸ simple operations per second is the working assumption.

| n up to | Target complexity | Algorithm class |
| --- | --- | --- |
| 10–12 | O(n!) | Permutations, brute-force TSP |
| 15–20 | O(2ⁿ) or O(2ⁿ · n) | Subsets, bitmask DP |
| 50–100 | O(n⁴) / O(n³) | Floyd–Warshall, interval/partition DP |
| 500 | O(n³) | Matrix chain, some 3-loop DP |
| 5,000 | O(n²) | 2D DP, LCS, edit distance, O(n²) LIS |
| 10⁵ | O(n log n) | Sorting, heaps, binary search, Dijkstra, most graph work |
| 10⁶ | O(n) or O(n log n) | Single pass, prefix sums, sliding window, counting sort |
| 10⁸ and above | O(log n) or O(1) | Binary search on the answer, closed form, maths |

> [!NOTE]
> **Use it in reverse, too**
>
> If n ≤ 20 and you are hunting for a clever polynomial trick, stop — the constraint is telling you a bitmask or full search is intended.
>
> If n = 10⁵ and your idea is O(n²), it will not pass. Do not code it; go back to step 1.
>
> If the answer is asked modulo 10⁹+7, it is a counting problem, almost always DP.

## 9.3 The 45-minute rule

- Genuine thinking, no editorial, no hints: 45 minutes on a new problem. 15 minutes on a re-solve.
- At the cap: read the editorial to the point where you see the key idea, then CLOSE IT. Do not read the code.
- Implement from the idea alone. If you can't, you didn't understand the idea — reopen and find out why.
- Log it as assisted (L1). Re-solve from scratch the next day. That second solve is the one that counts.
- Never grind past 90 minutes on one problem. The marginal minute is worth far less than the next problem.

## 9.4 The debugging ladder

| Symptom | First suspect | Check |
| --- | --- | --- |
| Wrong answer on a tiny input | Off-by-one or an inverted comparison | Trace n = 1 and n = 2 by hand |
| Works on samples, fails on a hidden case | Edge case — empty, single, all-equal, all-negative, duplicates | Appendix F checklist |
| Wrong on large inputs only | Integer overflow | Switch sums/products to long |
| TLE | Complexity is one class too high | §9.2 — recompute your actual complexity honestly |
| TLE on a graph problem | Missing visited marking, or visited-on-dequeue | Mark visited on enqueue |
| Stack overflow | Recursion depth on a skewed input | Convert to iterative, or note the depth bound |
| Duplicate results | Missing dedup in backtracking or two pointers | Sort first, then skip equal neighbours |
| Null pointer | Unchecked child / next / head | Null-guard at the top of every recursive call |
| Wrong on negatives | Java's % returns negative | ((x % k) + k) % k |
