---
id: s12
numeral: §12
title: Trees — the five shapes
card: 13
---

You have eleven tree problems and every one is a traversal or a mirror/symmetry check. That is one shape out of five. The other twenty problems on your sheet are not twenty problems — they are four shapes you have never practised, with roughly five instances each.

**This reframe is the entire section. Learn the shapes and the twenty become mechanical.**

## 12.0 The base node and the two questions

```java
class TreeNode { int val; TreeNode left, right; }

// Before writing ANY tree recursion, answer these two:
//   1. What do I RETURN to my parent?
//   2. What do I RECORD in the answer?
// If those are the same thing, it's a simple recursion.
// If they differ, it's Shape A and that difference IS the problem.
```

## 12.1 Shape A — Bottom-up: return one thing, record another

The most important shape in trees and the one that separates candidates. Information flows upward from the leaves; you combine children's results, record something about paths through the current node, and return something else to the parent.

```java
int best = 0;                              // recorded answer (field, not parameter)

int depth(TreeNode n) {
    if (n == null) return 0;
    int L = depth(n.left);
    int R = depth(n.right);
    best = Math.max(best, L + R);          // RECORD: longest path THROUGH n (diameter)
    return 1 + Math.max(L, R);             // RETURN: height, for the parent to use
}

// Maximum Path Sum — same skeleton, one extra guard
int gain(TreeNode n) {
    if (n == null) return 0;
    int L = Math.max(0, gain(n.left));     // a negative subtree is DROPPED, not added
    int R = Math.max(0, gain(n.right));
    best = Math.max(best, n.val + L + R);  // RECORD: path bending at n
    return n.val + Math.max(L, R);         // RETURN: a straight path the parent can extend
}

// Balanced Binary Tree — use a sentinel to fail fast
int h(TreeNode n) {
    if (n == null) return 0;
    int L = h(n.left);  if (L == -1) return -1;
    int R = h(n.right); if (R == -1) return -1;
    if (Math.abs(L - R) > 1) return -1;    // -1 propagates 'unbalanced' upward
    return 1 + Math.max(L, R);
}
```

- **Covers:** Maximum Depth, Minimum Depth, Diameter of Binary Tree, Balanced Binary Tree, Binary Tree Maximum Path Sum, LCA of Deepest Leaves, LCA of Binary Tree.
- **The drill:** for each of those, write the two blanks before coding — "I return ___, I record ___". If you can fill both, the problem is solved.
- **The trap in Max Path Sum:** Math.max(0, childGain). A negative subtree should contribute nothing, not a negative. That single guard is the whole difficulty.
- **The trap in Minimum Depth:** a node with one null child is NOT a leaf. min(L, R) returns 0 through the null side and gives the wrong answer. Handle the single-child case explicitly.

### LCA of a Binary Tree is Shape A in disguise

```java
TreeNode lca(TreeNode n, TreeNode p, TreeNode q) {
    if (n == null || n == p || n == q) return n;
    TreeNode L = lca(n.left,  p, q);
    TreeNode R = lca(n.right, p, q);
    if (L != null && R != null) return n;      // p and q split here -> n is the LCA
    return L != null ? L : R;                  // both on one side, or neither
}
```

*Return: 'the LCA if I found it, otherwise whichever target I saw'. Record: nothing. Four lines, and it is asked constantly.*

## 12.2 Shape B — Top-down: pass state down, act at the leaves

```java
void dfs(TreeNode n, int running) {
    if (n == null) return;
    running = running * 10 + n.val;                  // accumulate on the way DOWN
    if (n.left == null && n.right == null) {         // LEAF, not null
        total += running;
        return;
    }
    dfs(n.left,  running);
    dfs(n.right, running);
}

// Path Sum II — top-down with backtracking
void dfs(TreeNode n, int rem, List<Integer> path) {
    if (n == null) return;
    path.add(n.val);
    if (n.left == null && n.right == null && rem == n.val)
        res.add(new ArrayList<>(path));              // defensive copy
    else {
        dfs(n.left,  rem - n.val, path);
        dfs(n.right, rem - n.val, path);
    }
    path.remove(path.size() - 1);                    // UN-CHOOSE
}
```

- **Covers:** Path Sum, Path Sum II, Sum Root to Leaf Numbers, and every root-to-leaf variant you will ever meet.
- **The trap:** a leaf is a node with no children. A null node is not a leaf. Using n == null as the leaf test makes Path Sum return true for a single-child chain — the most common tree bug in interviews.
- **The link to Card 12:** Path Sum II is choose / explore / un-choose. It is backtracking on a tree, and recognising that makes it free.

## 12.3 Shape C — The BST invariant

A BST is not defined by "left child smaller than parent". It is defined by a range that narrows as you descend. Getting this wrong is exactly why a naive Validate BST passes [5,1,6,null,null,3,7] when it should fail.

```java
boolean valid(TreeNode n, long lo, long hi) {
    if (n == null) return true;
    if (n.val <= lo || n.val >= hi) return false;
    return valid(n.left, lo, n.val) && valid(n.right, n.val, hi);
}
// call with Long.MIN_VALUE / Long.MAX_VALUE -- Integer.MIN_VALUE is a legal node value

// THE OTHER BST SUPERPOWER: inorder traversal of a BST is SORTED.
//   Kth Smallest   -> inorder, stop at the kth visit
//   Validate BST   -> inorder, check strictly increasing
//   Two Sum IV     -> inorder into a list, then Card 1 two pointers
//   Recover BST    -> inorder, find the two out-of-order nodes, swap their VALUES

// LCA of a BST -- three lines, because ordering tells you the direction
TreeNode lcaBST(TreeNode n, TreeNode p, TreeNode q) {
    while (n != null) {
        if (p.val < n.val && q.val < n.val)      n = n.left;
        else if (p.val > n.val && q.val > n.val) n = n.right;
        else return n;                            // they split here
    }
    return null;
}
```

- **Covers:** Validate BST, Search in a BST, Kth Smallest in a BST, LCA of BST, Two Sum IV, Recover BST, Convert Sorted Array to BST.
- **Start with LCA of BST.** Three lines, immediate win, and it demonstrates the ordering property that carries the whole shape.
- **Recover BST is the elegant one:** in a corrupted inorder sequence, the first violation gives you node one and the last violation gives you node two. Swap values, not nodes.

## 12.4 Shape D — Construction from traversals

Two facts do all the work. Preorder's FIRST element is the root. Postorder's LAST element is the root. Inorder splits into left subtree and right subtree around the root. Everything else is index arithmetic.

```java
Map<Integer,Integer> idx = new HashMap<>();     // value -> index in inorder
int pre = 0;

TreeNode build(int[] preorder, int inLo, int inHi) {
    if (inLo > inHi) return null;
    int rootVal = preorder[pre++];
    TreeNode root = new TreeNode(rootVal);
    int mid = idx.get(rootVal);
    root.left  = build(preorder, inLo, mid - 1);     // LEFT first for preorder
    root.right = build(preorder, mid + 1, inHi);
    return root;
}

// POSTORDER version: consume from the END, and build RIGHT before LEFT.
int post;   // starts at postorder.length - 1
TreeNode buildPost(int[] postorder, int inLo, int inHi) {
    if (inLo > inHi) return null;
    int rootVal = postorder[post--];
    TreeNode root = new TreeNode(rootVal);
    int mid = idx.get(rootVal);
    root.right = buildPost(postorder, mid + 1, inHi);   // RIGHT FIRST
    root.left  = buildPost(postorder, inLo, mid - 1);
    return root;
}
```

- **Covers:** Construct from Preorder and Inorder, Construct from Postorder and Inorder, Convert Sorted Array to BST (the degenerate case where inorder is the entire input).
- **The trap:** without the HashMap you scan inorder linearly and the solution is O(n²). Interviewers wait for that map.
- **The postorder trap:** you must build the RIGHT subtree first, because you are consuming the array backwards. Reversing that is the whole problem.

## 12.5 Shape E — Level order (you already have this)

```java
Queue<TreeNode> q = new ArrayDeque<>();
if (root != null) q.add(root);
while (!q.isEmpty()) {
    int sz = q.size();                        // FREEZE the level boundary
    List<Integer> level = new ArrayList<>();
    for (int i = 0; i < sz; i++) {
        TreeNode n = q.poll();
        level.add(n.val);
        if (n.left  != null) q.add(n.left);
        if (n.right != null) q.add(n.right);
    }
    res.add(level);
}
```

**The int sz = q.size() line is the entire trick. Once you have it: zigzag is "reverse alternate levels", right-side view is "take the last of each level", level-order II is "reverse the outer list", maximum depth is "count the iterations", and level averages are "sum ÷ sz". Five problems, one line of insight.**

### Also worth having: iterative traversals

```java
// Iterative INORDER -- the one people can't reproduce under pressure
Deque<TreeNode> st = new ArrayDeque<>();
TreeNode cur = root;
while (cur != null || !st.isEmpty()) {
    while (cur != null) { st.push(cur); cur = cur.left; }
    cur = st.pop(); visit(cur); cur = cur.right;
}

// Iterative POSTORDER -- preorder with children swapped, then reversed
// push root; pop, add to front of result; push LEFT then RIGHT
```

## 12.6 Your 31 tree problems, mapped to shapes

| Shape | Problems | Status | Day |
| --- | --- | --- | --- |
| A — Bottom-up | Maximum Depth · Minimum Depth · Diameter · Balanced Binary Tree · Binary Tree Maximum Path Sum · LCA of Deepest Leaves · LCA of Binary Tree | [All untouched]{.red} | 1–2 |
| B — Top-down | Path Sum · Path Sum II · Sum Root to Leaf Numbers | [All untouched]{.red} | 2 |
| C — BST | Search in a BST · LCA of BST · Kth Smallest in a BST · Validate BST · Two Sum IV · Recover BST · Convert Sorted Array to BST | [All untouched]{.red} | 3 |
| D — Construction | Construct from Preorder+Inorder · Construct from Postorder+Inorder | [Untouched]{.red} | 4 |
| E — Level order | Level Order · Level Order II · Zigzag Level Order · Check Completeness | [3 of 4 solved]{.green} | Repair |
| F — Mirror / structural | Invert Binary Tree · Symmetric Tree · Same Tree · Subtree of Another Tree · Flip Equivalent Binary Trees | [All solved]{.green} | Repair |
| Traversals | Inorder · Preorder · Postorder | [Solved (recursive)]{.green} | Add iterative |

## 12.7 The four-day build

| Day | Shape | Problems (5 each) | Blank-page target |
| --- | --- | --- | --- |
| 1 | A — bottom-up | Maximum Depth → Minimum Depth → Balanced → Diameter → LCA of Binary Tree | The return/record skeleton |
| 2 | A finish + B | Binary Tree Maximum Path Sum → LCA of Deepest Leaves → Path Sum → Path Sum II → Sum Root to Leaf | Top-down with backtracking |
| 3 | C — BST | Search in BST → LCA of BST → Kth Smallest → Validate BST → Two Sum IV → Recover BST | The range-narrowing validator |
| 4 | D + E repair | Construct Pre+In → Construct Post+In → Convert Sorted Array to BST → Check Completeness → iterative inorder | Both construction directions |

> [!TIP]
> **Do not spread this over two weeks**
>
> Shapes are learned by doing five instances back to back and feeling the sameness. Five problems a day for four days, then one repair pass a week later. That is the entire tree plan, and it closes twenty of your sixty-five unsolved rows.

## 12.8 Complexity and follow-ups

| Operation | Time | Space |
| --- | --- | --- |
| Any full traversal (DFS or BFS) | O(n) | O(h) recursion / O(w) queue |
| BST search / insert / delete | O(h): O(log n) balanced, O(n) skewed | O(1) iterative |
| Construction from two traversals | O(n) with a HashMap, O(n²) without | O(n) |
| Serialize / deserialize | O(n) | O(n) |

- "Why is BST search O(h) and not O(log n)?" — because h is only log n if the tree is balanced. A sorted insertion sequence gives you a linked list.
- "How would you balance it?" — AVL or red-black rotations; you don't need to implement them, but know the names and the invariant each maintains.
- "Do it iteratively / with O(1) space." — Morris traversal uses threading to achieve O(1). Worth knowing it exists; rarely required.
- "Serialize and deserialize a binary tree." — preorder with null markers is the cleanest. A common follow-up to construction problems.
- "What if the tree is enormous and doesn't fit in memory?" — the cue to talk about BFS with an external queue, or B-trees.

## 12.9 Tree bugs in Java

- Using n == null as the leaf test instead of n.left == null && n.right == null.
- Recursion depth on a skewed tree of 10⁵ nodes — StackOverflowError. Mention the iterative alternative.
- Integer bounds in Validate BST — use long, or pass Integer objects and null-check.
- res.add(path) instead of res.add(new ArrayList<>(path)) in Path Sum II.
- LinkedList instead of ArrayDeque for the BFS queue — slower and it accepts nulls, hiding bugs.
- Computing q.size() inside the loop after polling, which loses the level boundary.
