---
id: s15
numeral: §15
title: Tries
card: 16
---

Not on your sheet at all, and it is a one-day topic that unlocks an entire class of string questions. Worth doing after Graphs and before deep DP.

## 15.1 The template

```java
class TrieNode {
    TrieNode[] next = new TrieNode[26];
    boolean isWord;
}

TrieNode root = new TrieNode();

void insert(String w) {
    TrieNode cur = root;
    for (char ch : w.toCharArray()) {
        int i = ch - 'a';
        if (cur.next[i] == null) cur.next[i] = new TrieNode();
        cur = cur.next[i];
    }
    cur.isWord = true;
}

TrieNode walk(String w) {                 // shared by search and startsWith
    TrieNode cur = root;
    for (char ch : w.toCharArray()) {
        cur = cur.next[ch - 'a'];
        if (cur == null) return null;
    }
    return cur;
}

boolean search(String w)     { TrieNode n = walk(w); return n != null && n.isWord; }
boolean startsWith(String p) { return walk(p) != null; }
```

*One walk() helper serves both queries. Writing search and startsWith as two separate loops is the mark of someone who hasn't thought about it.*

## 15.2 Wildcard search (the '.' variant)

```java
boolean dfs(String w, int i, TrieNode node) {
    if (node == null) return false;
    if (i == w.length()) return node.isWord;
    char ch = w.charAt(i);
    if (ch != '.') return dfs(w, i + 1, node.next[ch - 'a']);
    for (TrieNode nx : node.next)                 // '.' -> try every branch
        if (dfs(w, i + 1, nx)) return true;
    return false;
}
```

## 15.3 When to reach for a trie

- Many prefix queries against a fixed dictionary — autocomplete, spell check.
- "Word search on a board against a word list" — Word Search II. A trie turns a hopeless O(words × board) search into one board DFS guided by the trie.
- Longest common prefix across many strings.
- Bitwise tries: maximum XOR pair, using a 32-level binary trie. Niche but occasionally asked at semiconductor companies.
- Replace words / prefix substitution problems.

## 15.4 Problems, in order

| Problem | Why |
| --- | --- |
| Implement Trie (LC 208) | The template itself. Thirty minutes. |
| Design Add and Search Words (LC 211) | The wildcard variant. Twenty minutes after 208. |
| Longest Common Prefix (LC 14) | Doesn't need a trie, but shows when a trie is overkill — a useful judgement rep. |
| Word Search II (LC 212) | The payoff problem. Trie + grid backtracking (Card 12, Template 12C). |
| Maximum XOR of Two Numbers (LC 421) | Bitwise trie. Only if you have slack; strong signal if you land it. |

## 15.5 Complexity and follow-ups

| Operation | Time | Space |
| --- | --- | --- |
| insert / search / startsWith | O(L) where L is word length | O(total characters × 26) |

- "Trie or HashSet?" — HashSet gives O(1) exact lookup but cannot do prefixes. The moment prefixes matter, the trie wins.
- "How would you save memory?" — a HashMap<Character, TrieNode> instead of a 26-slot array when the alphabet is sparse, or a compressed/radix trie.
- "How do you delete a word?" — unset isWord, then prune upward while nodes have no children and aren't words themselves.
