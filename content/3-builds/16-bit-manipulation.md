---
id: s16
numeral: §16
title: Bit Manipulation
card: 17
---

Not on your sheet. A one-day topic, and disproportionately valuable if Qualcomm, AMD, Sandisk or Intel are still on your list — those companies ask it directly.

## 16.1 The operations you must have automatic

```java
x & 1                    // is x odd?
x >> 1                   // divide by 2 (arithmetic shift, keeps sign)
x >>> 1                  // UNSIGNED right shift -- Java-specific, use for bit counting
x & (1 << i)             // test bit i
x | (1 << i)             // set bit i
x & ~(1 << i)            // clear bit i
x ^ (1 << i)             // toggle bit i

x & (x - 1)              // clear the LOWEST set bit   <- the workhorse
x & (-x)                 // isolate the lowest set bit
x == 0 ? false : (x & (x-1)) == 0    // is x a power of two?

Integer.bitCount(x)      // popcount
Integer.highestOneBit(x) // largest power of 2 <= x
Integer.toBinaryString(x)

a ^ a == 0,  a ^ 0 == a,  XOR is commutative and associative
```

- **x & (x - 1) is the one to memorise.** Counting set bits by repeatedly clearing the lowest one runs in O(number of set bits), not O(32).

## 16.2 The XOR tricks

```java
// Single Number: every element appears twice except one
int r = 0; for (int x : a) r ^= x; return r;

// Missing number in [0..n]
int r = n; for (int i = 0; i < n; i++) r ^= i ^ a[i]; return r;

// Two numbers appear once, everything else twice:
//   1. XOR everything -> gives a ^ b
//   2. take the lowest set bit of that -> a bit where a and b differ
//   3. partition the array by that bit, XOR each half separately

// Swap without a temp (a party trick; never write this in production)
a ^= b; b ^= a; a ^= b;
```

## 16.3 Subset enumeration with bitmasks

```java
// All 2^n subsets of an n-element set (n <= ~20)
for (int mask = 0; mask < (1 << n); mask++) {
    List<Integer> sub = new ArrayList<>();
    for (int i = 0; i < n; i++)
        if ((mask & (1 << i)) != 0) sub.add(a[i]);
    ...
}

// Enumerate all SUBMASKS of a mask (used in bitmask DP)
for (int s = mask; s > 0; s = (s - 1) & mask) { ... }
```

- **The constraint tell:** n ≤ 20 in the constraints almost always means bitmask. See §9.2.

## 16.4 Problems, in order

| Problem | Idea |
| --- | --- |
| Single Number (LC 136) | XOR cancellation. Five minutes. |
| Number of 1 Bits (LC 191) | x & (x-1) loop. |
| Counting Bits (LC 338) | DP on bits: dp[i] = dp[i >> 1] + (i & 1). A lovely DP-meets-bits problem. |
| Missing Number (LC 268) | XOR or Gauss sum. Know both. |
| Reverse Bits (LC 190) | Shift-and-accumulate; watch the unsigned shift. |
| Power of Two (LC 231) | x & (x-1) == 0. |
| Single Number II / III | The 'appears three times' and 'two singletons' variants. Genuinely harder. |
| Subsets via bitmask (LC 78) | Ties back to Card 12 — the iterative alternative to backtracking. |

## 16.5 Java-specific traps

- >> is arithmetic and preserves the sign bit; >>> is logical. On a negative int, >> loops forever if you are shifting until zero. Use >>>.
- 1 << 31 overflows into Integer.MIN_VALUE. Use 1L << 31 when you need the value.
- Shift counts are taken modulo 32 for int and 64 for long: x << 32 is x, not zero.
- Operator precedence: & and | bind more loosely than ==. Always parenthesise (x & mask) != 0.
