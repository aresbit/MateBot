# Geometry and Range Searching

Geometric reinterpretations of data-structure problems, point location, orthogonal range searching, fractional cascading, and kinetic viewpoints.

## Included Lectures
- L03.md
- L04.md

---

## L03.md


## Page 1

Today: Geometry I (of 2)

- point location

  - static via persistence

  - dynamic via retroactivity

- orthogonal range searching

  - range trees

  - layered range trees

- dynamization with augmentation via weight balance

- fractional cascading

Planar point location: given planar map,

(planar) graph drawn in plane

with straight edges & without crossings

support query: which face contains point (x,y)?

- e.g. which GUI element got clicked?

which city are these GPS coords. in?

- static: preprocess map

- dynamic: add/delete edges (& deg.-∅ vertices)

Vertical ray shooting: given planar map, support query: which edge first hit by ray ♠(x,y)

- implies (static) solution to point location: maintain pointer from edge to face below it

- also dynamic reduction with +O(lgn) overhead
## Page 2

Line sweep: technique traditionally used for line-segment intersection



a a d)

a b b) a a c)

/ a (b (c c c c) a a)

see e.g. CLRSJ

- maintain order

of intersection

with vertical

line which

sweeps right

- left/right

endpoints are

inserts/deletes

- order swaps

are crossings



<div style="text-align: center;"><img src="imgs/img_in_image_box_125_332_719_805.jpg" alt="Image" width="48%" /></div>


- typically intersection DS = balanced BST  

⇒ line-segment intersection in O(nlg n + k)

- if we use partially persistent balanced BST then successor(y) query at time t = upward ray shooting query from (t, y)

⇒ O(lg n) query after O(nlg n) preprocessing [Dobkin & Lipton-SCOMP 1976]

(part of the initial motivation for persistence)
## Page 3

- if we use fully retroactive balanced BST then Insert/Delete (t₁, insert(y))

+ Insert/Delete (t₂, delete(y))

= insert/delete edge (t₁,y)→(t₂,y)

⇒ O(lg n) dynamic vertical ray shooting

among horizontal line segments

[Giova & Kaplan - T. Alg. 2009]

also: [Blelloch - SODA 2008] (later)

- also reduces back to retroactive successor

OPEN: O(lg n) dynamic vertical ray shooting

in general planar map?

- O(lg n lg lg n) query & insert; O(lg² n) delete

[Baumgarten, Jung, Mehlhorn - J.Alg. 1994]

- O(lg n) query, O(lg¹⁺₅ n) insert, O(lg²⁺₅ n) delete

[Arge, Brodal, Georgiadis - FOCs 2006]

OPEN: O(lg n) static ray shooting (not vertical)

- O( $ \frac{n}{v^{2}} $ polylg n) query & O(s^{1+ε}) space

## [Agarwal-S(COMP 1992)]

- conjectured nearly optimal

- 3D even harder e.g. [Agarwal & Sharir-S1COMP 1996]

- motivation: ray tracing
## Page 4

Orthogonal range searching:

maintain n points in d dimensions subject to

query: given box  $ [a_{1}, b_{1}] \times \cdots \times [a_{d}, b_{d}] $,

report existence/count/k points in box

- static: preprocess points; dynamic: insert/delete

- motivation: query in database table with d cols.

Range trees: O(lg^{d} n + k) query

(see de Berg, Cheong, Van Kreveld book)

[Bentley - IPL; Lee & Wong - TDS; Lueker - FOCS; Willard - TR]

- ID: balanced BST on leaves = points

  - internal node key = max(left subtree)

  - query([a,b]): search(a); search(b)

  BST

<div style="text-align: center;"><img src="imgs/img_in_image_box_237_853_1077_1268.jpg" alt="Image" width="68%" /></div>


pred(a)→☐☐☐



(can also do this with regular BST but messier a especially to generalize)
## Page 5

- 2D: 1D tree on x + each subtree links to 1D

  x ∧

  free on y on same points

- each point appears in ☉(lg n) structures

⇒ ⊙(nlg n) space

- query([a₁,b₁]×[a₂,b₂]):

  - x query([a₁,b₁]) → ⊙(lg n) × subtrees

  - follow pointers → ⊙(lg n) y trees

  - ⊙(lg n) y queries → ⊙(lg² n) y subtrees

⇒ ⊙(lg² n + k) time

- augment y trees with subtree sizes for count



<div style="text-align: center;"><img src="imgs/img_in_image_box_353_135_908_353.jpg" alt="Image" width="45%" /></div>


-dD: recurse on d

-O(lg^{d} n) query

-O(n lg^{d-1} n) space & preprocessing

-O(lg^{d} n) update: recursively update each node along root-to-leaf path
## Page 6

Layered range tree: O(lg d-1 n) query for d>1

[Gabow, Bentley, Tarjan-STOC: Willard-PhD/SIComp]

1984:

- 2D: search in x as before

- lca(pred(a), succ(b))



- store y structures as arrays (sorted by y)

- search once in root y structure ~O(lg n)

- carry those search results down to result subtree roots

- from one level down: store pointers to corresponding spots

(successors)

⇒ find start & end in O(lg n) y arrays in O(1) per level. O(lg n) overall

- can still compute counts & report k points





<div style="text-align: center;"><img src="imgs/img_in_image_box_736_751_1155_976.jpg" alt="Image" width="34%" /></div>


- dD: same as before, just use 2D base case

- O(n lg^{d-1} n) space & preprocessing
## Page 7

Dynamization with augmentation via weight balance

- BB[α] trees: [Nievergelt & Reingold - STOC 1972]

- for each node x:

  size(left(x)) & size(right(x)) are ≥ α·size(x)

⇒ height ≤ log₁₀ n

- when node is unbalanced, can afford to

  perfectly rebuild entire subtree of size k:

  - charge to ∅(k) of additive imbalance

  - update gets charged ∅(lg n) times

⇒ ∅(lg n) amortized cost

- applied to layered range tree:

[idea in Lueker-FOCS; see e.g. Willard-SCOMP]

- rebuild costs ☉(k kg⁻¹ k)

(some details here to maintain crosslinking)

⇒ O(kg⁻¹ n) amortized update

Static improvement:

- can reduce space to  $ O(\frac{n\lg d-1}{n}) $

[Chazelle - SICOMP 1986]

- for  $ d \geq 3 $, can improve query to  $ O(\lg d-2n) $

-  $ O(n\lg d\ n) $ space via fractional cascading

[Chazelle & Guibas - Alg. 1986 × 2]

-  $ O(n\lg d-1 + \varepsilon\ n) $ space [Alstrup, Brodal, Rauhe - FOCs 2000]
## Page 8

Fractional cascading: [Chazelle & Gubas - Alg. 1986 ×2] dynamic: [Mehlhorn & Näher - Alg. 1990]

Warmup: predecessor/successor search for x

"1.5D" among k lists each of length n

- O(k lg n) trivial (k binary searches)

- O(k + lg n) solution:

  - let Li = Li + every other element of Li + 1

   $ \Rightarrow |L_i| = n + \frac{1}{2} \cdot |L_{i+1}| = O(n) $ (geometric)

  - link between identical elements in Li & Li + 1

  - each element in Li stores pointer to previous/next element in Li - Li

  - each element in Li - Li stores pointer to previous/next element in Li

<div style="text-align: center;"><img src="imgs/img_in_image_box_253_845_983_1065.jpg" alt="Image" width="59%" /></div>


## -search(x):

- binary search in L1 → O(lg n)

→ if amid L1-L1, follow pointers to neighbors in L1 to solve L1 problem

- if amid L1, follow pointers to neighbors in L1-L1 (else stay)

- walk down to L2

- repeat
## Page 9

General: graph where each

- vertex contains set of elements

- edge labeled with range [a,b]

- locally bounded degree: # incoming

- edges whose labels  $ \geq x $ is  $ \leq c $.

search(x) wants to find x in k vertices' sets found by navigating (online) from any vertex, along edges whose labels  $ \Rightarrow x $ improve  $ O(k \lg n) $ to  $ O(k+\lg n) $

idea: same as warmup

new: cycles in graph

but very few items go around cycles
## Page 10

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L04.md


## Page 1

TODAY: Geometry II (of 2)

- application of fractional cascading

- kinetic data structures

O(lg n) 3D orthogonal range searching: (static) [Chazelle & Guibas – Alg. 1986]

①  $ (-\infty, b_{2}] \times (-\infty, b_{3}) $: search for  $ b_{3} $ in z list + O(k)

- equivalent to stabbing vertical rays

(from points) with horizontal ray (from  $ (b_{2}, b_{3}) $)

<div style="text-align: center;"><img src="imgs/img_in_image_box_223_710_654_1019.jpg" alt="Image" width="35%" /></div>


- draw horizontal segments through points

- subdivide faces to have bounded degree by extending some horizontal segments

- like fractional cascading; insert ≤ 1/2 into left neighbor, recurse; ditto right

⇒ O(n) space [Chazelle-SICamp 1986]

- query searches for b3 among left rays then walks right k steps in O(k) (each crossed ray = 1 point in output)
## Page 2

②  $ [a_{1}, b_{1}] \times (-\infty, b_{2}) \times (-\infty, b_{3}) $;  $ O(\lg n \cdot \text{search} + k) $

- range tree on x

- each node stores ① on points in subtree

→ query reduces to  $ O(\lg n) $ ① queries

③  $ [a_{1}, b_{1}] \times [a_{2}, b_{2}] \times (-\infty, b_{3}) $:  $ \bigcirc (\lg n \cdot \text{search} + k) $

- "range tree" on y

- node v stores key = max(left(v)) (as before)

& ② on points in right(v)

& y-inverted ②' on points in left(v)

→ query  $ [a_{1}, b_{1}] \times (a_{2}, \infty) \times (-\infty, b_{3}) $

- query: walk down tree

- if key < a_{2} < b_{2}: walk right

- if key > b_{2} > a_{2}: walk left

- if a_{2} ≤ key ≤ b_{2}: stop

- query ② for  $ [a_{1}, a_{2}] \times (-\infty, b_{2}) \times (-\infty, b_{3}) $

- query ②' for  $ [a_{1}, a_{2}] \times (a_{2}, \infty) \times (-\infty, b_{3}) $

⇒  $ \bigcirc (\lg n) + \bigcirc(1) $ ② queries

④  $ [a_{1}, b_{1}] \times [a_{2}, b_{2}] \times [a_{3}, b_{3}] $:  $ \alpha(\text{lgn} \cdot \text{search} + k) $

- same as ③ but on z & recursing with ③

  instead of y ↓ instead of ② ↓

- naively  $ \textcircled{O}(\log^{2} n + k) $

- fractional cascading  $ \Rightarrow \textcircled{O}(\log n + k) $

  - bounded degree 5: parent, children, 2aux.

- space:  $ \textcircled{O}(n \log^{3} n) $ (lg per ②, ③, ④)
## Page 3

Kinetic data structures: moving data

- think: tracking physical objects (phones, cars, ...)

[Basch, Guibas, Hershberger-J.Alg. 1999]

Data: value/coordinate = (known) function of time

- e.g. affine a + b t (instead of a initial velocity single number)

- bounded-degree algebraic  $ a + b t + c t^{2} + \cdots $

- pseudo-algebraic: any certificate of interest

- flips true/false O(1) times

## Operations:

- modify(x, f(t)): replace x's function

- idea: motion estimation accurate "for a while"

- advance(t): go forward in virtual time

- other updates/queries usually about present (virtual) time

## Approach:

- store data structure accurate now

- augment with certificates: conditions under which DS is accurate, which are true now

- compute failure time for each certificate

- store them in a priority queue

- as certs. invalidate, fix DS & replace certs
## Page 4

kinetic predecessor:

- want pred/succ search in present in O(lg n)

- let's try a BST

- certificates:  $ \{x_i \leq x_{i+1}\} $

where  $ x_1, x_2, \ldots, x_n $ is an in-order traversal

- failure:  $ \inf \{t \geq \text{now} \mid x_i(t) \geq x_{i+1}(t)\} $

  (next time certificate i will fail)

- advance(t):

  - while  $ t \geq Q $.min:

    - now = Q.min

    - event(Q.delete-min)

  - now = t

- event  $ (x_i \leq x_{i+1}) $: (in fact,  $ x_i = x_{i+1} $ now)

  - swap  $ x_i $ &  $ x_{i+1} $ in BST

  - add certificate  $ x_i' \leq x_{i+1} $

  - replace certificate  $ x_{i-1} \leq x_i $ with  $ x_{i-1} \leq x_i' $

  & certificate  $ x_{i+1} \leq x_{i+2} $ with  $ x_{i+1}' \leq x_{i+2} $

- update failure times in priority queue
## Page 5

Metrics:

① responsive: when certificate expires (event) can fix DS quickly 0(kg n)

② local: no object participates in many certs.

⇒ modify is fast

③  $ \underline{\text{compact}} $: # c $ \underline{\text{erts}} $, is small

→ low space

④  $ \underline{\text{efficient}} $:

worst-case # DS events is small

worst-case # "necessary changes" O(1)

Efficiency: (the vaguest part of kinetic DSs)

- If we need to "know" sorted order

  "at all times", need to update for each

  order change & that's what we do

- if we need to support fast pred./succ.

  "at all times", need to "approximately

  know" sorted order (?)

- usually study worst-case behavior

  for affine/pseudo-alg. data with no updates

- here: ☉(n²)

- Ω: ☉ ☉ ☉ ☉ ← ☉☉

- O: each pair passes ≤ once for affine  $ \rightarrow $ O(1) for pseudo-alg.
## Page 6

Kinetic heap: [de Fonseca & de Figueiredo-IPL 2003]

- want find-min (& delete-min) in O(lg n)

- could use kinetic predecessor ~ can do better

- store a min-heap

- certificate:

<div style="text-align: center;"><img src="imgs/img_in_image_box_468_296_657_410.jpg" alt="Image" width="15%" /></div>


 $ x \leq y $

 $ x \leq z $

- event(x≤y):

  - swap x & y in tree

  - update adjacent certificates

① responsive: O(lg n) (priority queue)

② local: O(1)

③ compact: O(n)

④ efficient: O(lg n)

- ②(n) changes to min in worst case

- Ω: 0 1 2 3 etc.

- O: once min changes  $ x \rightarrow y_{n} $

  x cannot be min again

- claim O(n lg n) events in DS

for affine motion

- OPEN: (pseudo-) algebraic motions?

- OPEN: faster advance because don't need to query interim times?
## Page 7

Proof: (assuming affine motion)

 $ -\Phi(t)=\# \text{events in future} > t $

 $ =\sum_{x} (\# \text{descendants of } x \notin \text{time } t \text{ that will overtake } x \text{ in future} > t) $

\Phi(t,x)

 $ -\Phi(t,x)=\sum_{y_{of}x}\left(\frac{\#descendants\ of\ y\otimes time\ t}{\text{that will overtake}\ x\ in\ >t}\right) $

- consider event at time t:

<div style="text-align: center;"><img src="imgs/img_in_image_box_736_568_1188_748.jpg" alt="Image" width="36%" /></div>


 $$ \Phi(t_{n}^{t}v)=\Phi(t_{n}v)\quad\forall v\neq x_{n}y $$ 

 $$ (v\text{ gains/losses no descendants} $$ 

 $$ (t_{n}^{+}x) = \underline{\Phi(t_{n}x_{n}y)} - 1 $$ 

 $$ \begin{array}{c} -\Phi(t^{+}y)=\Phi(t_{1}y)+\Phi(t_{1}y_{1}z)\\ \leq\Phi(t_{1}y)+\Phi(t_{1}x_{1}z) \end{array} $$ 

 $$ (o v e r t a k e y\Rightarrow o v e r t a k e x) $$ 

 $$ =\Phi(t_{1}y)+\Phi(t_{1}x)-\Phi(t_{1}x_{1}y) $$ 

 $$ \Rightarrow\Phi(t^{+})\leq\Phi(t)^{-1} $$ 

 $$ \begin{array}{c} -\Phi(0) \leq \sum_{x} \underbrace{\# \text{descendants of } x}_{O(\lg n)} \\ = O(n \lg n) \end{array} $$ 
## Page 8

Kinetic survey: [Guibas-DS Handbook 2005]

- 2D convex hull [Basch, Guibas, Hershberger 1999]

- also diameter, width, min. area/perim. rectangle

- efficiency =  $ O(n^{2+2})/\Omega(n^{2}) $

- [OPEN]: 3D?

 $ -(1+E) $-approximate diameter, smallest disk/rectangle in  $ (1/E)^{0(1)} $ events [Agarwal & Har-Peled - SODA 2001]

- smallest enclosing disk: [Demaine, Eisenstat, efficiency  $ \Omega(n^{3+E})/\Omega(n^{2}) $ Guibas, Schulz - FWCG 2010]

- Delaunay triangulation [Albers, Guibas, Mitchell, Roos - O(1) efficiency IJCGA 1998]

- OPEN: how many changes?  $ \Omega(n^{3}) $ &  $ \Omega(n^{2}) $

— any triangulation:

— ∑(n²) changes even with Steiner points

[Agarwal, Basch, de Berg, Guibas, Hershberger — SoCG 1999]

— O(n²²⁺¹/³) events [Agarwal, Basch, Guibas, Hershberger,

— [OPEN]: O(n²²)? Zhang — WAFR 2000]

— O(n²) events for pseudo triangulations

— collision detection [Kirkpatrick, Snoeyink, Speckmann 2000]

[Agarwal, Basch, Guibas, Hershberger, Zhang 2000]

[Guibas, Xie, Zhang 2001] ≤ 3D

— MST

↑ sorted order of edge weights

- MST  $ \rightarrow $ sorted

- O(m²) easy: OPEN: o(m²)?

- O(n²-½) for H-minor-free graphs (e.g. planar) [Agarwal, Eppstein, Guibas, Henzinger - FOCs 1998]
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
