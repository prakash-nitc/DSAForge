---
id: s26
numeral: §26
title: Lists — the array that grows
---

`ArrayList` is the answer whenever the size is not known in advance. Declare it by the interface, create it by the class.

```java idiom
List<Integer> list = new ArrayList<>();      // the normal declaration
List<String> words = new ArrayList<>();
List<List<Integer>> res = new ArrayList<>(); // results made of groups
List<int[]> pairs = new ArrayList<>();       // a list of small arrays is fine and fast
```

The type inside `<>` must be an object type: `Integer`, not `int`. Boxing happens for you: `list.add(5)` works.

## 26.1 The operations

| Do this | Code | Notes |
| --- | --- | --- |
| Add to the end | `list.add(x)` | Amortised O(1) |
| Insert at a position | `list.add(i, x)` | O(n), everything shifts right |
| Read | `list.get(i)` | Not `list[i]` |
| Overwrite | `list.set(i, x)` | The slot must already exist |
| Remove by position | `list.remove(i)` | O(n) |
| Remove by value | `list.remove(Integer.valueOf(x))` | See the trap below |
| Remove the last | `list.remove(list.size() - 1)` | The backtracking undo |
| Size | `list.size()` | |
| Empty? | `list.isEmpty()` | Clearer than `size() == 0` |
| Contains | `list.contains(x)` | O(n). Use a `HashSet` if you ask often |
| First index of | `list.indexOf(x)` | `-1` when absent |
| Clear | `list.clear()` | |
| Add everything | `list.addAll(other)` | |
| Sort | `Collections.sort(list)` or `list.sort(null)` | Natural order |
| Sort by a rule | `list.sort((x, y) -> Integer.compare(x, y))` | |
| Reverse | `Collections.reverse(list)` | In place |
| Max, min | `Collections.max(list)`, `Collections.min(list)` | |
| Copy | `new ArrayList<>(other)` | The copy you need in backtracking |
| To array | `list.toArray(new String[0])`, or a loop for `int[]` | §23.4 |

## 26.2 Walking one

```java idiom
for (int i = 0; i < list.size(); i++) {
    int x = list.get(i);
    ...
}

// removing while you walk: go BACKWARDS, so the shifting does not skip elements
for (int i = list.size() - 1; i >= 0; i--) {
    if (list.get(i) == 0) list.remove(i);
}

// a list of lists
for (int i = 0; i < res.size(); i++) {
    List<Integer> row = res.get(i);
    for (int j = 0; j < row.size(); j++) { ... }
}
```

> [!WARNING]
> **`remove(2)` and `remove(Integer.valueOf(2))` do different things.** With a `List<Integer>`, the plain number is read as a position, not a value. To delete the number 2, box it.
>
> **Never remove inside a forward loop.** Positions shift left and you skip the next element. Walk backwards, or collect what to keep into a new list.
>
> **`Arrays.asList(arr)` and `List.of(...)` are not growable.** Both throw UnsupportedOperationException on `add`. Wrap them: `new ArrayList<>(Arrays.asList(arr))`.

## 26.3 Collecting groups, the backtracking shape

```java idiom
List<List<Integer>> res = new ArrayList<>();
List<Integer> path = new ArrayList<>();

path.add(x);                          // choose
dfs(...);                             // explore
path.remove(path.size() - 1);         // undo

res.add(new ArrayList<>(path));       // a COPY. Adding path itself stores a reference
                                      // that keeps changing, and every row ends up identical.
```
