---
id: s25
numeral: §25
title: Arrays — creation, size, walking, operations
---

## 25.1 Creating one

```java idiom
int[] a = new int[n];                  // n slots, all 0
int[] b = {3, 1, 2};                   // short form: ONLY on the declaration line
int[] c = new int[]{3, 1, 2};          // the long form works anywhere
String[] names = new String[n];        // all null: calling a method on one throws NPE
boolean[] seen = new boolean[n];       // all false
char[] letters = s.toCharArray();
int[][] grid = new int[rows][cols];    // all 0
int[][] fixed = {{1, 2}, {3, 4}};
int[] count = new int[26];             // letter counting, faster than a map
```

Defaults you get for free: `0` for `int` and `long`, `0.0` for `double`, `false` for `boolean`, `'\u0000'` for `char`, `null` for `String` and every other object.

## 25.2 Size — three different spellings

| Thing | Size | Note |
| --- | --- | --- |
| Array | `a.length` | No parentheses. This is the one people get wrong |
| String | `s.length()` | Parentheses |
| List, Map, Set, StringBuilder | `list.size()`, `sb.length()` | |
| 2D array | `g.length` rows, `g[0].length` columns | Rows first, always |

## 25.3 Walking one

```java idiom
for (int i = 0; i < a.length; i++) { ... }                  // forward
for (int i = a.length - 1; i >= 0; i--) { ... }             // backward
for (int i = 0; i < a.length - 1; i++) { a[i]; a[i + 1]; }  // adjacent pairs: stop one early
for (int i = 0, j = a.length - 1; i < j; i++, j--) { ... }  // two pointers from both ends
for (int i = 1; i < a.length; i++) { ... }                  // skip the first, compare with a[i-1]

for (int r = 0; r < g.length; r++) {                        // grid
    for (int c = 0; c < g[0].length; c++) {
        ...
    }
}
```

## 25.4 The operations

| Do this | Code | Notes |
| --- | --- | --- |
| Sort ascending | `Arrays.sort(a)` | Primitives only, in place |
| Sort part of it | `Arrays.sort(a, from, to)` | `to` is exclusive |
| Sort descending | box to `Integer[]`, then `Arrays.sort(b, Collections.reverseOrder())` | Or sort ascending and reverse |
| Sort rows by a column | `Arrays.sort(g, (x, y) -> Integer.compare(x[0], y[0]))` | Never `x[0] - y[0]`: it overflows |
| Fill | `Arrays.fill(a, -1)` | For 2D, loop over rows |
| Copy | `Arrays.copyOf(a, n)` | Longer `n` pads with zeros |
| Copy a slice | `Arrays.copyOfRange(a, i, j)` | `j` exclusive |
| Copy exactly | `a.clone()` | Shallow: for `int[][]` it copies row references only |
| Compare contents | `Arrays.equals(a, b)` | `a == b` compares references |
| Print for debugging | `Arrays.toString(a)`, `Arrays.deepToString(g)` | |
| Search a sorted array | `Arrays.binarySearch(a, key)` | Negative result means not found |
| Block copy | `System.arraycopy(src, sPos, dst, dPos, len)` | Fastest bulk copy |

```java idiom
// reverse in place
for (int i = 0, j = a.length - 1; i < j; i++, j--) {
    int t = a[i]; a[i] = a[j]; a[j] = t;
}

// max, min and sum in one pass
int max = Integer.MIN_VALUE, min = Integer.MAX_VALUE;
long sum = 0;                                   // long: an int sum overflows at ~2.1 billion
for (int i = 0; i < a.length; i++) {
    if (a[i] > max) max = a[i];
    if (a[i] < min) min = a[i];
    sum += a[i];
}

// counting with a fixed alphabet
int[] count = new int[26];
for (int i = 0; i < s.length(); i++) count[s.charAt(i) - 'a']++;
```

> [!WARNING]
> **An array cannot grow.** `new int[n]` is n slots forever. If you do not know the size in advance, collect into an `ArrayList` (§26) and convert at the end (§23.4).
>
> Index range is `0` to `length - 1`. `a[a.length]` is the classic ArrayIndexOutOfBoundsException, and `a[i + 1]` inside a loop that runs to `length - 1` is the same bug wearing a hat.
