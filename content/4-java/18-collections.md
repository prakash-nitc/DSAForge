---
id: s18
numeral: §18
title: Collections — what to use, and what it costs
---

| Structure | Use for | Key ops | Complexity |
| --- | --- | --- | --- |
| ArrayList | Default list. Random access. | get, add, set | O(1) get, amortised O(1) add, O(n) insert-at-index |
| ArrayDeque | Stack AND queue. Your default for both. | push/pop/peek, offer/poll | O(1) all |
| HashMap | Key→value, unordered | get, put, merge, computeIfAbsent | O(1) average, O(log n) worst since Java 8 |
| HashSet | Membership, dedup | add, contains | O(1) average |
| TreeMap | Sorted keys, range queries | floorKey, ceilingKey, firstKey, subMap | O(log n) |
| TreeSet | Sorted set, nearest-value | floor, ceiling, higher, lower | O(log n) |
| PriorityQueue | Always need the extreme | offer, poll, peek | O(log n) offer/poll, O(1) peek, O(n) contains |
| LinkedHashMap | Insertion or access order; LRU | same as HashMap + ordering | O(1) average |
| StringBuilder | Any string built in a loop | append, reverse, deleteCharAt | amortised O(1) append |
| int[] / char[] | Fixed small alphabet counting | direct indexing | O(1), and far faster than a map |

> [!TIP]
> **Three defaults that make you look experienced**
>
> ArrayDeque, never Stack or LinkedList. Stack is a synchronised legacy class; LinkedList has terrible cache behaviour. Interviewers notice.
>
> StringBuilder, never string concatenation in a loop. Concatenation in a loop is O(n²).
>
> int[26] for lowercase counting, never a HashMap. Faster, simpler, and it signals you think about constants.

## 18.1 The decision table

| I need… | Use |
| --- | --- |
| LIFO or FIFO | ArrayDeque |
| The largest / smallest, repeatedly | PriorityQueue |
| The nearest key above or below x | TreeMap.ceilingKey / floorKey |
| Counting occurrences | int[26] if the alphabet is fixed, else HashMap + merge |
| Grouping by a computed key | HashMap + computeIfAbsent |
| Order-preserving map | LinkedHashMap |
| Sorted iteration | TreeMap, or sort a list once |
| Fast membership on integers in a bounded range | boolean[] — beats HashSet decisively |
| A pair or triple in a collection | int[] — cheap, mutable, and comparator-friendly |
