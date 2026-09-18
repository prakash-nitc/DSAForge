---
id: card-6
numeral: Card 6
title: Merge Intervals
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair | 5 / 7 | L2 | L4 — cheap and asked constantly |

## Template 6A — Merge overlapping (sort by START)

```java
Arrays.sort(iv, (x, y) -> Integer.compare(x[0], y[0]));
List<int[]> out = new ArrayList<>();
int[] cur = iv[0];
for (int i = 1; i < iv.length; i++) {
    if (iv[i][0] <= cur[1]) cur[1] = Math.max(cur[1], iv[i][1]);   // overlap
    else { out.add(cur); cur = iv[i]; }
}
out.add(cur);                                     // the line people forget
```

## Template 6B — Maximum non-overlapping (sort by END, greedy)

```java
Arrays.sort(iv, (x, y) -> Integer.compare(x[1], y[1]));   // by END
int count = 0, lastEnd = Integer.MIN_VALUE;
for (int[] v : iv)
    if (v[0] >= lastEnd) { count++; lastEnd = v[1]; }
// removals needed = n - count
```

*Sorting by end is what makes the greedy provably optimal: finishing earliest leaves the most room for everything after. You do not currently have any problem using this shape.*

## Template 6C — Resource counting (sort by start + min-heap of ends)

```java
Arrays.sort(iv, (x, y) -> Integer.compare(x[0], y[0]));
PriorityQueue<Integer> ends = new PriorityQueue<>();
for (int[] m : iv) {
    if (!ends.isEmpty() && ends.peek() <= m[0]) ends.poll();   // a room freed up
    ends.add(m[1]);
}
return ends.size();                               // peak concurrency
```

## Template 6D — Difference array / sweep line

```java
TreeMap<Integer,Integer> delta = new TreeMap<>();
for (int[] v : iv) { delta.merge(v[0], 1, Integer::sum); delta.merge(v[1], -1, Integer::sum); }
int running = 0, peak = 0;
for (int d : delta.values()) { running += d; peak = Math.max(peak, running); }
```

*The sweep is often cleaner than the heap and generalises to 'how many active at time t'. Worth knowing both.*

## Template 6E — Insert into a sorted set without re-sorting

```java
int i = 0, n = iv.length;
while (i < n && iv[i][1] < ni[0]) out.add(iv[i++]);            // strictly before
while (i < n && iv[i][0] <= ni[1]) {                            // overlapping
    ni[0] = Math.min(ni[0], iv[i][0]);
    ni[1] = Math.max(ni[1], iv[i][1]); i++;
}
out.add(ni);
while (i < n) out.add(iv[i++]);                                 // strictly after
```

## The knobs — what actually varies across this family

- **Sort key —** start for merging, end for scheduling greedy. Choosing wrong costs the whole problem.
- **Touching counts as overlap? —** decides < vs <=. Always ask; never assume.
- **What you produce —** merged list, a count of removals, peak concurrency, or a boolean feasibility.

## Trigger signals

- Any input shaped as [start, end] pairs
- "Merge", "overlap", "conflict", "how many rooms / platforms / CPUs"
- "Insert a new interval into a sorted set"
- "Maximum number of non-overlapping" or "minimum removals" → sort by end
- "How many active at time t" → sweep

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Merge Intervals | The base. Should take four minutes flat. |
| 2 | Minimum Meeting Rooms | The heap variant — a different mental model on the same input shape. |
| 3 | Insert Interval | The three-phase linear walk without re-sorting. Tests precision, not insight. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 6A — merge | Merge Intervals · Overlapping Intervals · Intervals Intersection |
| 6C / 6D — concurrency | Minimum Meeting Rooms · Maximum CPU Load · Employee Free Time |
| 6E — insert | Insert Interval |
| 6B — scheduling greedy | Nothing on your sheet. This is the gap. |

## Decay signatures — how you'll know it's gone

- Sorting by end when you need start, or the reverse.
- Using < instead of <= for touching intervals when touching counts as overlap.
- Forgetting the final out.add(cur) after the loop.
- Re-sorting inside Insert Interval instead of the linear walk.

## Java bugs specific to this pattern

- (x, y) -> x[0] - y[0] overflows when coordinates are near Integer.MAX_VALUE. Always Integer.compare.
- out.toArray(new int[0][]) is the correct conversion; toArray() alone gives Object[].
- Mutating cur in place also mutates the original array element — clone if the caller needs the input intact.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Merge / insert after sort | O(n log n), O(n) if pre-sorted | O(n) output |
| Heap concurrency | O(n log n) | O(n) |
| Sweep with TreeMap | O(n log n) | O(n) |

## Interview follow-ups you will be asked

- "Why is sorting by end optimal for scheduling?" — the exchange argument: swapping in the earliest-ending compatible interval never makes the solution worse.
- "What if intervals arrive as a stream?" — you need a TreeMap keyed by start with floorKey/ceilingKey; this is the Calendar problem family.
- "Weighted version — maximise total value, not count?" — greedy fails; it becomes DP with binary search (weighted interval scheduling).
- "What if endpoints are floating point or dates?" — same logic, different comparator; watch equality semantics.

## Additions

- **Non-overlapping Intervals (LC 435) —** template 6B. You have no problem using the sort-by-end greedy and it is asked often.
- **Car Pooling / My Calendar I —** the sweep form. One problem, large conceptual payoff.
- **Your two untouched —** Employee Free Time is worth doing eventually; Maximum CPU Load is redundant with Minimum Meeting Rooms. Defer both past Graphs.
