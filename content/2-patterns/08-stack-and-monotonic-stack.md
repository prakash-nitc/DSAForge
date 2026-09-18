---
id: card-8
numeral: Card 8
title: Stack & Monotonic Stack
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair + two real gaps | 8 / 11 | L2 | L4 + add the two missing classics |

## Template 8A — Next greater element to the right

```java
Deque<Integer> st = new ArrayDeque<>();        // holds INDICES
int[] ans = new int[n]; Arrays.fill(ans, -1);
for (int i = 0; i < n; i++) {
    while (!st.isEmpty() && a[st.peek()] < a[i])   // '<' -> strictly greater
        ans[st.pop()] = a[i];
    st.push(i);
}
```

*Store indices, never values. The moment a problem asks for a distance or a width, values are useless and you have to rewrite from scratch.*

## Template 8B — Largest rectangle in a histogram (the payoff problem)

```java
Deque<Integer> s = new ArrayDeque<>();
int best = 0;
for (int i = 0; i <= n; i++) {
    int h = (i == n) ? 0 : a[i];               // sentinel flushes the stack
    while (!s.isEmpty() && a[s.peek()] >= h) {
        int height = a[s.pop()];
        int left = s.isEmpty() ? -1 : s.peek();
        best = Math.max(best, height * (i - left - 1));
    }
    s.push(i);
}
```

*The sentinel at i == n replaces a separate drain loop after the main loop. Once you see that trick you use it everywhere.*

## Template 8C — Stack of (value, count) pairs

```java
Deque<int[]> st = new ArrayDeque<>();          // {charCode, runLength}
for (char ch : s.toCharArray()) {
    if (!st.isEmpty() && st.peek()[0] == ch) {
        if (++st.peek()[1] == k) st.pop();
    } else st.push(new int[]{ch, 1});
}
```

## Template 8D — Greedy with a monotonic stack (remove k digits)

```java
Deque<Character> st = new ArrayDeque<>();
for (char d : num.toCharArray()) {
    while (k > 0 && !st.isEmpty() && st.peek() > d) { st.pop(); k--; }
    st.push(d);
}
while (k-- > 0) st.pop();                      // still budget left -> trim the tail
// then build the string, strip leading zeros
```

## Template 8E — Plain stack: matching and evaluation

```java
Deque<Character> st = new ArrayDeque<>();
for (char ch : s.toCharArray()) {
    if (ch == '(' || ch == '[' || ch == '{') st.push(ch);
    else {
        if (st.isEmpty() || !matches(st.pop(), ch)) return false;
    }
}
return st.isEmpty();                           // unclosed openers remain
```

## The knobs — what actually varies across this family

- **Direction —** left-to-right gives 'next'; right-to-left gives 'previous'.
- **Comparison —** < vs <= decides strict versus non-strict, which decides duplicate handling.
- **What you store —** indices (almost always), or (value, count) pairs when runs matter.
- **Sentinel —** a virtual 0 or ∞ at the end flushes the stack without a second loop.

## Trigger signals

- "Next / previous greater or smaller element"
- "Days until a warmer temperature" — same thing with a different noun
- Bracket matching, expression evaluation, path simplification, string decoding
- Histogram, rectangle, or trapping-water area problems
- "Remove k characters to make the smallest / largest result" → greedy monotonic
- Undo / backtrack semantics of any kind

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Next Greater Element | The knob check. Should be four minutes. |
| 2 | Daily Temperatures | Same template, different framing. Confirms you see through the noun. |
| 3 | Remove All Adjacent Duplicates in String II | Stack of (char, count) — the composite-state variant that decays first. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 8A — monotonic | Next Greater Element · Next Greater Element II · Previous Greater Element · Previous Smaller Element · Daily Temperatures |
| 8C — pairs | Remove Adjacent Duplicates · Remove All Adjacent Duplicates in String II |
| 8D — greedy | Remove K Digits (untouched) |
| 8E — plain | Balanced Parentheses · Simplify Path (untouched) |
| 8B — histogram | Nothing on your sheet. This is the biggest gap in the card. |

## Decay signatures — how you'll know it's gone

- You store values instead of indices and then cannot compute widths.
- You use Stack<> instead of ArrayDeque — legacy, synchronised, slower, and interviewers notice.
- You cannot decide between < and <= without trial and error.
- You never reach for the sentinel and write a separate drain loop instead.
- Next Greater Element II (circular): you forget to loop twice over the array modulo n.

## Java bugs specific to this pattern

- ArrayDeque as a stack: push/pop/peek operate on the HEAD. Do not mix with addLast/pollFirst in the same code or you'll build a queue by accident.
- ArrayDeque cannot store null — no null sentinels.
- st.peek()[1]++ works on int[] because arrays are references; the same trick fails on Integer.
- Iterating an ArrayDeque gives head-to-tail order, which for a stack is top-to-bottom. Reverse it if you're building a result string.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| All monotonic stack variants | O(n) amortised — each index pushed and popped once | O(n) |
| Largest rectangle | O(n) | O(n) |
| Maximal rectangle (2D) | O(mn) | O(n) |

## Interview follow-ups you will be asked

- "Why is it O(n) with a nested while?" — amortised: each index is pushed once and popped at most once.
- "Do the circular version." — iterate 2n times using i % n, and don't push in the second pass.
- "Trapping Rain Water three ways." — prefix-max arrays, two pointers, monotonic stack. Be able to name all three and say which you'd pick.
- "Extend the histogram solution to a binary matrix." — Maximal Rectangle: build a histogram per row, run 8B on each.

## Additions

- **Largest Rectangle in Histogram (LC 84) —** MISSING and the single highest-value stack problem in existence. Flipkart, Oracle, Amazon. Do it this week.
- **Maximal Rectangle (LC 85) —** the 2D extension. Only after 84 is at L4.
- **Min Stack (LC 155) —** design-flavoured, trivially quick, appears in warm-up rounds.
- **Asteroid Collision, Decode String, Evaluate Reverse Polish Notation —** three cheap mediums that broaden your stack instincts beyond monotonic.
- **Your three untouched —** do all three. Remove K Digits (the greedy-monotonic bridge), Simplify Path (15 minutes, appears in OAs), Remove Nodes From Linked List (monotonic stack on a list).
