---
id: card-4
numeral: Card 4
title: Kadane's Algorithm
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair | 6 / 6 | L2 | L4 — complete set, fastest card on the board |

## Template 4A — Maximum subarray sum

```java
int cur = a[0], best = a[0];
for (int i = 1; i < n; i++) {
    cur  = Math.max(a[i], cur + a[i]);      // start fresh here, or extend
    best = Math.max(best, cur);
}
return best;
```

*Initialise both to a[0], never to 0. Initialising best = 0 returns 0 for an all-negative array, which is the classic wrong answer.*

## Template 4B — Maximum product subarray (track both extremes)

```java
int mx = a[0], mn = a[0], ans = a[0];
for (int i = 1; i < n; i++) {
    int x = a[i], t = mx;                   // save mx BEFORE overwriting
    mx = Math.max(x, Math.max(mx * x, mn * x));
    mn = Math.min(x, Math.min(t  * x, mn * x));
    ans = Math.max(ans, mx);
}
```

*A negative number swaps the roles of min and max, which is why you must carry both. Forgetting the temp variable t is the standard bug.*

## Template 4C — Circular maximum subarray

```java
int total = 0, maxSum = a[0], curMax = 0, minSum = a[0], curMin = 0;
for (int x : a) {
    curMax = Math.max(curMax + x, x); maxSum = Math.max(maxSum, curMax);
    curMin = Math.min(curMin + x, x); minSum = Math.min(minSum, curMin);
    total += x;
}
return maxSum > 0 ? Math.max(maxSum, total - minSum) : maxSum;   // all-negative guard
```

## Template 4D — Kadane with one deletion (two rolling states)

```java
int keep = a[0], drop = 0, best = a[0];      // keep = no deletion used, drop = one used
for (int i = 1; i < n; i++) {
    drop = Math.max(drop + a[i], keep);      // delete a[i], or carry an earlier deletion
    keep = Math.max(keep + a[i], a[i]);
    best = Math.max(best, Math.max(keep, drop));
}
```

*This is the moment Kadane visibly becomes DP: two states instead of one. Say that out loud when you start §14 and DP stops feeling like a new continent.*

## The knobs — what actually varies across this family

- **Sum vs product —** product needs both extremes carried because negatives flip them.
- **Linear vs circular —** circular = max(normal Kadane, total − minimum-subarray), plus the all-negative guard.
- **Number of rolling states —** one for plain Kadane, two for one-deletion, k+1 for k-deletions.

## Trigger signals

- "Maximum / minimum sum or product of a CONTIGUOUS subarray"
- Circular array version of the same
- "...with at most one deletion / one modification"
- Any O(n) optimisation problem where the answer either extends a run or starts a new one

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Maximum Subarray Sum | The 90-second sanity check. If this is slow, the whole card is L1. |
| 2 | Maximum Product Subarray | The min/max swap and the temp-variable trap. Decays fast. |
| 3 | Maximum Sum Circular Subarray | The total-minus-min trick plus the all-negative edge case most people miss. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 4A | Maximum Subarray Sum · Smallest Sum Contiguous Subarray · Maximum Absolute Sum of Any Subarray |
| 4B | Maximum Product Subarray |
| 4C | Maximum Sum Circular Subarray |
| 4D | Maximum Subarray Sum with One Deletion |

## Decay signatures — how you'll know it's gone

- best initialised to 0, returning 0 on an all-negative array.
- In the product version you use the already-updated mx when computing mn.
- You forget the all-negative guard in the circular version.
- You cannot articulate the DP recurrence behind cur = max(a[i], cur + a[i]).
- Maximum Absolute Sum: you run Kadane once instead of twice (max subarray and min subarray, then take the larger magnitude).

## Java bugs specific to this pattern

- Products overflow int fast. Use long, or note the problem's guarantee that results fit.
- Math.abs(Integer.MIN_VALUE) is still Integer.MIN_VALUE — relevant to the absolute-sum variant.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| All variants | O(n) | O(1) |

## Interview follow-ups you will be asked

- "Return the indices, not just the sum." — track the start index whenever you restart the run.
- "Why is greedy correct here?" — because a prefix with negative sum can never help a later subarray; dropping it is always at least as good.
- "What if I want the maximum sum of exactly k elements, not contiguous?" — different problem: sort or heap.
- "2D version?" — fix a pair of rows, compress columns, run Kadane. O(n²m).

## Additions

- **Best Time to Buy and Sell Stock (LC 121) —** literally Kadane in disguise. Free problem, and it is the doorway into the DP-on-stocks family in §14.
- **Maximum Sum of Two Non-Overlapping Subarrays —** good stretch if you have slack, not required.
