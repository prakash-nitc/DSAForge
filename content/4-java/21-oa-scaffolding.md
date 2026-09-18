---
id: s21
numeral: §21
title: OA scaffolding
---

## 21.1 Fast input for large inputs

```java idiom
// Scanner is too slow above ~10^5 tokens. Use this instead.
BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
StringTokenizer st = new StringTokenizer(br.readLine());
int n = Integer.parseInt(st.nextToken());

// Fast output -- never call System.out.println in a tight loop
StringBuilder sb = new StringBuilder();
for (int x : ans) sb.append(x).append('\n');
System.out.print(sb);
```

*Most OA platforms give you a function signature, so this rarely matters — but on Codeforces-style judges and a few company platforms it is the difference between AC and TLE.*

## 21.2 The five-minute environment check before any OA

- Can you write a PriorityQueue with a custom comparator without looking it up?
- Can you write ArrayDeque used as a stack, and as a queue, without mixing the method families?
- Do you have the DIRS array and the grid bounds check in muscle memory?
- Do you reflexively reach for long on any accumulation?
- Do you know your IDE's shortcut for running a single test quickly?

## 21.3 The pre-submit checklist

| Check | Why |
| --- | --- |
| Empty input, single element | The two most common hidden test cases |
| All elements equal / all negative | Kills naive Kadane and several greedy solutions |
| Integer bounds — could any accumulator exceed 2³¹? | Silent wrong answer, hardest bug to find |
| Did I mutate the input when the caller needs it? | Common in in-place patterns |
| Off-by-one on every loop bound and every array size | n vs n+1 in DP; < vs <= in binary search |
| Did I return the right thing — the value, the index, or the count? | Reading the signature again takes ten seconds |
