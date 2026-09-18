---
id: s8
numeral: §8
title: The 60-second drill — training the first five minutes
---

An OA is won or lost in the first five minutes of each problem, when you decide what kind of problem it is. Implementation is the easy half. You have spent eleven weeks training implementation and roughly zero minutes training identification, because blocked practice handed you the answer in advance.

## 8.1 How to run it

- Take 40 problem statements — your solved list, LeetCode, anywhere.
- 60 seconds each. Read, then say out loud: pattern, data structure, loop shape, complexity.
- Do not solve. Do not open an editor. Move at the buzzer regardless.
- Mark each: instant / got there / wrong / no idea.
- Forty problems takes forty minutes and tells you more about OA readiness than a week of solving.

## 8.2 Reading the score

| Out of 40 | Meaning | Action |
| --- | --- | --- |
| 32+ instant | Identification is OA-ready. | Shift effort to implementation speed and untouched topics. |
| 24–31 | Functional but slow. You'll burn minutes you need. | Daily 5-rep drill (§7.7) until 32+. |
| 16–23 | This is your bottleneck, not your coding. | Two dedicated 40-rep sessions this week. |
| Under 16 | Patterns are not encoded as retrievable categories at all. | Run §7.3 before anything else. |

## 8.3 The trigger table — memorise this

| Signal in the statement | Reach for | Confirm with |
| --- | --- | --- |
| Longest / shortest contiguous subarray with a constraint | Sliding Window | Is the constraint monotone as the window grows? |
| Count subarrays summing to K, negatives present | Prefix Sum + HashMap | Window logic breaks with negatives |
| Sorted array, find a pair / triplet | Two Pointers | Sorted or sortable without losing the answer |
| K-th largest / smallest / most frequent / closest | Heap | Do I only ever need the extreme? |
| Running median / middle of a stream | Two Heaps | Online queries, not one-shot |
| Minimise the maximum / maximise the minimum | Binary Search on Answer | Is feasible(x) monotone in x? |
| Next / previous greater or smaller | Monotonic Stack | Am I asking about the nearest such element? |
| Number of ways / min cost to reach | Dynamic Programming | Overlapping subproblems + optimal substructure |
| All subsets / permutations / combinations | Backtracking | Output size is exponential — that IS the complexity |
| Connected components / islands / provinces | DFS or Union-Find | Static graph → DSU; needs traversal → DFS |
| Prerequisites / ordering / can it be completed | Topological Sort | Directed, and cycles mean impossible |
| Shortest path, unweighted | BFS | All edges cost the same |
| Shortest path, weighted non-negative | Dijkstra | Negative edges → Bellman-Ford |
| Intervals as [start, end] | Sort + sweep, or heap | Sort key: start for merge, end for scheduling |
| Cycle in a list / midpoint in one pass | Fast & Slow Pointers | O(1) space demanded |
| Max contiguous sum or product | Kadane | Contiguous, not subsequence |
| Prefix matching / autocomplete / word dictionary | Trie | Many queries against a fixed word set |
| Count / set / clear specific bits, subsets of ≤20 items | Bit Manipulation | n ≤ 20 is the tell for bitmask |
| Pick locally best repeatedly and it's provably optimal | Greedy | Can you state the exchange argument? |
