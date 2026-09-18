---
id: app-d
numeral: Appendix D
title: The complete 176-problem index
---

Every row from your tracker, with a priority so that no late-night decision is ever ambiguous.

| Code | Meaning |
| --- | --- |
| A | Anchor — permanent rotation |
| 1 | Do it — high frequency or a real gap |
| 2 | Do it if you have slack |
| 3 | Low value — only after everything else |
| × | Skip in September. Binding. |

## Two Pointers — 9 / 12

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Triplet Sum to Zero | Revised | A | All three dedup positions |
| Sort Colors (Dutch National Flag) | Revised | A | Don't advance mid on high-swap |
| Subarrays with Product Less than Target | Revised | A | Count is r−l+1 |
| Pair with Target Sum | Revised | 1 |  |
| Rearrange 0 and 1 | Revised | 1 | Write-pointer shape |
| Remove Duplicates | Revised | 1 |  |
| Squaring a Sorted Array | Revised | 1 | Merge from both ends |
| Triplet Sum Close to Target | Revised | 1 |  |
| Triplets with Smaller Sum | Revised | 2 |  |
| Comparing Strings containing Backspaces | Not started | 2 | String two-pointer from the back |
| Minimum Window Sort | Not started | 2 |  |
| Quadruple Sum to Target | Not started | × | 3Sum + one loop, no new idea |

## Fast & Slow Pointers — 7 / 8

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Start of LinkedList Cycle | Solved | A | Know the entry-point proof |
| Find Duplicate Number | Solved | A | Array as implicit list |
| Palindrome LinkedList | Solved | A | Composite: mid + reverse |
| LinkedList Cycle | Solved | 1 |  |
| Middle of the LinkedList | Solved | 1 |  |
| Happy Number | Solved | 2 |  |
| Rearrange a LinkedList | Solved | 2 |  |
| Cycle in a Circular Array | Not started | × | Hard, low frequency |

## Sliding Window — 7 / 11

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| No-repeat Substring | Solved | A |  |
| Longest Substring w/ Same Letters after Replacement | Solved | A | maxFreq stays monotone |
| Smallest Subarray with given sum | Solved | A | Record inside the while |
| Longest Substring with K Distinct Characters | Solved | 1 |  |
| Fruits into Baskets | Solved | 1 | = at most 2 distinct |
| Maximum Sum Subarray of Size K | Solved | 1 | Fixed window |
| Minimum Size Substring | Solved | 1 |  |
| Longest Subarray with Ones after Replacement | Not started | 1 | Medium in practice |
| Permutation in a String | Not started | 2 | Do this OR String Anagrams |
| String Anagrams | Not started | 3 | Duplicate of the above |
| Words Concatenation | Not started | × | High cost, low value |

## Kadane's Algorithm — 6 / 6

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Maximum Subarray Sum | Solved | A | 90-second sanity check |
| Maximum Product Subarray | Solved | A | Temp variable trap |
| Maximum Sum Circular Subarray | Solved | A | All-negative guard |
| Maximum Subarray Sum with One Deletion | Solved | 1 | Two rolling states = DP |
| Maximum Absolute Sum of Any Subarray | Solved | 2 | Run Kadane twice |
| Smallest Sum Contiguous Subarray | Solved | 2 |  |

## Prefix Sum — 4 / 6

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Subarray Sum Equals K | Solved | A | seen.put(0,1) |
| Contiguous Array | Solved | A | Map 0 → −1 |
| Subarray Sums Divisible by K | Solved | A | ((pre%k)+k)%k |
| Find Pivot Index | Solved | 1 |  |
| Count Range Sum | Not started | × | Needs BIT or merge sort |
| Shortest Subarray With Sum at Least K | Not started | × | Needs monotonic deque |

## Merge Intervals — 5 / 7

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Merge Intervals | Solved | A | Four minutes flat |
| Minimum Meeting Rooms | Solved | A | Heap variant |
| Insert Interval | Solved | A | Three-phase linear walk |
| Overlapping Intervals | Solved | 1 |  |
| Intervals Intersection | Solved | 1 |  |
| Employee Free Time | Not started | 3 | Worth doing eventually |
| Maximum CPU Load | Not started | × | Redundant with Meeting Rooms |

## In-place LL Reversal — 5 / 6

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Reverse a Sub-list | Solved | A | Boundary precision |
| Reverse every K-element Sub-list | Solved | A | Full group machinery |
| Rotate a LinkedList | Solved | A | k %= len |
| Reverse a LinkedList | Solved | 1 | Save, flip, advance, advance |
| Reverse List in Pairs | Solved | 1 | k = 2 |
| Reverse nodes in EVEN Length Groups | Not started | × | Fiddly, no new idea |

## Stack & Monotonic Stack — 8 / 11

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Next Greater Element | Solved | A | The knob check |
| Daily Temperatures | Solved | A | Same template, different noun |
| Remove All Adjacent Duplicates in String II | Solved | A | (char, count) pairs |
| Next Greater Element II | Solved | 1 | Circular: loop 2n with i%n |
| Previous Greater Element | Solved | 1 |  |
| Previous Smaller Element | Solved | 1 |  |
| Balanced Parentheses | Solved | 1 |  |
| Remove Adjacent Duplicates | Solved | 2 |  |
| Remove K Digits | Not started | 1 | Greedy-monotonic bridge |
| Simplify Path | Not started | 1 | 15 minutes, appears in OAs |
| Remove Nodes From Linked List | Not started | 2 | Monotonic stack on a list |

## Hash Maps — 4 / 4

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Longest Palindrome | Solved | A | Parity reasoning |
| First Non-repeating Character | Solved | A | Two passes or LinkedHashMap |
| Ransom Note | Solved | A | 30-second warm-up |
| Maximum Number of Balloons | Solved | 2 |  |

## Binary Search — 20 / 23  (your strongest pattern)

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Search in Rotated Sorted Array | Solved | A | Half-sorted case analysis |
| KOKO Eating Bananas | Solved | A | Cleanest predicate |
| Book Allocation Problem | Solved | A | Harder predicate + feasibility guard |
| Aggressive Cows | Solved | 1 | On the answer |
| Capacity to Ship Packages in D Days | Solved | 1 | On the answer |
| Split Largest Array | Not started | 1 | = Book Allocation; 15-min confirm |
| Median of Two Sorted Arrays | Not started | 1 | DO IT — the one real gap |
| Binary Search | Solved | 1 |  |
| Upper Bound / Ceiling | Solved | 1 |  |
| First and Last Position | Solved | 1 |  |
| Find Minimum in Rotated Sorted Array | Solved | 1 |  |
| Find Peak Element | Solved | 1 | Local-slope argument |
| Search 2D Matrix | Solved | 1 | Flatten to 1D |
| Search 2D Matrix II | Solved | 1 | Staircase, O(m+n) |
| Minimum Number of Days to Make M Bouquets | Solved | 2 |  |
| Max Candies to K Children | Solved | 2 |  |
| Kth Smallest in Sorted Matrix | Solved | 2 |  |
| Count Number of Occurrences | Solved | 2 |  |
| Find Number of Rotations in Sorted Array | Solved | 2 |  |
| Peak Index in a Mountain Array | Solved | 2 |  |
| H-Index II | Solved | 2 |  |
| Search in Infinite Sorted Array | Solved | 3 | Exponential probing |
| Kth Smallest in Multiplication Matrix | Not started | × | Redundant |

## Heap / Priority Queue — 14 / 17

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Top K Frequent Elements | Solved | A | Size-k min-heap |
| Merge K Sorted Arrays | Solved | A | (value, listIdx, elemIdx) |
| Reorganize String | Solved | A | Held-back previous element |
| Find Median from Data Stream | Not started | 1 | TOP PRIORITY — no two-heap coverage |
| Kth Largest Element in an Array | Solved | 1 |  |
| Kth Smallest Element | Solved | 1 |  |
| K Closest Points to Origin | Solved | 1 |  |
| CPU Task Scheduler | Solved | 1 | Know the formula solution too |
| Find K Closest Elements | Solved | 2 |  |
| Kth Smallest in Sorted Matrix (Heap) | Solved | 2 |  |
| Kth Weakest Row in Matrix | Solved | 2 |  |
| Last Stone Weight | Solved | 2 |  |
| Top K Frequent Words | Solved | 2 | Comparator with tie-break |
| IPO | Solved | 2 |  |
| Minimum Number of Refueling Stops | Solved | 2 |  |
| Sliding Window Median | Not started | 3 | After Find Median is L4 |
| Course Schedule III | Not started | × | Genuinely hard; October |

## Recursion & Backtracking — 11 / 11

| Problem | Status | P | Note |
| --- | --- | --- | --- |
| Permutations | Solved | A | used[] shape |
| Combination Sum | Solved | A | Recurse on i, not i+1 |
| Palindrome Partitioning | Solved | A | Validity check in the loop |
| Generate Parentheses | Solved | 1 |  |
| Letter Combinations of a Phone Number | Solved | 1 |  |
| Pow(x,n) | Solved | 1 | Divide & conquer; long for −MIN_VALUE |
| Fibonacci Number | Solved | 2 | Doorway to DP |
| Check if Array is Sorted | Solved | 3 |  |
| Check if String is Palindrome | Solved | 3 |  |
| Remove Occurrences of a Character in String | Solved | 3 |  |
| Sum of Digits of a Number | Solved | 3 |  |

## Trees — 11 / 31

| Problem | Status | P | Shape / note |
| --- | --- | --- | --- |
| Binary Tree Level Order Traversal | Solved | A | E — the size freeze |
| Binary Tree Zigzag Level Order Traversal | Solved | A | E — reverse alternate levels |
| Symmetric Tree | Solved | A | F — mirror recursion |
| Binary Tree Inorder Traversal | Solved | 1 | Add the iterative version |
| Binary Tree Preorder Traversal | Solved | 1 |  |
| Binary Tree Postorder Traversal | Solved | 1 | Iterative = preorder swapped, reversed |
| Binary Tree Level Order Traversal II | Solved | 2 | E — reverse the outer list |
| Invert Binary Tree | Solved | 2 | F |
| Same Tree | Solved | 2 | F |
| Subtree of Another Tree | Solved | 2 | F |
| Flip Equivalent Binary Trees | Solved | 2 | F |
| Maximum Depth of Binary Tree | Not started | 1 | A — start here |
| Minimum Depth of Binary Tree | Not started | 1 | A — single-child trap |
| Balanced Binary Tree | Not started | 1 | A — −1 sentinel |
| Diameter of Binary Tree | Not started | 1 | A — return vs record |
| LCA of Binary Tree | Not started | 1 | A — four lines |
| Binary Tree Maximum Path Sum | Not started | 1 | A — max(0, child) guard |
| LCA of Deepest Leaves | Not started | 2 | A |
| Path Sum | Not started | 1 | B — leaf ≠ null |
| Path Sum II | Not started | 1 | B + backtracking |
| Sum Root to Leaf Numbers | Not started | 1 | B |
| Search in a Binary Search Tree | Not started | 1 | C — warm-up |
| LCA of BST | Not started | 1 | C — three lines |
| Validate BST | Not started | 1 | C — range narrowing, use long |
| Kth Smallest Element in a BST | Not started | 1 | C — inorder is sorted |
| Two Sum IV - BST | Not started | 2 | C — inorder + two pointers |
| Recover BST | Not started | 2 | C — first and last violation |
| Construct Tree from Preorder and Inorder | Not started | 1 | D — HashMap or O(n²) |
| Construct Tree from Postorder and Inorder | Not started | 1 | D — build RIGHT first |
| Convert Sorted Array to BST | Not started | 1 | D — degenerate case |
| Check Completeness of Binary Tree | Not started | 2 | E — BFS, no gaps after a null |

## Graphs — 0 / 20  (highest OA risk on the board)

| Problem | Status | P | Shape / note |
| --- | --- | --- | --- |
| Number of Islands | Not started | A | G2 — Day 1 |
| Rotting Oranges | Not started | 1 | G1 multi-source — Day 1 |
| Surrounded Regions | Not started | 1 | G2 border trick — Day 1 |
| Graph BFS | Not started | 1 | G1 — Day 1 |
| Graph DFS | Not started | 1 | G2 — Day 1 |
| Shortest Path in Non-Weighted Graph | Not started | 1 | G1 — Day 1 |
| Topological Sort | Not started | A | G3 — Day 2 |
| Cycle Detection in Directed Graph | Not started | 1 | G4 three-colour — Day 2 |
| Cycle Detection in Undirected Graph | Not started | 1 | G4 parent DFS — Day 2 |
| Number of Provinces | Not started | A | G5 DSU — Day 3 |
| Construct Adjacency List from Edges | Not started | 1 | G0 — Day 3 |
| Dijkstra's Algorithm | Not started | 1 | G6 — Day 4 |
| Network Delay Time | Not started | 1 | G6 — Day 4 |
| Path With Minimum Effort | Not started | 1 | G6 with max-relaxation — Day 4 |
| Cheapest Flights Within K Stops | Not started | 1 | G7 — NOT plain Dijkstra |
| Bellman-Ford Algorithm | Not started | 2 | G7 — Day 4 |
| Bipartite Graph / Graph Coloring | Not started | 2 | G8 — Day 5 |
| Word Ladder | Not started | 2 | BFS on an implicit graph — Day 5 |
| Prim's MST | Not started | 3 | G8 — October |
| Swim in Rising Water | Not started | 3 | Dijkstra or BS + DFS — October |

## Dynamic Programming — 0 / 3 on the sheet (see §14 for the real set)

| Problem | Status | P | Shape / note |
| --- | --- | --- | --- |
| Climbing Stairs | Not started | 1 | D1 — run the four-step ladder explicitly |
| House Robber | Not started | 1 | D1 — first real take/skip choice |
| Fibonacci Number (DP) | Not started | 2 | D1 — memo vs tabulation demo |

## Not on your sheet — the nine Tier-1 additions

| Problem | Pattern | Why it's non-negotiable |
| --- | --- | --- |
| Subsets (LC 78) | Backtracking | The archetype of the pattern; absent from your sheet entirely |
| Subsets II (LC 90) | Backtracking | The dedup variant; 20 minutes after LC 78 |
| Largest Rectangle in Histogram (LC 84) | Monotonic Stack | Highest-value stack problem in existence |
| Find Median from Data Stream (LC 295) | Two Heaps | You have zero two-heap coverage |
| Sliding Window Maximum (LC 239) | Monotonic Deque | Bridges window and stack; very high frequency |
| Median of Two Sorted Arrays (LC 4) | Binary Search | The one gap in an otherwise excellent set |
| Course Schedule I + II (LC 207/210) | Topological Sort | The most-asked graph band at your targets |
| Product of Array Except Self (LC 238) | Prefix/Suffix | Asked everywhere; no coverage on your sheet |
| Non-overlapping Intervals (LC 435) | Greedy Intervals | The sort-by-END shape you don't have |
