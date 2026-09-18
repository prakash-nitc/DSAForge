---
id: s14
numeral: §14
title: Dynamic Programming — the ladder
card: 15
---

Your sheet carries three DP problems. That is not enough for any September target. But DP is also the topic where scope creep destroys the most candidates, so this section is deliberately capped: eight templates, roughly twenty problems, one method.

**Sequence DP after Graphs. Graphs has higher frequency at your specific targets and a much shorter time-to-competence.**

## 14.1 The four-step ladder — the method that makes DP click

| Step | What you write | Why you don't skip it |
| --- | --- | --- |
| 1. Recursive brute force | A function with explicit parameters and a base case. Ignore efficiency entirely. | The parameters you need ARE the state. You discover the state by writing the recursion, not by staring at the problem. |
| 2. Memoise | Add a cache keyed on exactly the parameters that change. | This alone converts exponential to polynomial. In an interview this is often a complete answer. |
| 3. Tabulate | Convert to bottom-up by reading the recursion's dependency direction. | Removes recursion depth risk and is usually faster by a constant factor. |
| 4. Space-optimise | Collapse to rolling rows or variables. | Only if asked, or if memory is the constraint. Do not lead with it. |

> [!TIP]
> **Narrate the ladder in interviews**
>
> "Here's the brute force. Here's why it's exponential — this subproblem repeats. Here's the memo. Here's the table." That narration is worth more than silently arriving at an optimised table, because it shows you derived the solution rather than recalled it.

## 14.2 The three questions that define any DP

- **What is the state?** The minimal set of parameters that fully determines the answer from this point. If your recursion needs five parameters, your state is five-dimensional and you should look for a smaller formulation.
- **What is the transition?** How does the answer at this state relate to smaller states? This is the recurrence.
- **What is the base case, and what is the answer?** Where does the recursion bottom out, and which cell holds the final answer?

## 14.3 Template D1 — 1D linear DP

```java
// Climbing Stairs / House Robber shape
int[] dp = new int[n + 1];
dp[0] = base0; dp[1] = base1;
for (int i = 2; i <= n; i++)
    dp[i] = f(dp[i-1], dp[i-2]);

// SPACE-OPTIMISED -- almost always available for 1D
int prev2 = base0, prev1 = base1;
for (int i = 2; i <= n; i++) { int cur = f(prev1, prev2); prev2 = prev1; prev1 = cur; }

// House Robber:  dp[i] = max(dp[i-1], dp[i-2] + a[i])       // skip, or take
// House Robber II (circular): run the linear version twice --
//   once on [0..n-2] and once on [1..n-1], take the max.
```

- **Problems:** Climbing Stairs, House Robber, House Robber II, Min Cost Climbing Stairs, Fibonacci.
- **The link back to Kadane:** Kadane is exactly this template with O(1) state. If Card 4 is solid, D1 is already familiar.

## 14.4 Template D2 — Grid DP

```java
int[][] dp = new int[m][n];
dp[0][0] = grid[0][0];
for (int i = 0; i < m; i++)
    for (int j = 0; j < n; j++) {
        if (i == 0 && j == 0) continue;
        int up   = (i > 0) ? dp[i-1][j] : INF_OR_ZERO;
        int left = (j > 0) ? dp[i][j-1] : INF_OR_ZERO;
        dp[i][j] = grid[i][j] + Math.min(up, left);      // or + (up + left) for counting
    }

// Counting paths -> initialise the first row and column to 1, then dp[i][j] = dp[i-1][j] + dp[i][j-1]
// Space: one rolling row of length n is always enough.
```

- **Problems:** Unique Paths, Unique Paths II (obstacles), Minimum Path Sum, Triangle, Maximal Square.

## 14.5 Template D3 — 0/1 Knapsack (take or skip)

```java
// 2D form -- write this one first, always
boolean[][] dp = new boolean[n + 1][target + 1];
for (int i = 0; i <= n; i++) dp[i][0] = true;
for (int i = 1; i <= n; i++)
    for (int s = 1; s <= target; s++)
        dp[i][s] = dp[i-1][s] || (s >= a[i-1] && dp[i-1][s - a[i-1]]);

// 1D form -- iterate capacity BACKWARDS so each item is used at most once
boolean[] dp = new boolean[target + 1]; dp[0] = true;
for (int x : a)
    for (int s = target; s >= x; s--)          // BACKWARDS = 0/1
        dp[s] |= dp[s - x];

// UNBOUNDED knapsack (reuse allowed) -- iterate FORWARDS
for (int coin : coins)
    for (int s = coin; s <= target; s++)       // FORWARDS = unlimited reuse
        dp[s] = Math.min(dp[s], dp[s - coin] + 1);
```

**The direction of the inner loop is the entire difference between 0/1 and unbounded knapsack. Backwards means each item is considered once; forwards lets an item be reused within the same pass. Write that sentence in your mistake log now.**

- **Problems:** Partition Equal Subset Sum, Coin Change, Coin Change II, Target Sum, Subset Sum, Last Stone Weight II.

## 14.6 Template D4 — Longest Increasing Subsequence

```java
// O(n^2) -- write this one first; it's usually accepted and always explainable
int[] dp = new int[n]; Arrays.fill(dp, 1);
for (int i = 1; i < n; i++)
    for (int j = 0; j < i; j++)
        if (a[j] < a[i]) dp[i] = Math.max(dp[i], dp[j] + 1);
int best = Arrays.stream(dp).max().getAsInt();

// O(n log n) -- 'tails' array + binary search (Card 10's lower bound)
List<Integer> tails = new ArrayList<>();
for (int x : a) {
    int i = lowerBound(tails, x);            // first index with tails[i] >= x
    if (i == tails.size()) tails.add(x); else tails.set(i, x);
}
return tails.size();      // NOTE: tails is NOT the actual subsequence, only its length
```

- **Problems:** Longest Increasing Subsequence, Russian Doll Envelopes, Longest Divisible Subset, Number of LIS.
- **The interview follow-up you will get:** "reconstruct the actual subsequence" — the O(n log n) tails array cannot do it directly; you need a parent-index array alongside.

## 14.7 Template D5 — Two-string DP

```java
// Longest Common Subsequence -- the parent of edit distance and friends
int[][] dp = new int[m + 1][n + 1];
for (int i = 1; i <= m; i++)
    for (int j = 1; j <= n; j++)
        dp[i][j] = (s.charAt(i-1) == t.charAt(j-1))
                 ? dp[i-1][j-1] + 1
                 : Math.max(dp[i-1][j], dp[i][j-1]);

// Edit Distance -- same grid, three operations
dp[i][j] = (s.charAt(i-1) == t.charAt(j-1))
         ? dp[i-1][j-1]
         : 1 + min(dp[i-1][j-1],   // replace
                   dp[i-1][j],     // delete
                   dp[i][j-1]);    // insert
// base row/col: dp[i][0] = i, dp[0][j] = j
```

- **Problems:** Longest Common Subsequence, Edit Distance, Longest Palindromic Subsequence (LCS of s and reversed s), Distinct Subsequences, Delete Operation for Two Strings.
- **The trick worth memorising:** Longest Palindromic Subsequence = LCS(s, reverse(s)). One line converts a hard-looking problem into one you already know.

## 14.8 Template D6 — State-machine DP (stocks)

```java
// Best Time to Buy and Sell Stock II -- unlimited transactions
int hold = -prices[0], free = 0;
for (int px : prices) {
    int prevFree = free;
    free = Math.max(free, hold + px);        // sell today
    hold = Math.max(hold, prevFree - px);    // buy today
}
return free;

// With a cooldown: three states -- hold, sold, rest
// With at most k transactions: dp[k][hold] -- two nested state dimensions
```

- **Problems:** Best Time to Buy and Sell Stock I, II, III, IV, with Cooldown, with Transaction Fee.
- **Why this family is worth the time:** six problems, one template, and it teaches you to think in states rather than in indices — which is the skill the rest of DP rests on.

## 14.9 Template D7 — Partition / interval DP

```java
// 'split the range at every position and combine' -- length-first iteration
for (int len = 2; len <= n; len++)
    for (int i = 0; i + len <= n; i++) {
        int j = i + len - 1;
        for (int k = i; k < j; k++)
            dp[i][j] = best(dp[i][j], dp[i][k] + dp[k+1][j] + cost(i, k, j));
    }
```

- **Problems:** Matrix Chain Multiplication, Burst Balloons, Minimum Cost to Cut a Stick, Palindrome Partitioning II.
- **Priority:** low. O(n³) and asked less often than the other six. Learn it in week two of DP, not week one.

## 14.10 Template D8 — DP on trees

```java
// Return an ARRAY of states from each node -- this is Shape A from §12
int[] dfs(TreeNode n) {                     // {best if we DON'T take n, best if we DO}
    if (n == null) return new int[]{0, 0};
    int[] L = dfs(n.left), R = dfs(n.right);
    int skip = Math.max(L[0], L[1]) + Math.max(R[0], R[1]);
    int take = n.val + L[0] + R[0];
    return new int[]{ skip, take };
}
```

- **Problems:** House Robber III, Binary Tree Maximum Path Sum, Diameter (already in §12), Longest Univalue Path.
- **The insight:** DP on trees is just §12 Shape A where the returned value is a small array of states instead of a single number.

## 14.11 The core ten — do these first

| # | Problem | Template | Why this one |
| --- | --- | --- | --- |
| 1 | Climbing Stairs | D1 | The smallest possible DP. Do the four-step ladder on it explicitly. |
| 2 | House Robber | D1 | First real choice structure: take or skip. |
| 3 | Unique Paths | D2 | The grid recurrence in its purest form. |
| 4 | Minimum Path Sum | D2 | Same grid, min instead of sum. Confirms transfer. |
| 5 | Coin Change | D3 unbounded | The forward loop. Also the classic 'why greedy fails' example. |
| 6 | Partition Equal Subset Sum | D3 0/1 | The backward loop. The two together fix the direction confusion permanently. |
| 7 | Longest Increasing Subsequence | D4 | Do O(n²) first, then the O(n log n) version. Ties DP to Card 10. |
| 8 | Longest Common Subsequence | D5 | The parent of the whole two-string family. |
| 9 | Best Time to Buy and Sell Stock I | Kadane / D6 | Free, and the doorway into state-machine thinking. |
| 10 | Best Time to Buy and Sell Stock II | D6 | Two states. The moment DP stops being about arrays. |

> [!NOTE]
> **Ten well-held DP problems beat forty half-held ones**
>
> DP is where candidates most often confuse coverage with capability. If you can derive these ten from the four-step ladder without looking anything up, you will handle the medium DP that appears in an Oracle or VISA OA. Forty problems at L1 will not.

## 14.12 The six-day DP build

| Day | Templates | Problems |
| --- | --- | --- |
| 1 | D1 | Climbing Stairs · Min Cost Climbing Stairs · House Robber · House Robber II |
| 2 | D2 | Unique Paths · Unique Paths II · Minimum Path Sum · Triangle |
| 3 | D3 | Coin Change · Coin Change II · Partition Equal Subset Sum · Target Sum |
| 4 | D4 + D5 | LIS (both versions) · Longest Common Subsequence · Longest Palindromic Subsequence |
| 5 | D6 | Stocks I · II · with Cooldown · with Fee |
| 6 | Repair + D8 | Cold re-solve four from Days 1–3 · House Robber III · Edit Distance |

## 14.13 DP bugs and traps in Java

- Array sized n instead of n+1, so dp[n] is out of bounds. Almost every DP wants n+1.
- Forgetting to initialise the unreachable state. For minimisation, fill with a large sentinel — but not Integer.MAX_VALUE, because MAX_VALUE + 1 overflows to negative. Use a safe INF like 10⁹.
- Iterating the knapsack capacity forwards when you meant 0/1.
- Memoising on the wrong key — if your recursion has three changing parameters, the cache key must have three components.
- Using an int[] memo where 0 is a legal answer; you cannot distinguish 'unset' from 'computed zero'. Fill with -1 or use Integer[].
- Recursion depth on top-down DP with n = 10⁵ — StackOverflowError. Convert to tabulation.
- Not taking the modulus in counting problems that say 'modulo 10⁹+7'.

## 14.14 Interview follow-ups

- "What's the space complexity, and can you reduce it?" — the near-universal DP follow-up. Rolling rows for 2D, two variables for 1D.
- "Reconstruct the actual solution, not just its value." — store parent pointers, or walk the table backwards from the answer cell.
- "Why doesn't greedy work here?" — Coin Change with coins {1, 3, 4} and target 6 is the standard counterexample: greedy gives 4+1+1, optimal is 3+3.
- "Top-down or bottom-up, and why?" — top-down is easier to derive and only computes reachable states; bottom-up avoids stack depth and is usually faster.
- "What if n is 10⁵ and your DP is O(n²)?" — either the state is wrong, or there is a monotone structure that allows binary search or a monotonic deque.
