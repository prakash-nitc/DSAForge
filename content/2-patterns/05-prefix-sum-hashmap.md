---
id: card-5
numeral: Card 5
title: Prefix Sum + HashMap
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair + fill | 4 / 6 | L2 | L4 — small set, disproportionately asked |

## Template 5A — COUNT subarrays with sum == k (store frequencies)

```java
Map<Integer,Integer> seen = new HashMap<>();
seen.put(0, 1);                          // the empty prefix — the line people forget
int pre = 0, count = 0;
for (int x : a) {
    pre += x;
    count += seen.getOrDefault(pre - k, 0);
    seen.merge(pre, 1, Integer::sum);
}
```

## Template 5B — LONGEST subarray with a property (store FIRST index)

```java
Map<Integer,Integer> first = new HashMap<>();
first.put(0, -1);                        // prefix 0 exists 'before' index 0
int pre = 0, best = 0;
for (int i = 0; i < n; i++) {
    pre += a[i];
    int key = ((pre % k) + k) % k;        // for divisible-by-k variants
    if (first.containsKey(key)) best = Math.max(best, i - first.get(key));
    else first.put(key, i);               // ONLY if absent
}
```

*Two different maps for two different questions. COUNT stores frequencies and always inserts. LONGEST stores the first index and inserts only if absent. Mixing them up is the silent failure in this pattern.*

## Template 5C — Static range sums

```java
int[] pre = new int[n + 1];
for (int i = 0; i < n; i++) pre[i+1] = pre[i] + a[i];
// sum of a[l..r] inclusive =
int rangeSum = pre[r + 1] - pre[l];
// the +1 offset removes every special case for l == 0
```

## Template 5D — Prefix and suffix products (no division)

```java
int[] res = new int[n];
res[0] = 1;
for (int i = 1; i < n; i++) res[i] = res[i-1] * a[i-1];   // prefix pass
int suf = 1;
for (int i = n - 1; i >= 0; i--) { res[i] *= suf; suf *= a[i]; }   // suffix pass
```

## Template 5E — 2D prefix sum (inclusion–exclusion)

```java
pre[i+1][j+1] = a[i][j] + pre[i][j+1] + pre[i+1][j] - pre[i][j];
// rectangle (r1,c1)..(r2,c2) =
pre[r2+1][c2+1] - pre[r1][c2+1] - pre[r2+1][c1] + pre[r1][c1];
```

## The knobs — what actually varies across this family

- **Count vs longest —** frequency map + always insert, vs first-index map + insert-if-absent.
- **Transformation —** 0 → −1 turns 'equal zeros and ones' into 'sum equals zero'. Modulo turns 'divisible by k' into 'equal remainders'.
- **Dimension —** 1D prefix, 2D prefix, or prefix+suffix pair.

## Trigger signals

- "Number of subarrays with sum K" with negatives present — window logic fails, prefix works
- "Subarray sum divisible by K" → prefix modulo
- "Equal number of 0s and 1s" → map 0 to −1
- Repeated range-sum queries on a static array (1D or 2D)
- "Product of everything except self, without division"

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Subarray Sum Equals K | The base case. If seen.put(0,1) isn't automatic, the card is L1. |
| 2 | Contiguous Array | The 0→−1 transformation plus first-index storage. Two ideas at once. |
| 3 | Subarray Sums Divisible by K | The ((pre % k) + k) % k line. Java's % returns negatives and this breaks silently. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 5A — count | Subarray Sum Equals K · Subarray Sums Divisible by K |
| 5B — longest | Contiguous Array |
| 5C — range | Find Pivot Index |
| Advanced (untouched) | Count Range Sum (needs BIT or merge sort) · Shortest Subarray With Sum at Least K (needs monotonic deque) |

## Decay signatures — how you'll know it's gone

- Missing seen.put(0, 1) — you undercount every subarray starting at index 0.
- Using Java's raw % on negative prefixes.
- Storing the latest index instead of the first on a longest-subarray problem.
- Reaching for sliding window when the array has negatives.

## Java bugs specific to this pattern

- Java's % is remainder, not modulo: −7 % 3 == −1, not 2. Always ((x % k) + k) % k.
- Prefix sums overflow int on 10⁵ elements with values up to 10⁹. Use long[].
- getOrDefault vs get: get returns null and auto-unboxing NPEs.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| 1D prefix + map | O(n) | O(n) |
| Static range query after O(n) build | O(1) per query | O(n) |
| 2D prefix | O(mn) build, O(1) query | O(mn) |

## Interview follow-ups you will be asked

- "Why can't sliding window do this?" — negatives break the monotonicity that shrinking relies on.
- "What if the array is updated between queries?" — prefix sums die; you need a Fenwick tree / BIT with O(log n) update.
- "Space optimise the 2D version?" — process row by row, keeping only the previous row.
- "Why store the first index for longest?" — because a later occurrence of the same prefix can only produce a shorter subarray.

## Additions

- **Product of Array Except Self (LC 238) —** template 5D. Asked everywhere; you have no problem covering it.
- **Continuous Subarray Sum (LC 523) —** prefix modulo with a length constraint. Good discriminator.
- **Range Sum Query 2D — Immutable —** template 5E, if you want the 2D extension.
- **Your two untouched —** both genuine Hards needing BIT/merge-sort or monotonic deque. Defer until Graphs and DP are standing.
