---
id: app-b
numeral: Appendix B
title: Complexity master table
---

## B1 · Data structures

| Structure | Access | Search | Insert | Delete | Space |
| --- | --- | --- | --- | --- | --- |
| Array | O(1) | O(n) | O(n) | O(n) | O(n) |
| Sorted array | O(1) | O(log n) | O(n) | O(n) | O(n) |
| ArrayList | O(1) | O(n) | O(1) amortised | O(n) | O(n) |
| Linked list | O(n) | O(n) | O(1) at head | O(1) given node | O(n) |
| HashMap / HashSet | — | O(1) avg | O(1) avg | O(1) avg | O(n) |
| TreeMap / TreeSet | — | O(log n) | O(log n) | O(log n) | O(n) |
| Heap | O(1) peek | O(n) | O(log n) | O(log n) | O(n) |
| ArrayDeque | O(1) ends | O(n) | O(1) | O(1) | O(n) |
| Trie | — | O(L) | O(L) | O(L) | O(chars × Σ) |
| Union-Find | — | ≈O(1) | ≈O(1) | — | O(n) |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) |
| BST (skewed) | O(n) | O(n) | O(n) | O(n) | O(n) |

## B2 · Algorithms

| Algorithm | Best | Average | Worst | Space | Stable |
| --- | --- | --- | --- | --- | --- |
| Quicksort | O(n log n) | O(n log n) | O(n²) | O(log n) | No |
| Mergesort | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes |
| Heapsort | O(n log n) | O(n log n) | O(n log n) | O(1) | No |
| Counting sort | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes |
| Binary search | O(1) | O(log n) | O(log n) | O(1) | — |
| BFS / DFS | O(V + E) | O(V + E) | O(V + E) | O(V) | — |
| Dijkstra (heap) | — | O((V+E) log V) | — | O(V) | — |
| Bellman-Ford | — | O(V·E) | — | O(V) | — |
| Floyd–Warshall | — | O(V³) | — | O(V²) | — |
| Kruskal / Prim | — | O(E log E) | — | O(V) | — |
| Kahn topological | — | O(V + E) | — | O(V) | — |

*Java note: Arrays.sort on primitives is dual-pivot quicksort (not stable, O(n²) adversarial worst case). On objects it is TimSort — stable, O(n log n) guaranteed.*

## B3 · Constraint → target complexity

| n up to | Target | Algorithm class |
| --- | --- | --- |
| 10–12 | O(n!) | Full permutation search |
| 15–20 | O(2ⁿ), O(2ⁿ·n) | Subsets, bitmask DP |
| 50–100 | O(n⁴), O(n³) | Floyd–Warshall, interval DP |
| 500 | O(n³) | Partition DP, matrix chain |
| 5,000 | O(n²) | 2D DP, LCS, edit distance |
| 10⁵ | O(n log n) | Sort, heap, binary search, Dijkstra |
| 10⁶ | O(n) | Single pass, prefix, window, counting |
| 10⁹+ | O(log n), O(1) | BS on answer, closed form |
