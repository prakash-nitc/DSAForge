---
id: card-3
numeral: Card 3
title: Sliding Window
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair + fill | 7 / 11 | L2 | L4 + close two of the four gaps |

## Template 3A — Variable window: LONGEST satisfying a condition

```java
int l = 0, best = 0;
Map<Character,Integer> cnt = new HashMap<>();
for (int r = 0; r < n; r++) {
    cnt.merge(s.charAt(r), 1, Integer::sum);          // 1. expand
    while (invalid(cnt)) {                            // 2. shrink WHILE broken
        char ch = s.charAt(l);
        if (cnt.merge(ch, -1, Integer::sum) == 0) cnt.remove(ch);
        l++;
    }
    best = Math.max(best, r - l + 1);                 // 3. record AFTER the while
}
```

## Template 3B — Variable window: SHORTEST satisfying a condition

```java
int l = 0, best = Integer.MAX_VALUE; long sum = 0;
for (int r = 0; r < n; r++) {
    sum += a[r];
    while (sum >= target) {                           // shrink WHILE valid
        best = Math.min(best, r - l + 1);             // record INSIDE, before shrinking
        sum -= a[l++];
    }
}
return best == Integer.MAX_VALUE ? 0 : best;
```

*3A and 3B differ in exactly two places: the while condition, and where you record. Getting them backwards is the number-one sliding-window error and it is silent — the code runs and returns the wrong answer.*

## Template 3C — Fixed window of size k

```java
long sum = 0;
for (int r = 0; r < n; r++) {
    sum += a[r];
    if (r >= k) sum -= a[r - k];                      // evict the element leaving
    if (r >= k - 1) best = Math.max(best, sum);       // window is full
}
```

## Template 3D — Monotonic deque (sliding window maximum)

```java
Deque<Integer> dq = new ArrayDeque<>();               // holds INDICES, values decreasing
for (int r = 0; r < n; r++) {
    while (!dq.isEmpty() && dq.peekFirst() <= r - k) dq.pollFirst();   // expire
    while (!dq.isEmpty() && a[dq.peekLast()] <= a[r]) dq.pollLast();   // dominate
    dq.offerLast(r);
    if (r >= k - 1) res[r - k + 1] = a[dq.peekFirst()];
}
```

*The bridge between sliding window and monotonic stack. You currently have zero problems using this and it is asked often.*

## Template 3E — 'At most K' → 'exactly K' by subtraction

```java
int exactlyK(int[] a, int k) { return atMost(a, k) - atMost(a, k - 1); }
// atMost() is a standard 3A window. This trick converts a hard problem into two easy ones.
```

## The knobs — what actually varies across this family

- **Longest vs shortest —** decides the while condition (shrink while invalid vs while valid) and where you record.
- **Fixed vs variable size —** fixed uses an index-based eviction; variable uses a condition-based one.
- **The state you carry —** a running sum, a frequency map, a distinct-count, or a max via deque.
- **Validity function —** the whole problem usually reduces to writing invalid() correctly.

## Trigger signals

- "Longest / shortest contiguous subarray or substring with property P"
- "At most K distinct / at most K replacements / at most K zeros"
- Fixed-size k window with a running aggregate
- Anagram or permutation containment in a string
- "Maximum in every window of size k" → monotonic deque
- Warning: negatives usually break window logic — check before committing

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | No-repeat Substring | Canonical variable window with a map. Baseline health check. |
| 2 | Longest Substring with Same Letters after Replacement | Needs the maxFreq trick and the window-never-shrinks insight. Decays first. |
| 3 | Smallest Subarray with given sum | The shortest variant — proves you know the record-inside-the-while rule. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 3A — longest | No-repeat Substring · Longest Substring with K Distinct Characters · Longest Substring with Same Letters after Replacement · Fruits into Baskets · Longest Subarray with Ones after Replacement |
| 3B — shortest | Smallest Subarray with given sum · Minimum Size Substring |
| 3C — fixed | Maximum Sum Subarray of Size K · Permutation in a String · String Anagrams · Words Concatenation |
| 3D — deque | Nothing on your sheet. This is the gap. |

## Decay signatures — how you'll know it's gone

- You record outside the while on a shortest problem, or inside on a longest one.
- In the replacement problem you recompute maxFreq every iteration instead of letting it stay monotone.
- You don't remove a key at count zero, so your distinct-count is silently wrong.
- You reach for a window on an array with negatives where the monotonicity doesn't hold.
- Fruits into Baskets: you don't recognise it as 'longest substring with at most 2 distinct'.

## Java bugs specific to this pattern

- cnt.merge(ch, -1, Integer::sum) returns the NEW value — comparing it to 0 is correct; comparing cnt.get(ch) after removal NPEs.
- Using int for sums in a shortest-subarray problem with large values. Use long.
- ArrayDeque cannot hold null. Never store a null sentinel.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Variable / fixed window | O(n) — each element enters and leaves once | O(k) or O(alphabet) |
| Monotonic deque | O(n) amortised | O(k) |
| 'Exactly K' via two 'at most' passes | O(n) | O(k) |

## Interview follow-ups you will be asked

- "Why is this O(n) when there's a nested while?" — amortised: each index is added once and removed at most once.
- "What breaks with negative numbers?" — the sum is no longer monotone in window size, so shrinking is no longer safe.
- "Can you do it with O(1) space?" — yes when the alphabet is fixed (int[26] instead of a HashMap).
- "How would you handle a stream instead of an array?" — the same window, but you cannot look ahead; discuss what that costs.

## Additions

- **Sliding Window Maximum (LC 239) —** MISSING and important. Monotonic deque, high frequency at Flipkart and Oracle. Do this one this week.
- **Minimum Window Substring (LC 76) —** the hardest common variable window and a very frequent interview question. Worth 60 minutes.
- **Longest Subarray with Ones after Replacement (your untouched) —** do it. It's Max Consecutive Ones III, a medium despite your sheet's HARD tag.
- **Permutation in a String / String Anagrams —** do one, skip the other. Same fixed-window frequency match twice.
- **Words Concatenation —** skip. Low frequency, high cost.
