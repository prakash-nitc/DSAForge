---
id: s19
numeral: §19
title: The idiom sheet
card: 19/sorting-and-comparators
---

These should come out of your fingers without thought. If any of them makes you pause, that pause costs you seconds in an OA and confidence in a round.

### Maps

```java idiom
map.getOrDefault(k, 0)
map.merge(k, 1, Integer::sum);                          // count
map.computeIfAbsent(k, x -> new ArrayList<>()).add(v);  // group
map.putIfAbsent(k, v);
for (Map.Entry<K,V> e : map.entrySet()) { e.getKey(); e.getValue(); }
map.entrySet().removeIf(e -> e.getValue() == 0);
```

### Sorting and comparators

```java idiom
Arrays.sort(a);                                          // primitives: dual-pivot quicksort
Arrays.sort(iv, (x, y) -> Integer.compare(x[0], y[0]));  // NEVER x[0] - y[0]
Arrays.sort(iv, Comparator.comparingInt(x -> x[0]));
Arrays.sort(iv, Comparator.<int[]>comparingInt(x -> x[0])
                          .thenComparingInt(x -> x[1]));
Collections.sort(list);
list.sort(Comparator.reverseOrder());
Arrays.sort(boxed, Collections.reverseOrder());          // descending needs Integer[], not int[]
```

### Arrays

```java idiom
Arrays.fill(dp, -1);
Arrays.fill(dp2d[i], -1);                                // 2D needs a loop over rows
int[] b = Arrays.copyOfRange(a, i, j);
int[] c = a.clone();                                     // shallow: fine for int[], not int[][]
Arrays.equals(a, b);
Arrays.toString(a);   Arrays.deepToString(grid);         // debugging
Arrays.stream(a).max().getAsInt();
Arrays.stream(a).sum();                                  // returns int -- watch overflow
```

### Strings and characters

```java idiom
s.toCharArray();
s.charAt(i) - 'a';                                       // 0..25
Character.isDigit(ch) / isLetter(ch) / toLowerCase(ch)
String.valueOf(charArray);
new StringBuilder(s).reverse().toString();
sb.append(x); sb.setCharAt(i, ch); sb.deleteCharAt(sb.length()-1);
s.split("/");   s.substring(i, j);   s.indexOf(t);
String.join(",", list);
```

### Deques, heaps, and grids

```java idiom
Deque<Integer> st = new ArrayDeque<>();  st.push(x); st.pop(); st.peek();
Deque<Integer> q  = new ArrayDeque<>();  q.offer(x);  q.poll(); q.peek();
Deque<Integer> dq = new ArrayDeque<>();  dq.offerLast(x); dq.pollFirst(); dq.peekLast();

PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[1], y[1]));
PriorityQueue<Integer> mx = new PriorityQueue<>(Comparator.reverseOrder());

static final int[][] DIRS = {{1,0},{-1,0},{0,1},{0,-1}};
int m = grid.length, n = grid[0].length;
```
