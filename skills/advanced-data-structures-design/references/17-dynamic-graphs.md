# Dynamic Graphs

Link-cut trees, Euler-tour trees, dynamic connectivity, and lower bounds for dynamic graph maintenance.

## Included Lectures
- L19.md
- L20.md
- L21.md

---

## L19.md


## Page 1

TODAY: Dynamic graphs I (of 3)

- link-cut trees

- preferred paths (again) [LG]

- heavy-light decomposition

Link-cut trees: [Sleator & Tarjan - 1983; Tarjan - book]

    maintain forest of rooted (unordered) trees

    subject to O(lg n)-time operations:

    - make tree: return new vertex in new tree

    - link(v_w): make v new child of w

        → adding edge (v_w)

    - cut(v): delete edge (v_parent(v))

    - find root(v): return root of tree containing v

    - path aggregate(v): compute sum/min/max/etc.

        of node/edge weights on v-to-root path

<div style="text-align: center;"><img src="imgs/img_in_image_box_968_684_1171_820.jpg" alt="Image" width="16%" /></div>


Idea: represent unbalanced trees using balanced trees
## Page 2

Preferred path decomposition: (like Tango trees [16])

- preferred child of node v: differs

= { none if last access in v's subtree was v's  

  w if last access was in child w's subtree  

- preferred path = chain of preferred edges  

→ partition represented tree into paths

Auxiliary trees: (also like Tango trees [16])

represent each preferred path by a

splay tree keyed on depth

- root of aux. tree stores path parent:

  path's top node's parent in represented tree

  (can't easily store path children ~can be many)

- auxiliary trees + path parent pointers

  = tree of auxiliary trees
## Page 3

access(v): make root-to-v path preferred

& make v the root of its aux.tree

⇒ v is the root of tree of aux.trees

→ w. pathparent

→ v has no right child

(deepest node on preferred path

because v has no preferred child)
## Page 4

findroot(v):

- access(v)

- v = v.left until v.left = none

- splay v → so fast next time

- return v

path aggregate(v): (for vertex weights)

- access(v)

- return v.subtree sum

augmentation within each aux.tree

cut(v):

- access(v)

- v.left.parent = none

- v.left = none

link(v.w):

- access(v)

- access(w)

- v.left = w

- w.parent = v

- v becomes deepest node in w's preferred path







<div style="text-align: center;"><img src="imgs/img_in_image_box_941_110_1100_350.jpg" alt="Image" width="12%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_976_382_1112_523.jpg" alt="Image" width="11%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_784_657_1210_823.jpg" alt="Image" width="34%" /></div>


[OR w.right = v ~ similar analysis]
## Page 5

O(lg n) amortized bound:

- link & cut & path-aggregate cost O(1+access)

- findroot costs access + find/splay min

- access costs splay. #preferred child changes

- lemma: splay analysis works in this setting (or use balanced BSTs)

⇒ O(lg n) amortized/splay

⇒ m operations cost

O(lg n) · (m + total #preferred child changes)

claim: O(m lg n)

- for this, need a tool:

Heavy-light decomposition: (in represented free)

- size(v) = # nodes in v's subtree

- call edge (v. parent(v)):

  - heavy if size(v) > 1/2 size(parent(v))

  - light otherwise

 $ \Rightarrow $  $ \leq $ 1 heavy child of a node

 $ \Rightarrow $ heavy edges form heavy_paths

  which partition the nodes

- light depth(v) = # light edges on root-to-v path

   $ \leq $ lg n (size halves each time)

→ represented edge can be (preferred) & (heavy) not light
## Page 6

 $ \underline{\text{O(mg n) preferred child changes}} $:

- #changes ≤ # light preferred edge creations

+ #heavy preferred edge destructions

+ n-1

#edges ~ in case created & not destroyed

or destroyed & not created

& light

- access(v):

- creates preferred edges along root-to-v path

- ≤lg n of them can be light

- each heavy preferred edge destroyed

→ light preferred edge created

... except former preferred child of v31

⇒ ≤lg n+1

⇒ O(lg n) total

- link(v.w): "heavens" nodes on root-to-w path

⇒ some of these edges might become heavy

& some edges off path might become light

(⇒ create light edges & destroy heavy edges)

- but former preferred & latter not, by access

⇒ φ

- cut(v): lightens nodes on root-to-v path

- ≤ lg n of path edges can be(come) light

- also destroy edge (v. parent(v)), possibly heavy

⇒ O(lg n)
## Page 7

O(lg n) amortized bound:

- W(v) = # nodes in v's subtree in tree of aux.trees

  =  $ \sum_{w \in aux, v \in V} (1 + size(aux, trees hanging off w)) $

- potential  $ \Phi = \sum_{i} \lg W(v) \sim \text{splay potential} $

- access lemmai amortized cost of splay(v)

   $ \leq 3(\lg W(\text{root of } v's \text{ aux. tree}) - \lg W(v)) + 1 $

  - splay(v) affects W's only within v's aux.tree

   $ \Rightarrow $ standard splay analysis applies:

  - amortized cost of one splay step

   $ \leq 3(\lg W^{\text{after}}(v) - \lg W^{\text{before}}(v)) $

  (some checking & concavity of  $ \lg $)

   $ \Rightarrow $ telescopes, +1 for final rotation

- amortized cost of access(v)

  = O( $ \lg n $) + O(\# preferred child changes)

   $ \Rightarrow $ O( $ \lg n $) amortized

  - changing preferred children doesn't affect W

  (tree of aux. trees remains the same)

- W(v)  $ \leq $ W( $ \text{root of } v's \text{ aux. tree} $)  $ \leq $ W(w)

- splay(v) costs  $ \leq 3(\lg W(w) - \lg W(v)) + 1 $

- sum telescopes

   $ \Rightarrow $ W(v) in next splay

   $ \Rightarrow $  $ \leq 3(\lg W(\text{root}) - \lg W(v)) + O(\# preferred child changes) $

- cut(v) only decreases W's  $ \Rightarrow $  $ \Phi $ only decreases

- cut(v) only decreases W's  $ \Rightarrow $  $ \Phi $ only decreases

- link(v,w) increases only W(v). by  $ \leq n $

 $ \Rightarrow $  $ \leq $lg n increase in  $ \Phi $
## Page 8

Worst-case O(lg n): [Sleator & Tarjan]

- store heavy paths in aux. trees

- aux. tree = globally biased search tree

[Bent. Sleator. Tarjan - S1COMP1985]

- similar to weight-balanced trees in L16

but dynamic with careful split/concat.
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
/terms.

---

## L20.md


## Page 1

TODAY: Dynamic graphs II

- fully vs. partially dynamic

- Euler-tour trees

- O(1) incremental connectivity in trees

- O(lg²n) fully dynamic connectivity

- survey

Dynamic connectivity:

- maintain undirected graph subject to

- insert/delete edges or vertices (with no edges)

- connectivity (v.w): is there a v→w path?

or (): is the graph connected? (same)

Dynamic graph problems: characterized by updates

- fully dynamic: insert & delete & default

- partially dynamic:

  - incremental: just insert

  - incremental: just delete
## Page 2

Dynamic connectivity results:

- trees: O(lg n) → link-cut [Lig] & Euler tour trees

  - incremental: O(1) amortized → TODAY

- plane graphs: O(lg n)

  - embedded planar [Eppstein, Gall, Italiano, Spencer - 1996]

- general graphs, amortized:

  - OPEN: O(lg n) update & query

  - O(lg² n) update, O(lg n) query → TODAY

  - Holm, de Lichtenberg, Thorup - J.ACM 2001

- O(lg n (lg lg n³)) update, O(lg n) query

  - Thorup - STOC 2000

  - incremental: O(α(m,n)) via union-find [Tarjan - 1975]

  - incremental: O(mlg n + n polylg n + #queries) total

  - [Thorup - J.ACM 1999]

- worst case: (general graphs)

  - OPEN: polylg update & query

  - O(ln) update, O(1) query

  - Eppstein, Gall, Italiano, Nissenweig - JACM 1997

  - incremental: ∅(x) updates ⇒ ∅(lg n) queries

  - [Alstrup, Ben-Amran, Raube - STOC 1999]

- lower bounds: Ω(lg n) update or query even

  - O(x lg n) update ⇒ Ω(lg n) query for paths!

  - O(x lg n) query ⇒ Ω(lg n) update

  - [LAI] & [Patrascu & Demoine - STOC 2004/S1COMP2006]

  - points on trade-off curve

  - OPEN: O(lg n) update & polylg n query?
## Page 3

Euler-tour trees: [Henzinger & King - STOC 1995]

- Simpler dynamic trees than link-cut

- aggregates over subtrees, vs. paths

- Euler tour [L15] around tree

- visits each edge twice

- store node visits by Euler tour in balanced BST

- each node stores pointers to first & last visits

<div style="text-align: center;"><img src="imgs/img_in_image_box_844_123_1198_345.jpg" alt="Image" width="28%" /></div>


- find root(v): start at first visit to v in BST walk up to root of BST

- walk left to min of BST

- first visit of root node

- cut(v): split BST at v's first & last visits  

  concatenate "before" & "after" trees  

  first v last v

- link(v.w): split w's BST before w's last visit concatenate "before last w", new single w, v's BST, and "after last w"

- connectivity(v.w): findroot(v) ≡ findroot(w)

- subtree aggregate(v): (min/max/sum/etc.)

range query in BST between first & last visit

- O(lg n) time/op.
## Page 4

## rooted

Decremental connectivity in a tree: [Alstrup, Secher, Spork-IPL 1997]

O(1) amortized, assuming all n-1 edges deleted

① O(1) amortized, assuming all n-1 edges deleted

(simpler way: maintain explicit node-component id. & related the smaller side)

② leaf trimming: cut below maximally deep nodes with > lgn descendants

⇒ top tree has O(log n) leaves/branching nodes

- use ① on compressed top tree

- connectivity(v,w):

<div style="text-align: center;"><img src="imgs/img_in_image_box_454_631_884_884.jpg" alt="Image" width="35%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_800_612_1211_897.jpg" alt="Image" width="33%" /></div>


≤2"path" queries

1 bottom query

③ bottom tree in O(1): (worst case, fully dynamic)

- store bit vector of which edges don't exist

- preprocess mask of each node's ancestors (1 word)

- XOR masks for v & w, mask, check whether

④ path in O(1) amortized:

- split path into  $ \frac{n}{gn} $ chunks of length lg n

- store each chunk as bit vector (1 word)

- use ① on  $ \frac{n}{gn} $ chunk summaries (OR)

- query:  $ \frac{\text{chunk}}{\leftarrow\lg n\rightarrow} $  $ \frac{v}{\uparrow} $  $ \frac{w}{\uparrow} $

mask & check whether
## Page 5

O(lg^{2}n) dynamic connectivity: [Holm et al. - J.ACM 2001]

- store spanning forest with Euler-tour trees

- hierarchically divide connected components

→ O(lg n) levels of spanning forests

- Charging mechanism

- level of edge starts at lg n, only decreases →

-  $ G_{i} = \text{subgraph of edges at level} \leq i $

⇒  $ G_{lg n} = G $

- INVARIANT 1: every conn. comp. of  $ G_{i} $ has  $ \leq 2^{i} $ vxs.

-  $ F_{i} = \text{spanning forest of } G_{i} $

- store using Euler-tour tree DS

⇒  $ F_{lg n} $ is desired spanning forest of G

- INVARIANT 2:  $ F_{0} \subseteq F_{1} \subseteq \cdots \subseteq F_{lg n} $ i.e.  $ F_{i} = F_{lg n} \cap G_{i} $

i.e.  $ F_{lg n} $ is a min. spanning forest w.r.t. level

insert(e=(v,w)): O(lg n)

- add e to v & w incidence lists

- e.level = lg n

- if v & w disconnected in Flg n:

  - add e to Flg n (link)

    (reroot to make v root via cyclic shift)

connectivity:  $ O(\frac{\log n}{\log g n}) $

- make Fegn B-trees with branching factor  $ \Theta(\lg n) $

 $ \Rightarrow O(\frac{\log n}{\log g n}) $ findroot \&  $ O(\frac{\log^{2} n}{\log g n}) $ update

depth

depth·branching factor
## Page 6

delete(e=(v.w)):

- remove e from v & w incidence lists

- if e is in Fg n: (v.parent=w or vice versa)

 $ lg^{2}n \rightarrow - $ delete e from Fe.level a …, Fg n (cut)

- look for replacement edge to reconnect vdw

- can't be any edges with level < e.level

⇒ find min. possible level ≥ e.level [Invariant2]

- for $i=e$. level, ..., lg n:

- let $T_V$ & $T_W$ be trees of $F_i$ containing $V\&W$ resp

- relabel so that $|T_V| \leq |T_W|$

- Invariant $1$ (before) $\Rightarrow |T_V| + |T_W| \leq 2^i \Rightarrow |T_V| \leq 2^{i-1}$

$\Rightarrow$ can "afford" to push all of $T_V$ down to level $i-1$

- for each level-i edge $e'=(x_i y)$ with $x \in T_V$:

Euler-tour tree augmentation:

→- subtree sizes to test (Tvl vs. Twl in O(1))

→-for each node v in tree of F_{i}:

    does v's subtree contain any nodes

    incident to level-i edges?

⇒ can find next level-i edge incident to x∈TV in O(lgu) time (successor, skipping over empty subtrees)

→time: O(lg²n + #charges·lg n)

- each inserted edge charged ≤ lg n times
## Page 7

k-connectivity: vertex or edge

-disjoint paths between pairs of vertices:

-2-edge: O(lg4n) -2-vertex: O(lg5n) [Holme et al. - JACM]

-OPEN: polylg n for k=O(1)? k=polylg n?

-planar incremental: O(lg2n) 3-edge-conn.

[Giammaresi & Italiano - Algorithmica 1996]

-worst case: [Eppstein et al. - JACM 1997]

-2-edge-conn.: O(√n) -2-vertex-conn.: O(n)

-3-edge-conn.: O(n2/3) -3-vertex-conn.: O(n)

-k=4: O(n·α(n))

-O(1)-edge-conn.: O(n·lg n)

-whole graph ≈ min cut = max flow

-O(polylg n)-edge-conn. ( & min cut up to that size):

O(√n·polylg n) [Thorup - STOC 2001]

-OPEN: polylg n for k=O(1)? k=polylg n?

Minimum spanning forest: (MST on each conn.comp. as dyn.tree)

- O(lg4 n) update [Holm, de Lichtenberg, Thorup-J.ACM 2001]

- worst case: O(ln) update [Eppstein et al.-J.ACM 1997]

- plane graphs: O(lg n) [Eppstein et al.-J.ACM 1992]

- can use to solve bipartiteness: is graph 2-colorable?

Planarity testing: insert e or report planarity violation

- O(n^{2/3}) [Galil, Italiano, Sarnak-J.ACM 1997]

- plane (fix embedding): O(lg^{2} n) [Eppstein et al.-J.ACM 1997]

- incremental: O(α(m,n)) amortized [la Poutre-STOC 1994]
## Page 8

Directed graphs:

Transitive closure: is there a v→w directed path?

- bulk update: insert/delete vertex & incident edges

- O(n²) am. bulk update, O(1) worst-case query

[Demetrescu & Italiano - FOCs 2000: Rodity - SODA 2003]

- same, worst case [Sankowski - FOCs 2004]

- optimal if explicitly storing trans. closure matrix

- OPEN:  $ O(n^{2}) $ worst-case update?

-  $ O(m\sqrt{n}\cdot t) $ am. bulk update,  $ O(\sqrt{n}/t) $ w.c. query for any  $ t=O(\sqrt{n}) $ [Rodity & Zwick - FOCs 2002]

-  $ O(m+n\lg n) $ am. bulk update,  $ O(n) $ w.c. query [Rodity & Zwick - STAR 2004]

-OPEN: full trade-off: update·query = O(mn) or O(n²)

-acyclic: O(n¹·575·t) update, O(n⁰·575/t) query, t = O(ln²)

-decremental: O(n) am. update, O(1) w.c. query

[Demetrescu & Italiano - Focs 2000]

All-pairs shortest paths: weight of shortest v→w path

- O(n²(lg n + lg²(1+m))) am. bulk update, O(1) w.c. query

[thorup-SWAT 2004] improving [Demetrescu & Italiano-Stoc2003]

- OPEN: O(n²) or o(n²) update, even undirected graphs?

- O(n².75) w.c. update, O(1) query [thorup-Stoc2005]

- unweighted: O(m√n-polylg n) am. update.

O(n^{3/4}) w.c. query [Roditty & Zwick-ESA 2024]

- undirected, unweighted & (1+ε)-approx.: [Roditty&Zwick

O(√m·t) am. update, O(√m/t) w.c. query, t=O(√n) -Facs 2004]

- static & (1+ε)-approx.: distance oracles [...]
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
://ocw.mit.edu/terms.

---

## L21.md


## Page 1

TODAY: Dynamic graphs III (of 3)

- dynamic connectivity lower bound:

  - block operations

  - bit-reversal bad access sequence

  - tree over time

  - sum lower bound

  - connectivity lower bound
## Page 2

Dynamic connectivity lower bound:

(Patrascu & Demaine - SCOMP 2006)

inserting/deleting edges & connectivity queries

require Ω(lg n) cell probes/op.

even if connected components are paths

even amortized (but here prove for worst case)

⇒ link-cut & Euler-tour trees are optimal

## Proof:

- consider  $ \sqrt{n} \times \sqrt{n} $ grid with

perfect matching between

columns i & i+1 for each i.

forming permutation  $ \pi_i $

- block operations:

  - update  $ (i_i \pi) $:  $ \pi_i \leftarrow \pi $

  -  $ \pi_i $ edge deletions & insertions

  - verify  $ -\sum(i_i \pi) $:  $ \sum_{j=1}^{i} \pi_j = \pi $?

  - compose

  -  $ \pi_i $ connectivity queries

- claim:  $ \sqrt{n} $ updates +  $ \sqrt{n} $ verify sums

  - require  $ \Omega(\sqrt{n} \cdot \sqrt{n} \cdot \lg n) $ cell probes

  -  $ \Omega(\lg n) $/op.

<div style="text-align: center;"><img src="imgs/img_in_image_box_814_535_1220_798.jpg" alt="Image" width="33%" /></div>

## Page 3

Bad access sequence:

- for i in bit-reversal sequence:

  - verify-sum(i, j=1,  $ \pi_j $)  $ \Rightarrow $ answer=yes

  (but DS must check)

  - update(i,  $ \pi_{random} $)

  uniform random permutation

- build free over time:

<div style="text-align: center;"><img src="imgs/img_in_image_box_182_485_1189_722.jpg" alt="Image" width="82%" /></div>


-left & right subtrees of each node \underline{interleave}

-Claim: for every node v in tree,

    say with l leaves in its subtree,

    during right subtree of v (time interval)

    must do ∑(l√n) expected cell probes

    reading cells last written during left subtree

- sum lower bound over all nodes:

- read r of write w only counted at  $ lcal(r,w) $

- linearity of expectation

⇒  $ \Omega(n \lg n) $ lower bound total

(each leaf in  $ \odot(\lg n) $ subtrees)
## Page 4

Proof of claim:

root of claim:

- left subtree has l/2 updates with l/2 rand. perms.

- any encoding of these permutations must use

$\Omega(\lfloor\sqrt{n}\rfloor\lg n)$ bits [information/Kolmogorov theory]

- if claim fails, find smaller encoding $\Rightarrow$ contradict.

- setup: know the past (before v's subtree)

- goal: encode (verified) sums in right subtree

$\Rightarrow$ can recover (updated) perms. in left subtree

left right

 $ \pi_{i}=\underbrace{\pi_{i-1}^{-1}\cdots\cdots\cdots\cdots}_{farther\ left\Rightarrow known}\underbrace{\pi_{1}^{-1}}_{right\Rightarrow q}\underbrace{\pi_{j}^{-1}}_{not\ yet\ updated} $

Warmup: query is sum(i) → j = 1 πj (partial sums)

- let R = {cells read during right subtree}

W = {cells written during left subtree}

- encode R ∩ W (address & contents of each cell)

⇒ |R ∩ W| · O(lg n) bits [assume poly. space

⇒ w = ∅ (log n)

-decoding alg. for sums in right subtree:

  -simulate sum queries in right subtree

  -to read cell written in right subtree: easy

  in left subtree: RnW

  in past: known

 $ \Rightarrow |R \cap W| \cdot O(\lg n) = \Omega(\lg \sqrt{n} \lg n) $

 $ \Rightarrow |R \cap W| = \Omega(\lg \sqrt{n}) $
## Page 5

Verify-sum instead of sum:

- permutations  $ \pi $ given to verify-sum

encode the information we want  $ \left(\Rightarrow_{no}\right) $

info.CB

- setup: - know (fixed) past

- don't know updates in left subtree

- don't know queries in right subtree

- but know that queries return YES

-decoding idea:

  -simulate all possible input permutations

  for each query in right subtree

  -know one returns YES, all others no

- \underline{trouble} incorrect query simulation reads colls R'≠R

- if read re R'~R, it must be incorrect

- but can't tell whether reW~R or past~(Rrw)

- can't afford to encode R or W

- idea: encode separator S

  for R∧W & W∧R

- when decoding, to read cell

  written in right subtree: easy

  in R∧W: encoded explicitly

  in S: must be in past ⇒ known

  not in S: must not be in R ⇒ incorrect; ABORT

- only one simulation returns YES; rest NO or ABORT

⇒ recover desired permutation

⇒ lencoding = ∑(∫√n∫g n)



<div style="text-align: center;"><img src="imgs/img_in_image_box_859_979_1173_1104.jpg" alt="Image" width="25%" /></div>

## Page 6

Separators:

- given universe U & number m

- separator family g for size-m sets if

   $  \forall A, B \subseteq U  $ with  $  |A| \cdot |B| \leq m  $ &  $  A \cap B = \varnothing  $;

    $  \exists C \in \mathcal{G}  $ such that  $  A \subseteq C  $ &  $  B \subseteq \mathcal{U} \cap C  $

- claim: 3 separator family g

  with  $  |g| \leq 2^{O(m + lg \lg g U)}  $

- proof sketch:

  - perfect hash family 94 with  $  |94| \leq 2^{O(m + lg \lg g U)}  $

  [Hagerup & Tholey - STACS 2001]

  gives mapping from A & B to  $  O(m)  $-size table

  - store A-or-B bit in each table entry

   $  - 2^{O(m)}  $ such vectors

   $  \Rightarrow 2^{O(m)} \cdot 2^{O(m + lg \lg g U)} = 2^{O(m + lg \lg g U)}  $

<div style="text-align: center;"><img src="imgs/img_in_image_box_918_346_1188_476.jpg" alt="Image" width="22%" /></div>


Encoding:  $ R \cap W $ + separator of  $ R \cap W \& W \cap R $

- size:  $ |R \cap W| \cdot O(\lg n) + O(|R| + |W| + \lg \lg n) $

  =  $ \Omega(\lg \sqrt{n} \lg n) $

 $ \Rightarrow |R \cap W| = \Omega(\lg \sqrt{n}) $  $ \Rightarrow $ claim

or  $ |R| + |W| = \Omega(\lg \sqrt{n} \lg n) $  $ \Rightarrow $  $ \Omega(\lg n) $ for op.
## Page 7

Update-query_trade-off: (possible by same technique)

 $ t_{g} \lg \frac{t_{u}}{t_{g}} = \Omega(\lg u)  $

 $ t_{u} \lg \frac{t_{g}}{t_{u}} = \Omega(\lg n) $

- for  $ t_{u}=\Omega(t_{g}) $, trees can match

(small mods. to link-cut trees)

- for  $ t_{u}=\Omega(l_{g}n(l_{g}l_{g}n)^{3}) $, can match

[Thorup-STOC 2000]
## Page 8

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
