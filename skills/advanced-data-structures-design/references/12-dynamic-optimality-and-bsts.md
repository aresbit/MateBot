# Dynamic Optimality and BSTs

Binary search tree access sequences, geometric execution views, competitive BSTs, and the dynamic optimality program.

## Included Lectures
- L05.md
- L06.md

---

## L05.md


## Page 1

TODAY: Dynamic Optimality I (of 2)

- binary search trees

- analytic bounds

- splay trees

- geometric view

- greedy algorithm
## Page 2

Q: is there one best binary search tree (BST)?

BST: comparison data structure supporting search (& predecessor/successor, insert/delete)

Also a model of computation (for DSS)

- data must be stored in a BST

- unit-cost operations:

  - walk left, right, or up (parent)

  - rotate this node & its parent

<div style="text-align: center;"><img src="imgs/img_in_image_box_362_701_1132_911.jpg" alt="Image" width="62%" /></div>


(- create/destroy leaf)

⇒ search cost = length of root-to-node path

DSs in this model:

- vanilla BST (no rotations)

- AVL trees

- red-black trees (B-trees)

- BB[α] trees

- splay trees

- Tango trees

- Greedy

focus here
## Page 3

Is O(lg n)/search optimal?

- depends on sequence of searches

- say we're storing keys {1,2,……,n}

& search for x1,x2,……,xm

 $ \frac{\text{Sequential access}}{\text{In } 2n \cdots n} \Rightarrow \mathcal{O}(1) \text{ amortized/op.} $

[in-order traversal in any BST]

Dynamic finger property:

 $ |x_{i}-x_{i-1}|=k \Rightarrow O(\lg k)/\alpha. $ possible

[think level-linked B-trees ~ but BST]

Entropy bound / static optimality:  $ \Rightarrow $ best possible without rotation

k appears  $ p_{k} $ fraction of the time  $ \Rightarrow O\left(\sum_{k=1}^{n}p_{k} \lg \frac{1}{p_{k}}\right) / \rho $

[store  $ x_{i} $ at height  $ \leq \lg \frac{1}{p_{k}} + 1 $]

Working-set property:

if  $ t_{i} $ distinct keys accessed since last access to  $ x_{i} $ then  $ O(lg t_{i}) $ possible

[intuition: store most recent higher up]

⇒ if all  $ x_{i} \in S $ then  $ O(lg |S|)/op. $ possible

[form BST on  $ S_{n} $ put rest below]

⑦ = hard to do with BST, but possible!
## Page 4

Unified property: [Iacono-SODA 2001]

if  $ t_{ij} $ distinct keys accessed in  $ x_{in} \ldots x_{j} $

then  $ x_{j} $ costs  $ O(\lg \min [|x_{i} - x_{j}| + t_{ij} + \lambda]) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_51_221_213_343.jpg" alt="Image" width="13%" /></div>


- e.g.  $ 1_{\frac{n}{2}}, 2_{\frac{n}{2}}+1, 3_{\frac{n}{2}}+3, \ldots \Rightarrow O(1)/op. $

- implies both working set & dynamic finger

- possible on pointer machine [Iacono: Badiou, Cole, Demaine, Iacono-Algorithmica 2007]

- possible on BST up to additive O(lg(n))

[Bose, Douieb, Dujmovic, Howat-Algorithmica 2012]

- [OPEN]: possible on a BST?

Dynamic optimality / O(1) - competitive: total cost = O(OPT)

min. cost of any BST on this access sequence

- OPEN: possible for any (online) BST?

  for any pointer-machine DS?

- OPEN: is any pointer-machine DS

  = O(OPT offline pointer-machine DS)?

- balanced BST is O(lg n)-competitive

- Tango trees are O(lg ln n)-competitive [LG]
## Page 5

Splay trees: [Sleator & Tarjan - JACM 1985]

- binary search for x

- modify the path:

- zig zig: z

<div style="text-align: center;"><img src="imgs/img_in_image_box_172_241_1194_778.jpg" alt="Image" width="83%" /></div>


- at the end, possible single rotation to put x at root

- key feature: at most half the nodes on the path go down in the tree

Performance: (amortized)

- has working-set property [Sleator & Tarjan]

- has dynamic-finger property [Cole-S1comp2005]

- CONJECTURE: has unified property [Iacono]

- CONJECTURE: dynamically optimal [Sleator & Tarjan]
## Page 6

Geometric view:

[Demaine, Harmon, Iacono, Kane, Pátrascu-SODA 2009]



access sequence

→ point set

 $ \{x_{i,i}\} $

<div style="text-align: center;"><img src="imgs/img_in_image_box_612_207_1161_749.jpg" alt="Image" width="44%" /></div>


time↑

BST execution

→ point set:

which nodes touched

during search(xi)?

Theorem: point set is a valid BST execution

 $ \Leftrightarrow $ Arborally Satisfied Set (ASS)

 $ \Leftrightarrow $ rectangle spanned by two points

in set, not on horizontal/vertical line,

contains another point

- in fact must have another point

on a rectangle

side incident

to either corner:

Corollary: OPT = smallest ASS containing input

OPEN: complexity? O(1)-approximation?
## Page 7

Proof of Theorem:

(⇒) consider rectangle spanned

by  $ (i, x) \rightarrow (j, y) $

- let  $ a_t = lca $ of  $ x \& y $

just before time t

- for all  $ t: x \leq a_t \leq y $

\&  $ a_t $ is an ancestor of  $ x \& y $

\Rightarrow (a_{i,i}) \& (a_{j,j}) \in execution

(need to touch all ancestors

of touched nodes

- want a third point in the rectangle

- if  $ a_i \neq x $ then use  $ (a_{i,i}) $

- if  $ a_j \neq y $ then use  $ (a_{j,j}) $

- else: a changes from  $ x $ to  $ y $

between times i & j

\Rightarrow y rotated before time j

\Rightarrow (y_t) \in execution for some  $ i \leq t < j $

<div style="text-align: center;"><img src="imgs/img_in_image_box_1018_120_1165_314.jpg" alt="Image" width="12%" /></div>

## Page 8

(⇔) define tree at all times to be treap:

BST & heap ordered by next-touch-time

- note: next-touch-time has some ties,

so this is not uniquely defined

- when we reach time i, nodes to touch form a connected subtree at the top (by heap-order property)

- these nodes get new next-touch-time

- re-arrange into local treap (this still may be ambiguous — break ties arbitrarily — but still restricts global choice)

- claim: global treap

<div style="text-align: center;"><img src="imgs/img_in_image_box_348_743_1212_923.jpg" alt="Image" width="70%" /></div>


if y to be touched sooner than x then (x, now) → (y, next-touch(y)) is an unsatisfied rectangle: (according to 2nd definition of ASS)

empty by "if"→y

leftmost such point would be right child of x after search(x). not y
## Page 9

Simple example:

<div style="text-align: center;"><img src="imgs/img_in_image_box_51_207_1203_721.jpg" alt="Image" width="94%" /></div>

## Page 10

Greedy algorithm: [Lucas 1988; Munro 2000]

- consider point set one row at a time

- add the necessary points on that row

- in tree view: re-arrange root-to-x path

  optimally for future searches

CONJECTURE: Greedy = O(OPT) or even: = OPT + O(m)

seems obvious..."just" need to show you needn't stray from the access path

So what?

Theorem: online ASS algorithm

→ online BST (with O(1) slowdown)

Corollary: Greedy is actually an online BST!

- Conjecture  $ \Rightarrow $ dynamically optimal
## Page 11

Proof sketch of theorem:

store touched nodes from access in a

split tree: split(x) moves x to root &

deletes x, leaving 2 split trees

in O(1) amortized time ~if fully split:

- really: all n splits in O(n) time

(& make split tree on n items in O(n))

- 2-3-4 tree with min & max pointers can split

into n' & n" in O(lgmin{n',n}) + O(n) total merges

- use potential $\Phi = \sum$ (|T| - lg |T|)

split tree T

⇒ O(1) amortized search cost for split

- simulate with BST:

  interleaved min/max search

⇒ BST is "treap of split trees".

where heap order is by previous touch

& ties mean in split tree (⇒ optimal order)

- use proof similar to (↔) above

- by ASSₙ when touching node in split tree,

also touch predecessor & successor in

parent split tree ⇒ cheap to reach
## Page 12

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L06.md


## Page 1

TODAY: Dynamic Optimality II (of 2)

- lower bounds:

  - independent rectangles

  - Willber 1 & 2

  - signed greedy

- Tango trees: O(lg lg n)-competitive

Recall:

- point set is a valid BST execution

 $ \Leftrightarrow $ arborally satisfied set:

    rectangle spanned by two points

    not on a horizontal/vertical line

    contains another point

- Greedy algorithm conjectured O(optimal)

- can be simulated online

<div style="text-align: center;"><img src="imgs/img_in_image_box_675_1074_1204_1371.jpg" alt="Image" width="43%" /></div>

## Page 2

Lower bounds: [Demaine, Harmon, Iacono, Kane, Patrascu]

Independent rectangles are unsatisfied &

$\Rightarrow$ in input point set (accesses)

no corner is strictly inside another

<div style="text-align: center;"><img src="imgs/img_in_image_box_148_326_603_531.jpg" alt="Image" width="37%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_657_322_1055_521.jpg" alt="Image" width="32%" /></div>


dependent

independent

Theorem:  $ OPT \geq \text{input} | + \frac{1}{2} \max \# \text{independent rectangles} $

Signed rectangles: ☐ & ☐ types

- ☐-satisfied if all ☐ rectangles have another pt.

- OPT = smallest ☐-satisfied superset of points

Lemma:  $ \text{OPT}_{\square} \geq \text{input} + \max \# \text{independent} \square - \text{rectangles} $

Proof: ① find rectangle in indep. set & vertical line hitting just it

→ segments with endpoints on top & bottom edges of rectangle

② find horizontally adjacent pts. of OPT in rect. crossing line a

③ charge indep. rectangle to those points
## Page 3

Assume input x&y coords, all distinct

①: take the widest rectangle

7<sharing neither a nor b

<div style="text-align: center;"><img src="imgs/img_in_image_box_402_251_905_519.jpg" alt="Image" width="41%" /></div>


impossible (widest)

- sharing-a rects. left of sharing-b's (indep.)

- sharing-neithers fit in between vertical edges

→ room left for vertical line

②: take p=topmost rightmost point in rectangle & left of line (e.g. a)

q=bottommost leftmost point in rectangle & right of line & not below p (e.g. b)

<div style="text-align: center;"><img src="imgs/img_in_image_box_344_1048_1195_1204.jpg" alt="Image" width="69%" /></div>


③: p&q are not in any other common rectangle

⇒ pair won't get charged again

- in any horizontal chain of charges

≤1 in input (by distinct y's)

⇒ added ≥ # indep. rectangles

<div style="text-align: center;"><img src="imgs/img_in_image_box_999_1365_1214_1542.jpg" alt="Image" width="17%" /></div>

## Page 4

Wilber's second lower bound: [Wilber-SICOMP 1989]

(-given input (access) point set

- for each point p:

- look at orthogonally visible points below p

- count # alternations between left/right of p

- sum over all p

<div style="text-align: center;"><img src="imgs/img_in_image_box_777_196_1186_590.jpg" alt="Image" width="33%" /></div>


Proof: independent rectangle V alternation:

 $ \underline{\text{Conjecture:}} $ OPT =  $ \bigcirc $ (Wilber  $ \alpha $)

Key-independent optimality: [Iacono-ISAAC 2002]

- suppose key values are "meaningless"

⇒ might as well permute them uniformly at random

- claim: E[OPT] = working-set bound

⇒ splay trees are key-indep. optimal

- proof sketch: E[Wilber 2(x_i)] = ⊓(lg t_i)

(expected # changes to max. in random permutation)
## Page 5

Wilber's first lower bound: [Wilber-SICMP 1989]

- fix a lower-bound tree P on same keys

(e.g. perfect binary tree)

- for each node y of P:

  count #alternations in  $ x_{1}, x_{2}, \ldots, x_{n} $

  between accesses in left & right subtrees of y

  (ignoring accesses to y or outside y's subtree)

- sum over all y

Proof: independent rectangle Valteruation

Example: bit-reversal seque

000 0

001 4

010 2

011 6

100 1

101 5

110 3

111 7





<div style="text-align: center;"><img src="imgs/img_in_image_box_983_464_1174_633.jpg" alt="Image" width="15%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_733_680_1150_965.jpg" alt="Image" width="34%" /></div>


⇒ # alternations at y = size of y's subtree

⇒ Wilber 1 = ∅(n lg n)

⇒ OPT = ∅(n lg n)

OPEN: Vaccess sequence ∃ free P such that

OPT = ∅(Wilber 1)
## Page 6

Tango trees: [Demaine, Harmon, Jacono, Pátrascu - SICOMP2007]

- O(lg lg n) - competitive online BST

- P = perfect BST on n keys

- define preferred child of node y in P to be left if accessed left subtree of y more recently right if accessed right subtree of y more recently none if no access to either subtree yet

- preferred path = chain

of preferred child pointers

- partition of nodes of P

- idea: store each preferred path in auxiliary tree

- conceptually separate balanced BST (e.g. AVL)

- leaves link to roots of aux. trees of children paths

- has ≤ lg n nodes (height of perfect P)

⇒ supports search in O(lg lg n) time

- search starts at top aux. tree (containing root of P)

- each jump to next aux. tree = nonpreferred edge

= preferred edge change = +1 in Wilber-1

- k jumps ⇒ CB Kn UB (k+1) - O(lg lg n)

⇒ O(lg lg n) - competitive ... if we can update preferred edges OK

<div style="text-align: center;"><img src="imgs/img_in_image_box_784_467_1224_708.jpg" alt="Image" width="35%" /></div>

## Page 7

Auxiliary trees:

- changing a preferred child

= cutting one path &

joining two paths:

<div style="text-align: center;"><img src="imgs/img_in_image_box_893_66_1151_305.jpg" alt="Image" width="21%" /></div>


- if aux. trees were sorted by depth,

this would be like split & concatenate

- depth > d translates to

interval of keys

<div style="text-align: center;"><img src="imgs/img_in_image_box_939_415_1143_528.jpg" alt="Image" width="16%" /></div>


⇒ can implement cuts & joins

with O(1) splits & concatenates

- each costs O(lg laux.treel) = O(lglg n)

In one tree: mark roots of aux. trees

- modify split & concat. to ignore children trees & manipulate adjacent trees:

<div style="text-align: center;"><img src="imgs/img_in_image_box_338_922_952_1141.jpg" alt="Image" width="50%" /></div>

## Page 8

Signed Greedy:

— Sweep as in Greedy

— only satisfy boxes

— for every added point,

  get independent ☐-rectangle

⇒ get lower bound: ☐-Greedy

Theorem:  $ \max\{\varnothing,-\text{Greedy}, \varnothing,-\text{Greedy}\} $

 $ \Rightarrow \Theta(\text{biggest independent-rectangle }LB) $

Proof: define  $ \text{OPT}_{\varnothing} = \text{smallest union of } \varnothing, -\text{satisfying superset } \& \varnothing, -\text{satisfying superset} $

 $ OPT \geq OPT_{\Delta} $

What we actually proved on p.2

 $ \Rightarrow \geq \text{input} + \frac{1}{2} \max \# \text{independent rectangles} $

 $ \Rightarrow \frac{1}{2} \max \{\square - Greedy_n \square - Greedy\} $

 $ \Rightarrow \frac{1}{2} \max \{\text{OPT}_\varnothing \text{ - OPT}_\varnothing\} $

 $ \Rightarrow \frac{1}{4} (\text{OPT}_\varnothing + \text{OPT}_\varnothing) $

 $ \Rightarrow \frac{1}{4} \text{OPT}_\varnothing $

 $ \Rightarrow \text{constant} - \text{factor} \text{sandwich} $

## Summary: so close!


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Greedy ☐ &amp; ☐ uB</td><td style='text-align: center; word-wrap: break-word;'>vs.</td><td style='text-align: center; word-wrap: break-word;'>Signed Greedy ☐ + ☐ LB</td></tr></table>

PROJECT: compare UBs & LBs for many pt sets
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
