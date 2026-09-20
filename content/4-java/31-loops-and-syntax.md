---
id: s31
numeral: §31
title: Loops, conditions and the small syntax
---

## 31.1 The loops you need

```java idiom
for (int i = 0; i < n; i++) { ... }          // start, keep going while, step
for (int i = n - 1; i >= 0; i--) { ... }     // backwards
for (int i = 0; i < n; i += 2) { ... }       // every second one

int i = 0;
while (i < n) { ...; i++; }                  // when the step is not regular

do { ... } while (cond);                     // runs at least once; rare

for (int i = 0; i < n; i++) {                // nested: i outer, j inner
    for (int j = i + 1; j < n; j++) { ... }  // j = i + 1 gives each pair once
}
```

`break` leaves the loop. `continue` skips to the next pass. Both act on the **innermost** loop only, so to leave a nested pair, set a flag or extract the loops into a method and `return`.

## 31.2 The for-each loop, in one minute

You can avoid it everywhere except maps and sets, which have no index. That makes it worth exactly one minute:

```java idiom
for (int x : a) { ... }                 // reads "for each int x in a"
```

`x` is a **copy**. Assigning to it changes nothing in the array, which is why editing always uses the indexed loop. You also lose `i`, so anything needing a position, a neighbour, or two pointers stays indexed.

## 31.3 Conditions and small operators

```java idiom
if (a > b) { ... } else if (a == b) { ... } else { ... }
int max = a > b ? a : b;                 // ternary: condition ? whenTrue : whenFalse
if (i < n && a[i] == x) { ... }          // && stops early, so the bounds check must come FIRST
if (s == null || s.isEmpty()) { ... }    // same idea for null

int q = 7 / 2;                           // 3: integer division chops
int r = 7 % 2;                           // 1: remainder
int neg = -7 % 3;                        // -1 in Java, NOT 2. Use ((x % m) + m) % m for a positive one
i++; i--; i += 3; i *= 2;
int mid = lo + (hi - lo) / 2;            // never (lo + hi) / 2: it overflows
```

```java idiom
switch (c) {                             // the classic form
    case 'a':
        ...
        break;                           // without break it falls through to the next case
    default:
        ...
}
```

## 31.4 A file you can run

```java idiom
public class Main {
    public static void main(String[] args) {
        int[] a = {3, 1, 2};
        System.out.println(solve(a));
        System.out.println(Arrays.toString(a));   // arrays never print by themselves
    }

    static int solve(int[] a) {                   // static, because main is static
        return a.length;
    }
}
```

On LeetCode you get `class Solution` instead and you never write `main`. Fast input for large inputs is §21.1.

## 31.5 Printing and debugging

```java idiom
System.out.println(x);
System.out.println("i=" + i + " val=" + a[i]);       // + glues text and numbers
System.out.printf("%d %.2f%n", count, avg);          // %n is the newline
System.out.println(Arrays.toString(a));              // array
System.out.println(Arrays.deepToString(grid));       // 2D array
System.out.println(list);                            // lists and maps print fine on their own
```

## 31.6 The errors, and what they mean

| What you see | Cause | Fix |
| --- | --- | --- |
| cannot find symbol | Typo, or declared inside a narrower `{ }` | Declare before the loop that uses it |
| incompatible types | Returning or assigning the wrong type | §23.2, §24 |
| missing return statement | A path returns nothing | Add a final `return` |
| ArrayIndexOutOfBoundsException | `a[a.length]`, or `a[i + 1]` on the last pass | Loop to `length - 1` when you look ahead |
| StringIndexOutOfBoundsException | `charAt` or `substring` past the end | The `substring` end is exclusive |
| NullPointerException | Method called on `null`: an unfilled `String[]`, a missing map key | `getOrDefault`, and check for `null` first |
| ConcurrentModificationException | Changing a list or map while a for-each walks it | Walk backwards by index, or copy the keys |
| NumberFormatException | `Integer.parseInt` on spaces or empty text | `trim()` first |
| Stack overflow | Recursion with no base case, or depth beyond ~10⁴ | Fix the base case, or rewrite as a loop with a stack (§29) |

> [!TIP]
> **Scope in one line**
>
> A variable declared inside `{ }` dies at the closing brace. `int best` used after a loop must be declared **before** the loop. That single rule explains most "cannot find symbol" errors.
