---
id: s24
numeral: §24
title: Conversions — every direction you actually need
---

One table per family. When you blank mid-problem, this is the page to open.

## 24.1 Numbers and text

| From | To | Code | Watch |
| --- | --- | --- | --- |
| `String` | `int` | `Integer.parseInt(s)` | Throws on spaces or empty text. `s.trim()` first |
| `String` | `long` | `Long.parseLong(s)` | Use for big inputs |
| `String` | `double` | `Double.parseDouble(s)` | |
| `int` | `String` | `String.valueOf(x)` | `"" + x` and `Integer.toString(x)` are the same thing |
| `int` | `long` | `(long) x` | Cast **before** multiplying: `(long) a * b` |
| `long` | `int` | `(int) v` | Silently truncates. Only when you know it fits |
| `double` | `int` | `(int) d` | Chops toward zero: `2.9` becomes `2` |
| `double` | rounded | `Math.round(d)` | Returns `long` for a double |
| `Integer` | `int` | `x` | Automatic, but a null `Integer` throws NullPointerException |
| `int` | `Integer` | `x` | Automatic. `Integer.valueOf(x)` is explicit |

## 24.2 Characters

| From | To | Code | Watch |
| --- | --- | --- | --- |
| `char` digit | its value | `c - '0'` | `'7' - '0'` is `7`. Only for `'0'`–`'9'` |
| value | `char` digit | `(char) (d + '0')` | The cast is required |
| `char` letter | 0–25 index | `c - 'a'` | This is how you index `int[26]` |
| 0–25 index | `char` | `(char) ('a' + i)` | |
| `char` | `String` | `String.valueOf(c)` | `"" + c` works too. `(String) c` does **not** compile |
| `String` | one `char` | `s.charAt(i)` | |
| `char` | uppercase | `Character.toUpperCase(c)` | Also `toLowerCase` |

Useful tests: `Character.isDigit(c)`, `isLetter(c)`, `isLetterOrDigit(c)`, `isUpperCase(c)`, `isWhitespace(c)`.

## 24.3 Strings, arrays and lists

| From | To | Code | Watch |
| --- | --- | --- | --- |
| `String` | `char[]` | `s.toCharArray()` | The standard way to edit a string |
| `char[]` | `String` | `new String(arr)` | `arr.toString()` prints garbage like `[C@1b6d` |
| `String` | `String[]` | `s.split(" ")` | The argument is a **regex**: a dot is `split("\\.")` |
| `String[]` | `String` | `String.join(",", arr)` | Works with a list too |
| `String` | `StringBuilder` | `new StringBuilder(s)` | |
| `StringBuilder` | `String` | `sb.toString()` | |
| `String[]` | `List<String>` | `new ArrayList<>(Arrays.asList(arr))` | Bare `Arrays.asList(arr)` is fixed size: `add` throws |
| `List<Integer>` | `int[]` | loop, see §23.4 | No one-liner without streams |
| `int[]` | `List<Integer>` | loop, see §23.4 | |

## 24.4 Bits and bases

```java idiom
Integer.toBinaryString(x);      // "1011"
Integer.parseInt("1011", 2);    // 11
Integer.toHexString(x);
Integer.bitCount(x);            // how many 1 bits
Integer.MAX_VALUE;              // 2147483647  -- the overflow line
Long.MAX_VALUE;                 // when int is not enough
```

> [!WARNING]
> **Two conversion traps that cost real marks**
>
> `Integer == Integer` compares object identity, and it only looks correct because Java caches −128 to 127. Compare boxed values with `a.equals(b)`, or pull out `int` values first. Plain `int == int` is always fine.
>
> `char + char` produces an `int`. `char next = (char) (c + 1);` needs the cast, and `'a' + 1` on its own is the number 98.
