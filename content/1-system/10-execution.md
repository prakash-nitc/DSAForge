---
id: s10
numeral: §10
title: Execution — the OA and the interview
---

Preparation is one skill; performing under a timer with someone watching is another. This section is the second one.

## 10.1 The seven-step method (every problem, always)

| Step | What | Why it matters |
| --- | --- | --- |
| 1 | Restate the problem in your own words. | Forces clarity and catches misreads before they cost 20 minutes. |
| 2 | Name the pattern — or admit you can't and go to §9. | Identification is the skill being tested first. |
| 3 | State the brute force and its complexity out loud. | Guarantees you have something. Also the interview safety net. |
| 4 | Dry-run on a small input BEFORE coding. | Catches the inverted comparison on paper, not in the debugger. |
| 5 | Code it, narrating the invariant as you go. | The invariant is what the interviewer is listening for. |
| 6 | Test: sample, empty, single, boundary, duplicate. | Volunteering edge cases reads as seniority. |
| 7 | State final complexity, time and space, unprompted. | Not saying it is a silent deduction. |

## 10.2 OA triage — the first three minutes

- Read ALL problems before writing a line. Three minutes, no exceptions.
- Rank by (confidence × points) ÷ estimated time. Do the highest ratio first, not the first one on screen.
- If you cannot name a pattern in three minutes, flag it and move on. Come back with whatever time remains.
- Bank a full solve before attempting a partial. Two clean problems beat three half-solutions in almost every scoring scheme.
- Fifteen minutes left and nothing working? Write the brute force. Partial credit is real credit.
- Never leave a problem completely blank. A brute force with correct I/O handling scores; an empty editor does not.

## 10.3 The interview talk-track

```talk-track
"Let me restate: given <input>, I need <output>, with <constraints>. Correct?"
"Two clarifiers: can the input be empty, and can values be negative?"
"Let me try a small example..."                     [work it on the board]
"The brute force is <X>, which is O(n^2). Let me see what's wasteful."
"I'm recomputing <Y> — that suggests <pattern>."
"Here's my plan: <3 sentences>. Shall I code it?"     [pause for buy-in]
                                                       [code, narrating the invariant]
"Let me trace it on the example... and now the edges: empty, single, duplicates."
"Final complexity: O(n log n) time, O(n) space. The bottleneck is the sort."
"If I had more time I'd <one concrete improvement>."
```

## 10.4 What to say when you are stuck, live

- **Never go silent.** Silence is the only unrecoverable failure mode. An interviewer cannot help a black box.
- **Narrate the search, not the panic.** "I'm trying to decide between a heap and sorting here — the heap wins if I only need the top K." That sentence is worth points even if you then pick wrong.
- **Ask for a nudge properly.** "I've established X and Y. I'm stuck on Z. Am I on a reasonable track?" — a targeted question reads as competence; "I'm stuck" reads as surrender.
- **Take the hint immediately and visibly.** Interviewers score how you use a hint, not whether you needed one. Say "that's helpful — so if I…" and move.
- **When time is short, say so.** "I have the approach; let me code the core and describe the edge handling rather than typing it." That is a senior move, not a concession.

## 10.5 The four things that lose interviews that have nothing to do with algorithms

- Coding before agreeing on the approach. Ten minutes of wrong code is far worse than two minutes of alignment.
- Not stating complexity unprompted. It reads as not knowing.
- Being unable to defend your own project. For VISA and SAP this decides the round outright.
- Arguing with a hint. Even a wrong-sounding hint is a signal about what they want to see.
