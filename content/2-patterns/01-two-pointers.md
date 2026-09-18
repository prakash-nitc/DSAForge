---
id: card-1
numeral: Card 1
title: Two Pointers
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair | 9 / 12 | L2 (marked Revised) | L4 — best quick win on the board |

## Template 1A — Converging pointers on a sorted array (the 3Sum shape)

```java
Arrays.sort(a);
for (int i = 0; i < n - 2; i++) {
    if (i > 0 && a[i] == a[i-1]) continue;              // dedup #1: outer
    int l = i + 1, r = n - 1;
    while (l < r) {
        int sum = a[i] + a[l] + a[r];
        if (sum == target) {
            res.add(List.of(a[i], a[l], a[r]));
            l++; r--;
            while (l < r && a[l] == a[l-1]) l++;         // dedup #2: left
            while (l < r && a[r] == a[r+1]) r--;         // dedup #3: right
        } else if (sum < target) l++;
        else r--;
    }
}
```

*Three dedup positions, not one. Missing #2 and #3 is the single most common failure in this family and it produces silently wrong output rather than a crash.*

## Template 1B — Same-direction write pointer (in-place filter / compaction)

```java
int w = 0;                                  // write index
for (int rd = 0; rd < n; rd++)              // read index
    if (keep(a[rd])) a[w++] = a[rd];
return w;                                   // new logical length
```

*No sorting required. This is what 'Remove Duplicates', 'Move Zeroes' and 'Rearrange 0 and 1' actually are.*

## Template 1C — Three-way partition (Dutch National Flag)

```java
int low = 0, mid = 0, high = n - 1;
while (mid <= high) {
    if (a[mid] == 0)      { swap(a, low++, mid++); }
    else if (a[mid] == 1) { mid++; }
    else                  { swap(a, mid, high--); }   // do NOT advance mid
}
```

*The 'do not advance mid' line is the whole problem. The element swapped in from the right end is unexamined, so it must be re-inspected.*

## Template 1D — Expanding window from centre (palindromic substrings)

```java
for (int centre = 0; centre < 2*n - 1; centre++) {
    int l = centre / 2, r = l + centre % 2;      // handles odd AND even centres
    while (l >= 0 && r < n && s.charAt(l) == s.charAt(r)) { l--; r++; }
    // window (l+1 .. r-1) is a palindrome of length r-l-1
}
```

## The knobs — what actually varies across this family

- **Direction —** converging (l and r move toward each other) vs same-direction (read and write both advance left-to-right).
- **Sort or not —** converging almost always needs a sorted array; same-direction almost never does.
- **What you record —** the pair itself, a count, or a compacted array length.
- **Dedup strategy —** skip-equal-neighbours after sorting, at every pointer that can produce a duplicate.

## Trigger signals

- Sorted array + "find a pair / triplet / quadruple summing to X"
- "Remove / move / partition in place with O(1) extra space"
- "Count subarrays with product or sum less than K" on positive numbers
- Palindrome checks from both ends, or expanding from a centre
- Three-way partition by value (Dutch National Flag)
- Two sorted arrays to merge or intersect

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Triplet Sum to Zero | Carries all three dedup positions and the sort-first instinct. If this holds, the family holds. |
| 2 | Sort Colors (Dutch National Flag) | The three-pointer partition — the shape people forget entirely. |
| 3 | Subarrays with Product Less than Target | Hybrid window with a non-obvious counting step (r - l + 1 per right end). This is the one that quietly decays. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 1A — converging | Pair with Target Sum · Triplet Sum to Zero · Triplet Sum Close to Target · Triplets with Smaller Sum · Quadruple Sum to Target |
| 1B — write pointer | Remove Duplicates · Rearrange 0 and 1 · Squaring a Sorted Array (converging into a write pointer from the back) |
| 1C — three-way partition | Sort Colors |
| Hybrid / window | Subarrays with Product Less than Target · Minimum Window Sort |
| String two-pointer | Comparing Strings containing Backspaces (from the back) |

## Decay signatures — how you'll know it's gone

- You forget dedup #2 and #3 and emit duplicate triplets.
- In Sort Colors you advance mid after the high-swap and lose an element.
- You reach for two pointers on an unsorted array where the answer needs a hash map.
- You cannot say why the counting step in the product problem is (r - l + 1) rather than 1.
- Squaring a Sorted Array: you sort the squares instead of merging from both ends.

## Java bugs specific to this pattern

- Arrays.sort on int[] is dual-pivot quicksort — not stable and O(n²) on adversarial input. On Integer[] it is TimSort and stable.
- Writing a[i] + a[l] + a[r] with values near Integer.MAX_VALUE overflows. Use long for the sum when the constraint allows large values.
- List.of(...) returns an immutable list — fine for results, fatal if you later mutate it.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Converging pair on sorted array | O(n) after sort → O(n log n) | O(1) or O(log n) for sort |
| 3Sum | O(n²) | O(1) excluding output |
| Write pointer / partition | O(n) | O(1) |
| Expand from centre | O(n²) | O(1) |

## Interview follow-ups you will be asked

- "Why does sorting not lose information here?" — because you only need existence of a combination, not original indices.
- "Can you do 3Sum without sorting?" — yes with a hash set, but dedup becomes far uglier and space goes to O(n).
- "What if the array is huge and doesn't fit in memory?" — external sort, then a streaming two-pointer.
- "Generalise to k-Sum." — recursive peeling: k-Sum reduces to (k-1)-Sum inside a loop, bottoming out at 2Sum. O(n^(k-1)).

## Additions

- **Container With Most Water —** the 'move the shorter wall' greedy argument is a classic follow-up. Asked directly at product companies.
- **Trapping Rain Water (two-pointer version) —** highest-frequency Hard in this family. Do the two-pointer solution, not just the prefix-max arrays version.
- **Move Zeroes, Valid Palindrome II, Boats to Save People —** three cheap reps that lock 1B and the converging instinct.
- **Of your three untouched:** do Comparing Strings containing Backspaces and Minimum Window Sort; skip Quadruple Sum to Target (3Sum with one more loop, zero new insight).
