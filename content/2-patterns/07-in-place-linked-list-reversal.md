---
id: card-7
numeral: Card 7
title: In-place Linked List Reversal
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair | 5 / 6 | L2 | L4 — pure mechanics, decays fast, cheap to restore |

## Template 7A — Full reverse

```java
ListNode prev = null, cur = head;
while (cur != null) {
    ListNode nxt = cur.next;    // save
    cur.next = prev;            // flip
    prev = cur;                 // advance prev
    cur = nxt;                  // advance cur
}
return prev;                    // new head
```

*Save, flip, advance, advance. Four lines, always in that order. Say it out loud while you write it.*

## Template 7B — Reverse every k nodes (the group machinery)

```java
ListNode dummy = new ListNode(0); dummy.next = head;
ListNode prevGroup = dummy;
while (true) {
    ListNode kth = prevGroup;
    for (int i = 0; i < k && kth != null; i++) kth = kth.next;
    if (kth == null) break;                     // fewer than k remain
    ListNode groupNext = kth.next;

    ListNode prev = groupNext, cur = prevGroup.next;
    while (cur != groupNext) {                  // reverse this group
        ListNode nxt = cur.next; cur.next = prev; prev = cur; cur = nxt;
    }
    ListNode tail = prevGroup.next;             // old head becomes new tail
    prevGroup.next = kth;
    prevGroup = tail;
}
return dummy.next;
```

## Template 7C — Reverse a sub-list between positions m and n

```java
ListNode dummy = new ListNode(0); dummy.next = head;
ListNode prev = dummy;
for (int i = 1; i < m; i++) prev = prev.next;   // node before position m
ListNode cur = prev.next;
for (int i = 0; i < n - m; i++) {               // head-insertion, n-m times
    ListNode nxt = cur.next;
    cur.next = nxt.next;
    nxt.next = prev.next;
    prev.next = nxt;
}
```

*Head insertion, not repeated reversal. Each iteration lifts the node after cur and splices it directly behind prev.*

## Template 7D — Rotate right by k

```java
int len = 1; ListNode tail = head;
while (tail.next != null) { tail = tail.next; len++; }
tail.next = head;                    // close the ring
k %= len;                            // the line that saves you on huge k
ListNode newTail = head;
for (int i = 1; i < len - k; i++) newTail = newTail.next;
ListNode newHead = newTail.next;
newTail.next = null;                 // cut
return newHead;
```

## The knobs — what actually varies across this family

- **Scope —** whole list, a positional sub-list, or fixed-size groups.
- **Dummy node —** use it every single time. It costs one line and removes the entire class of head special-cases.
- **Leftover policy —** does a final group of fewer than k get reversed or left alone? Always ask.

## Trigger signals

- "Reverse", "rotate", "swap pairs", "reorder" on a linked list
- "In groups of k" or "between positions m and n"
- Any linked-list problem where O(1) extra space is stated
- Palindrome list (reverse the second half in place)

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Reverse a Sub-list | Boundary precision — the m..n indices are where people bleed. |
| 2 | Reverse every K-element Sub-list | The full group machinery. If this is fluent, the family is fluent. |
| 3 | Rotate a LinkedList | Different mechanic (length, ring, cut) — proves you aren't just pattern-matching to reversal. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 7A | Reverse a LinkedList |
| 7B | Reverse every K-element Sub-list · Reverse List in Pairs (k = 2) · Reverse nodes in EVEN Length Groups |
| 7C | Reverse a Sub-list |
| 7D | Rotate a LinkedList |

## Decay signatures — how you'll know it's gone

- You skip the dummy and then hand-write four lines of head special-casing.
- You lose the pointer to the node before the group and cannot reattach.
- In Rotate you forget k %= len and loop pointlessly for large k.
- You can write it but cannot draw the pointer state after each iteration — memorised, not understood.

## Java bugs specific to this pattern

- Assigning cur.next before saving nxt destroys the rest of the list. Save first, always.
- Not cutting newTail.next = null in Rotate leaves a cycle; the judge hangs or stack-overflows on printing.
- Comparing nodes with .equals() rather than ==.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| All reversal variants | O(n) | O(1) |
| Recursive reversal | O(n) | O(n) stack — mention this trade-off |

## Interview follow-ups you will be asked

- "Do it recursively." — then be ready for "what's the space complexity now?" The answer is O(n) stack, which is why iterative is preferred.
- "What if the last group has fewer than k nodes?" — the two variants (leave as is, or reverse anyway) differ only in the break condition.
- "Reverse in groups of increasing size 1, 2, 3, …?" — same machinery with a growing k. Good stress test.
- "Detect whether reversal broke the list." — walk it and count; also the cue to mention cycle risk.

## Additions

- **Reorder List —** midpoint + reverse + interleave. Extremely common as a single interview question and it exercises Cards 2 and 7 together.
- **Merge Two Sorted Lists —** different pattern, same pointer hygiene. Five minutes.
- **Reverse nodes in EVEN Length Groups (your untouched) —** skip. Fiddly, low frequency, no new idea.
