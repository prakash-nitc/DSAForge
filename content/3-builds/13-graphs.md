---
id: s13
numeral: §13
title: Graphs — the eight templates
card: 14
---

Twenty problems, none started, and the highest expected OA impact of anything on your board. Flipkart, Oracle and VISA all ask graph questions in the medium band, and they ask from a small, extremely predictable set of shapes.

> [!NOTE]
> **Templates before problems — this is not optional**
>
> The universal mistake with graphs is grinding problems while the templates are shaky, which makes every problem feel like a fresh topic. Spend the first ninety minutes writing BFS, DFS, Kahn, DSU and Dijkstra until each is blank-pageable cold. Then the twenty problems take six days instead of three weeks.

## 13.0 Representation — always build this first

```java
// Adjacency list (the default for everything)
List<List<Integer>> g = new ArrayList<>();
for (int i = 0; i < n; i++) g.add(new ArrayList<>());
for (int[] e : edges) {
    g.get(e[0]).add(e[1]);
    g.get(e[1]).add(e[0]);          // omit this line for a DIRECTED graph
}

// Weighted: store {to, weight}
List<List<int[]>> wg = new ArrayList<>();
for (int[] e : edges) wg.get(e[0]).add(new int[]{ e[1], e[2] });

// GRIDS ARE GRAPHS. Neighbours are directions, not an adjacency list.
static final int[][] DIRS = {{1,0},{-1,0},{0,1},{0,-1}};   // add diagonals if 8-connected
for (int[] d : DIRS) {
    int nr = r + d[0], nc = c + d[1];
    if (nr < 0 || nr >= m || nc < 0 || nc >= n) continue;
    ...
}
```

*Stop hand-writing four if-blocks for grid neighbours. The DIRS array costs one line and eliminates an entire bug class.*

## 13.1 Template G1 — BFS (shortest path, unweighted)

```java
Queue<Integer> q = new ArrayDeque<>();
boolean[] vis = new boolean[n];
int[] dist = new int[n]; Arrays.fill(dist, -1);
q.add(src); vis[src] = true; dist[src] = 0;
while (!q.isEmpty()) {
    int u = q.poll();
    for (int v : g.get(u))
        if (!vis[v]) {                     // MARK ON ENQUEUE, not on dequeue
            vis[v] = true;
            dist[v] = dist[u] + 1;
            q.add(v);
        }
}

// LEVEL-BY-LEVEL variant (when you need the layer number explicitly)
int level = 0;
while (!q.isEmpty()) {
    int sz = q.size();                     // same freeze as tree level-order
    for (int i = 0; i < sz; i++) { ... }
    level++;
}

// MULTI-SOURCE BFS: seed the queue with ALL sources at distance 0.
// This is Rotting Oranges, and it is why that problem is easy once you see it.
```

- **Mark visited on ENQUEUE.** Marking on dequeue lets the same node enter the queue many times. On a large grid that is a TLE, and it is the single most common graph bug.

## 13.2 Template G2 — DFS (connectivity, components, flood fill)

```java
void dfs(int u) {
    vis[u] = true;
    for (int v : g.get(u)) if (!vis[v]) dfs(v);
}

// Grid flood fill (Number of Islands)
void fill(char[][] grid, int r, int c) {
    if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != '1') return;
    grid[r][c] = '0';                       // mark in place -> no visited array needed
    for (int[] d : DIRS) fill(grid, r + d[0], c + d[1]);
}

// Component count
int components = 0;
for (int i = 0; i < n; i++) if (!vis[i]) { dfs(i); components++; }

// ITERATIVE DFS when depth is a risk
Deque<Integer> st = new ArrayDeque<>();
st.push(src);
while (!st.isEmpty()) {
    int u = st.pop();
    if (vis[u]) continue;
    vis[u] = true;
    for (int v : g.get(u)) if (!vis[v]) st.push(v);
}
```

## 13.3 Template G3 — Topological sort (Kahn's algorithm)

```java
int[] indeg = new int[n];
for (int u = 0; u < n; u++) for (int v : g.get(u)) indeg[v]++;

Queue<Integer> q = new ArrayDeque<>();
for (int i = 0; i < n; i++) if (indeg[i] == 0) q.add(i);

List<Integer> order = new ArrayList<>();
while (!q.isEmpty()) {
    int u = q.poll();
    order.add(u);
    for (int v : g.get(u)) if (--indeg[v] == 0) q.add(v);
}

boolean hasCycle = order.size() != n;      // Kahn doubles as a directed cycle test
```

- **Two problems, one algorithm.** Course Schedule asks "can it be finished" (hasCycle). Course Schedule II asks "in what order" (order). Same twenty lines.
- **The DFS alternative:** post-order DFS pushing to a stack gives the reverse topological order. Know both; Kahn is easier to get right under pressure.

## 13.4 Template G4 — Cycle detection (they are different algorithms)

```java
// UNDIRECTED -- DFS carrying the parent
boolean dfs(int u, int parent) {
    vis[u] = true;
    for (int v : g.get(u)) {
        if (!vis[v]) { if (dfs(v, u)) return true; }
        else if (v != parent) return true;      // visited and not my parent -> cycle
    }
    return false;
}

// DIRECTED -- three colours
// 0 = unvisited, 1 = in the current recursion stack, 2 = fully processed
boolean dfs(int u) {
    colour[u] = 1;
    for (int v : g.get(u)) {
        if (colour[v] == 1) return true;        // back edge -> cycle
        if (colour[v] == 0 && dfs(v)) return true;
    }
    colour[u] = 2;
    return false;
}
```

**Blending these is a classic error. Undirected: parent tracking (or DSU). Directed: three colours (or Kahn's count). A single boolean visited array is not enough for the directed case.**

## 13.5 Template G5 — Union-Find (Disjoint Set Union)

```java
int[] par, sz;
void init(int n) { par = new int[n]; sz = new int[n];
    for (int i = 0; i < n; i++) { par[i] = i; sz[i] = 1; } }

int find(int x) { return par[x] == x ? x : (par[x] = find(par[x])); }   // path compression

boolean union(int a, int b) {
    a = find(a); b = find(b);
    if (a == b) return false;                 // already connected -> this edge closes a cycle
    if (sz[a] < sz[b]) { int t = a; a = b; b = t; }   // union by size
    par[b] = a; sz[a] += sz[b];
    return true;
}
```

- **The return value is the point.** union() returning false means the two endpoints were already connected — which is exactly Redundant Connection, and exactly the cycle test inside Kruskal's MST.
- **Component count for free:** start at n, decrement every time union() returns true. That is Number of Provinces in three lines.
- **Accounts Merge pattern:** map each string to an integer id, union on shared items, then group by find(id). This id-mapping trick appears constantly.

## 13.6 Template G6 — Dijkstra (weighted, non-negative)

```java
PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[1], y[1]));
int[] dist = new int[n]; Arrays.fill(dist, Integer.MAX_VALUE);
dist[src] = 0; pq.add(new int[]{ src, 0 });

while (!pq.isEmpty()) {
    int[] cur = pq.poll();
    int u = cur[0], d = cur[1];
    if (d > dist[u]) continue;                   // stale entry -- lazy deletion
    for (int[] e : wg.get(u)) {                  // e = {to, weight}
        int nd = d + e[1];
        if (nd < dist[e[0]]) { dist[e[0]] = nd; pq.add(new int[]{ e[0], nd }); }
    }
}
```

- **The stale-entry skip is mandatory.** Java's PriorityQueue has no decrease-key, so you push duplicates and discard the outdated ones on poll. Without that line you do exponentially redundant work.
- **Path With Minimum Effort is Dijkstra with a different relaxation:** instead of nd = d + w you use nd = max(d, w). Same skeleton, different combining operator. Recognising that is worth more than memorising both.

## 13.7 Template G7 — Bellman-Ford and the K-stops trap

```java
// Bellman-Ford: handles negative weights; detects negative cycles
int[] dist = new int[n]; Arrays.fill(dist, INF); dist[src] = 0;
for (int i = 0; i < n - 1; i++)
    for (int[] e : edges)
        if (dist[e[0]] != INF && dist[e[0]] + e[2] < dist[e[1]])
            dist[e[1]] = dist[e[0]] + e[2];
// an n-th round that still relaxes something => a negative cycle exists

// CHEAPEST FLIGHTS WITHIN K STOPS is Bellman-Ford with k+1 rounds,
// relaxing from a SNAPSHOT of the previous round:
for (int i = 0; i <= k; i++) {
    int[] tmp = dist.clone();                 // the clone is the whole trick
    for (int[] e : flights)
        if (dist[e[0]] != INF) tmp[e[1]] = Math.min(tmp[e[1]], dist[e[0]] + e[2]);
    dist = tmp;
}
```

**Cheapest Flights is not plain Dijkstra. The stop limit breaks the greedy invariant — a cheaper path may use too many stops. Expect to get this wrong once; log it and move on.**

## 13.8 Template G8 — MST and bipartite

```java
// KRUSKAL -- sort edges, union greedily (needs G5)
Arrays.sort(edges, (x, y) -> Integer.compare(x[2], y[2]));
int cost = 0, used = 0;
for (int[] e : edges)
    if (union(e[0], e[1])) { cost += e[2]; if (++used == n - 1) break; }

// PRIM -- grow from one node with a min-heap
// push (node, weight); poll the cheapest unvisited; add its edges

// BIPARTITE -- 2-colour with BFS
int[] colour = new int[n]; Arrays.fill(colour, -1);
for (int s = 0; s < n; s++) {
    if (colour[s] != -1) continue;
    colour[s] = 0; Queue<Integer> q = new ArrayDeque<>(); q.add(s);
    while (!q.isEmpty()) {
        int u = q.poll();
        for (int v : g.get(u)) {
            if (colour[v] == -1) { colour[v] = 1 - colour[u]; q.add(v); }
            else if (colour[v] == colour[u]) return false;
        }
    }
}
```

## 13.9 Your 20 graph problems, mapped to templates

| Template | Problems | Day |
| --- | --- | --- |
| G1 / G2 — BFS & DFS on grids | Number of Islands · Rotting Oranges · Surrounded Regions · Graph BFS · Graph DFS · Shortest Path in Non-Weighted Graph | 1 |
| G3 / G4 — Topological & cycles | Topological Sort · Cycle Detection in Directed Graph · Cycle Detection in Undirected Graph | 2 |
| G5 — Union-Find | Number of Provinces · Construct Adjacency List from Edges | 3 |
| G6 — Dijkstra | Dijkstra's Algorithm · Network Delay Time · Path With Minimum Effort | 4 |
| G7 — Bellman-Ford | Bellman-Ford Algorithm · Cheapest Flights Within K Stops | 4 |
| G8 — MST & bipartite | Prim's MST · Bipartite Graph / Graph Colouring | 5 (or defer) |
| Composite / harder | Word Ladder (BFS on implicit graph) · Swim in Rising Water (Dijkstra or binary search + DFS) | 5 |

## 13.10 The six-day build

| Day | Focus | What you do | Blank-page target |
| --- | --- | --- | --- |
| 0 | Templates only — 90 min | Write G1–G6 from scratch, three times each. No problems today. | All six, cold |
| 1 | Grid traversal | Number of Islands → Rotting Oranges (multi-source) → Surrounded Regions (border trick) → Graph BFS → Graph DFS | BFS + DFS |
| 2 | Ordering & cycles | Topological Sort → Course Schedule → Course Schedule II → Cycle Detection (directed) → Cycle Detection (undirected) | Kahn + three-colour |
| 3 | Union-Find | Number of Provinces → Construct Adjacency List → Redundant Connection → Accounts Merge | DSU with path compression |
| 4 | Weighted shortest path | Dijkstra → Network Delay Time → Path With Minimum Effort → Cheapest Flights Within K Stops | Dijkstra + Bellman-Ford |
| 5 | Breadth & repair | Bipartite → Shortest Path in Non-Weighted → Word Ladder + cold re-solve of four from Days 1–3 | All templates again, cold |
| 6+ | Leftovers | Prim's MST · Swim in Rising Water · Bellman-Ford as a standalone | Optional — October is fine |

## 13.11 The five things that will trip you

- **Visited on enqueue, not dequeue.** The number-one graph bug. Duplicate queue entries, then TLE.
- **Directed and undirected cycle detection are different algorithms.** Parent-tracking or DSU for undirected; three colours or Kahn for directed.
- **Dijkstra without the stale-entry skip.** No decrease-key in Java's PriorityQueue means you must discard outdated pops.
- **Cheapest Flights with K stops is not Dijkstra.** The stop limit breaks the greedy invariant. Bellman-Ford with a cloned snapshot per round.
- **find() without path compression.** It works and it TLEs. One character of syntax — the assignment inside the return.

## 13.12 Complexity reference

| Algorithm | Time | Space | When |
| --- | --- | --- | --- |
| BFS / DFS | O(V + E) | O(V) | Unweighted reachability, components, shortest hops |
| Topological sort (Kahn) | O(V + E) | O(V) | Ordering with prerequisites; directed cycle test |
| Union-Find (with both optimisations) | ≈O(α(n)) ≈ O(1) amortised | O(V) | Static connectivity, Kruskal, cycle edges |
| Dijkstra (binary heap) | O((V + E) log V) | O(V) | Weighted, non-negative |
| Bellman-Ford | O(V · E) | O(V) | Negative weights, or a hop limit |
| Floyd–Warshall | O(V³) | O(V²) | All-pairs, V ≤ ~400 |
| Kruskal / Prim | O(E log E) / O(E log V) | O(V) | Minimum spanning tree |

## 13.13 Interview follow-ups

- "Why doesn't Dijkstra work with negative weights?" — the greedy invariant assumes a finalised node can never be improved; a negative edge breaks that.
- "BFS or DFS here, and why?" — shortest path in hops → BFS. Existence, components, or backtracking structure → DFS. Say the reason, not just the choice.
- "What is α(n) in Union-Find?" — the inverse Ackermann function; below 5 for any input that fits in the universe. Effectively constant.
- "How would you detect a cycle in a very large graph that doesn't fit in memory?" — the cue to discuss external algorithms and streaming; they want the thought process, not an implementation.
- "0-1 BFS?" — a deque: push weight-0 edges to the front and weight-1 edges to the back. O(V+E) instead of Dijkstra's log factor. Worth knowing the name.

## 13.14 Not on your sheet but frequently asked

- **Course Schedule I and II —** the single most-asked graph question band at your targets. Do them on Day 2.
- **Clone Graph —** DFS or BFS with a HashMap from old node to new. Tests reference handling more than graph theory.
- **Redundant Connection and Accounts Merge —** the two canonical DSU applications. Do them on Day 3.
- **Pacific Atlantic Water Flow —** reverse-direction multi-source DFS from both borders. A good Day-5 stretch.
