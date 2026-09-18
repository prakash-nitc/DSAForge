---
id: card-10
numeral: Card 10
title: Binary Search (including on the answer)
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Protect — your strongest asset | 20 / 23 | L2, broadest coverage on the board | L4 — do not let this rot |

## Template 10A — Lower bound (use this ONE invariant everywhere)

```java
int lo = 0, hi = n;                    // hi is EXCLUSIVE
while (lo < hi) {
    int mid = lo + (hi - lo) / 2;      // never (lo + hi) / 2
    if (a[mid] >= target) hi = mid;    // predicate true -> shrink right
    else lo = mid + 1;
}
return lo;                             // first index with a[i] >= target; n if none
```

*One invariant for the whole family: converge on the FIRST position where a monotone predicate becomes true. Upper bound is the same loop with > instead of >=. Learn one, derive the rest.*

## Template 10B — Binary search on the ANSWER

```java
long lo = minPossible, hi = maxPossible;
while (lo < hi) {
    long mid = lo + (hi - lo) / 2;
    if (feasible(mid)) hi = mid;       // mid works -> try smaller
    else lo = mid + 1;
}
return lo;                             // smallest feasible answer

boolean feasible(long capacity) {      // the ENTIRE problem lives here
    long groups = 1, cur = 0;
    for (int w : weights) {
        if (w > capacity) return false;
        if (cur + w > capacity) { groups++; cur = 0; }
        cur += w;
    }
    return groups <= maxGroups;
}
```

*Almost every 'minimise the maximum' problem collapses to writing feasible() correctly. Once you internalise this, KOKO, Book Allocation, Split Largest Array, Capacity to Ship and Aggressive Cows are the same problem five times.*

## Template 10C — Rotated sorted array

```java
while (lo <= hi) {
    int mid = lo + (hi - lo) / 2;
    if (a[mid] == target) return mid;
    if (a[lo] <= a[mid]) {                              // LEFT half sorted
        if (a[lo] <= target && target < a[mid]) hi = mid - 1; else lo = mid + 1;
    } else {                                             // RIGHT half sorted
        if (a[mid] < target && target <= a[hi]) lo = mid + 1; else hi = mid - 1;
    }
}
return -1;
```

## Template 10D — Binary search on a 2D matrix

```java
// fully sorted matrix: treat as a flat array of length m*n
int r = mid / cols, cl = mid % cols;

// row-sorted AND column-sorted (Search 2D Matrix II): staircase, O(m+n)
int r2 = 0, c2 = cols - 1;
while (r2 < rows && c2 >= 0) {
    if (mat[r2][c2] == target) return true;
    if (mat[r2][c2] > target) c2--; else r2++;
}
```

## Template 10E — Median of two sorted arrays (partition search)

```java
// binary search the CUT position in the shorter array
int lo = 0, hi = m;                       // m = shorter array length
while (lo <= hi) {
    int i = (lo + hi) / 2;                // cut in A
    int j = (m + n + 1) / 2 - i;          // matching cut in B
    int aL = i == 0 ? MIN : A[i-1], aR = i == m ? MAX : A[i];
    int bL = j == 0 ? MIN : B[j-1], bR = j == n ? MAX : B[j];
    if (aL <= bR && bL <= aR) { /* correct partition -> compute median */ }
    else if (aL > bR) hi = i - 1;
    else lo = i + 1;
}
```

*Your one real gap in this card. Budget 90 minutes and a second pass a week later.*

## The knobs — what actually varies across this family

- **Search space —** an index range, or a range of candidate answers.
- **Predicate —** the monotone boolean; getting its direction right is 90% of the work.
- **Loop form —** lo < hi with hi exclusive (converging) or lo <= hi with an explicit return (exact match).
- **Which half is sorted —** the extra case analysis rotation adds.

## Trigger signals

- Sorted or rotated-sorted array plus a search
- "Minimise the maximum" / "maximise the minimum" — the on-the-answer tell
- "Smallest k such that…" with a monotone feasibility check
- The answer lies in a numeric range and CHECKING a candidate is far cheaper than constructing one
- "Find the k-th smallest" in a structured space (sorted matrix, multiplication table)

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Search in Rotated Sorted Array | The half-sorted case analysis. Highest interview frequency in the family. |
| 2 | KOKO Eating Bananas | The cleanest on-the-answer predicate. If feasible() writes itself, the card is healthy. |
| 3 | Book Allocation Problem | Same shape, harder predicate, plus the 'is it even possible' guard. Confirms transfer. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 10A — bounds | Binary Search · Upper Bound / Ceiling · First and Last Position · Count Number of Occurrences · Search in Infinite Sorted Array |
| 10B — on the answer | KOKO Eating Bananas · Book Allocation Problem · Aggressive Cows · Capacity to Ship Packages in D Days · Split Largest Array · Max Candies to K Children · Minimum Number of Days to Make M Bouquets |
| 10C — rotated | Search in Rotated Sorted Array · Find Minimum in Rotated Sorted Array · Find Number of Rotations in Sorted Array |
| 10D — matrix / peaks | Search 2D Matrix · Search 2D Matrix II · Kth Smallest in Sorted Matrix · Kth Smallest in Multiplication Matrix · Find Peak Element · Peak Index in a Mountain Array · H-Index II |
| 10E — partition | Median of Two Sorted Arrays (untouched) |

## Decay signatures — how you'll know it's gone

- You mix lo <= hi with hi = mid and infinite-loop.
- You write mid = (lo + hi) / 2 and overflow on large ranges.
- You cannot state the monotonicity that makes the predicate valid.
- You use int for a range where the sum of all elements exceeds 2³¹.
- You reach for a linear scan on Find Peak Element instead of noticing the local-slope argument.

## Java bugs specific to this pattern

- (lo + hi) / 2 overflows when both are near Integer.MAX_VALUE. Always lo + (hi - lo) / 2.
- Arrays.binarySearch returns (-insertionPoint - 1) when absent — usable, but write your own for anything non-trivial.
- Collections.binarySearch on a LinkedList is O(n log n), not O(log n).
- Long arithmetic inside feasible() when the accumulator can exceed int range.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Index binary search | O(log n) | O(1) |
| On the answer | O(n · log(range)) | O(1) |
| Rotated array | O(log n) distinct, O(n) worst with duplicates | O(1) |
| Median of two sorted arrays | O(log min(m, n)) | O(1) |

## Interview follow-ups you will be asked

- "Why does binary search still work on a rotated array?" — at least one half is always sorted, so you can always decide which half can contain the target.
- "What breaks with duplicates?" — a[lo] == a[mid] no longer tells you which half is sorted; you shrink by one and worst case becomes O(n).
- "Prove your predicate is monotone." — this is the question that separates people who understand on-the-answer from people who memorised it.
- "Find the peak in O(log n) — why is that even possible without sorting?" — because a local slope argument guarantees a peak in the uphill direction.

## Additions

- **Median of Two Sorted Arrays (your untouched) —** DO IT. The most-asked Hard in the pattern and the one thing missing from an otherwise excellent set.
- **Split Largest Array (your untouched) —** you already have Book Allocation, which is the same problem. Do it anyway; a 15-minute confirmation.
- **Single Element in a Sorted Array —** the parity-index trick. Short, elegant, asked.
- **Kth Smallest in Multiplication Matrix —** skip. Redundant with Kth Smallest in Sorted Matrix.
