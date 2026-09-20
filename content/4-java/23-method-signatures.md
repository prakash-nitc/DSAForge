---
id: s23
numeral: §23
title: Method signatures — the line you write before the logic
---

Most "I forgot the syntax" moments happen on the first line of the method, not inside the algorithm. This page is that first line, and the return statement that has to match it.

## 23.1 The anatomy of a signature

```java idiom
public        int[]        twoSum      (int[] nums, int target)  { ... }
// visibility  return type  method name  parameters: type, then name, comma separated
```

The return type is a promise: every `return` in the method must hand back exactly that type. Change the algorithm all you like; the signature is fixed by the question.

## 23.2 What the question asks for, and what you write

| The answer is | Return type | The return statement |
| --- | --- | --- |
| One number | `int` | `return best;` |
| Yes or no | `boolean` | `return true;` |
| Two indices | `int[]` | `return new int[]{i, j};` |
| A fixed set of numbers | `int[]` | `return new int[]{a, b, c};` |
| Numbers, count unknown | `List<Integer>` | `return res;` |
| Groups, paths, triplets | `List<List<Integer>>` | `return res;` |
| Words, count known | `String[]` | `return new String[]{x, y};` |
| Words, count unknown | `List<String>` | `return res;` |
| A grid | `int[][]` or `char[][]` | `return grid;` |
| Text | `String` | `return sb.toString();` |
| Nothing, you edit in place | `void` | no return at all, or bare `return;` to exit early |

## 23.3 Making the thing you return

```java idiom
int[] pair = {i, j};                 // short form: ONLY on a declaration line
return new int[]{i, j};              // anywhere else: return, argument, field
return new int[0];                   // empty array. Not null.
return new ArrayList<>();            // empty list
return new int[]{-1, -1};            // the usual "not found" answer
return "";                           // empty string
return -1;                           // the usual "not found" for an int
```

## 23.4 List to array and back — asked for constantly

```java idiom
// List<Integer> -> int[]   (you collected results, the signature wants an array)
int[] out = new int[res.size()];
for (int i = 0; i < res.size(); i++) out[i] = res.get(i);
return out;

// int[] -> List<Integer>
List<Integer> list = new ArrayList<>();
for (int i = 0; i < a.length; i++) list.add(a[i]);

// List<String> -> String[]
String[] arr = list.toArray(new String[0]);
```

## 23.5 Helper methods

```java idiom
class Solution {
    public List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> res = new ArrayList<>();
        dfs(0, nums, new ArrayList<>(), res);      // hand the collector down
        return res;
    }

    private void dfs(int i, int[] nums, List<Integer> path, List<List<Integer>> res) {
        res.add(new ArrayList<>(path));            // a COPY, never path itself
        for (int k = i; k < nums.length; k++) {
            path.add(nums[k]);
            dfs(k + 1, nums, path, res);
            path.remove(path.size() - 1);          // undo
        }
    }
}
```

> [!NOTE]
> **Two shapes of helper**
>
> A `void` helper collects into a list you passed in. A helper with a return type hands one value back up: `private int depth(TreeNode node)`. Pick one and stay with it inside a problem.
>
> Anything the helper needs is either a parameter or a field. If the parameter list gets long, make the fixed things fields instead.

```java idiom
class Solution {
    private int count;                  // a field: every method in the class sees it
    private char[][] grid;              // set it once, stop passing it around

    public int solve(char[][] g) {
        count = 0;                      // RESET. The judge may reuse the object between tests.
        grid = g;
        ...
        return count;
    }
}
```

## 23.6 The compile errors this causes, and the fix

| Message | What it means | Fix |
| --- | --- | --- |
| missing return statement | Some path out of the method returns nothing | Put a `return` after the loop, not only inside the `if` |
| incompatible types: int cannot be converted to int\[\] | You returned a number where an array is promised | `return new int[]{x};` |
| non-static method cannot be referenced from a static context | `main` is `static`, your helper is not | Make the helper `static`, or call it on `new Solution()` |
| cannot find symbol | Typo, or the variable was declared inside a narrower `{ }` | Declare it before the loop that needs it |
| array required, but List found | `res[i]` on a list | `res.get(i)` |
