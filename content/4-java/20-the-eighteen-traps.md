---
id: s20
numeral: §20
title: The eighteen traps
---

Every one of these produces a wrong answer or a crash that is hard to see by reading. Most have cost people offers.

| # | Trap | The fix |
| --- | --- | --- |
| 1 | (lo + hi) / 2 overflows for large indices or ranges | lo + (hi - lo) / 2 |
| 2 | Comparator written as a - b overflows near MAX_VALUE | Integer.compare(a, b) |
| 3 | Java's % returns a negative for negative operands | ((x % k) + k) % k |
| 4 | int sums overflow silently at ~2.1 billion | Use long for sums, products, and BS-on-answer ranges |
| 5 | Integer == compares references outside −128..127 | .equals() or unbox to int first |
| 6 | map.get() returns null and NPEs on auto-unboxing | getOrDefault |
| 7 | List<Integer>.remove(int) is by INDEX, remove(Integer) by value | list.remove(list.size()-1) for backtracking |
| 8 | Arrays.asList() and List.of() are fixed-size / immutable | new ArrayList<>(Arrays.asList(...)) |
| 9 | Modifying a collection while iterating it | Iterator.remove(), or removeIf() |
| 10 | PriorityQueue iteration is NOT sorted order | Poll repeatedly if you need sorted output |
| 11 | PriorityQueue.remove(Object) is O(n) | Lazy deletion, or use a TreeSet |
| 12 | ArrayDeque cannot hold null | Use a sentinel value, or a different structure |
| 13 | String concatenation inside a loop is O(n²) | StringBuilder |
| 14 | >> preserves the sign; a loop shifting a negative never terminates | >>> for unsigned shift |
| 15 | Math.abs(Integer.MIN_VALUE) is still negative | Widen to long before taking the absolute value |
| 16 | 2D array clone() is shallow — rows are shared | Clone each row, or use a stream copy |
| 17 | Recursion depth beyond ~10⁴ frames throws StackOverflowError | Convert to iterative, or bound the depth |
| 18 | Mutating an object used as a HashMap key | Never mutate keys; the entry becomes unreachable |
