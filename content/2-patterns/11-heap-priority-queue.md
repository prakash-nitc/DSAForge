---
id: card-11
numeral: Card 11
title: Heap / Priority Queue
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair + a real gap | 14 / 17 | L2 | L4 + close the two-heaps hole |

## Template 11A — Top K with a size-k heap

```java
// K LARGEST -> keep a MIN-heap of size k
PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[1], y[1]));
for (Map.Entry<Integer,Integer> e : freq.entrySet()) {
    pq.offer(new int[]{ e.getKey(), e.getValue() });
    if (pq.size() > k) pq.poll();          // evict the smallest
}
// K SMALLEST -> keep a MAX-heap of size k
```

*It reads backwards and that is exactly why it decays. Say the reason out loud: the heap root is the thing you are willing to throw away.*

## Template 11B — Two heaps (running median)

```java
PriorityQueue<Integer> lo = new PriorityQueue<>(Comparator.reverseOrder()); // max-heap, lower half
PriorityQueue<Integer> hi = new PriorityQueue<>();                          // min-heap, upper half

void add(int x) {
    lo.offer(x);
    hi.offer(lo.poll());                   // funnel through to keep the split correct
    if (hi.size() > lo.size()) lo.offer(hi.poll());   // rebalance, lo may be larger by 1
}
double median() {
    return lo.size() > hi.size() ? lo.peek() : (lo.peek() + hi.peek()) / 2.0;
}
```

*The funnel (offer to lo, poll from lo into hi) makes correctness automatic — you never have to compare against the current median.*

## Template 11C — Merge k sorted sources

```java
PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));
for (int i = 0; i < k; i++) if (lists[i].length > 0) pq.offer(new int[]{ lists[i][0], i, 0 });
while (!pq.isEmpty()) {
    int[] t = pq.poll();                   // {value, listIndex, elementIndex}
    res.add(t[0]);
    if (t[2] + 1 < lists[t[1]].length)
        pq.offer(new int[]{ lists[t[1]][t[2]+1], t[1], t[2]+1 });
}
```

## Template 11D — Greedy with a heap (task scheduling / reorganise)

```java
PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(y[1], x[1])); // max by count
int[] prev = null;
while (!pq.isEmpty()) {
    int[] cur = pq.poll();
    sb.append((char) cur[0]);
    if (prev != null && prev[1] > 0) pq.offer(prev);   // release the held-back one
    cur[1]--; prev = cur;                              // hold current out for one round
}
```

*The held-back previous element is the whole trick. Without it you place the same character twice in a row.*

## Template 11E — Heap over an interval sweep

```java
// 'always serve the currently best available option' — IPO, refuelling stops
// 1. sort candidates by the gating key (cost, position)
// 2. push everything now reachable into a max-heap keyed by value
// 3. poll the best, advance, repeat
```

## The knobs — what actually varies across this family

- **Min vs max —** decided by what you want to discard, not what you want to keep.
- **Size-bounded vs unbounded —** size-k gives O(n log k); dumping everything in gives O(n log n).
- **What you store —** a value, a (value, index) pair, or a (value, listIdx, elemIdx) triple.
- **One heap or two —** two when you need the middle rather than an extreme.

## Trigger signals

- "K largest / smallest / most frequent / closest"
- "Merge k sorted things"
- Running median or anything about the "middle of a stream" → two heaps
- Greedy where you repeatedly need the current best (tasks, refuelling, IPO)
- "Schedule / allocate to minimise" where you must always serve the extreme

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Top K Frequent Elements | Size-k min-heap discipline plus HashMap counting. Baseline. |
| 2 | Merge K Sorted Arrays | The triple in the heap. Common and easy to half-remember. |
| 3 | Reorganize String | Greedy plus the held-back previous element. Decays first. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 11A — top K | Top K Frequent Elements · Top K Frequent Words · Kth Largest Element in an Array · Kth Smallest Element · K Closest Points to Origin · Find K Closest Elements · Kth Weakest Row in Matrix |
| 11B — two heaps | Find Median from Data Stream (untouched) · Sliding Window Median (untouched) |
| 11C — merge k | Merge K Sorted Arrays · Kth Smallest in Sorted Matrix (Heap) |
| 11D / 11E — greedy | CPU Task Scheduler · Reorganize String · Last Stone Weight · IPO · Minimum Number of Refueling Stops · Course Schedule III (untouched) |

## Decay signatures — how you'll know it's gone

- You build a heap of everything and poll k times instead of keeping size k.
- You write (x, y) -> x[1] - y[1] on values that can overflow.
- You cannot recall which heap holds which half in the two-heap median.
- You forget that PriorityQueue's iterator is NOT in sorted order.
- In Reorganize String you drop the held-back element and emit adjacent duplicates.

## Java bugs specific to this pattern

- PriorityQueue.remove(Object) and contains() are O(n), not O(log n). If you need decrease-key, use a TreeSet or lazy deletion.
- Iterating or printing a PriorityQueue gives heap order, not sorted order — a classic silent wrong answer.
- Comparator subtraction overflows. Comparator.comparingInt(x -> x[1]) is safer and clearer.
- new PriorityQueue<>(k, cmp) — the first argument is initial capacity, not a size cap. There is no size cap; you enforce it yourself.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Build heap from a collection | O(n) | O(n) |
| offer / poll | O(log n) | — |
| Top K with size-k heap | O(n log k) | O(k) |
| Merge k sorted lists, N total elements | O(N log k) | O(k) |
| Two-heap median: add / query | O(log n) / O(1) | O(n) |

## Interview follow-ups you will be asked

- "Top K — heap or quickselect?" — heap is O(n log k) and streaming-friendly; quickselect is O(n) average but destroys the array and is O(n²) worst case.
- "How is a heap actually stored?" — an array; children of i are 2i+1 and 2i+2. Be ready to describe sift-up and sift-down.
- "Why is building a heap O(n) and not O(n log n)?" — the sum over levels telescopes; most nodes are near the bottom and sift down very little.
- "Make the two-heap median support removal." — lazy deletion with a 'to remove' map; this is exactly Sliding Window Median.

## Additions

- **Find Median from Data Stream (your untouched) —** DO THIS. Two-heaps is asked at Oracle, VISA and Flipkart, and you have zero coverage. Highest-priority single addition in the card.
- **Sliding Window Median (your untouched) —** the harder variant with lazy deletion. Only after the above is L4.
- **Kth Largest Element in a Stream —** trivial afterwards, five minutes, good confidence rep.
- **Course Schedule III (your untouched) —** greedy plus a max-heap swap. Genuinely hard. Defer to October.
