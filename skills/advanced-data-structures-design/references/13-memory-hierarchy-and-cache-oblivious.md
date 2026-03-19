# Memory Hierarchy and Cache-Oblivious Design

External-memory thinking, cache-oblivious structures, ordered file maintenance, geometry under memory-transfer cost, and the history of I/O models.

## Included Lectures
- L07.md
- L08.md
- L09.md
- L22.md

---

## L07.md


## Page 1

TODAY: Memory Hierarchies I (of 3)

- external-memory model

- cache-oblivious model

- cache-oblivious B-trees

External memory / I/O / Disk Access Model:

[Aggarwal & Vitter - CACM 1988]

two-level memory hierarchy

 $ \frac{M}{B} $ blocked blocks  $ \frac{SLOW}{} $

block = B words

CACHE/MEMORY

 $ H_{2}O $ DISK

- focus on # memory transfers: blocks read/written between cache & disk

- ≤ RAM running time

- ≥ cell-probe LB

- when can we save this factor of  $ \geq B^{3} $
## Page 2

Basic results in external memory:

⑧ Scanning: O(1/87) to read/write N words in order

Search Trees

- B-trees with branching factor ☐(B)

support insert, delete, predecessor search

in ☐(logB+1 N) memory transfers

( & ☐(lg N) time, with care, in comparison model)

- Ω(logB+1 N) for search in comparison model:

  - where query fits among N items requires

    lg (N+1) bits of information ↑↑↑↑↑

  - each block read reveals where query fits

    among B items ⇒ ≤ lg (B+1) bits of info.

⇒ need ≥ lg (N+1) memory transfers

- also optimal in "block-brake model" if B>1

- also optimal in "block-probe model" if B≥w

[Patrascu & Thorup - see L11]

② Sorting:  $  O(\frac{N}{B} \log_{W} B^{\frac{N}{B}})  $ memory transfers

 $ \Rightarrow B \times $ faster than B-tree sort!

 $ \Omega(\text{ditto}) \text{ in comparison model} $

③ Permuting: O(min{N,  $ \frac{N}{B} $ log_{MB}  $ \frac{N}{B} $})

physical:  $ \Omega $(dito) in indivisible model

execution:  $ \leq $can't pack pieces of input words in words

④ Buffer tree: O( $ \frac{1}{B} $ log $ _{WB} $  $ \frac{N}{B} $) amortized mem. transfer for delayed queries & batched updates & O( $ \phi $) delete-min ( $ \Rightarrow $ priority queues)
## Page 3

Cache-olivious model: [Frigo, Leiserson, [6.046]

Prokop, Ramachandran-FACS 1999: Prokop-MEng 1999

- like external-memory model

- but algorithm doesn't know B or M (!)

→ must work for all B & M

- automatic block transfers triggered by word access

with offline optimal block replacement

- FIFO, LRU, or any conservative replacement

is 2-competitive given cache of 2x size

(resource augmentation)

- dropping M ↘ M/2 doesn't affect

typical bounds eg. sorting bound

Cool:

- clean model: algorithm just like RAM

- adapts to changing B (disk tracks & cache)

& M (competing processes)

-OPEN: formalize this

-adapts to all levels of multilevel memory hierarchy: CPU:  $ M_{1} $  $ M_{2} $  $ M_{3} $  $ M_{4} $

- often possible!
## Page 4

Basic cache-oblivious results:

① Scanning: same algorithm & bound

in O(logB+1 N) memory transfers S&L21

[Bender, Demaine, Farach-Colton — FOCs 2000/SICMP2005]

[Bender, Duan, Jacono, Wu — SODA 2002/J.Alg. 2004]

[Brodal, Fagerberg, Jacob — SODA 2002]

— best constant is lg e, not 1

[Bender, Brodal, Fagerberg, Ge, He, Hu, Jacono,

López-Ortiz — FOCs 2003]

② Sorting:  $ O(\frac{N}{B} \log_{M/B} \frac{N}{B}) $ memory transfers

[Frigo et al. 1999; Brodal & Fagerberg-I CALP 2002]

- uses tall-cache assumption:  $ M = \Omega(B^{1 + \varepsilon}) $

- impossible otherwise [Brodal & Fagerberg-STOC 2003]

③ Permuting: min impossible [Brodal & Fagerberg-same]

* (4) Priority queue: O( $ \frac{1}{3} $ log $ _{10} $ B) amortized mem.transf.

- uses fall-cache assumption

[Arge, Bender, Demaine, Holland-Minkley, Munro -

  STOC 2002/SICOMP 2007; Brodal & Fagerberg - ISAAC 2002]
## Page 5

Cache-oblivious static search trees:

(binary search)

[Prokop-MEng 1999]



- store N elements in N-node complete BST

- carve tree at middle level of edges

⇒ one top piece, ≈√N bottom pieces, each size ≈√N

 $ \lg N \uparrow \frac{1}{2} \lg N \uparrow $

 $ \downarrow \frac{1}{2} \lg N \uparrow $

<div style="text-align: center;"><img src="imgs/img_in_image_box_82_382_1191_666.jpg" alt="Image" width="90%" /></div>


 $ \overbrace{\frac{A}{N}\Delta\cdots\Delta}\approx\sqrt{N} $

-recursively lay out pieces & concatenate; (in any order)

<div style="text-align: center;"><img src="imgs/img_in_image_box_113_811_1018_1062.jpg" alt="Image" width="73%" /></div>


→order to store nodes

"van Emde Boas layout"

- generalizes to [Bender, Demaine, Faroch-Colton 2000]

- height not a power of 2

- node degrees  $ \geq 2 \& O(1) $
## Page 6

Analysis:

- level of detail (refinement) straddling B:

<div style="text-align: center;"><img src="imgs/img_in_image_box_278_209_993_600.jpg" alt="Image" width="58%" /></div>


-cutting height in half until piece size ≤ B

⇒ height of piece between  $ \frac{1}{2} $lg B & lg B (sloppy)

(⇒ size between  $ \sqrt{B} $ & B)

⇒ # pieces along root-to-leaf path ≤  $ \frac{lg N}{2} $lg B = 2logB

-each piece stores ≤ B elements consecutively

⇒ occupies ≤ 2 blocks (depending on alignment)

⇒ #memory transfers ≤ 4logB N (assuming M≥2B)

(really should be B+1)

Improvements: [BBFGHHIL 2003]

① randomize starting location (w.r.t. block)

⇒ expected cost ≤ (2 +  $ \frac{3}{18} $) log $ _{B} $ N

② split height into  $ \frac{1}{2} $ -  $ \varepsilon $:  $ \frac{1}{2} $ +  $ \varepsilon $ ratio

⇒ expected cost ≤ (lg e + o(1)) log $ _{B} $ N

= O(lg lg B/lg B)
## Page 7

Cache-oblivous B-trees as in [Bender, Duan, Jacono, Ww]

① ordered file maintenance: (to do in L8)

store N elements in specified order

in an array of size O(N) with O(1) gaps

- updates: insert element between two given

delete element

by re-arranging array interval of O(lg^2N) am.

② build static search free on top:

each node stores max key in subtree (if any)

<div style="text-align: center;"><img src="imgs/img_in_image_box_52_714_1132_1083.jpg" alt="Image" width="88%" /></div>


③ operations:

- binary search via left child's key

- insert(x) finds predecessor & successor,

- inserts there in ordered file,

- updates leaves & max's up tree via postorder traversal

- delete similar
## Page 8

④ update analysis:

if K cells change in ordered file then update tree in O( $ \frac{K}{B} + \log_{B} N $) mem.tr - look at level of detail straddling B - look at bottom two levels:

<div style="text-align: center;"><img src="imgs/img_in_image_box_241_371_1193_639.jpg" alt="Image" width="77%" /></div>


- within chunk of >B, jumping between ≤2 pieces of ≤B (assume M≥2B)

⇒ O(chunk/B) memory transfers in chunk Cportion in update interval +3 maybe (first, last, & root)



⇒ O(k/B) memory transfers in bottom 2 levels

- updated nodes above these two levels:

  - subtree of ≤ k chunk roots

  up to their LCA: costs O(k/B)

- path from LCA to root of tree:

  costs O(log_B N) as above

⇒ O(k/B + log_B N) total memory transfers

So far: search in ☐(log₂ N) = 0(log N)

update in ☐(log₂ N + ∫(log N) N) amortized
## Page 9

⑤  $ \frac{\text{indirection}}{\text{cluster elements into } \Theta(\frac{N}{g_{N}})\text{ groups, each of size } \Theta(\text{lg } N)} $

- use previous structure on min's of clusters

previous structure  $ \Theta(N/\lg N) $

min min min

 $ \Theta(\lg N) $  $ \Theta(\lg N) $ ...  $ \Theta(\lg N) $

- update cluster by complete rewrite

  ⇒ O(2/8) memory transfers

- split/merge clusters as necessary

  to keep between 25% & 100% full

  ⇒ Ω(lg N) updates to charge to

  ⇒ O(2/8^2N) update cost in top structure

  only "every" Ω(lg N) actual updates

  ⇒ amortized update cost O(2/8)

  (plus search cost)

Finally:  $ \bigcirc(\log_B N) $ insert, delete, predecessor, successor

just like B-trees in external mem. (known B)
## Page 10

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L08.md


## Page 1

TODAY: Memory Hierarchies II (of 3)

- ordered file maintenance (for B-tree in L7)

- list labeling (for persistence in L1)

- cache-obligious priority queue

Ordered file maintenance: [Itai, Konheim, Roteh-IcalP1981: Bender, Demaine, Farach-Colton-Focs 2000]

Goal: store N elements in specified order in an array of size O(N) with gaps of size O(1)

⇒ scanning K consecutive elts. costs O(1/8) mem.trans.

subject to elt. deletion & insertion between 2 elts.

by re-arranging elts. in array interval of O(lg² N) amortized elts. via O(1) interleaved scans

⇒ costs O(1/8) amortized memory transfers

Idea: upon updating element. ensure locally not too dense/sparse by redistributing elements in surrounding interval

— intervals defined by nodes in complete binary tree on O(lg n)-size chunks of array:

 $ \hat{n}=\lg n-\Theta(\lg\lg n) $

conceptual complete binary tree

 $ \forall\Theta(\lg n)\quad\Theta(\lg n)\quad\Theta(\lg n)\quad\Theta(\lg n)\quad\Theta(\lg n)\quad\Theta(\lg n) $
## Page 2

Update:

① update leaf by rewriting ② (lg n)-size chunk

③ walk up tree until reach ancestor whose density(node) = #elts. stored below node #array slots in interval is within threshold at its depth d:

- density ≥  $ \frac{1}{2} - \frac{1}{4} \frac{d}{h} \in [\frac{1}{4}, \frac{1}{2}] $ (not too sparse)

- density ≤  $ \frac{3}{4} + \frac{1}{4} \frac{d}{h} \in [\frac{3}{4}, 1] $ (not too dense)

③ evenly rebalance elements below node

Analysis:

- thresholds get fighter as we go up

⇒ rebalancing node puts children FAR within threshold:

  ldensity - threshold ≈ 1/4/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/1/

→ O(lg N) amortized rebuild cost

to update element below a node

- each leaf is below h=Θ(lg N) ancestors

→ O(lg² N) amortized cost per update

Worst-case bounds possible [Willard - I&C 1992; Bender, Cole, Demaine, Farach-Colton, Zito - ESA 2002]

Conjecture:  $ \Omega(\lg^{2}N) $ necessary
## Page 3

List labeling: closely related problem

maintain explicit integer label in each node in a linked list, subject to insert/delete node here, such that labels are monotone at all times (label = index in array)

label space best known time/update

 $ (1+\varepsilon)n \cdots n \lg n $  $ \quad O(\lg^{2} n) $ - ordered file maintenance

 $ n^{1+\varepsilon} \cdots n^{O(1)} $  $ \quad \Theta(\lg n) $  $ \rightarrow O $ via modified threshold: density  $ \leq \frac{1}{\alpha}, 1 < \alpha \leq 2 $

 $ 2^{n} $  $ \quad \Theta(1) $ - trivial

List order maintenance: easier problem, from L1

maintain linked list subject to insert/delete node here

& order query: is node x before node y?

- O(1) solution via indirection: [Dietz & Sleator - STOC1987; Bender, Cole, Demaine, Farach-Colton, Zito - ESA2002]

 $ \Theta\left(\frac{n}{\lg n}\right) $  $ \left\{\begin{array}{l}\Theta(\lg n) \text{ solution} \\ \text{using label space } n^{\Theta(1)}\end{array}\right. $

 $ \Theta(\lg n) \Theta(\lg n) \cdots \Theta(\lg n) $  $ \left\{\begin{array}{l}\text{trivial } \Theta(1) \text{ solution} \\ \text{using exponential label space}\end{array}\right. $

- implicit node label = (top label, bottom label)

→ can compare two labels in O(1) time

- top updates change many implicit labels at once

- bottom chunks slow top updates by O(lg n) factor

→ O(1) amortized cost

- worst-case bounds possible [same refs.]
## Page 4

Cache-obvious priority queue; (as in Arge et al. 2007)

- lg lg n levels of size  $ N_{a} $  $ N^{2/3} $  $ N^{4/9} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/3} $  $ N^{2/

Layout: store levels in order, small to large

Invariants:

-down buffers ordered in a level (but ansorted)

-down buffers @X^{3/2} <down buffers @X^{9/4}

-down buffers <up buffer in same level
## Page 5

Find-min: smallest element in smallest down buffer

Delete-min: delete from down buffer: if empty, pull

## Insert:

① append to bottom up buffer

② swap into bottom down buffers if necessary

③ if up buffer overflows: push

Push X elements into level X^{32}

all > down buffers at level X & below

① sort elements

② distribute among down & up buffers:

- scan elements, visiting down buts in order

- when down but, overflows, split in half & link

- when #down buts, overflows, move last to up but

- when up but, overflows, push it up to  $ x^{9/4} $

Pull X smallest elts, from level X3/2 ( & above)

① sort first, two down bufs. & extract leading elts.

② if <X: pull X^3/2 smallest elts. from X^9/4 (&above)

sort these elements & up buffer

refill up buffer to previous size

with largest elements

extract needed smallest elts. fill X total

split rest up into down buffers
## Page 6

Analysis: push/pull at level  $ X^{3/2} $ sans recursion costs  $ O(\frac{x}{B}\log_{MB}\frac{x}{B}) $ memory transfers - assume all levels of size  $ \leq M $ stay in cache - tall cache assumption:  $ M \geq B^{2} $ (say) - push at level  $ X^{3/2} \geq B^{2} \Rightarrow X > B^{4/3} \Rightarrow \frac{x}{B} > 1 $ - sort costs  $ O(\frac{x}{B}\log_{MB}\frac{x}{B}) $ memory transfers - distribute costs  $ O(X^{1/2} + \frac{x}{B}) $ mem. transf. startup per down buf.

- if  $ X \geq B^{2} $ then cost =  $ O(\frac{x}{B}) $

- else: only one such level:  $ B^{4/3} \leq X \leq B^{2} $ can keep 1 block per down buf. in cache.

- if  $ X \leq B^{2} \Rightarrow X^{1/2} \leq B \leq \frac{M}{B} $ by tall cache so just pay  $ O(\frac{x}{B}) $ at this level too

- pull at level  $ X^{3/2} \geq B^{2} $:

- sort costs  $ O(\frac{x}{B}\log_{MB}\frac{x}{B}) $ memory transfers

- another sort of  $ X^{3/2} $ elts. only when recurring  $ \Rightarrow $ charge to recursive pull

Total: each element goes up & then down (roughly - real proof harder)

& costs  $ O(\frac{1}{B} \log_{MB} \frac{x}{B}) $ per push & pull @X

 $ \Rightarrow O(\frac{1}{B} \sum_{i} \log_{MB} \frac{x}{B}) $ amortized cost per element

 $ \exp. geometric \leftrightarrow geometric $

=  $ O(\frac{1}{B} \log_{MB} \frac{N}{B}) $.
## Page 7

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L09.md


## Page 1

TODAY: Memory Hierarchies meet Geometry

- distribution sweeping via Lazy Funnelsort

- orthogonal 2D range searching:

- batched -online

 $ \frac{\text{[K-funnel: merges K sorted lists of total}}{\text{size } \Delta(k^{3})} $

- recursive layout: each △ stored consecutive

- fill buffer by merging 2 child buffers;

if one empties, recursively fill it

-  $ N^{1/3} $-way mergesort with  $ N^{1/3} $-funnel merger

sorts in  $ \bigcirc(\frac{N}{B}\log_{M/B}\frac{N}{B}) $ (as needed in L8 prio.queue)
## Page 2

Distribution sweeping: [Brodal & Fagerberg - ICAI2003]

- use lazy funnelsort to drive divide & conquer

- replace binary merger by thinking about streams of inputs & output.

adding extra data along the way

Problems: all solved in O( $ \frac{N}{B}\log_{MB}\frac{N}{B}+\frac{output}{B} $)

- measure of 2D rectangles

- batch orthogonal range queries

- orthogonal line segment intersection

- pairwise rectangle intersection

- line segment visibility from a point

- all Euclidean 2D nearest neighbors

- all maximal points in 3D
## Page 3

Batch orthogonal range searching: given N points & N rectangles, report which points are in which rectangles - first count # rectangles containing each pt:

① sort points & corners by x coordinate

② divide & conquer in x via lazy funnelsort in y (!) where binary merger = upward sweep

<div style="text-align: center;"><img src="imgs/img_in_image_box_331_545_685_682.jpg" alt="Image" width="28%" /></div>


← split by  $ x_{1} $

sorted by  $ y_{1} $

merging y orders

= sweep

- maintain  $ c_{L}=\#active $ rectangles

- stabbed by sweep line

with left corners in L & spanning R (right corners are right of R)

- symmetrically CR = # active rectangles with right corners in R & spanning L

- when encountering a point in L, add CR to its counter

- similarly compute #outputs from each merge

- allocate that much space for reporting pass

- split up recursion into O(N)-space parts

(necessary for analysis to work out-

see Brodal & Fagerberg)
## Page 4

Orthogonal range searching: preprocess set of points to support reporting queries in O( $ \log_{B}N+\frac{\text{output}}{8} $)

<div style="text-align: center;"><img src="imgs/img_in_image_box_149_208_381_348.jpg" alt="Image" width="18%" /></div>


 $$ 4-s i d e d $$ 

<div style="text-align: center;"><img src="imgs/img_in_image_box_470_207_697_410.jpg" alt="Image" width="18%" /></div>


 $$ 3-\operatorname{sided} $$ 

<div style="text-align: center;"><img src="imgs/img_in_image_box_760_207_971_408.jpg" alt="Image" width="17%" /></div>


 $$ 2-\operatorname{sided} $$ 

query: O(log_{B} N + \frac{out}{B})

- Space:

 $ \frac{2}{3} $ -  $ \frac{2}{3} $ -  $ \frac{2}{3} $ -  $ \frac{2}{3} $ -  $ \frac{2}{

 $$ [\mathrm{A r g e l Z e h}-\mathrm{S o C G2006}] $$ 

 $$ [\text{Arge},\text{Brodal}, $$ 

 $$ \text{Fagerberg} $$ 

 $$ Laustsen-SoC G2005] $$ 

(static)

-compare with RAM:  $ O(N\frac{\lg N}{\lg \lg N}) $ space [L3]
## Page 5

2-sided: [A266]

-static search tree on points, keyed by y

-array of points, with duplication

<div style="text-align: center;"><img src="imgs/img_in_image_box_158_252_1019_495.jpg" alt="Image" width="70%" /></div>


Query:  $ (≤ x_{1}≤ y) $

① binary search for y in tree

② follow pointer into array

③ scan array to the right

until reach a point whose x-coord > query x

- output unique points in (≤ x_i ≤ y)

↑ filter

Claims: - find all points in  $ (≤ x_{n}≤ y) $

- # scanned points is O(#output points)

- array has size O(N)

Density:

- query  $ (≤x_{n}≤y) $ dense in S

  if #points in  $ (≤x_{n}*) $ ≤ α·#points in  $ (≤x_{n}≤y) $

  i.e. sorting S by x & scanning  $ (-\infty, x) $

   visits #points ≤ α·#points points in S

- else  $ (≤x_{n}≤y) $ sparse in S
## Page 6

First try:

- let $S_0$ = all points (sorted by $x$)

- observation: $(\leq x_1 \leq y)$ is surely dense in $S_0$

- for $y$ large e.g. $y \geq \max y$ coord.

- let $y_i$ = largest $y$ where some query $(\leq x_i \leq y_i)$

- is sparse in $S_{i-1}$

- let $S_i = S_{i-1} \cap \{*_\cdot \leq y_i\}$ (sorted by $x$)

- repeat until $S_k$ of constant size

- array = $S_0 \times S_{1-1} \times S_{2-1} \cdots \times S_k$

- correct & fast queries

- but quadratic space:

<div style="text-align: center;"><img src="imgs/img_in_image_box_840_550_1180_799.jpg" alt="Image" width="27%" /></div>


Correct attempt: maximize common suffix

- define  $ y_i $ (but not  $ S_i $) as before

- let  $ x_i = \max $, where  $ ( \leq x_{i_n} \leq y_i)  $ is sparse for  $ S_{i-1} $

- let  $ P_{i-1} = S_{i-1} \cap (\leq x_{i_n} *) $

- let  $ S_i = S_{i-1} \cap ( (*_n \leq y_i) \cup (>x_{i_n} *)) $

- array =  $ P_{0n}P_{1n}P_{2n} \ldots a P_{i-1n}S_i $

<div style="text-align: center;"><img src="imgs/img_in_image_box_992_985_1164_1128.jpg" alt="Image" width="14%" /></div>

## Page 7

Proof of claims:

- correctness: the repeated elements always have x coord. <last seen point. in any query -can avoid duplicates by focusing on monotone sequence of x coords.

- space:  $ \left|P_{i-1}\cap S_{i}\right|\leq\frac{1}{\alpha}\cdot\left|P_{i-1}\right| $

because  $ (x_{i},y_{i}) $ is sparse in  $ S_{i-1} $

 $ \Rightarrow $ charge storing  $ P_{i-1} $ to  $ P_{i-1}\cdot S_{i} $

 $ \Rightarrow $ each point charged only once.

factor  $ \frac{1}{1-\frac{1}{\alpha}}=\frac{\alpha}{\alpha-1} $

 $ \Rightarrow $  $ \leq\frac{\alpha}{\alpha-1}\cdot N $ space

-query time: repetition is geometric series

  → lose only O(1)×

- can be computed in  $ O(\frac{N}{B}\log_{M B}\frac{N}{B}) $ [Bradal]
## Page 8

3-sided:  $ [A_{2}O_{6}] $

 $ O(\log_{B} N + \frac{\text{output}}{B}) $ query:  $ O(N \lg N) $ space

-just like structure ③ in L4:

-static search tree where leaves = points keyed by x:

<div style="text-align: center;"><img src="imgs/img_in_image_box_257_350_547_552.jpg" alt="Image" width="23%" /></div>


stores two 2-sided structures for ☐ & ☐ on points in the subtree

 $ \Rightarrow \Delta(N\lg N) $ space

query  $ [x_{1}, x_{2}], n \leq y_{2}] $:

- find  $ lca(l_{1}, r) $ (VEB analysis)

- query  $ (z_{x_{1}}, z_{y_{2}}) $ in left child

- query  $ (s_{x_{2}}, s_{y_{2}}) $ in right child

<div style="text-align: center;"><img src="imgs/img_in_image_box_843_542_1158_764.jpg" alt="Image" width="25%" /></div>


OPEN: 3-sided range queries

O(log₂ N + ∂ output / B) query

O(N) space

i.e. match persistent B-tree of external memory
## Page 9

4-sided: [ABFL05]

O( $ \log_{B}N+\frac{\text{output}}{B} $) query: O( $ N\frac{\log_{2}N}{\log_{B}N} $) space

- static search tree on leaves=points, keyed by y

<div style="text-align: center;"><img src="imgs/img_in_image_box_268_295_608_483.jpg" alt="Image" width="27%" /></div>


- conceptually contract $\frac{1}{2}lg\ln n$-height subtrees

into $\sqrt{lg n}$-degree nodes:

$\Rightarrow$ height = O$\left(\frac{lg n}{lg\ln n}\right)$

- for each such node, store

- two 3-sided structures for 回 回

  on points in subtree

- lgn static search trees, keyed by x, 30(k) spc

  on points in each interval of children $\cdot$gK



<div style="text-align: center;"><img src="imgs/img_in_image_box_796_576_1095_704.jpg" alt="Image" width="24%" /></div>


- query  $ [x_{1}, x_{2}], [y_{1}, y_{2}] $:

  - find lca  $ (y_{1}, y_{2}) $ in tree

  - query  $ (x_{1}, x_{2}], \geq y_{1}) $ in (left) child  $ \ni y_{1} $

  - query  $ (x_{1}, x_{2}], \leq y_{2}) $ in (right) child  $ \ni y_{2} $

  - query  $ (x_{1}, x_{2}], *) $ in children in between

<div style="text-align: center;"><img src="imgs/img_in_image_box_921_1027_1174_1180.jpg" alt="Image" width="20%" /></div>


- space:

O(NlgN  $ \frac{lgN}{lgN} $)

3-sided #repetitions of element tree #trees
## Page 10

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L22.md


## Page 1

## The History of I/O Models

## Erik Demaine
## Page 2

## Memory Hierarchies in Practice

<div style="text-align: center;"><img src="imgs/img_in_image_box_69_104_1372_988.jpg" alt="Image" width="90%" /></div>


Outer Space

< 10^{83}

Courtesy of Rjt. Used with permission.

Courtesy of NASA, ESA, and M. Livio and the Hubble 20th Anniversary Team (STScI). License: Creative Commons BY.
## Page 3

## Models, Models, Models


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Model</td><td style='text-align: center; word-wrap: break-word;'>Year</td><td style='text-align: center; word-wrap: break-word;'>Blocking</td><td style='text-align: center; word-wrap: break-word;'>Caching</td><td style='text-align: center; word-wrap: break-word;'>Levels</td><td style='text-align: center; word-wrap: break-word;'>Simple</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Idealized 2-level</td><td style='text-align: center; word-wrap: break-word;'>1972</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>✓</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Red-blue pebble</td><td style='text-align: center; word-wrap: break-word;'>1981</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>✓ -</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>External memory</td><td style='text-align: center; word-wrap: break-word;'>1987</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>✓</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>HMM</td><td style='text-align: center; word-wrap: break-word;'>1987</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>∞</td><td style='text-align: center; word-wrap: break-word;'>✓</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>BT</td><td style='text-align: center; word-wrap: break-word;'>1987</td><td style='text-align: center; word-wrap: break-word;'>~</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>∞</td><td style='text-align: center; word-wrap: break-word;'>✓ -</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(U)MH</td><td style='text-align: center; word-wrap: break-word;'>1990</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>∞</td><td style='text-align: center; word-wrap: break-word;'>✗</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Cache oblivious</td><td style='text-align: center; word-wrap: break-word;'>1999</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>2-∞</td><td style='text-align: center; word-wrap: break-word;'>✓ +</td></tr></table>
## Page 4

## Physics

Case for nonuniform access cost

• Circuits?
## Page 5

## Idealized Two-Level Storage [Floyd — Complexity of Computer Computations 1972]

- RAM = blocks of ≤ B items

- Block operation:



■ Read up to B items from two blocks i, j

Write to third block k

<div style="text-align: center;"><img src="imgs/img_in_image_box_858_255_1432_739.jpg" alt="Image" width="39%" /></div>


● Ignore item order within block

• Items are indivisible

CPU operations considered free
## Page 6

## Permutation Lower Bound [Floyd — Complexity of Computer Computations 1972]

- Theorem: Permuting N items to N/B (full) specified blocks needs

 $$ \Omega\left(\frac{N}{B}\log B\right) $$ 

<div style="text-align: center;"><img src="imgs/img_in_image_box_859_445_1055_556.jpg" alt="Image" width="13%" /></div>


block operations, in average case

<div style="text-align: center;"><img src="imgs/img_in_image_box_1051_252_1418_744.jpg" alt="Image" width="25%" /></div>


■ Assuming  $ \frac{N}{B} > B $ (tall disk)

• Simplified model: Move items instead of copy

☑ Equivalence: Follow item's path from start to finish
## Page 7

## Permutation Lower Bound [Floyd — Complexity of Computer Computations 1972]

•  $ \underline{\text{Potential:}} $  $ \Phi = \sum_{i,j} n_{ij} \log n_{ij} $

# items in block i destined for block j

■ Maximized in target configuration of full blocks  $ (n_{ii}=B) $:  $ \Phi = N \log B $

■ Random configuration with  $ \frac{N}{B} > B $

has  $ \mathrm{E}[n_{ij}] = O(1) \Rightarrow \mathrm{E}[\Phi] = O(N) $

■  $ \underline{\text{Claim: Block operation increases  $ \Phi $ by  $ \leq B $}} $



<div style="text-align: center;"><img src="imgs/img_in_image_box_1050_251_1421_744.jpg" alt="Image" width="25%" /></div>


■ ⇒ Number of block operations ≥  $ \frac{N \log B - O(N)}{B} $
## Page 8

## Permutation Lower Bound [Floyd — Complexity of Computer Computations 1972]

•  $ \underline{\text{Potential:}} $  $ \Phi = \sum_{i,j} n_{ij} \log n_{ij} $

# items in block i destined for block j

■ Maximized in target configuration of full blocks  $ (n_{ii}=B) $:  $ \Phi = N \log B $

■ Random configuration with  $ \frac{N}{B} > B $

has  $ \mathrm{E}[n_{ij}] = O(1) \Rightarrow \mathrm{E}[\Phi] = O(N) $

Claim: Block operation increases  $ \Phi $ by  $ \leq B $

○  $ \underline{\text{Fact:}} $  $ (x + y) \log(x + y) \leq x \log x + y \log y + x + y $

○ So combining groups x & y increases  $ \Phi $ by  $ \leq x + y $



<div style="text-align: center;"><img src="imgs/img_in_image_box_1050_251_1419_742.jpg" alt="Image" width="25%" /></div>

## Page 9

## Permutation Bounds

[Floyd — Complexity of Computer Computations 1972]

• Theorem:  $ \Omega\left(\frac{N}{B}\log B\right) $

■ Tight for  $ B = O(1) $

• Theorem:  $ O\left(\frac{N}{B}\log\frac{N}{B}\right) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_855_208_1429_695.jpg" alt="Image" width="39%" /></div>


■ Similar to radix sort,

where key = target block index

■ Accidental claim: tight for all $B \left(<\frac{N}{B}\right)$



By information theoretic considerations, most permutations with w > p require O(w(log₂ p + log₂ w)) operations.

■  $ \underline{\text{We will see:}} $ tight for  $ B > \log \frac{N}{B} $
## Page 10

## Idealized Two-Level Storage [Floyd — Complexity of Computer Computations 1972]

## • External memory & word RAM:

B items

Obviously the above results apply equally, whether (1) the pages are blocks on a disc or drum, the records are in fact records, or (2) the pages are words of internal memory, the records are bits. The latter corresponds to the problem of transposing a Boolean matrix in core memory. The former corresponds to tag sorting of records on a disc memory.

<div style="text-align: center;"><img src="imgs/img_in_image_box_1063_670_1374_739.jpg" alt="Image" width="21%" /></div>

## Page 11

## Idealized Two-Level Storage [Floyd — Complexity of Computer Computations 1972]

## • External memory & word RAM:

Obviously the above results apply equally, the pages are blocks on a disc or drum, the recor records, or (2) the pages are words of i records are bits. The latter correspond transposing a Boolean matrix in core memory. T corresponds to tag sorting of records on a disc me

<div style="text-align: center;"><img src="imgs/img_in_image_box_1055_227_1414_708.jpg" alt="Image" width="24%" /></div>


## • Foreshadowing future models:

The above results apply to an idealized three-address machine. Work is in progress attempting to apply a similar analysis to idealized single-address machines with fast memories capable of holding two or more pages.

© Springer-Verlag US. All rights reserved. This content is excluded from our Creative Commons license. For more information, see http://ocw.mit.edu/help/faq-fair-use/.
## Page 12

### Pebble Game [Hopcroft, Paul, Valiant — J. ACM 1977]

- View computation as DAG of data dependencies

• Pebble = "in memory"

Moves:

inputs:

Place pebble on node

if all predecessors have a pebble

<div style="text-align: center;"><img src="imgs/img_in_image_box_951_253_1429_668.jpg" alt="Image" width="33%" /></div>


outputs:

Remove pebble from node

• Goal: Pebbles on all output nodes

Minimize maximum number of pebbles over time
## Page 13

### Pebble Game [Hopcroft, Paul, Valiant — J. ACM 1977]

- Theorem: Any DAG can be “executed” using  $ O\left(\frac{n}{\log n}\right) $ maximum pebbles inputs:



<div style="text-align: center;"><img src="imgs/img_in_image_box_949_253_1429_669.jpg" alt="Image" width="33%" /></div>


• Corollary:

DTIME(t) ⊆ DSPACE  $ \left(\frac{t}{\log t}\right) $
## Page 14

## Red-Blue Pebble Game [Hong & Kung — STOC 1981]

• Red pebble = "in cache"

● Blue pebble = "on disk"

Moves:

■ Place  $ \underline{\text{red}} $ pebble on node if all predecessors have red pebble

Remove pebble from node inputs:



<div style="text-align: center;"><img src="imgs/img_in_image_box_951_254_1430_670.jpg" alt="Image" width="33%" /></div>


■ Write: Red pebble → blue pebble

■ Read: Blue pebble → red pebble

minimize



•  $ \underline{\text{Goal:}} $ Blue inputs to blue outputs

■ ≤ M red pebbles at any time
## Page 15

## Red-Blue Pebble Game [Hong & Kung — STOC 1981]

• Red pebble = "in cache"

● Blue pebble = "on disk"

<div style="text-align: center;"><img src="imgs/img_in_image_box_102_435_632_1071.jpg" alt="Image" width="36%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_951_254_1431_668.jpg" alt="Image" width="33%" /></div>


minimize number of

cache  $ \leftrightarrow $ disk I/Os

(memory transfers)
## Page 16

## Red-Blue Pebble Game Results [Hong & Kung — STOC 1981]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Computation DAG</td><td style='text-align: center; word-wrap: break-word;'>Memory Transfers</td><td style='text-align: center; word-wrap: break-word;'>Speedup</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Fast Fourier Transform (FFT)</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log_M N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log M) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Ordinary matrix-vector multiplication</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^2}{M}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(M) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Ordinary matrix-matrix multiplication</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^3}{\sqrt{M}}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\sqrt{M}) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Odd-even transposition sort</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^2}{M}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(M) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>$ \underbrace{N \times N \times \cdots \times N}_{d} \text{ grid} $</td><td style='text-align: center; word-wrap: break-word;'>$ \Omega\left(\frac{N^d}{M^{1/(d-1)}}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(M^{1/(d-1)}\right) $</td></tr></table>
## Page 17

## Comparison

Idealized two-

level storage

[Floyd 1972]

<div style="text-align: center;"><img src="imgs/img_in_image_box_49_454_579_948.jpg" alt="Image" width="36%" /></div>


blocks but no cache

<div style="text-align: center;"><img src="imgs/img_in_image_box_665_284_808_356.jpg" alt="Image" width="9%" /></div>


Red-blue

pebble game

[Hong & Kung 1981]

<div style="text-align: center;"><img src="imgs/img_in_image_box_833_443_1366_1052.jpg" alt="Image" width="37%" /></div>


cache but no blocks
## Page 18

## I/O Model

[Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

• AKA: External Memory Model, Disk Access Model

• Goal: Minimize number of I/Os (memory transfers)

<div style="text-align: center;"><img src="imgs/img_in_image_box_216_430_895_922.jpg" alt="Image" width="47%" /></div>


cache and blocks

<div style="text-align: center;"><img src="imgs/img_in_image_box_898_435_1227_960.jpg" alt="Image" width="22%" /></div>


 $$ \cdots\cdots\cdots $$ 

 $$ \cdots\cdots\cdots $$ 

<div style="text-align: center;"><img src="imgs/img_in_image_box_903_991_1224_1050.jpg" alt="Image" width="22%" /></div>

## Page 19

### Scanning [Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

- Visiting N elements in order costs  $ O\left(1+\frac{N}{B}\right) $ memory transfers

• More generally, can run ≤  $ \frac{M}{R} $ parallel scans,

keeping 1 block per scan in cache

■ E.g., merge $O\left(\frac{M}{B}\right)$ lists of total size $N$ in $O\left(1+\frac{N}{B}\right)$ memory transfers

<div style="text-align: center;"><img src="imgs/img_in_image_box_1099_570_1366_1067.jpg" alt="Image" width="18%" /></div>


 $$ \cdots\cdots\cdots $$ 
## Page 20

## Practical Scanning [Arge]

• Does the B factor matter?

Should I presort my linked list before traversal?

Example:

■  $ N = 256{,}000{,}000 \sim 1 \text{GB} $

■  $ B = 8{,}000 \sim 32KB $ (small)



■ 1ms disk access time (small)

■ N memory transfers take 256,000 sec ≈ 71 hours

■  $ \frac{N}{B} $ memory transfers take 256/8 = 32 seconds
## Page 21

### Searching [Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

• Finding an element x among N items requires  $ \Theta(\log_{B+1} N) $ memory transfers

•  $ \underline{\text{Lower bound:}} $ (comparison model)

■ Each block reveals where x fits among B items

▪  $ \Rightarrow $ Learn  $ \leq $  $ \log(B + 1) $ bits per read

▪ Need  $ \log N + 1 $ bits





• Upper bound:

<div style="text-align: center;"><img src="imgs/img_in_image_box_761_708_1105_827.jpg" alt="Image" width="23%" /></div>


B-tree

■ Insert & delete in  $ O(\log_{B+1} N) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_1135_596_1378_1056.jpg" alt="Image" width="16%" /></div>

## Page 22

### Sorting and Permutation [Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

• Sorting bound:  $ \Theta\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right) $

• Permutation bound:  $ \Theta\left(\min\left\{N,\frac{N}{B}\log_{M/B}\frac{N}{B}\right\}\right) $

Either sort or use naïve RAM algorithm

Solves Floyd’s two-level storage problem  $ (M = 3B) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_1200_687_1403_1067.jpg" alt="Image" width="14%" /></div>

## Page 23

### Sorting Lower Bound [Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

• Sorting bound:  $ \Omega\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right) $

■ Always keep cache sorted (free)

Might as well presort each block

■ Upon reading a block, learn how those B items fit

amongst M items in cache

$$\Rightarrow \text{Learn } \lg \binom{M+B}{B} \sim B \lg \frac{M}{B} \text{bits}$$

■ Need  $ \lg N! \sim N \lg N $ bits

■ Know N lg B bits from block presort

<div style="text-align: center;"><img src="imgs/img_in_image_box_1077_615_1326_1069.jpg" alt="Image" width="17%" /></div>

## Page 24

### Sorting Upper Bound [Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

• Sorting bound:  $ O\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right) $

■  $ O\left(\frac{M}{B}\right) $-way mergesort

 $$ \textcircled{~}T(N)=\frac{M}{B}T\left(N/{\frac{M}{B}}\right)+O\left(1+\frac{N}{B}\right) $$ 

 $$ \blacksquare~T(B)=O(1) $$ 

 $$ \begin{array}{ccc}M/B&N/B&\cdots\cdots\cdots\cdots\quad N/B\\\log_{M/B}\frac{N}{B}&&\cdots\cdots\cdots\cdots\quad N/B\\ levels&&\\1&1&1\cdots\cdots\quad N/B\\\end{array} $$ 

\[\begin{array}{c} B\text{ items} \quad \rightarrow\\ \hline \quad \quad \
## Page 25

## Distribution Sort

[Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

•  $ \sqrt{M/B} $-way quicksort

1. Find  $ \sqrt{M/B} $ partition elements, roughly evenly spaced

2. Partition array into  $ \sqrt{M/B} + 1 $ pieces



■ Scan:  $ O\left(\frac{N}{B}\right) $ memory transfers

3. Recurse

Same recurrence as mergesort

<div style="text-align: center;"><img src="imgs/img_in_image_box_1111_637_1347_1073.jpg" alt="Image" width="16%" /></div>

## Page 26

### Distribution Sort Partitioning [Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

1. or first, second, ... interval of M items:

Sort in  $ O(M/B) $ memory transfers

■ Sample every  $ \frac{1}{4}\sqrt{M/B} $ th item

■ Total sample: 4N/ $ \sqrt{M/B} $ items

2. For  $ i = 1,2, \ldots, \sqrt{M/B} $:

■ Run linear-time selection to find sample element at  $ i/\sqrt{M/B} $ fraction

■ Cost:  $ O\left(\left(\frac{N}{\sqrt{M/B}}\right)/B\right) $ each

 $$ \bullet \quad \bullet \quad \bullet \quad \bullet \quad \bullet $$ 

■ Total:  $ O(N/B) $ memory transf.

<div style="text-align: center;"><img src="imgs/img_in_image_box_1067_430_1396_1060.jpg" alt="Image" width="22%" /></div>


 $$ \cdots\cdots\cdots $$ 

 $$ \cdots\cdots\cdots $$ 

 $$ \bullet \quad \bullet \quad \bullet \quad \bullet \quad \bullet $$ 

 $$ \bullet \quad \bullet \quad \bullet \quad \bullet \quad \bullet $$ 
## Page 27

## Disk Parallelism

[Aggarwal & Vitter — ICALP 1987, C. ACM 1988]

P
## Page 28

## Parallel Disks

J. Vitter and E. Shriver. Algorithms for parallel memory: Two-level memories. Algorithmica, 12:110-147, 1994.
## Page 29

### Random vs. Sequential I/Os [Farach, Ferragina, Muthukrishnan — FOCS 1998]

• Sequential memory transfers are part of bulk read/write of  $ \Theta(M) $ items

Random memory transfer otherwise

Sorting:

■ 2-way mergesort achieves $O\left(\frac{N}{B}\log\frac{N}{B}\right)$ sequential

■ $o\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right)$ random implies $\Omega\left(\frac{N}{B}\log\frac{N}{B}\right)\text{total}_{\leftarrow B\text{items}}\rightarrow$



• Same trade-off for suffix-tree construction

<div style="text-align: center;"><img src="imgs/img_in_image_box_1187_819_1329_1074.jpg" alt="Image" width="9%" /></div>

## Page 30

## Hierarchical Memory Model (HMM) [Aggarwal, Alpern, Chandra, Snir — STOC 1987]

• Nonuniform-cost RAM:

■ Accessing memory location x costs f(x) = [log x]

<div style="text-align: center;"><img src="imgs/img_in_image_box_30_490_1382_763.jpg" alt="Image" width="93%" /></div>


“particularly simple model of computation that mimics the behavior of a memory hierarchy consisting of increasingly larger amounts of slower memory”
## Page 31

## Why  $ f(x) = \log x $? [Mead & Conway 1980]

<div style="text-align: center;"><img src="imgs/img_in_image_box_25_201_712_865.jpg" alt="Image" width="47%" /></div>


<div style="text-align: center;">Fig. 8.31 Three levels of a memory hierarchy with alpha = 4.</div>


© Pearson. All rights reserved. This content is excluded from our Creative Commons license. For more information, see http://ocw.mit.edu/help/faq-fair-use/.

##### 8.5.2.3 Access Time of the RAM

For a RAM of S words, the access time in units of  $ \tau $ is then  $ \alpha b_{0}(\log S/2\log \alpha) $.
## Page 32

HMM Upper & Lower Bounds

[Aggarwal, Alpern, Chandra, Snir — STOC 1987]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>Time</td><td style='text-align: center; word-wrap: break-word;'>Slowdown</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Semiring matrix multiplication</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{3}) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(1) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Fast Fourier Transform</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N \log \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log \log N) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N \log \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log \log N) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Scanning input (sum, max, DFS, planarity, etc.)</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log N) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Binary search</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log^{2} N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log N) $</td></tr></table>
## Page 33

## Defining “Locality of Reference” [Aggarwal, Alpern, Chandra, Snir — STOC 1987]

• Any problem solvable in  $ T(n) $ time on RAM is solvable in  $ O(T(n)\log n) $ time on HMM

• Problem is

■ Nonlocal     if  $ \Theta(T(n)\log n) $ is optimal

■ Local if  $ \Theta(T(n)) $ is possible

Semilocal if  $ \frac{\text{OPT}_{\text{HMM}}}{\text{OPT}_{\text{RAM}}} $ is  $ \omega(1) $ and  $ o(\log n) $
## Page 34

## HMM Results

[Aggarwal, Alpern, Chandra, Snir — STOC 1987]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>Locality</td><td style='text-align: center; word-wrap: break-word;'>$ \frac{OPT_{HMM}}{OPT_{RAM}} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Matrix multiplication on a semiring</td><td style='text-align: center; word-wrap: break-word;'>Local</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(1) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Fast Fourier Transform</td><td style='text-align: center; word-wrap: break-word;'>Semilocal</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log \log n) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting</td><td style='text-align: center; word-wrap: break-word;'>Semilocal</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log \log n) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Scanning input (sum, max, DFS, planarity, etc.)</td><td style='text-align: center; word-wrap: break-word;'>Nonlocal</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log n) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Binary search</td><td style='text-align: center; word-wrap: break-word;'>Nonlocal</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log n) $</td></tr></table>
## Page 35

## Defining “Locality of Reference” [Aggarwal, Alpern, Chandra, Snir — STOC 1987]

• Any problem solvable in  $ T(n) $ time on RAM is solvable in  $ O\left(T(n) \cdot f(T(n))\right) $ time on HMM

• Problem is

■ Nonlocal if  $ \Theta(T(n)\log n) $ is optimal

■ Local if  $ \Theta(T(n)) $ is possible

Semilocal if  $ \frac{\text{OPT}_{\text{HMM}}}{\text{OPT}_{\text{RAM}}} $ is  $ \omega(1) $ and  $ o(\log n) $
## Page 36

## HMM $ _{f(x)} $

[Aggarwal, Alpern, Chandra, Snir — STOC 1987]

• Say accessing memory location x costs  $ f(x) $

• Assume  $ f(2x) \leq c f(x) $ for a constant c > 0

("polynomially bounded")

• Write  $ f(x) = \sum_{i} w_{i} \cdot [x \geq x_{i}] $

(weighted sum of threshold functions)

<div style="text-align: center;"><img src="imgs/img_in_image_box_1054_424_1436_692.jpg" alt="Image" width="26%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_182_704_1311_1024.jpg" alt="Image" width="78%" /></div>

## Page 37

## Uniform Optimality

[Aggarwal, Alpern, Chandra, Snir — STOC 1987]

- Consider one term  $ f_{M}(x) = [x \geq M?] $

- Algorithm is uniformly optimal if optimal on HMM $ _{f_{M}(x)} $ for all M



• Implies optimality for all  $ f(x) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_141_568_1003_1055.jpg" alt="Image" width="59%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_1050_418_1435_685.jpg" alt="Image" width="26%" /></div>

## Page 38

HMM $ _{f_{M}(x)} $ Upper & Lower Bounds

[Aggarwal, Alpern, Chandra, Snir — STOC 1987]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>Time</td><td style='text-align: center; word-wrap: break-word;'>Speedup</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Semiring matrix multiplication</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{\sqrt{M}}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{1\sqrt{M}}{M}\right) $ upper bounds known by Hong &amp; Kung 1981</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Fast Fourier Transform</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log_M N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log M) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log_M N) $</td><td style='text-align: center; word-wrap: break-word;'>other bounds follow from Aggarwal &amp; Vitter 1987</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Scanning input (sum, max, DFS, planarity, etc.)</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N - M) $</td><td style='text-align: center; word-wrap: break-word;'>$ 1 + 1/M $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Binary search</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(\log N - \log M) $</td><td style='text-align: center; word-wrap: break-word;'>$ 1 + 1/\log M $</td></tr></table>
## Page 39

## Implicit HMM Memory Management [Aggarwal, Alpern, Chandra, Snir — STOC 1987]

• Instead of algorithm explicitly moving data, use any conservative replacement strategy (e.g., FIFO or LRU) to evict from cache [Sleator & Tarjan — C. ACM 1985]

-  $ T_{\mathrm{LRU}}(N, M) \leq 2 \cdot T_{\mathrm{OPT}}(N, 2M) $

    =  $ O(T_{\mathrm{OPT}}(N, M)) $ assuming  $ f(2x) \leq c f(x) $

- Not uniform!



<div style="text-align: center;"><img src="imgs/img_in_image_box_300_730_1103_1063.jpg" alt="Image" width="55%" /></div>

## Page 40

## Implicit HMM Memory Management [Aggarwal, Alpern, Chandra, Snir — STOC 1987]

- For general $f$, split memory into chunks at $x$ where $f(x)$ doubles (up to rounding)

 $$ \begin{array}{c}0\\ CPU \quad x_{0}\quad w_{0}\quad x_{1}-x_{0}\quad w_{1}\quad x_{2}-x_{1}\quad w_{2}\quad\cdots\end{array} $$ 
## Page 41

## Implicit HMM Memory Management [Aggarwal, Alpern, Chandra, Snir — STOC 1987]

- For general $f$, split memory into chunks at $x$ where $f(x)$ doubles (up to rounding)

- LRU eviction from first chunk into second;

LRU eviction from second chunk into third; etc.

Like MTF

 $$ \begin{array}{c|ccc} \hline &1 &1&1\\ \hline &1&1&2\\ \hline \end{array} $$ 
## Page 42

## HMM with Block Transfer (BT) [Aggarwal, Chandra, Snir — FOCS 1987]

• Accessing memory location x costs  $ f(x) $

- Copying memory interval from  $ x - \delta \ldots x $ to  $ y - \delta \ldots y $ costs  $ f(\max\{x, y\}) + \delta $

Models memory pipelining ~ block transfer

■ Ignores block alignment, explicit levels, etc.

 $$ \begin{array}{c c c c c c c c c c}{{{CPU}}}&{{{1}}}&{{{1}}}&{{{1}}}&{{{2}}}&{{{1}}}&{{{4}}}&{{{1}}}&{{{8}}}&{{{1}}} \\{{{2^{i}}}} \\\end{array} $$ 
## Page 43

## BT Results

[Aggarwal, Chandra, Snir — FOCS 1987]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = \log x $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, 0 &lt; \alpha &lt; 1 $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, \alpha &gt; 1 $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Dot product, merging lists</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log^{*} N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{\alpha}) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Matrix mult.</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{3}) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{3}) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{3}) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{\alpha}) $ if  $ \alpha &gt; 1.5 $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Fast Fourier Transform</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log^{2} N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{\alpha}) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log^{2} N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{\alpha}) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Binary search</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{\log^{2} N}{\log \log N}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{\alpha}) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{\alpha}) $</td></tr></table>
## Page 44

## Memory Hierarchy Model (MH) [Alpern, Carter, Feig, Selker — FOCS 1990]

• Multilevel version of external-memory model

-  $ M_i \leftrightarrow M_{i+1} $ transfers happen in blocks of size  $ B_i $ (subblocks of  $ M_{i+1} $), and take  $ t_i $ time

• All levels can be actively transferring at once

<div style="text-align: center;"><img src="imgs/img_in_image_box_67_696_1438_1043.jpg" alt="Image" width="95%" /></div>

## Page 45

## Uniform Memory Hierarchy (UMH) [Alpern, Carter, Feig, Selker — FOCS 1990]

• Fix aspect ratio  $ \alpha = \frac{M/B}{B} $, block growth  $ \beta = \frac{B_{i+1}}{B_i} $

•  $ B_{i} = \beta^{i} $

$$\frac{M_{i}}{B_{i}}=\alpha\cdot\beta^{i}$$

2 parameters

1 function

•  $ t_{i} = \beta^{i} \cdot f(i) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_61_697_1439_1042.jpg" alt="Image" width="95%" /></div>

## Page 46

## Random Access UMH (RUMH) [Vitter & Nodine — SPAA 1991]

- RAM program + block move operations like BT, instead of manual control of all levels

<div style="text-align: center;"><img src="imgs/img_in_image_box_67_696_1438_1045.jpg" alt="Image" width="95%" /></div>

## Page 47

## (skipping SUMH)

• Worse (tight) bounds in Vitter & Nodine
## Page 48

## UMH Results

[Alpern, Carter, Feig, Selker — FOCS 1990]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>Upper Bound</td><td style='text-align: center; word-wrap: break-word;'>Lower Bound</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Matrix transpose  $ f(i) = 1 $</td><td style='text-align: center; word-wrap: break-word;'>$ O\left(\left(1 + \frac{1}{\beta^{2}}\right)N^{2}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Omega\left(\left(1 + \frac{1}{\alpha\beta^{4}}\right)N^{2}\right) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Matrix mult.  $ f(i) = 0\left(\beta^{i}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ O\left(\left(1 + \frac{1}{\beta^{3}}\right)N^{3}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Omega\left(\left(1 + \frac{1}{\beta^{3}}\right)N^{3}\right) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>FFT  $ f(i) ≤ i $</td><td style='text-align: center; word-wrap: break-word;'>$ O(1) $</td><td style='text-align: center; word-wrap: break-word;'>$ B_{4} $</td></tr></table>

General approach: Divide & conquer
## Page 49

## (R)UMH Sorting [Vitter & Nodine — SPAA 1991]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>$ f(i) = 1 $</td><td style='text-align: center; word-wrap: break-word;'>$ f(i) = \frac{1}{i + 1} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(i) = \frac{1}{\beta^{ci}}, c &gt; 0 $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N \log N \cdot \log \log N) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta(N^{1+\frac{c}{2}} + N \log N) $</td></tr></table>
## Page 50

## P-HMM Results

[Vitter & Shriver — STOC 1990]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = \log x $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, 0 &lt; \alpha &lt; \frac{1}{2} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{1/2} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, \alpha &gt; \frac{1}{2} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting &amp; FFT</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P} \log N \cdot \log \frac{\log N}{\log P}\right) $</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P}\right)^{\alpha+1} + \frac{N}{P} \log N $</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Matrix mult.</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{P^{3/2}} \log N + \frac{N^{3}}{P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\left(\frac{N^{2}}{P}\right)^{\alpha+1} + \frac{N^{3}}{P}\right) $</td></tr></table>
## Page 51

## P-BT Results

[Vitter & Shriver — STOC 1990]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = \log x $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, 0 &lt; \alpha &lt; 1 $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{1} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, \alpha &gt; 1 $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting &amp; FFT</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P} \log N\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P} \log N\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P} \left( \log^{2} \frac{N}{P} + \log N \right)\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\left(\frac{N}{P}\right)^{\alpha} + \frac{N}{P} \log N\right) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = \log x $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, 0 &lt; \alpha &lt; \frac{3}{2} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{3/2} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(x) = x^{\alpha}, \alpha &gt; \frac{3}{2} $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Matrix mult.</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N^{3}}{P^{3/2}} \log N + \frac{N^{3}}{P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\left(\frac{N^{2}}{P}\right)^{\alpha}\right) $</td></tr></table>
## Page 52

### (skipping UPMH from Alpern et al.)
## Page 53

## P-(R)UMH Sorting [Vitter & Nodine — SPAA 1991]


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Problem</td><td style='text-align: center; word-wrap: break-word;'>$ f(i) = 1 $</td><td style='text-align: center; word-wrap: break-word;'>$ f(i) = \frac{1}{i + 1} $</td><td style='text-align: center; word-wrap: break-word;'>$ f(i) = \frac{1}{\beta^{ci}}, c &gt; 0 $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Sorting</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P}\log N\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\frac{N}{P}\log N \cdot \log \frac{\log N}{\log P}\right) $</td><td style='text-align: center; word-wrap: break-word;'>$ \Theta\left(\left(\frac{N}{P}\right)^{1+\frac{c}{2}} + \frac{N}{P}\log N\right) $</td></tr></table>

<div style="text-align: center;"><img src="imgs/img_in_image_box_814_710_1348_1075.jpg" alt="Image" width="37%" /></div>

## Page 54

## Cache-Oblivious Model [Frigo, Leiserson, Prokop, Ramachandran — FOCS 1999]

• Analyze RAM algorithm (not knowing B or M) on external-memory model

■ Must work well for all B and M

<div style="text-align: center;"><img src="imgs/img_in_image_box_302_479_1117_1033.jpg" alt="Image" width="56%" /></div>

## Page 55

## Cache-Oblivious Model [Frigo, Leiserson, Prokop, Ramachandran — FOCS 1999]

• Automatic block transfers via LRU or FIFO

• Lose factor of 2 in M and number of transfers

■ Assume  $ T(B, 2M) \leq c T(B, M) $

<div style="text-align: center;"><img src="imgs/img_in_image_box_345_501_1184_1062.jpg" alt="Image" width="58%" /></div>

## Page 56

## Cache-Oblivious Model [Frigo, Leiserson, Prokop, Ramachandran — FOCS 1999]

• Clean model

- Adapts to changing B (e.g., disk tracks) and changing M (e.g., competing processes)

• Adapts to multilevel memory hierarchy (MH)

Assuming inclusion

<div style="text-align: center;"><img src="imgs/img_in_image_box_47_717_583_1048.jpg" alt="Image" width="37%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_591_691_1419_1059.jpg" alt="Image" width="57%" /></div>

## Page 57

## Scanning [Frigo, Leiserson, Prokop, Ramachandran — FOCS 1999]

• Visiting N elements in order costs  $ O\left(1+\frac{N}{B}\right) $ memory transfers

- More generally, can run $O(1)$ parallel scans

  - Assume $M \geq c$ $B$ for appropriate constant $c > 0$

- E.g., merge two lists in $O\left(\frac{N}{B}\right)$



<div style="text-align: center;"><img src="imgs/img_in_image_box_1128_623_1367_1066.jpg" alt="Image" width="16%" /></div>

## Page 58

## Cache Oblivious

• Prokop: cache-oblivious -> SUMH conversion

● Also obviously cache-oblivious -> external memory
## Page 59

## Searching [Prokop — Meng 1999]

<div style="text-align: center;"><img src="imgs/img_in_image_box_19_168_1426_574.jpg" alt="Image" width="97%" /></div>


"van Emde Boas layout"

<div style="text-align: center;"><img src="imgs/img_in_image_box_53_709_1310_1055.jpg" alt="Image" width="87%" /></div>

## Page 60

## Searching [Prokop — Meng 1999]

<div style="text-align: center;"><img src="imgs/img_in_image_box_12_167_1430_569.jpg" alt="Image" width="98%" /></div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_5_165_888_1078.jpg" alt="Image" width="61%" /></div>


 $$ \bullet \mathrm{height}(\Delta)\atop\geq\frac{1}{2}\lg B $$ 

- ≤ 2 memory transfers per △

• ≤ 4 log $ _{B} $ N total
## Page 61

## Cache-Oblivious Searching

•  $ \left(\lg e + o(1)\right)\log_B N $ is optimal

[Bender, Brodal, Fagerberg, Ge, He, Hu, Iacono, López-Ortiz — FOCS 2003]

• Dynamic B-tree in  $ O(\log_B N) $ per operation

[Bender, Demaine, Farach-Colton — FOCS 2000]

[Bender, Duan, Iacono, Wu — SODA 2002]



[Brodal, Fagerberg, Jacob — SODA 2002]

<div style="text-align: center;"><img src="imgs/img_in_image_box_509_692_1436_1075.jpg" alt="Image" width="64%" /></div>

## Page 62

## Cache-Oblivious Sorting

• $O\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right)$ possible, assuming $M\geq\Omega(B^{1+\varepsilon})$ (tall cache)

Funnel sort: mergesort analog

Distribution sort

[Frigo, Leiserson, Prokop, Ramachandran — FOCS 1999; Brodal & Fagerberg — ICALP 2002]

<div style="text-align: center;"><img src="imgs/img_in_image_box_844_439_1424_805.jpg" alt="Image" width="40%" /></div>


• Impossible without tall-cache assumption [Brodal & Fagerberg — STOC 2003]
## Page 63

Parallel Caching (Multicore), GPU, etc.
## Page 64

## ALA
## Page 65

###### http://courses.csail.mit.edu/6.851/

Lecture 7 in 6.851: Advance

← → ⓘ courses.csail.mit.edu/6.851/spring12/lectures/L07.html

### 6.851 : Advanced Data Structures (Spring'12)

madalgo

Prof.  $ \underline{\text{Erik Demaine}} $ TAs: Tom Morgan, Justin Zhang

CENTER FOR MASSIVE DATA ALGORITHMICS

[Home] [Lectures] [Assignments] [Project] [Problem Session] [Forum]

## Lecture 7 Video [previous] [next]

[+] Memory hierarchy: models, cache-oblivious B-trees  $ \underline{\text{Scribe Notes [src]}} $

<div style="text-align: center;"><img src="imgs/img_in_image_box_28_520_772_940.jpg" alt="Image" width="51%" /></div>


Lecture notes, page 5/9 • [previous page] • [next page] • [PDF]

Video times: • 36:42–43:10

Cache-oblivious static search trees:

(binary search) [Prokop-MEng 1999]

- store N elements in N-node complete BST

- carve tree at middle level of edges

⇒ one top piece, ≈√N bottom pieces, each size ≈√N

<div style="text-align: center;"><img src="imgs/img_in_image_box_832_783_1420_963.jpg" alt="Image" width="40%" /></div>

## Page 66

## Models, Models, Models


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Model</td><td style='text-align: center; word-wrap: break-word;'>Year</td><td style='text-align: center; word-wrap: break-word;'>Blocking</td><td style='text-align: center; word-wrap: break-word;'>Caching</td><td style='text-align: center; word-wrap: break-word;'>Levels</td><td style='text-align: center; word-wrap: break-word;'>Simple</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Idealized 2-level</td><td style='text-align: center; word-wrap: break-word;'>1972</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>✓</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Red-blue pebble</td><td style='text-align: center; word-wrap: break-word;'>1981</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>✓ -</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>External memory</td><td style='text-align: center; word-wrap: break-word;'>1987</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>✓</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>HMM</td><td style='text-align: center; word-wrap: break-word;'>1987</td><td style='text-align: center; word-wrap: break-word;'>✗</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>∞</td><td style='text-align: center; word-wrap: break-word;'>✓</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>BT</td><td style='text-align: center; word-wrap: break-word;'>1987</td><td style='text-align: center; word-wrap: break-word;'>~</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>∞</td><td style='text-align: center; word-wrap: break-word;'>✓ -</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(U)MH</td><td style='text-align: center; word-wrap: break-word;'>1990</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>∞</td><td style='text-align: center; word-wrap: break-word;'>✗</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Cache oblivious</td><td style='text-align: center; word-wrap: break-word;'>1999</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>✓</td><td style='text-align: center; word-wrap: break-word;'>2-∞</td><td style='text-align: center; word-wrap: break-word;'>✓ +</td></tr></table>
## Page 67

MIT OpenCourseWare http://ocw.mit.edu

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
