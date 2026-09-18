---
id: app-a
numeral: Appendix A
title: The Complete Template Library
---

> [!NOTE]
> **Print this appendix**
>
> This is what you blank-page from. One template every morning in the daily loop (§7.7), rotating through the list. Nineteen entries, roughly nineteen days per full cycle.

## A1 · Two pointers, converging

```java
Arrays.sort(a);
for (int i = 0; i < n-2; i++) { if (i>0 && a[i]==a[i-1]) continue;
  int l=i+1, r=n-1;
  while (l<r) { int s=a[i]+a[l]+a[r];
    if (s==target) { record(); l++; r--;
      while (l<r && a[l]==a[l-1]) l++; while (l<r && a[r]==a[r+1]) r--; }
    else if (s<target) l++; else r--; } }
```

## A2 · Fast & slow, cycle entry

```java
slow=head; fast=head;
while (fast!=null && fast.next!=null) { slow=slow.next; fast=fast.next.next; if (slow==fast) break; }
if (fast==null||fast.next==null) return null;
slow=head; while (slow!=fast) { slow=slow.next; fast=fast.next; } return slow;
```

## A3 · Sliding window, variable

```java
int l=0, best=0;
for (int r=0; r<n; r++) { add(a[r]);
  while (invalid()) { remove(a[l++]); }        // LONGEST: shrink while invalid
  best = Math.max(best, r-l+1); }              // record AFTER
// SHORTEST: while (valid()) { record(r-l+1); remove(a[l++]); }   record INSIDE
```

## A4 · Monotonic deque (window max)

```java
Deque<Integer> dq = new ArrayDeque<>();
for (int r=0; r<n; r++) {
  while (!dq.isEmpty() && dq.peekFirst() <= r-k) dq.pollFirst();
  while (!dq.isEmpty() && a[dq.peekLast()] <= a[r]) dq.pollLast();
  dq.offerLast(r);
  if (r>=k-1) res[r-k+1] = a[dq.peekFirst()]; }
```

## A5 · Kadane

```java
int cur=a[0], best=a[0];
for (int i=1;i<n;i++){ cur=Math.max(a[i], cur+a[i]); best=Math.max(best,cur); }
// product: carry mx and mn, save mx in a temp before overwriting
// circular: max(kadaneMax, total - kadaneMin), guard all-negative
```

## A6 · Prefix sum + map

```java
Map<Integer,Integer> seen=new HashMap<>(); seen.put(0,1);
int pre=0,count=0;
for (int x:a){ pre+=x; count+=seen.getOrDefault(pre-k,0); seen.merge(pre,1,Integer::sum); }
// LONGEST variant: first.put(0,-1); insert ONLY if absent; key = ((pre%k)+k)%k
```

## A7 · Intervals

```java
Arrays.sort(iv,(x,y)->Integer.compare(x[0],y[0]));      // START for merging
int[] cur=iv[0];
for (int i=1;i<iv.length;i++)
  if (iv[i][0]<=cur[1]) cur[1]=Math.max(cur[1],iv[i][1]);
  else { out.add(cur); cur=iv[i]; }
out.add(cur);
// scheduling greedy: sort by END, take if start >= lastEnd
```

## A8 · Linked list reversal (groups of k)

```java
ListNode dummy=new ListNode(0); dummy.next=head; ListNode prevGroup=dummy;
while (true) { ListNode kth=prevGroup;
  for (int i=0;i<k&&kth!=null;i++) kth=kth.next;
  if (kth==null) break;
  ListNode gn=kth.next, prev=gn, cur=prevGroup.next;
  while (cur!=gn){ ListNode nx=cur.next; cur.next=prev; prev=cur; cur=nx; }
  ListNode tail=prevGroup.next; prevGroup.next=kth; prevGroup=tail; }
return dummy.next;
```

## A9 · Monotonic stack

```java
Deque<Integer> st=new ArrayDeque<>();          // INDICES
for (int i=0;i<n;i++){
  while(!st.isEmpty() && a[st.peek()] < a[i]) ans[st.pop()] = a[i];
  st.push(i); }
// histogram: loop i<=n with sentinel h=0; width = i - (st.isEmpty()?-1:st.peek()) - 1
```

## A10 · Binary search — one invariant

```java
int lo=0, hi=n;                                 // hi EXCLUSIVE
while (lo<hi){ int mid=lo+(hi-lo)/2;
  if (predicate(mid)) hi=mid; else lo=mid+1; }
return lo;                                      // first index/value where predicate is true
```

## A11 · Heap — top K and two heaps

```java
// K largest -> MIN-heap of size k
pq.offer(x); if (pq.size()>k) pq.poll();
// two heaps: lo = max-heap (lower half), hi = min-heap (upper half)
lo.offer(x); hi.offer(lo.poll()); if (hi.size()>lo.size()) lo.offer(hi.poll());
```

## A12 · Backtracking

```java
void bt(int start, List<Integer> path){
  res.add(new ArrayList<>(path));               // subsets: record at every node
  for (int i=start;i<n;i++){
    if (i>start && a[i]==a[i-1]) continue;
    path.add(a[i]); bt(i+1,path); path.remove(path.size()-1); } }
// permutations: used[] + record at leaves; dedup rule is (i>0 && a[i]==a[i-1] && !used[i-1])
```

## A13 · Tree — bottom-up (return vs record)

```java
int dfs(TreeNode n){ if(n==null) return 0;
  int L=dfs(n.left), R=dfs(n.right);
  best = Math.max(best, L+R);        // RECORD: path through n
  return 1 + Math.max(L,R); }        // RETURN: for the parent
```

## A14 · Tree — top-down and BST

```java
void dfs(TreeNode n,int run){ if(n==null) return; run=run*10+n.val;
  if(n.left==null&&n.right==null){ total+=run; return; }   // LEAF not null
  dfs(n.left,run); dfs(n.right,run); }

boolean valid(TreeNode n,long lo,long hi){ if(n==null) return true;
  if(n.val<=lo||n.val>=hi) return false;
  return valid(n.left,lo,n.val)&&valid(n.right,n.val,hi); }
```

## A15 · Tree — level order and construction

```java
while(!q.isEmpty()){ int sz=q.size();          // FREEZE the level
  for(int i=0;i<sz;i++){ TreeNode n=q.poll(); level.add(n.val);
    if(n.left!=null)q.add(n.left); if(n.right!=null)q.add(n.right);} res.add(level);}

TreeNode build(int[] pre,int lo,int hi){ if(lo>hi) return null;
  TreeNode r=new TreeNode(pre[p++]); int mid=idx.get(r.val);
  r.left=build(pre,lo,mid-1); r.right=build(pre,mid+1,hi); return r; }
```

## A16 · Graph — BFS, DFS, Kahn

```java
q.add(src); vis[src]=true;                     // MARK ON ENQUEUE
while(!q.isEmpty()){ int u=q.poll();
  for(int v:g.get(u)) if(!vis[v]){ vis[v]=true; dist[v]=dist[u]+1; q.add(v);} }

for(int u=0;u<n;u++) for(int v:g.get(u)) indeg[v]++;
for(int i=0;i<n;i++) if(indeg[i]==0) q.add(i);
while(!q.isEmpty()){ int u=q.poll(); order.add(u);
  for(int v:g.get(u)) if(--indeg[v]==0) q.add(v); }
boolean cycle = order.size()!=n;
```

## A17 · Graph — Union-Find and Dijkstra

```java
int find(int x){ return par[x]==x ? x : (par[x]=find(par[x])); }
boolean union(int a,int b){ a=find(a); b=find(b); if(a==b) return false;
  if(sz[a]<sz[b]){int t=a;a=b;b=t;} par[b]=a; sz[a]+=sz[b]; return true; }

pq.add(new int[]{src,0}); dist[src]=0;
while(!pq.isEmpty()){ int[] c=pq.poll(); if(c[1]>dist[c[0]]) continue;
  for(int[] e: wg.get(c[0])){ int nd=c[1]+e[1];
    if(nd<dist[e[0]]){ dist[e[0]]=nd; pq.add(new int[]{e[0],nd}); } } }
```

## A18 · DP — the four forms

```java
// 1D:        dp[i] = f(dp[i-1], dp[i-2])
// grid:      dp[i][j] = cost + min(dp[i-1][j], dp[i][j-1])
// 0/1 knap:  for(int x:a) for(int s=T; s>=x; s--) dp[s] |= dp[s-x];   // BACKWARDS
// unbounded: for(int c:coins) for(int s=c; s<=T; s++) dp[s]=min(dp[s],dp[s-c]+1);  // FWD
// LCS:       match ? dp[i-1][j-1]+1 : max(dp[i-1][j], dp[i][j-1])
// LIS O(nlogn): tails[] + lowerBound
```

## A19 · Trie

```java
class TrieNode { TrieNode[] next=new TrieNode[26]; boolean isWord; }
void insert(String w){ TrieNode c=root;
  for(char ch:w.toCharArray()){ int i=ch-'a';
    if(c.next[i]==null) c.next[i]=new TrieNode(); c=c.next[i]; }
  c.isWord=true; }
```
