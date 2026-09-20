---
id: s28
numeral: §28
title: StringBuilder — building text without the O(n²)
---

Any string you assemble in a loop goes through a `StringBuilder`. It is a growable `char[]` with a friendly surface.

```java idiom
StringBuilder sb = new StringBuilder();        // empty
StringBuilder sb2 = new StringBuilder(s);      // starts with an existing string
```

## 28.1 The operations

| Do this | Code | Notes |
| --- | --- | --- |
| Add to the end | `sb.append(x)` | Takes `String`, `char`, `int`, anything |
| Add at a position | `sb.insert(i, x)` | O(n) |
| Length | `sb.length()` | A method, like `String` |
| Read one character | `sb.charAt(i)` | |
| Change one character | `sb.setCharAt(i, c)` | |
| Remove the last | `sb.deleteCharAt(sb.length() - 1)` | The backtracking undo |
| Remove a range | `sb.delete(i, j)` | `j` exclusive |
| Replace a range | `sb.replace(i, j, "x")` | |
| Empty it, keep the object | `sb.setLength(0)` | Faster than making a new one |
| Reverse | `sb.reverse()` | In place, returns itself |
| Finish | `sb.toString()` | Call once, at the end |
| Find | `sb.indexOf("ab")` | |

## 28.2 The three patterns you actually use

```java idiom
// 1. build a result in a loop
StringBuilder sb = new StringBuilder();
for (int i = 0; i < a.length; i++) {
    sb.append(a[i]);
    if (i < a.length - 1) sb.append(",");     // separator between, not after
}
String out = sb.toString();

// 2. reverse a string
String rev = new StringBuilder(s).reverse().toString();

// 3. backtracking with characters
sb.append(c);                                  // choose
dfs(...);                                      // explore
sb.deleteCharAt(sb.length() - 1);              // undo
```

## 28.3 Run-length encoding, the shape that shows up in OAs

```java idiom
StringBuilder sb = new StringBuilder();
int i = 0;
while (i < s.length()) {
    char c = s.charAt(i);
    int j = i;
    while (j < s.length() && s.charAt(j) == c) j++;   // stretch the run
    sb.append(c).append(j - i);                       // append chains
    i = j;
}
return sb.toString();
```

> [!NOTE]
> **Three things to remember**
>
> Call `toString()` once, at the end. Calling it inside the loop copies everything each time and brings back the O(n²) you were avoiding.
>
> `sb.equals(other)` compares objects, not text. Compare `sb.toString().equals(t)`.
>
> `append` returns the builder, so `sb.append(a).append(b)` chains. `sb = sb.append(a)` is pointless but harmless.
