---
id: app-e
numeral: Appendix E
title: The pattern decision tree
---

```decision-tree
READ THE CONSTRAINTS FIRST.  n tells you the complexity class (Appendix B3).

Is the input a LINKED LIST?
  |- cycle / midpoint / O(1) space ......... Fast & Slow          (Card 2)
  '- reverse / rotate / group .............. In-place Reversal    (Card 7)

Is the input a TREE?
  |- level by level / views ................ BFS + size freeze    (Shape E)
  |- something about each subtree .......... Bottom-up DFS        (Shape A)
  |- root-to-leaf .......................... Top-down DFS         (Shape B)
  |- it's a BST ............................ Range invariant      (Shape C)
  '- rebuild from traversals ............... Construction         (Shape D)

Is the input a GRAPH or a GRID?
  |- shortest hops, unweighted ............. BFS                  (G1)
  |- components / flood fill ............... DFS or DSU           (G2, G5)
  |- prerequisites / ordering .............. Topological sort     (G3)
  |- weighted, non-negative ................ Dijkstra             (G6)
  '- negative weights or hop limit ......... Bellman-Ford         (G7)

Is it a CONTIGUOUS subarray/substring question?
  |- longest/shortest with a constraint .... Sliding Window       (Card 3)
  |- max sum or product .................... Kadane               (Card 4)
  |- count with sum K, negatives present ... Prefix + HashMap     (Card 5)
  '- max in every window of size k ......... Monotonic deque      (3D)

Is it about ORDER or NEAREST elements?
  |- next/previous greater or smaller ...... Monotonic Stack      (Card 8)
  |- k-th largest / most frequent .......... Heap                 (Card 11)
  |- running median ........................ Two Heaps            (11B)
  '- nearest key above/below ............... TreeMap floor/ceiling

Is the array SORTED, or is the ANSWER monotone?
  |- search in sorted ...................... Binary Search        (10A)
  |- minimise the max / maximise the min ... BS on the answer     (10B)
  '- find a pair/triplet ................... Two Pointers         (Card 1)

Does it ask for ALL of something, or COUNT/MIN of something?
  |- enumerate all ......................... Backtracking         (Card 12)
  |- count ways / min cost ................. Dynamic Programming  (§14)
  '- one locally-best choice, provably ..... Greedy               (§17)

Is it about PREFIXES of strings? ........... Trie                 (§15)
Is n <= 20, or is it about BITS? ........... Bitmask              (§16)
```
