---
id: s29
numeral: §29
title: Stack, queue and deque — one class does all three
---

`ArrayDeque` is your stack **and** your queue. `Stack` is a legacy synchronised class and `LinkedList` wastes cache; interviewers notice both (§18).

```java idiom
Deque<Integer> stack = new ArrayDeque<>();     // a stack
Deque<Integer> queue = new ArrayDeque<>();     // a queue
Deque<int[]> q = new ArrayDeque<>();           // grid problems: store {row, col}
```

## 29.1 As a stack, last in first out

| Do this | Code | Empty behaviour |
| --- | --- | --- |
| Put on top | `stack.push(x)` | |
| Take off the top | `stack.pop()` | **Throws** NoSuchElementException |
| Look at the top | `stack.peek()` | Returns `null` |
| Empty? | `stack.isEmpty()` | |
| How many | `stack.size()` | |

```java idiom
// monotonic stack: next greater element. Store INDICES, not values.
int[] res = new int[n];
Arrays.fill(res, -1);
Deque<Integer> st = new ArrayDeque<>();
for (int i = 0; i < n; i++) {
    while (!st.isEmpty() && a[st.peek()] < a[i]) {
        res[st.pop()] = a[i];
    }
    st.push(i);
}
```

## 29.2 As a queue, first in first out

| Do this | Code | Empty behaviour |
| --- | --- | --- |
| Add at the back | `queue.offer(x)` | `add(x)` is the same but throws when full |
| Take from the front | `queue.poll()` | Returns `null` |
| Look at the front | `queue.peek()` | Returns `null` |
| Empty? | `queue.isEmpty()` | |

```java idiom
// BFS with levels. The inner loop must read the size BEFORE adding to the queue.
Deque<Integer> q = new ArrayDeque<>();
q.offer(start);
boolean[] seen = new boolean[n];
seen[start] = true;
int level = 0;
while (!q.isEmpty()) {
    int size = q.size();                       // freeze this level
    for (int i = 0; i < size; i++) {
        int node = q.poll();
        for (int j = 0; j < adj[node].size(); j++) {
            int next = adj[node].get(j);
            if (!seen[next]) {
                seen[next] = true;             // mark ON ENQUEUE, never on dequeue
                q.offer(next);
            }
        }
    }
    level++;
}
```

## 29.3 Both ends at once

| Front | Back |
| --- | --- |
| `addFirst(x)` | `addLast(x)` |
| `pollFirst()` | `pollLast()` |
| `peekFirst()` | `peekLast()` |

`push` is `addFirst`, `offer` is `addLast`, and `pop` and `poll` are both `pollFirst`. That single fact is why one class covers a stack and a queue.

## 29.4 Priority queue, when you always need the extreme

```java idiom
PriorityQueue<Integer> min = new PriorityQueue<>();                          // smallest first
PriorityQueue<Integer> max = new PriorityQueue<>(Collections.reverseOrder()); // largest first
PriorityQueue<int[]> byCost = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));

pq.offer(x);        // O(log n)
int top = pq.poll();// O(log n), removes
int look = pq.peek();// O(1), keeps
pq.size(); pq.isEmpty();
```

> [!WARNING]
> **`ArrayDeque` refuses `null`.** Storing one throws NullPointerException, which is why `poll` returning `null` reliably means empty.
>
> **`pop` throws, `poll` returns null.** Guard with `while (!st.isEmpty())` and the difference never matters.
>
> **A `PriorityQueue` is not sorted when you print it.** Only the head is guaranteed. Poll in a loop if you need order.
>
> **`queue.size()` changes as you add.** In level BFS, read it into `size` before the inner loop, or the level never ends.
