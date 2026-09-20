---
id: s30
numeral: §30
title: Maps and sets — counting, lookup, membership
---

```java idiom
Map<Character, Integer> count = new HashMap<>();
Map<String, List<String>> groups = new HashMap<>();
Set<Integer> seen = new HashSet<>();
```

Keys and values are object types: `Integer`, `Character`, `String`. Not `int`, not `char`.

## 30.1 Map operations

| Do this | Code | Notes |
| --- | --- | --- |
| Store | `map.put(k, v)` | Replaces any existing value |
| Read | `map.get(k)` | Returns `null` when missing |
| Read with a fallback | `map.getOrDefault(k, 0)` | Use this and null never bites you |
| Present? | `map.containsKey(k)` | |
| Remove | `map.remove(k)` | |
| How many | `map.size()` | |
| All keys | `map.keySet()` | |
| All values | `map.values()` | |
| Key and value together | `map.entrySet()` | |

```java idiom
// counting: the pattern to memorise
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    count.put(c, count.getOrDefault(c, 0) + 1);
}

// grouping: make the list only if it is missing
for (int i = 0; i < words.length; i++) {
    String key = keyOf(words[i]);
    if (!groups.containsKey(key)) groups.put(key, new ArrayList<>());
    groups.get(key).add(words[i]);
}
```

## 30.2 Walking a map

A map has no index, so `get(i)` does not exist. Two ways, both fine:

```java idiom
// 1. the for-each loop. This is the one place it is worth knowing (§31.2).
for (Map.Entry<Character, Integer> e : count.entrySet()) {
    char k = e.getKey();
    int v = e.getValue();
}

// 2. indexed, by copying the keys out first
List<Character> keys = new ArrayList<>(count.keySet());
for (int i = 0; i < keys.size(); i++) {
    char k = keys.get(i);
    int v = count.get(k);
}
```

The second one is also the safe way to delete while walking, because the copy is not the map.

## 30.3 Set operations

| Do this | Code | Notes |
| --- | --- | --- |
| Add | `set.add(x)` | Returns `false` if it was already there — a free duplicate check |
| Present? | `set.contains(x)` | O(1) average |
| Remove | `set.remove(x)` | |
| Size, empty | `set.size()`, `set.isEmpty()` | |
| From an array | loop with `add`, or `new HashSet<>(list)` | |

```java idiom
// "have I seen this before" in one line
if (!seen.add(a[i])) return true;      // add failed, so it is a duplicate
```

## 30.4 When to use something else

| Need | Use | Why |
| --- | --- | --- |
| Lowercase letters only | `int[26]` | Faster, simpler, no boxing: `count[c - 'a']++` |
| Digits only | `int[10]` | Same reason |
| Sorted keys, nearest key | `TreeMap` | `firstKey`, `floorKey`, `ceilingKey`, O(log n) |
| Sorted values, nearest value | `TreeSet` | `floor`, `ceiling`, `higher`, `lower` |
| Insertion order preserved | `LinkedHashMap` | Also the base for an LRU cache |

> [!WARNING]
> **`map.get(k)` returns `null`, and assigning it to an `int` throws.** `int v = map.get(k);` blows up on a missing key. Use `getOrDefault`.
>
> **Changing a map while a for-each walks it throws ConcurrentModificationException.** Copy the keys first, as above.
>
> **`HashMap` has no order at all.** If you print it and the order looks sorted, that is luck. Use `TreeMap` when order is part of the answer.
