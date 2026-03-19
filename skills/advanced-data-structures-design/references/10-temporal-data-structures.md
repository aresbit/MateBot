# Temporal Data Structures

Persistence, full persistence, confluent persistence, and retroactivity. Use for versioned state, branching history, and time-travel operation models.

## Included Lectures
- L01.md
- L02.md

---

## L01.md


## Page 1

Prof. Erik Demaine

TAs: Tom Morgan & Justin Zhang

## TOPICS:

- Time travel: remembering/changing the past [THIS WEEK]

- geometry: >1 dimension (maps, DB tables)

- dynamic optimality: is there one best BST?

- memory hierarchy: minimize cache misses

- hashing: most used DS in CS

- integers: beat lg n time/op, or prove impossible

- dynamic graphs: changing computer/social network

- strings: search for phrase in text (DNA, web)

- succinct: reduce space to ≈ bare minimum

## Administration:

- video recording of lectures

- requirements: attending lecture, ≈ weekly, psets, scribing, project

- signup sheet

- listeners welcome

- problem session (starting ~ week 3)

[- scribe for today]
## Page 2

Theme in this class: THE MODEL MATTERS

Pointer machine: model of computation

<div style="text-align: center;"><img src="imgs/img_in_image_box_69_277_1138_657.jpg" alt="Image" width="87%" /></div>


- field = data item or pointer to node

- operations: O(1) time each

  - x = new node

  - x = y.field

  - x.field = y

  - x = y + z etc. (data operations)

[−destroy x (if no pointers to it)]

where x,y,z are fields of root (or root)

⇒ constant working space

e.g. linked list, binary search tree (BST), most object-oriented programs
## Page 3

Temporal data structures:

- persistence [L1]

- retroactivity [L2]

think: time travel

## Persistence:

ersistence:

- keep all versions of DS

- DS operations relative to specified version

- update creates (& returns) new version

(never modify a version) most of Terminator/

"1" -vels: Sarah Conner Chron.

①  $ \underline{\text{partial persistence}} $:

 $ \uparrow $ - update only latest version

 $ \Rightarrow $ versions linearly ordered

 $ \rightarrow $ movie

Déjà Vu

part 1

② full persistence:

- update any version

→ versions form a tree

③ confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- update any version

→ versions form a tree

- confluent persistence:

- full persistence:

- can combine >1 given version into new V.

 $ \Rightarrow $ versions form a DAG TV show Sliders

(4) functional:

- never modify nodes; only create new

- version of DS represented by pointer
## Page 4

Partial_persistence: [Driscoll, Sarnak, Sleator, Tarjan

any pointer-machine DS with -JCSS1989]

≤p=O(1) pointers to any node (in any version)

can be made partially persistent

with O(1) amortized multiplicative overhead

& O(1) space per change

node back mod

- store reverse pointers for nodes in latest version (only)

- allow ≤2p (version, field, value)

- mods. in a node (using that p = 0(1))

- to read node.field at version v.

  check for mods with time ≤ v

- when update changes node.field = x:

  - if node not full: add mod. (now.field.x)

  - else: - create node' = node with mods. applied

  - empty mods.

  - now old

- change back pointers to node → node'

  - found by following pointers

root node

part of

returned

Version

- change back pointers to node→node'

- found by following pointers

- recursively change pointers to node→'

found via back pointers



(— add back pointer from x to node)

— potential  $ \Phi = c \cdot \sum_{i} \# \text{mods. in nodes in latest version} \Rightarrow \text{amortized cost} \leq c + c - 2c p + p \text{recursions}  $

 $ \sum_{i} \text{mod. if recurse} \leq 2c $
## Page 5

will persistence: ditto [Driscoll et al. 1989]

—linearize tree of versions via in-order

traversal, marking begin & end of

subtree

<div style="text-align: center;"><img src="imgs/img_in_image_box_914_150_1208_327.jpg" alt="Image" width="24%" /></div>


- store sequence of b's & e's in order-maintenance DS:

[L8: Dietz & Sleator- STBC 1987]

- insert item before/after specified item (like linked list)

- relative order of 2 items?

in O(1) time/op.

- version v ancestor of w ⇔ b_v < b_w < e_w < e_v

 $ b_{1}b_{2}e_{2}b_{3}e_{3}e_{1} $

⇒ ∅(1) time/op.

⇒ can tell which mods apply to specified version

- create child version of ∅ via ∅ inserts after b∅

- allow ≤ ∅(d+p+1) mods. per node

- when changed node is full:

- split into two nodes, each half full (like B-

by making copy with half mods. applied, half left

- recursively update pointers & back pointers to copy

- potential $\Phi = -c \cdot \sum_{i} \neq$ empty mod. slots (all nodes live)

$\Rightarrow$ charge $\leq d + p + (d + p + 1)$ recursions to $\Phi \searrow c \partial (d + p + 1)$

from rest from mods. $\Rightarrow$ $\mathcal{O}(1)$ amortized

De-amortization: (see L10)

- partial: O(1) worst case [Bradal-NJC 1996]

- full: OPEN: O(1) worst case?
## Page 6

 $ OGOGOGO $

Confluent persistence:

- after u confluent updates, can get size  $ 2^{u} $

- general transformation: [Fiat & Kaplan - J.Alg.2003]

-  $ d(v) = \text{depth of version } v \text{ in version DAG} $

-  $ e(v) = 1 + \lg(\# \text{ paths from root to } v) $

-  $ \text{overhead: } \lg(\# \text{ updates}) + \max_{v} e(v) \text{ time} \& \text{space} $

- still exponentially better than complete copy...

- lower bound:  $ \sum_{i} e(v) $ bits of space [Fiat&Kaplan]

 $ \Rightarrow \Omega(e(v)) $ for update if queries are free

- construction makes  $ \approx e(v) $ queries per update

- OPEN: O(1) or even O(lg n) overhead per op.?

- disjoint transformation: [Collette, Iacono, Langerman - SODA 2012]

  - assume confluent ops. performed only on versions with no shared nodes

  - then (lg n) overhead possible

Idea: each node in subtree of version DAG

  - only some of those versions modify node

  - 3 types of versions:

    - node modified ~easy

    - along path between mods.

    - below a leaf ~hard

  - fractional cascading [L3]

  & link-cut trees [L19]



<div style="text-align: center;"><img src="imgs/img_in_image_box_909_1267_1221_1506.jpg" alt="Image" width="25%" /></div>

## Page 7

Functional: [Okasaki - book 2003]

- simple example: balanced BSTs

- work top-down ⇒ no parent pointers

- duplicate all changed nodes & ancestors

before changing

 $ \Rightarrow O(lg n)/op. $

→ link-cut trees too [Demaine, Langerman, Price]

- e.g.  $ \underline{\text{deques}} $ with concat. in O(1)/op.

double-ended queries [Kaplan, Okasaki, Tarjan- $ \underline{\text{SICOMP}} $]

+ update & search in O(lg n)/op.

[Brodal, Makris, Tsichlas - ESA 2006]

- tries with local navigation & subtree copy/delete

& O(1) fingers maintained to present

[Demaine, Langerman, Price-Algorithmica 2010]

lg △ lg △
## Page 8

Beyond:

- functional: ≥ log separation from pointer machine [Pippinger - TPLS 1997]

- OPEN: bigger separation?

    general transformations?

    & co-fluent

-OPEN: lists with split & concatenate?

-OPEN: arrays with copy & paste?
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L02.md


## Page 1

TODAY: temporal data structures II

- partial retroactivity

- full retroactivity

- nonoblivious retroactivity

think: time travel

Retroactivity: [Demaine, Iacono, Langerman - T. Alg. 2007]

- traditional DS formed by sequence of updates

- allow changes to that sequence (destroying old ver.

- maintain linear timeline

(plastic timeline)

insert(5) insert(7) delete-min

    t=∅ 1 2

Dr. Who, Timecop,

Back to the future

- Insert(t, "op"): retroactively do op() at time t

- Delete(t): retroactively undo op. at time t

- Query(t, "op"): execute query at time t

(relative to current timeline only)

- time specified as index, or via order-maintenance DS

- partial retroactivity: Query only in present (last t)

- full retroactivity: Query at any time "Q" in Star Trek
## Page 2

Easy case:

- commutative updates:  $ x_{1}y \equiv y_{2}x $

 $ \Rightarrow \text{Insert}(t_{1}x) \equiv x \text{ in present} $

+ invertible updates:  $ x_{n}x^{-1} \equiv Q $

 $ \Rightarrow \text{Delete}(t) \equiv x^{-1} \text{ in present} $

 $ \Rightarrow \text{partial retroactivity easy (update in present)} $

-e.g. hashing, or array with A[i] += △

-e.g. search problem: maintain set S of objects subject to query(x, S) for object x

& insert/delete objects

-decomposable search problem: [Bentley&Saxe-J.A&1980]

query(x, AUB) = f(query(x, A), query(x, B))

-e.g. nearest neighbor, successor, point location

-full retroactivity in O(lg n) factor overhead

via segment tree: balanced BST

<div style="text-align: center;"><img src="imgs/img_in_image_box_237_1025_1134_1292.jpg" alt="Image" width="73%" /></div>


union all ancestors of query (time)

time interval maps to O(lg n) subtree intervals

Insert/Delete modify element's existence interval

 $ \Rightarrow $O(lg n) updates to DSs in nodes

Query combines O(lg n) searches via f □


## Page 3

General transformations: [Demaine et al. 2003]

- rollback method: retro. op. r time units in past

with factor-r overhead via logging

('undo persistence') movie Retroactive

- lower bound: $\Omega(r)$ overhead can be necessary

- DS maintains two values $X\&Y_{\sim}$ initially $\emptyset$

- $ops: X = x_{a} \ Y + = \Delta_{n} \ Y = X \cdot Y_{a}$ query: return $Y$

- $O(1)$ time/op. in "straight-line program" model

- $Y + = a_{n}, X = X \cdot Y_{a}, Y + = a_{n-1}, X = X \cdot Y_{a}, \ldots, Y + = a_{0}$

  computes polyn. $a_{n}x^{n} + a_{n-1}x^{n-1} + \ldots + a_{0}$ [Cramer's rule]

- Insert $(t = \emptyset, \text{ "X = x"})$ changes $x$ value

- evaluating degree-n polynomial requires $\Omega(n)$ worst-case arithmetic ops. in any field, independent of $a_{i}$ preprocessing,

  in "history-independent algebraic decision tree"

  $\Rightarrow$ integer RAM $\Rightarrow$ generalized real RAM

  [Frandsena, Hansenb., Miltersen – I&C 2001]

- cell-probe lower bound: Ω(√r/lg r)

- DS maintains n words: arithmetic updates +&

- compute FFT using O(n lg n) ops.

- changing Wi requires Ω(√n) cell probes

[Frandsena et al. 2001]

-OPEN:  $ \Omega(r/\text{poly}g r) $ cell-probe lower bound?
## Page 4

Priority queues: [Demaine, Iacono, Langerman 2003]

insert & delete-min, partially retroactive in O(lg u)/op.

- assume keys inserted only once

- L view: insert = rightward ray

delete-min = upward ray

<div style="text-align: center;"><img src="imgs/img_in_image_box_115_357_1181_950.jpg" alt="Image" width="87%" /></div>


>also Delete("delete-min")

- Insert(t_{n} "insert(k)") inserts into Qnow max {k_{n} k') k' deleted at time ≥ t} hard to maintain

- bridge at time t if  $ Q_{t} \subseteq Q_{now} $

- if t' is the bridge preceding time t then  $ \max\{k', | k' deleted \ at \ time \geq t\} $

    =  $ \max\{k', Q_{now} | k' inserted \ at \ time \geq t'\} $
## Page 5

- store Qnow as balanced BST; one change/update

- store balanced BST on leaves = insertions, ordered by time, augmented with

    Node x: max{k'‡ Qnow | k' inserted in x's subtrees}

- store balanced BST on leaves = updates, ordered by time, augmented with

    O for insert(k) with k∈Qnow

    +1 for insert(k) with k‡Qnow

    -1 for delete-min

& subtree sums

⇒ bridge = prefix summing to ∅

⇒ can find preceding bridge, change to Qnow in O(lg n) time

Other structures:

- queue: O(1) partial, O(lg m) full

- degree: O(lg n) full

- union-find (incremental connectivity): O(lg m) full

- priority queue: O(√m lg m) full

  (via general partial → full transform, ×O(√m))

- successor: O(lg m) partial via search

  O(lg² m) full via decomposable search

  O(lg m) full [Giora & Kaplan - 2009]

  → uses fractional cascading [L3]

  & van Emde Boas [L11]
## Page 6

Nonoblivious retroactivity: [Acar, Blelloch, Tangwongsan - CMUTR]

- in algorithmic use of DS (e.g. priority queue in Dijkstra)

updates performed depend on results of queries

→put queries on timeline too

- retroactive update may change result of future queries

- new retro. DS query: time of earliest error

- assume that algorithm corrects errors by further retroactive updates (e.g. Delete & re-Insert query)

in increasing time order always ≤ errors

- idea: just rerunning what's changed of algorithm

Priority_queue: insert, delete, & min in O(lg m) time/op.

keys↑ insert 9 delete

<div style="text-align: center;"><img src="imgs/img_in_image_box_281_906_1172_1299.jpg" alt="Image" width="72%" /></div>


—invariant: all crossings involve horiz. segments

with left endpoint left of all errors

—maintain lowest leftmost crossing

= leftmost lowest crossing
## Page 7

-assume keys inserted only once

-maintain earliest floating error on each key row

-maintain priority queue on all errors by time

⇒always know earliest error

-Insert(x, "min"): upward ray shot

= fully retroactive successor(-∞) ∈ 0(lgm)

= fully retroactive insert, delete, min

(decomposable search problem ~but then lg m)

- Insert(x, "insert(y)") / Delete(x, "delete(y)"): rightward ray shot to find earliest crossing (if lower than existing lower left crossing) = fully retroactive successor(x)  $ \leftarrow O(g_m) $ ...when all inserts are at time  $ -\infty $

- Insert(x, "delete(y)") / Delete(x, "insert(y)"):

  - if was lowest crossover, find next by upward ray shot from leftmost crossover query

  - rightward ray shot to find earliest floater

-Delete (x, "min"):

  -if floating; rightward ray shot to next in row

  -if leftmost crossover; find next by upward ray

  -shot for next min query (successor among queries)
## Page 8

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
