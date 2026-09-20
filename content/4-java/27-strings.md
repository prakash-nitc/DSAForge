---
id: s27
numeral: §27
title: Strings — operations, comparison, splitting
---

A `String` never changes. Every "modification" builds a new one, which is why building a string inside a loop needs `StringBuilder` (§28).

## 27.1 The operations

| Do this | Code | Notes |
| --- | --- | --- |
| Length | `s.length()` | With parentheses, unlike `a.length` |
| One character | `s.charAt(i)` | Returns `char`, not `String` |
| Piece of it | `s.substring(i)` | From `i` to the end |
| Piece of it | `s.substring(i, j)` | `j` is **exclusive**; the length is `j - i` |
| Find | `s.indexOf("ab")` | `-1` when absent. `indexOf(ch, from)` to continue |
| Find last | `s.lastIndexOf("ab")` | |
| Contains | `s.contains("ab")` | |
| Starts, ends | `s.startsWith("ab")`, `s.endsWith("z")` | |
| Compare content | `s.equals(t)` | **Never** `==` |
| Ignore case | `s.equalsIgnoreCase(t)` | |
| Order | `s.compareTo(t)` | Negative, zero, positive. Sorts alphabetically |
| Empty | `s.isEmpty()` | Only length zero |
| Blank | `s.isBlank()` | Empty or only spaces |
| Trim spaces | `s.trim()` | Returns a new string |
| Case | `s.toLowerCase()`, `s.toUpperCase()` | |
| Replace | `s.replace('a', 'b')`, `s.replace("ab", "cd")` | All occurrences |
| Split | `s.split(" ")` | Argument is a regex |
| Join | `String.join(",", list)` | Also takes an array |
| Repeat | `"ab".repeat(3)` | |
| To characters | `s.toCharArray()` | The way to edit a string |
| Number to text | `String.valueOf(x)` | §24 |

## 27.2 Walking one

```java idiom
for (int i = 0; i < s.length(); i++) {
    char c = s.charAt(i);
    ...
}

// two pointers: the palindrome check
int i = 0, j = s.length() - 1;
while (i < j) {
    if (s.charAt(i) != s.charAt(j)) return false;
    i++;
    j--;
}
return true;

// editing: copy out, change, copy back
char[] ch = s.toCharArray();
for (int k = 0; k < ch.length; k++) {
    if (ch[k] == 'a') ch[k] = 'b';
}
String out = new String(ch);
```

## 27.3 Comparison, the one that fails silently

```java idiom
if (s.equals(t))            { }     // CORRECT: compares the characters
if (s == t)                 { }     // WRONG: compares object identity, sometimes true by luck
if (s.charAt(i) == t.charAt(j)) { } // fine: char is a primitive
if (s.isEmpty())            { }     // safe only when s is not null
```

> [!WARNING]
> **`split` takes a regular expression.** `s.split(".")` returns nothing at all, because a dot means "any character". Use `s.split("\\.")`. For runs of spaces use `s.split("\\s+")`, and trim first, since a leading space produces an empty first piece.
>
> **`substring(i, j)` throws when `j > s.length()`.** The end is exclusive, so the last valid call is `s.substring(i, s.length())`.
>
> **Concatenating in a loop is O(n²).** `res += c;` builds a whole new string each pass. Use `StringBuilder` (§28).

## 27.4 Characters as numbers

```java idiom
int idx = c - 'a';                       // 0..25 for lowercase
int val = c - '0';                       // 0..9 for a digit character
char up = Character.toUpperCase(c);
boolean d = Character.isDigit(c);
boolean l = Character.isLetterOrDigit(c);  // the usual filter for "valid palindrome"
```
