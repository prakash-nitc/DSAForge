---
id: card-9
numeral: Card 9
title: Hash Maps & Frequency
---

| Status | Your coverage | Current level | Target |
| --- | --- | --- | --- |
| Fold into other cards | 4 / 4 | L2 | L4 — but never study this in isolation |

## Template 9A — Frequency counting, three ways

```java
// fixed lowercase alphabet: fastest, O(1) space
int[] cnt = new int[26];
for (char ch : s.toCharArray()) cnt[ch - 'a']++;

// general keys
Map<Character,Integer> m = new HashMap<>();
for (char ch : s.toCharArray()) m.merge(ch, 1, Integer::sum);

// grouping
Map<String,List<String>> g = new HashMap<>();
g.computeIfAbsent(key, x -> new ArrayList<>()).add(word);
```

## Template 9B — Complement lookup (Two Sum shape)

```java
Map<Integer,Integer> seen = new HashMap<>();      // value -> index
for (int i = 0; i < n; i++) {
    Integer j = seen.get(target - a[i]);
    if (j != null) return new int[]{ j, i };
    seen.put(a[i], i);                            // insert AFTER the lookup
}
```

*Insert after the lookup, not before — otherwise an element pairs with itself when target == 2\*a[i].*

## Template 9C — Canonical key for grouping

```java
// anagram groups: sorted characters, or a 26-slot signature
char[] arr = word.toCharArray(); Arrays.sort(arr);
String key = new String(arr);
// faster: build "1#0#2#..." from an int[26] count array
```

## Template 9D — LinkedHashMap as an LRU cache

```java
new LinkedHashMap<K,V>(cap, 0.75f, true) {          // true = access order
    protected boolean removeEldestEntry(Map.Entry<K,V> e) { return size() > cap; }
};
```

*Know this exists; in an interview they usually want the HashMap + doubly-linked-list version so you can explain the O(1) guarantees.*

## The knobs — what actually varies across this family

- **Key design —** the whole difficulty of most hash problems is choosing what to key on.
- **Value —** count, index, first index, or a list.
- **Array vs map —** fixed small alphabet → int[26] or int[128]; anything else → HashMap.

## Trigger signals

- "Have I seen this before / how many times"
- "Group these by some property"
- "Find the pair / complement"
- Deduplication, or an O(1) membership test
- Any O(n²) scan where an inner loop is just searching

## Anchors — cold re-solve these, 15-minute cap

| # | Anchor | Why this one |
| --- | --- | --- |
| 1 | Longest Palindrome | Counting with parity reasoning — more thought than it looks. |
| 2 | First Non-repeating Character | Two passes, or a LinkedHashMap. Both worth knowing. |
| 3 | Ransom Note | Trivial, but it is the 30-second warm-up that confirms the counting idiom is automatic. |

## Your sheet, mapped to templates

| Template | Your problems |
| --- | --- |
| 9A | Ransom Note · Maximum Number of Balloons · Longest Palindrome · First Non-repeating Character |
| Used inside other cards | Subarray Sum Equals K (Card 5) · No-repeat Substring (Card 3) · Top K Frequent (Card 11) · Accounts Merge (Card 14) |

## Decay signatures — how you'll know it's gone

- You write a nested loop where a map would make it linear.
- You use get() and NPE on auto-unboxing instead of getOrDefault.
- You forget that HashMap iteration order is undefined and depend on it.
- You choose a key that doesn't actually distinguish the groups.

## Java bugs specific to this pattern

- Integer caching: == works for values in −128..127 and silently fails outside it. Use .equals() or intValue().
- map.get() returns null; int x = map.get(k) NPEs. Use getOrDefault.
- Mutating an object used as a key corrupts the map — its hash changes and it becomes unreachable.
- HashMap has no ordering; if you need sorted keys or floor/ceiling, you want TreeMap and O(log n).

## Complexity

| Variant | Time | Space |
| --- | --- | --- |
| HashMap get / put | O(1) average, O(n) worst | O(n) |
| TreeMap get / put / floorKey / ceilingKey | O(log n) | O(n) |
| int[26] counting | O(1) | O(1) |

## Interview follow-ups you will be asked

- "What's the worst case for a HashMap and why?" — hash collisions degrade to a list; Java 8+ converts long buckets to red-black trees, giving O(log n) rather than O(n).
- "How would you implement a HashMap?" — buckets, hash function, collision resolution, load factor, resize.
- "When would you use TreeMap instead?" — ordering, range queries, floor/ceiling. Trade O(1) for O(log n) to buy structure.
- "Design an LRU cache." — HashMap + doubly linked list. Be able to draw it.

## Additions

- **Group Anagrams (LC 49) —** the canonical key-design problem. Do it; it teaches the skill the other three don't.
- **LRU Cache (LC 146) —** a design classic asked at Oracle and Flipkart. Worth one session.
- **Longest Consecutive Sequence (LC 128) —** the O(n) HashSet trick that looks impossible until you see it.
- **Do not run this card in isolation.** Hash maps are a component of Cards 3, 5, 11 and 14. Fold the practice into those sessions.
