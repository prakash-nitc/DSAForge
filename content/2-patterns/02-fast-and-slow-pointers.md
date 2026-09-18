---
id: card-2
numeral: Card 2
title: Fast & Slow Pointers (Floyd's cycle detection)
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Repair | 7 / 8 | L2 | L4 — small pattern, cheap to fully own |

## Template 2A — Cycle detection and entry point

```java
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next.next;
    if (slow == fast) break;                       // meeting point
}
if (fast == null || fast.next == null) return null; // no cycle

slow = head;                                       // reset ONE pointer
while (slow != fast) { slow = slow.next; fast = fast.next; }
return slow;                                       // cycle entry
```

*The reset step is arithmetic, not intuition: if the tail before the cycle has length a and the meeting point is b into a cycle of length c, then a ≡ (c − b) mod c. Be able to sketch that in 60 seconds — Oracle and VISA both like asking for it.*

## Template 2B — Midpoint in one pass

```java
ListNode slow = head, fast = head;
while (fast != null && fast.next != null) { slow = slow.next; fast = fast.next.next; }
// odd length  -> slow is the exact middle
// even length -> slow is the SECOND middle
// for the FIRST middle on even length, start fast = head.next
```

## Template 2C — Array as an implicit linked list

```java
// values in [1..n] with one duplicate: index i -> a[i] is an edge
int slow = a[0], fast = a[a[0]];
while (slow != fast) { slow = a[slow]; fast = a[a[fast]]; }
slow = 0;
while (slow != fast) { slow = a[slow]; fast = a[fast]; }
return slow;                                      // the duplicate value
```

*The disguise. If you don't see that the array is a functional graph, you write O(n) space and lose the point of the question.*

## The knobs — what actually varies across this family

- **Step ratio —** almost always 1 and 2. Other ratios exist but no interview needs them.
- **Start offset —** both at head, or fast at head.next, decides which middle you land on for even lengths.
- **What you return —** the meeting point, the entry node, the midpoint, or a boolean.

## Trigger signals

- Linked list + "cycle", "loop", "where does it start"
- Array of values that are indices in [1, n] — implicit linked list
- "Middle of the list" / "reorder" / "palindrome list" — needs a midpoint in one pass
- Any repeated-state process that must converge to a loop (Happy Number)
- "O(1) extra space" stated explicitly on a linked list problem

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Start of LinkedList Cycle | The entry-point arithmetic — the step people can execute but cannot explain. |
| 2 | Find Duplicate Number | The disguise. Seeing the array as a graph is the entire difficulty. |
| 3 | Palindrome LinkedList | Composite: find middle, reverse second half, compare, restore. Also exposes Card 7 decay. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 2A — cycle | LinkedList Cycle · Start of LinkedList Cycle · Happy Number · Cycle in a Circular Array |
| 2B — midpoint | Middle of the LinkedList · Palindrome LinkedList · Rearrange a LinkedList |
| 2C — implicit list | Find Duplicate Number |

## Decay signatures — how you'll know it's gone

- You find the meeting point and cannot recall the reset-to-head step.
- You null-check only fast, not fast.next, and NPE on even-length lists.
- On Find Duplicate Number you reach for a HashSet.
- You cannot state which middle your loop returns for even length without running it.

## Java bugs specific to this pattern

- while (fast.next != null && fast != null) is the wrong order — you dereference before the null check. Order matters in Java's short-circuit &&.
- Comparing nodes with .equals() instead of == — you want reference identity here.

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| Cycle detection + entry | O(n) | O(1) |
| Midpoint | O(n) | O(1) |
| Palindrome list (with restore) | O(n) | O(1) |

## Interview follow-ups you will be asked

- "Prove the entry-point step." — the distance argument above. Practise saying it in four sentences.
- "Why not a HashSet?" — it works in O(n) time but O(n) space; Floyd is the O(1)-space answer, which is what the question is testing.
- "What's the cycle length?" — from the meeting point, walk forward until you return to it.
- "Does this generalise beyond linked lists?" — yes, to any deterministic state transition function; that's why Happy Number works.

## Additions

- **Reorder List —** combines midpoint + reverse + merge. Very common as a single interview question.
- **Linked List Cycle II is your Start of LinkedList Cycle —** no need to duplicate.
- **Cycle in a Circular Array (your one untouched) —** leave it. Hard, low frequency, and the pattern is already covered seven times over.
