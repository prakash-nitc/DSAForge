---
id: card-12
numeral: Card 12
title: Recursion & Backtracking
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair + one glaring gap | 11 / 11 | L2–L3 (Pow at 30%) | L4 + add the Subsets family |

## Template 12A — The universal skeleton (subsets / combinations)

```java
void bt(int start, List<Integer> path) {
    res.add(new ArrayList<>(path));                 // subsets: record at EVERY node
    for (int i = start; i < n; i++) {
        if (i > start && a[i] == a[i-1]) continue;   // dedup (needs sorted input)
        path.add(a[i]);                             // CHOOSE
        bt(i + 1, path);                            // EXPLORE  (i, not i+1, if reuse allowed)
        path.remove(path.size() - 1);               // UN-CHOOSE
    }
}
```

## Template 12B — Permutations (used[] instead of a start index)

```java
void perm(List<Integer> path, boolean[] used) {
    if (path.size() == n) { res.add(new ArrayList<>(path)); return; }   // record at LEAVES
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        if (i > 0 && a[i] == a[i-1] && !used[i-1]) continue;   // dedup for permutations
        used[i] = true;  path.add(a[i]);
        perm(path, used);
        path.remove(path.size() - 1);  used[i] = false;
    }
}
```

*The permutation dedup rule (!used[i-1]) is DIFFERENT from the subsets rule (i > start). Confusing them is a common and quiet bug.*

## Template 12C — Grid backtracking (word search, N-Queens)

```java
boolean dfs(int r, int c, int k) {
    if (k == word.length()) return true;
    if (r < 0 || r >= m || c < 0 || c >= n) return false;
    if (board[r][c] != word.charAt(k)) return false;

    char tmp = board[r][c]; board[r][c] = '#';        // mark visited IN PLACE
    for (int[] d : DIRS)
        if (dfs(r + d[0], c + d[1], k + 1)) { board[r][c] = tmp; return true; }
    board[r][c] = tmp;                                // restore
    return false;
}
```

## Template 12D — Divide & conquer recursion (fast power)

```java
double pow(double x, long n) {
    if (n == 0) return 1;
    if (n < 0) { x = 1 / x; n = -n; }      // careful: -Integer.MIN_VALUE overflows, use long
    double half = pow(x, n / 2);
    return (n % 2 == 0) ? half * half : half * half * x;
}
```

## Template 12E — Pruning (the thing that turns TLE into AC)

```java
for (int i = start; i < n; i++) {
    if (a[i] > remaining) break;          // sorted input -> everything after is worse
    if (!isValidSoFar(path, a[i])) continue;
    ...
}
```

## The knobs — what actually varies across this family

- **Where you record —** every node (subsets) or only at leaves (permutations, fixed-size combinations).
- **How you advance —** start index (no reuse), i itself (reuse allowed), or used[] (permutations).
- **Dedup rule —** i > start for combinations; !used[i-1] for permutations. Both require sorted input.
- **Pruning —** break on a sorted bound, or continue on a validity check. Often the difference between passing and TLE.

## Trigger signals

- "All subsets / combinations / permutations / partitions"
- "Generate all valid …" (parentheses, words, board configurations)
- Constraint satisfaction: N-Queens, Sudoku, word search on a grid
- The output size is itself exponential — that IS the complexity
- n ≤ 20 in the constraints — the tell for search rather than a polynomial trick

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Permutations | The used[] shape. Baseline. |
| 2 | Combination Sum | The reuse-allowed variant (recurse on i, not i+1). Confirms knob two. |
| 3 | Palindrome Partitioning | Backtracking with a validity check inside the loop — the composite shape. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 12A — subsets/combinations | Combination Sum · Palindrome Partitioning · Generate Parentheses · Letter Combinations of a Phone Number |
| 12B — permutations | Permutations |
| 12D — divide & conquer | Pow(x,n) · Fibonacci Number · Sum of Digits of a Number · Check if Array is Sorted · Check if String is Palindrome · Remove Occurrences of a Character in String |
| 12C — grid | Nothing on your sheet. Word Search is the gap and it doubles as your Graphs on-ramp. |

## Decay signatures — how you'll know it's gone

- You add path directly instead of new ArrayList<>(path) and every result comes back empty.
- You forget the un-choose and results bleed across branches.
- You cannot say whether to recurse on i or i+1 without trial and error.
- You apply the subsets dedup rule to permutations.
- You never prune, and a solvable problem TLEs.

## Java bugs specific to this pattern

- res.add(path) stores a reference to a list you then mutate. Always new ArrayList<>(path).
- path.remove(path.size() - 1) vs path.remove(Object) — with a List<Integer>, remove(int) is by index and remove(Integer) is by value. This bites constantly.
- Recursion depth: default JVM stack handles roughly 10⁴ frames. Deep recursion on a skewed input throws StackOverflowError.
- -n where n == Integer.MIN_VALUE is still Integer.MIN_VALUE. Use long in Pow(x,n).

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Subsets | O(2ⁿ · n) | O(n) recursion depth |
| Permutations | O(n! · n) | O(n) |
| Combination Sum | O(2^target) | O(target) |
| N-Queens | O(n!) | O(n²) |

## Interview follow-ups you will be asked

- "Why is the complexity 2ⁿ·n and not 2ⁿ?" — the extra n is the cost of copying each subset into the result.
- "Do subsets iteratively." — bitmask over 0..2ⁿ−1, or repeatedly double the existing result list.
- "How would you prune this?" — the question they are actually testing on Combination Sum and N-Queens.
- "Convert this recursion to iteration." — explicit stack; be ready to say why you'd bother (stack depth).

## Additions

- **Subsets (LC 78) and Subsets II (LC 90) —** MISSING from your entire sheet, which is a real hole. Subsets is the archetype the pattern is taught from. Both take 40 minutes total.
- **Combination Sum II —** no-reuse-with-duplicates. Completes the four-way matrix with Combination Sum.
- **N-Queens —** the classic constraint-satisfaction problem. MathWorks and Flipkart favour it.
- **Word Search (LC 79) —** grid backtracking with in-place visited marking. Also your gentlest on-ramp into Graphs — do it the day before you start §13.
- **Sudoku Solver —** only with slack. High cost, moderate frequency.
