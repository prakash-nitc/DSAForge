---
id: app-f
numeral: Appendix F
title: Edge-case checklist
---

| Input type | Always test |
| --- | --- |
| Array | empty · single element · two elements · all equal · all negative · duplicates · already sorted · reverse sorted · max/min int values |
| String | empty · single char · all same char · mixed case · spaces · non-alphanumeric · very long |
| Linked list | null head · single node · two nodes · cycle present · k larger than length |
| Tree | null root · single node · left-skewed · right-skewed · complete · duplicate values · negative values |
| Graph | single node · no edges · disconnected · self-loop · parallel edges · cycle · fully connected |
| Matrix | 1×1 · single row · single column · non-square · all zeros |
| Numeric range | 0 · 1 · negative · Integer.MAX_VALUE · Integer.MIN_VALUE · overflow on sum or product |
| k-style parameter | k = 0 · k = 1 · k = n · k > n |

> [!TIP]
> **Volunteer these, don't wait to be asked**
>
> Saying "let me check the empty case and the all-negative case" before the interviewer does is one of the cheapest positive signals available. It costs twenty seconds and it separates you from candidates who submit and hope.
