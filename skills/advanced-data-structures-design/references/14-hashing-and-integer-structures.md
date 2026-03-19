# Hashing and Integer Structures

Hashing schemes, predecessor search, van Emde Boas style structures, fusion trees, and lower bounds for integer problems.

## Included Lectures
- L10.md
- L11.md
- L12.md
- L13.md
- L14.md

---

## L10.md


## Page 1

TODAY: Hashing

- universal & k-wise independent

- simple tabulation hashing

- chaining & perfect hashing

- linear probing

- cuckoo hashing

Hash function: h: {0, 1, ..., u-1} → {0, 1, ..., m-1}

universe of keys table size

—Totally random:  $ \Pr\{h(x)=t\}^{2}=1/m $,

independent of  $ h(y) $ for all  $ x\neq y\in U $

— $ \bigcirc(u\lg m) $ bits of information —Too BIG

—“simple uniform hashing” of [CLRS]

- Universal: choose h from family H with

  Pr{h(x)=h(y)} = O(1/m) for all x ≠ y ∈ U

  heH

  C'strong if ≤ 1/m

  [Carter & Wegman - JCSS 1979]

  - h(x) = [(ax) mod p] mod m for O < a < p

or: vector dot product

  → prime ≥ u = |U|

  - h(x) = [(ax) mod u] // 2^{lgu - lg m} for odd a < 2^{w}

  = (a • x) ≃ (lgu - lg m) ↔ integer division m & u =

  ↑ right shift powers of 2

  [Dietzfelbinger, Hagerup, Katajainen, Penttonen - J.Alg.1997]
## Page 2

- k-wise independent: family of hash functions

with Pr{h(x₁)=t₁ &cdots & h(xₖ)=tₖ} = O(1/mᵖ)

for all distinct x₁, x₂, ..., xₖ ∈ U

[Weaman & Carter-JCSS 1981]

- pairwise  $ (k=2) $ is stronger than universal

-  $ h(x)=[(ax+b)\bmod p]\bmod m $ for  $ O<a<p $

-  $ h(x)=\left[\left(\sum_{i=0}^{k-1}a_{i}x^{i}\right)\bmod p\right]\bmod m $ for  $ O\leq b<p $

-  $ [WC81] $ and  $ O\leq a_{i}<p $

-  $ O(n^{2}) $ space,  $ f(k) $ query, uniform, & practical

- esp.  $ k=5 $ [thorup & Zhang-SODA2004]

-  $ O(n^{2}) $ space,  $ O(1) $ query for  $ k=0 $ (lgn)

- necessary for [Siegel-SICMP2004]

-Simple tabulation hashing: [WC81]

-view x as vector  $ x_{1}, x_{2}, \ldots, x_{c} $ of characters

-totally random hash table  $ T_{i} $ on each character

 $ \Rightarrow O(c u^{1/c}) $ words of space

 $ -h(x) = T_{1}(x_{1}) \oplus T_{2}(x_{2}) \oplus \cdots \oplus T_{c}(x_{c}) $

 $ \Rightarrow O(c) $ time to compute

-3-independent
## Page 3

u

<div style="text-align: center;"><img src="imgs/img_in_image_box_284_159_1003_336.jpg" alt="Image" width="58%" /></div>


$$-E[C_t=\text{length of chain}t]=\frac{\sum_{i}Pr\{h(x_i)=t\}}{}\$$

$$-universal\Rightarrow O(n/m)=O(1)\text{for}m=\Omega(n)$$

$$-Var[C_t]=E[C_t^2]-E[C_t]^2$$

$$-assuming h\text{is "symmetric":}$$

$$E[C_t^2]=\frac{1}{m}\sum_{i}E[C_i^2]=\frac{1}{m}\sum_{i,j}Pr\{h(x_i)=h(x_j)\}$$

$$-universal\Rightarrow=\frac{1}{m}\cdot n^2\cdot O(1/m)=O(n^2/m^2)$$

$$=O(1)\text{for}m=\Omega(n)$$

$$-tight\Rightarrow1-\frac{1}{n}c\text{for any}c$$

$$-totally\text{random}\Rightarrow C_t=O(\frac{\log n}{\log n})\text{with high probability}$$

$$-Pr\{C_t>c\cdot\mu\}\leq e^{\frac{(c-1)\mu}{(c\mu)}c\mu}\text{[Chernoff]}\$$

$$-c=\frac{\log n}{\log n}\Rightarrow\Pr\approx\frac{1}{O(\frac{\log n}{\log n})}\frac{O(\frac{\log n}{\log n})}{}\Rightarrow\frac{1}{n}O(1)$$

$$-\Theta(\frac{\log n}{\log n})-\text{wise independence}\Rightarrow\text{same}$$

$$[Schmidt, Siegel, Srinivasan-SIDMA1995]$$

$$-simple tabulation\mathbf{hashing}\Rightarrow\text{same}$$

$$[Patrascu\&Thorup-STOC2011]$$

$$-with "cache" of \Omega(\log n)\text{items, totally random}\Rightarrow$$

$$O(1)\text{amortized w.h.p.:}$$

$$-\Theta(\log n)\text{keys collide with "batch" of log n ops.whp.}$$

$$-\mu=\log n,\ c=\alpha\Rightarrow\Pr\leq e^{\log n}/(\alpha\log n)^{2\log n}<\frac{1}{n}c$$
## Page 4

EKS_perfect_hashing: [Fredman, Komlós, Szemeredi_J.ACM]

- store chain Ct as hash table of size  $ \Theta(C_{t}^{2}) $

 $ \Rightarrow $ 2-level hashing:

<div style="text-align: center;"><img src="imgs/img_in_image_box_172_229_1133_735.jpg" alt="Image" width="78%" /></div>


- E[# collisions in C_t table] = ∑_{i,j ∈ C_t}Pr{h(x_i) = h(x_j)}

- universal ⇒ = C_t^2 ⋅ O(1/C_t^2)

- set ⊖ constant to make ≤ 1/2

⇒ Pr{∅ collisions in C_t table} ≥ 1/2

⇒ O(1) expected trials to build collision-free C_k

- E[space] = ⊖(m + ∑_{i} C_t^2) = ⊖(m + n^2/m)

  = ⊖(n) for m = ⊖(n)

→ O(1) deterministic query

O(n) space { one in expectation

O(n) preprocessing }
## Page 5

Dynamic: [Dietzfelbinger, Karlin, Mehlhorn, Meyer auf der Heide, Rohnert, Tarjan – SICOMP 1994]

- maintain Ct table size  $ \epsilon[\frac{1}{4}, 4]\cdot c\cdot C_{t}^{2} $

- double/halve table if Ct changes a lot

- charge linear cost to linear # updates

- if space > c·n: rebuild entire table

- Pr {happening} = O( $ \frac{1}{n} $) [Markov]

⇒ expected O(1) cost per update

→ O(1) deterministic query

O(1) expected update → w.hip. possible!

O(n) space [Dietzelfinger & Meyer auf der Heide - 1990]

→ 10y. slower than memory access (Patrascu)

Linear probing: great cache perf.

- insert(x) puts x at first

    available slot  $ [h(x)+i] $ mod m  $ \times_2 $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \sqrt{ } $  $ \
## Page 6

Proof that totally random $h \Rightarrow O(1)$ expected

[Pagh, Pagh, Ružić - STOC 2007] (cf. Patrascu)

- totally random hash $h \Rightarrow balls$ in bins

- assume here $m = 3n$

- build perfect binary tree

on leaves = slots

- call node of height $h$ dangerous

if $>\frac{2}{3} \cdot 2^h = 2^M$ keys hash within node (via $h$)

- Pr $\{ > 2\mu \}$ ≤ e^$\mu$ / 2^2m = (e/4) 2^h/3 [Chernoff]

- consider run in table of length $\in [2^l, 2^{l+1})$

- look at nodes of height $h = l - 3$ spanning run

→ between 8 & 17 of them

- first 4 nodes span > 3·2^h slots of the run

- these keys must hash within the 4 nodes (via $h$)

- if nodes not dangerous: ≤ 4·$\frac{2}{3} \cdot 2^h = \frac{8}{3} \cdot 2^h$ keys hash within the nodes

⇒ ≥ 1 node dangerous

⇒ Pr {length of run ≥ x has length $\in [2^l, 2^{l+1})$}

≤ 17·Pr {node of height $l - 3$ is dangerous}

≤ 17·(e/4) 2^2/2^4

- E[length of run ≥ x] = ⊝ ($\sum_{i=1}^{i} 2^i \cdot Pr \{len. \in [2^l, 2^{l+1})\}$)

= ⊝ (1) 1/doubly exponential

- cache of lg^{1+ε} n ⇒ O(1) amortized w.h.p. [Pat11]

- for batch of lg^{1+ε} n, E[# dangerous @ height $h] = lg^{1+ε} n / c^{2^h}$

<div style="text-align: center;"><img src="imgs/img_in_image_box_736_240_1204_405.jpg" alt="Image" width="38%" /></div>


- cache of  $ \lg^{1+\varepsilon}n \Rightarrow O(1) $ amortized w.h.p. [Pat11]

- for batch of  $ \lg^{1+\varepsilon}n_{n}E[\#dangerous@height h] = \lg^{1+\varepsilon}n/c^{2^{h}} $

⇒ for  $ h \leq \lg \lg n_{n} \odot (\text{that}) $ w.h.p. i  $ h > \lg \lg n \Rightarrow \text{not dang.w.h.p.} $
## Page 7

Cuckoo hashing: [Pagh & Rodler–J.Alg.]

- 2 tables of size  $ m \geq (1 + \varepsilon) \cdot n $

- 2 hash functions  $ (g \rightarrow A, h \rightarrow B) $

- query(x): check A[g(x)] & B[h(x)]

- insert(x): put in A[g(x)] or B[h(x)]

- if kicked out y from A[g(y)]:

  move to B[h(y)]

A B

think of as

bipartite

graph2



<div style="text-align: center;"><img src="imgs/img_in_image_box_873_9_1148_228.jpg" alt="Image" width="22%" /></div>


- etc.

- if stuck: rehash entire structure

 $ -\left(2+\varepsilon\right)n $ space

 $ -\lambda $ deterministic probes for query

- fully random or  $ \Theta(\lg n) $-wise independence  $ \Rightarrow $

   $ \Theta(1) $ expected update \&  $ \Theta(1/n) $ failure prob. [PRO4]

   $ \Rightarrow $ construction on n keys

- Some 6-wise independent hash functions fail w.h.p.

even if  $ m = n^{1 + \varepsilon} $ [Cohen & Kame - manuscript 2009]

- Simple tabulation hashing  $ \Rightarrow $ fail with prob. $ \Theta(n^{1/3}) $

 $ \Rightarrow \Theta(n^{4/3}) $ inserts OK [Patrascu & Thorup - STOC 2011]
## Page 8

Proof that totally random hash functions  $ \Rightarrow $ Pr{follow a path of length  $ k\}, \leq 1/2^{k} $ [PT11] [Patrascu - blog, Feb. 2, 2010]

assume m = 2n

implied by existence of

encoding of g&h in 2nlgm-k bits:

- does path start in A or B? 1 bit

- slots of nodes along path: (k+1)lgm bits

- keys of edges along path: (k-1)lgm bits

- rest of g&h: (n-k)2lgm bits

- total:

 $ 2n\lg m - k + O(\lg k) $ bits  $ \frac{1\text{ bit}}{\text{Savings}} $

similar proofs for cycles a etc.
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L11.md


## Page 1

TODAY: Integers & van Emde Boas

- models: word RAM & cell probe

- predecessor problem

- van Emde Boas DS

- y-fast trees

Models for integer data structures:

- word = w-bit integer ∈ {0, 1, ..., u-1}

  ↑ all elements: inputs, outputs, ...

- transdichotomous RAM (Random Access Machine):

  - memory = array of S words

  - operations read/write O(1) words

  - words serve as pointers

  ⇒ w ≥ lg S

  - in particular w ≥ lg n machine/problem

- word RAM: transdichotomous RAM

  with C-style operations: [], cell probe

  + _ _ * _ / _ % _ < _ > _ & _ l _ ^ _ ^ < _ > _

  - standard model

- cell probe: count # memory reads & writes

  - computation is free

  - unrealistic

  - useful for lower bounds

STRONG

word RAM

pointer machine

BST WEAR
## Page 2

Predecessor problem: maintain set S of n words

subject to -insert(x∈U)

-delete(x∈S)

-predecessor(x∈U): max{y∈S|y<x}

-successor(x∈U): min{y∈S|y>x}

-harder than dictionaries/hashing

-comparison model  $ \Rightarrow $ BST:  $ \Theta(\lg n)/\mathrm{op} $. optimal

- word RAM:

 $ \begin{cases}

- van Emde Boas: & O(\lg w) / op. & \Theta(u) space \\

[Focs 1975; IPL 1977] & O(\lg w) w.h.p. & \Theta(n) space \\

- y-fast trees: & O(\lg w) w.h.p. & \Theta(n) space \\

[Willard-IPL 1983]

\end{cases} $

L12  $ \xi $- fusion trees: & O( $ \log_w n $) whip. & \Theta(n) space

[Fredman & Willard-JCSS 1993: Raman-ESA 1996]

L13  $ \Rightarrow $ - min: &  $ \leq O(\sqrt{\lg n}) w.h.p. $ & \Theta(n) space

- cell probe lower bound: &  $ \Omega(\min\{\log_w n, \frac{\lg w}{\lg w} \geq \frac{\lg w}{\lg w}\}) \Rightarrow $ vEB optimal for w=O( $ \log_w n $) & fusion trees optimal for w=2

- pointer machine, word specified by node pointer;

- van Emde Boas: O(lg(u)/op. O(u) space

- lower bound: S(lg(u)/op. S(u) space

[Mehlhorn, Näher, Alt-S1comp1988]
## Page 3

van Emde Boas: (Peter) (reinterpreted by Bender

- idea:  $ T(u) = T(\sqrt{u}) + O(1) $ & Farach-Colton)

- split universe  $ u $ into

 $ \sqrt{u} $ clusters, each size  $ \sqrt{u} $

- hierarchical coordinates: word  $ x = \langle c, i \rangle $

-  $ c = x // \sqrt{u} = \text{cluster containing } x $

-  $ i = x \uparrow \% \sqrt{u} = x's \text{ index within cluster} $

- integer division  $ \uparrow \mod $

-  $ x = c \sqrt{u} + i \Rightarrow O(1) - \text{time conversion} $

- binary perspective:

  - split bits in half

  - c = high order = x  $ \gg $ w/2

  - i = low order = x  $ \&((1 \ll w/2) - 1) $

  - x = (c  $ \ll $ w/2) | i

  -  $ \sqrt{\frac{w}{2}} $

- recursive vEB V of size u: cluster cluster cluster

- V.cluster[i] = vEB of size ∫u for O≤i<∫u

- V.summary = vEB of size ∫u &w' = w/2

- stores which clusters c are nonempty

- V.min = minimum element in V, not stored recursively

OR None if V is empty

- V.max = (copy of) max. element in V
## Page 4

Successor  $ (V_{a}x = (c_{a}i)) $:

- if  $ x < V_{min} $: return  $ V_{min} $ (special: not stored recursively)

- if  $ i < V_{cluster}[c] $. max:

    return  $ (c_{a} Successor(V_{a} cluster[c], i)) $

- else:  $ c' = Successor(V_{a} summary, c) $

    return  $ (c', V_{a} cluster[c']_{min}) $

Insert(V₁, x = <c, i>):

- if V₁,min = None: V₁,min = V₁,max = x; return

- if x < V₁,min: swap x ↔ V₁,min

- if x > V₁,max: V₁,max = x

- if V₁,cluster[c].min = None:

  Insert(V₁, summary, c) ⇒ next call is 0(1)

- Insert(V₁, cluster[c], i)

Delete(V₁, x = <c, i>):

- if x = V₁,min:

  - c = V₁,summary,min

  - if c = None: V₁,min = None; return

  - x = V₁,min = <c,i = V₁,cluster[c],min> (unstore new min)

- Delete(V₁,cluster[c], i)

- if V₁,cluster[c],min = None: (empty now)

  Delete(V₁,summary,c) ⇒ previous call 0(1)

- if V₁,summary,min = None: V₁,max = V₁,min

  - else: c' = V₁,summary,max

  V₁,max = <c',V₁,cluster[c],max>
## Page 5

Tree view: expand recursion [VEB-FOCS 1975]

[van Emde Boas, Kaas, Zijlstra-Math.Sys.Th.1977]

Summary 1

Summary bits → 1 0 1 1 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

- node = OR of children

⇒ path from leaf × to root is monotone

⇒ could binary search for 0→1 transition

- max/min of last 0's left/right sibling

is predecessor/successor of × (if ∅ S)

- store sorted linked list on elements

to find successor/predecessor

⇒ query in O(lg lg u) ~ roughly same as above

-even in pointer machine & O(ulg w) space:

node stores linked list of pointers to

ancestor of height  $ 2^{i} $ for  $ i=0,1,\ldots,lg w $

- but updating these bits costs ☹(lg u)/op.

- vEB's not-storing-min reduces to ☹(lg w)

- again possible on pointer machine

with O(u/g w) space [VEBKZ77]
## Page 6

[Indirection: (trick from [Willard - IPL 1983])

- take O(lg w) query. O(w) update DS

such as "simple" tree above

- reduce update to O(lg w):

split n elements into chunks of size O(w)

one representative

 $ \Theta(\omega) $  $ \Theta(\omega)\cdots\Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega) $  $ \Theta(\omega)\

- query: query top → O(lg ω)

    query bottom → O(lg ω)

- update: update bottom → O(lg ω)

    split & possibly merge with neighbor

        to keep chunks ⊝(ω) size

        ⇒ update top → O(ω) n charged

        to ⊙(ω) updates in chunk

⇒ O(lg ω) query & amortized update

- top structure can actually use  $ u' = u / \theta(\omega) $:

  bottoms can guarantee separation  $ \Omega(\omega) $

  between representatives

   $ \Rightarrow \Theta(\omega) $ space ~ on pointer machine!

  - similar trick, splitting u directly instead of n, applied to stratified trees in [VEB-IPL1977]
## Page 7

Saving space: [Bender, Demaine, Farach-Colton?.]

- start from VEB

- don't store empty clusters

⇒ V.clusters = hash table

- ⊝(1) w.h.p. e.g. via dynamic perfect hashing

- space = O(# nonempty "child" clusters+1)

- charge each table entry to min in child

⇒ each element charged once

⇒ O(n) space

x-fast trees: [Willard-IPL 1983]

- don't store 0s in simple tree view

- store hash table of root-to-1 paths

or one per length viewed in binary: 0=left, 1=right

(as in Willard) i.e. prefixes of elements in S

- 0(lg w) query via binary search as before

- 0(w) update as before

- 0(n w) space

y-fast trees: [Willard-IPL 1983]

- x-fast trees + indirection as above

- O(lg ω) query still

- O(lg ω) amortized update

- O(n) space

 $ \theta(\omega) $  $ \theta(\omega) $  $ \cdots $  $ \theta(\omega) $
## Page 8

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L12.md


## Page 1

TODAY: Fusion trees

- sketch & why it's enough

- approximate sketch via multiplication

- parallel comparison

- most significant set bit

1 year after "cold debacle

Fusion trees: [Fredman & Willard - JCSS 1993]

- store n w-bit integers - here, statically

- O(logₙ n) time for predecessor/successor

- O(n) space

- word RAM

⇒ predecessor ≤ min{logₙ n, logₙ}

≤√log n

- AC∅ RAM version [Andersson, Mültersen, Thorup-TCS 1999]

→ ops. are constant-depth (unbounded fan) circuits

⇒ no multiplication

- dynamic version via exponential trees:

O(log₂ n + lg lg u) deterministic updates

[Andersson & Thorup - JACM 2007]

- dynamic version via hashing: [Raman-ESA 1996]

O(logw n) expected updates

-OPEN:  $ O(\log_{w}n) $ w.h.p. updates?
## Page 2

Idea: B-tree with branching factor  $ \Theta(\omega^{1/5}) $

 $ \Rightarrow $ height =  $ \Theta(\log_{w} n) $

 $ \Rightarrow $  $ \Theta(\log_{n}/\log_{w}) $

- search must visit a node in O(1) time

- not enough time to read the node

(w¹/⁵ w-bit words) to figure out which child

Fusion-tree node:

- store  $ k = O(\omega^{1/5}) $ keys  $ x_{0} < x_{1} < \cdots < x_{k-1} $

-  $ O(1) $ time for predecessor/successor

-  $ k^{0}(1) $ preprocessing
## Page 3

Distinguishing  $  k = O(\omega^{1/5})  $ keys:

- view keys  $  x_0, x_1, \ldots, x_{k-1}  $ as binary strings  $  \left( \frac{1}{2} \right)  $

i.e. root-to-leaf paths in height-w binary tree (left/right)

 $ \Rightarrow k-1 $ branching nodes

 $ \Rightarrow \leq k-1 $ levels

containing branching nodes

i.e. bits where  $  x_0 \sim x_{1n} \ldots \sim x_{k-1}  $ first differ

(first distinct prefix)

- call these important bits  $  b_0 < b_1 < \ldots < b_{r-1}  $

<div style="text-align: center;"><img src="imgs/img_in_image_box_839_203_1199_454.jpg" alt="Image" width="29%" /></div>


(perfect) sketch(x) = extract bits  $ b_{0}, b_{1}, \ldots, b_{r-1} $ from x

i.e. r-bit vector whose ith bit = b_i, b_j of word x

⇒ sketch( $ x_0 $) < sketch( $ x_1 $) < ... < sketch( $ x_{k-1} $)

& can pack (fuse) into one word:  $ k \cdot r = O(\omega^{2/5}) $ bits

- computable in O(1) time as AC^0 operation

[Andersson, Miltersen, Thorup - TCS 1999]

- we'll see a cool way to compute approximate sketch using multiplication & standard ops.

Node search: for query q, compare sketch(q)

in parallel to sketch(x₀), ..., sketch(xₖ-1)

- again AC⁰ operation on O(1) words

& we'll see a nice way with standard ops.

⇒ find where sketch(q) fits among sketch(x₀) < ... < sketch(xₖ₋₁)

- want where q fits among x₀ < ... < xₖ₋₁
## Page 4

\underline{Desketchifying:

<div style="text-align: center;"><img src="imgs/img_in_image_box_174_132_1166_558.jpg" alt="Image" width="81%" /></div>


sketch:

 $ \underline{\text{0000}} $  $ \underline{\text{0010}} $  $ q=\underline{\text{0101}} $

 $ \underline{\text{00}} $ 01 00



- suppose sketch(x₁)≤sketch(q)＜sketch(x₁+1)

- longest common prefix = lowest common ancestor

between q & (either x₁ or x₁+1)

wnsketch

= node y where q fell off paths to x₁'s

- if lyl+1st bit of q is 1:

  - nearest x₁ is in y0 subtree

  - nearest extreme in that

  - subtree is e=y011-1

<div style="text-align: center;"><img src="imgs/img_in_image_box_833_909_1213_1352.jpg" alt="Image" width="31%" /></div>


- else: e = y100...0

predecessor & successor of q among  $ x_{i}^{'s} $

predecessor & successor of sketch(e) among sketch( $ x_{i}^{'s} $)

(in terms of rank i ~ can translate to  $ x_{i} $)
## Page 5

Approximate sketch(x): on word RAM

- don't need sketch to pack bi bits consecutively

- can spread out in predictable pattern of length O(w^{4/5})

Idea: mask important bits:  $ x' = x \text{ AND } \sum_{i=0}^{v-1} 2^{bi} $

& multiply  $ x'\cdot m = \left(\sum_{i=0}^{v-1} x_{b_i} 2^{bi}\right) \cdot \left(\sum_{j=0}^{v-1} 2^{mj}\right) $

&=\sum_{i=0}^{v-1} \sum_{j=0}^{v-1} x_{b_i} 2^{b_i + m_j} $

Claim: for any  $ b_{0}, b_{1}, \ldots, b_{r-1} $, can choose  $ m_{0}, m_{1}, \ldots, m_{r-1} $ such that  $ \textcircled{a} b_{i} + m_{j} $ are all distinct (no collision)

 $ \textcircled{b} b_{0} + m_{0} < \cdots < b_{r-1} + m_{r-1} $ (preserve order)

 $ \textcircled{c} (b_{r-1} + m_{r-1}) - (b_{0} + m_{0}) = O(r^{4}) = O(w^{4/5}) $ (small)

 $ \Rightarrow $ approx-sketch  $ (x) = \left[(x \cdot m) \text{ AND } \sum_{i=0}^{r-1} 2^{b_{i} + m_{i}}\right] \gg (b_{0} + m_{0}) $

Proof: ① choose  $ m_{0}^{\prime}, m_{1}^{\prime}, \ldots, m_{r-1}^{\prime} < r^{3} $ such that  $ b_{i} + m_{j}^{\prime} $ are all distinct modulo  $ r^{3} $ (strong a)

- pick  $ m_{0}^{\prime}, m_{1}^{\prime}, \ldots, m_{r-1}^{\prime} $ by induction

-  $ m_{t}^{\prime} $ must avoid  $ m_{i}^{\prime} + b_{j} - b_{k} $  $ \forall i, j, k $

 $ \Rightarrow $ choice for  $ m_{t}^{\prime} $ exists

② Let  $ m_{i}=m_{i}^{\prime}+(\omega-b_{i}+i r^{3} $ rounded down to mult. of  $ r^{3} $

 $ \equiv m_{i}^{\prime} $ (mod  $ r^{3} $)

 $ \Rightarrow m_{i}+b_{i} $ in  $ r^{3} $ interval after  $ \left(\left[\frac{\omega}{r^{3}}\right]+i\right)\cdot r^{3} $

 $ \Rightarrow m_{0}+b_{0}<\cdots<\underbrace{m_{r-1}+b_{r-1}}_{} \textcircled{6} $
## Page 6

Parallel comparison: protect from underflow

- sketch(node) = ① sketch(x₀) … 1 sketch(xₖ₋₁)

- sketch(g)ᵣ = ○ sketch(g) … ○ sketch(g)

  = sketch(g) • ○ 00001 … ○ 00001

- difference = (1/0) ****** * … (1/0) ****** *

- AND with 1 00000 … 1 00000

  → (1/0) 00000 … (1/0) 00000

1 if sketch(q) ≤ sketch(x_i)

0 if sketch(q) > sketch(x_i)

→ these bits look like 0000①11 where sketch(q) fits

- multiply with ○ 00001 … ○ 00001

→ #1's ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ 

⇒ AND with 1111 & shift right to get # 1's

= index of ∅→1 transition

= k-rank in sketch world

- special case of:

Index of most significant 1 bit: 00010110 → 4

- AC $ ^{\circ} $ operation [Andersson, Miltersen, Thorup 1999]

- instruction on most modern CPUs

(see Linux kernel: include/asm-*/bitops.h; GCC: --builtin_clz; VC++: _BitScanReverse)

- needed during desketchifying (q xor xi(+1))
## Page 7

Word RAM solution: [Fredman & Willard 1993]

- split word into √W clusters of √W bits each:

     $ x = 0101 \quad | 0000 \quad | 1000 \quad | 1101 \quad \leftarrow \sqrt{w} \rightarrow \leftarrow \sqrt{w} \rightarrow \leftarrow \sqrt{w} \rightarrow $

## $\sqrt{w}$

- similar to van Emde Boas, but no recursion

- identify first nonempty cluster, then first 1 within

① identify nonempty clusters

- AND x with F = 1000 1000 1000 1000

→ 0000 0000 1000 1000

= which clusters have first bit set

- XOR with x → 0101 0000 0000 0101

= remaining bits

- subtract F - this: 0*** 1000 1000 0***

    borrow ↔ nonempty ↔ no borrow ↔ subtract ↔

- AND with F → 0000 1000 1000 0000

- XOR with F → 1000 0000 0000 1000

## empty

→ OR with which clusters have first bit set

→ y=1000 0000 1000 1000

= which clusters are nonempty
## Page 8

② perfect sketch of y → 1011

-  $ b_{i} = \sqrt{w} - 1 + i\sqrt{w} $

- use  $ m_{j} = w - (\sqrt{w} - 1) - j\sqrt{w} + j $

 $ \Rightarrow b_{i} + m_{j} = w + (i - j)\sqrt{w} + j $ are unique for  $ 0 \leq i, j < \sqrt{w} $

 $ \& b_{i} + m_{i} = w + i $

 $ \Rightarrow $ bits  $ w_{n} w + 1_{n}, \ldots, w + \sqrt{w} - 1 $ of  $ y \cdot m $

(shifted right w) form perfect-sketch(y)

③ find first 1 bit in sketch(y)

= first nonempty cluster c

- use parallel comparison

  to find rank among:

  {

    0001

    0010

    0100

    1000

  }

  of 2

- fits:  $ \sqrt{w} \cdot (\sqrt{w} + 1) < 2w $ bits

④ find first 1 bit d in identified cluster c

- shift right c. √W & AND with 1111

  to obtain cluster

- use parallel comparison as in ③

⑤ answer = c√ω + d
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L13.md


## Page 1

TODAY: Predecessor lower bounds

- history/survey

- communication complexity

  perspective of a data structure

- round elimination

-  $ \Omega(\min\{\frac{\lg w}{\log n}, \log w n\}) $ proof

(for polynomial space DS)

- information theory for very briefly round elimination lemma covered in class
## Page 2

Predecessor lower bounds:

[Ajtai-Combinatorica 1988]

- first w(1) bound: complicated (accidental claim)

- ∀w ∃n s.t. Ω(∫lg w) (of Ω(lg w))

[Miltersen-Stoc 1994]

- better understanding of "same" proof

- connection to communication complexity

- ∀w∃n s.t. Ω(∫lgω)

- ∀n ∃w s.t. Ω(3/∫lg n)

[Miltersen, Nisan, Safra, Wigderson-STOC 1995 & JCSS 1998]

- round elimination proof ~clean

- introduction of round elim. technique

[Beame & Fich - STOC 1999 & JCSS 2002 & manuscript 1994]

-  $ \forall w \exists n \text{ s.t. } \Omega\left(\frac{\log w}{\log w}\right) $ complicated

-  $ \forall n \exists w \text{ s.t. } \Omega\left(\sqrt{\frac{\log n}{\log n}}\right) $ complicated

- static DS achieving  $ \bigcirc(\min\{\frac{\log w}{\log \lg w} \sqrt{\frac{\log n}{\log \lg n}}\}) $

 $ \Rightarrow \text{best "pure" bounds in } n \& w $

[Xiao - Ph.D. thesis 1992 @ U.C. San Diego] <Citation>

- Same lower bounds! (still complicated)

- Beame & Fich was independent discovery
## Page 3

[Sen - CCC 2003: Sen & Venkatesh - JCSS 2006]

- round elimination proof ~ clean TODAY

(Patrascu & Thorup - STOC 2006; SODA 2007)

- fight n vs. w vs. space trade-off: (static)

 $ \log\left(\frac{\ln\frac{w}{a}}{\ln\frac{a}{a}}\right) $

- O(n polylg n) space ⇒ θ(min {log w n, lg (log w n)}

⇒ van Emde Boas is optimal for w = O(polylg n) & fusion trees optimal for lg w = ∑(lg n lg lg n)

Colored predecessor problem:

- each element is colored red or blue

- predecessor/succ. query just needs to return color

- easier problem → stronger lower bound

- useful for reductions later
## Page 4

Communication complexity  $ \underline{\text{viewpoint}} $

 $ \pi\# address bits = \lg(space) $

Alice  $ \xrightarrow{query\ a.g.} $  $ \xrightarrow{msgs. \leq a\ bits} $ Bob  $ \xrightarrow{memory} $ goal: knows x  $ \xleftarrow{msgs. \leq b\ bits} $ knows y  $ \xleftarrow{f(x,y)} $ query data structure color

- # messages = 2 · # cell probes (LOADs from memory)

Claim:  $ \Omega(\min\{\log_a w, \log_b n\}) $

 $ \Rightarrow \Omega(\min\{\frac{\log_w}{\log_b n}, \frac{\log_w n\}}{\sim vEB}, \text{fusion} \quad (\text{e.g. poly(n) space}) $

Corollary: Beame-Fich-Xiao pure bound

- assume a = O(lg n) (polynomial space)

- lower bound largest when

log a w = log b n

i.e.  $ \frac{lg w}{lg lgn} = \frac{lg n}{lg w} $ (up to ②)

i.e.  $ \log^2 w = \lg n - \lg lgn \Rightarrow \lg lgn w = \lg lgn $

i.e.  $ \lg w = \sqrt{\lg n \cdot \lg lgn} $

 $ \Rightarrow $ lower bound is  $ \frac{\lg w}{\lg g n}=\sqrt{\frac{\lg n}{\lg g n}}=\frac{\lg w}{\lg g n} $
## Page 5

Round elimination:

 $ f^{(k)} $: variation on problem f

- Alice has k inputs  $ x_{1}, x_{2}, \ldots, x_{k} $

- Bob has input y & integer  $ i \in \{1, 2, \ldots, k\} $

& already knows  $ x_{1}, x_{2}, \ldots, x_{i-1} $

- goal: compute  $ f(x_{i}, y) $

Intuition: first message sent by Alice nearly useless if a bits << k inputs (don't know i)

→ should eliminate first message &

start communication protocol from second msg.

- apply to Bob→Alice direction ⇒ eliminate round

Round elimination lemma:

if ∃protocol for f^{(k)} where Alice speaks first

using m messages & error probability S

then ∃protocol for f where Bob speaks first

using m-1 messages & error probability S+O(√∂/∂k)

Intuition: if i were chosen uniformly at random then expect  $ \frac{a}{k} $ bits to be "about"  $ x_{i} $

- Bob can guess these bits randomly

- Pr{correct guess} = 1/2^{a/k}

⇒ error increase = 1 -  $ \frac{1}{2} $^{a/k} (union bound)

≈ a/k (1 -  $ \frac{1}{2} $e^{x} ≈ x)

- correct bound is  $ \sqrt[k]{a/k} $ (proof below)
## Page 6

Proof of predecessor lower bound:

- let $t = \#$ cell probes (rounds) for predecessor

- goal: $t$ round eliminations

$\Rightarrow$ remaining protocol has no messages

$\Rightarrow$ answer must be guessed (if $n' \geq 2$)

$\Rightarrow$ Pr{success} $\leq$ 1/2

- get contradiction if error < 1/2 (t small)

① eliminate message from Alice to Bob:

- Alice's input has $w'$ bits (initially $w$)

- break into $k = \Theta(at^2)$ equal-size chunks:

  $x_1, x_2, \ldots, x_k$

$\Rightarrow$ error increase will be $\mathcal{O}(\sqrt{\frac{a}{a+2}}) = \mathcal{O}(1/t)$

- constrain $n'$ elements to all differ in $i$th chunk

- only Bob knows $i$

- Bob also knows common

  prefix of all elements $\Theta(at^2)$

  $(x_1, x_2, \ldots, x_{i-1})$

- goal: query $x_i$ in DS $y$ for $i$th chunk

$\Rightarrow$ elimination reduces $w' \rightarrow \Theta(w' / at^2)$



<div style="text-align: center;"><img src="imgs/img_in_image_box_874_864_1167_1074.jpg" alt="Image" width="23%" /></div>


ANALOGY: van Emde Boas binary searches

on levels to find longest prefix match,

reducing w as it goes
## Page 7

② eliminate message from Bob to Alice

- Bob's input is n' integers of w' bits each

- divide integers into  $ k = \Theta(bt^2) $ equal chunks

⇒ error increase will be  $ \Delta(1/t) $

- constrain input so that ith chunk  $ x_i $ starts with prefix "i" in binary

- only Alice knows i: which  $ x_i $ contains query (prefix "i")

- goal: search for query in  $ x_i $

⇒ elimination reduces  $ n' \rightarrow \Theta(n' / 6t^2) $

 $ w' \rightarrow w' - \log(6t^2) $

ANALOGY: fusion trees branch by polynomial factor in w, reducing n

- round elimination reduces  $ w' \rightarrow \Theta(w\% at^{2}) $

 $ n' \rightarrow \Theta(n\% at^{2}) $

- t-round error ≤ 1/3 if set constants right

- stop when w' hits log b or when n' hits 2

⇒ t = Ω (min { log at 2 wn log at 2 n})

because  $  t = 0 (\lg n)  $ and  $  \log n  $

 $  = \Omega (\min \{\log a, w_1, \log b, n\})  $
## Page 8

Information-theory basics:

 $ -H(x) = \frac{1}{x_0} \frac{1}{x_0} = \frac{\sum_{x_0} \Pr\{x = x_0\}}{\log \frac{1}{Pr\{x = x_0\}}} = \frac{1}{x_0} $

-H(xly)=entropy of x given y  

=#bits to represent x if you know y  

=Ey_{0}[H(xly=y_{0})]

propagate into Pr's

- I(x:y) = shared information between x&y = H(x) + H(y) - H((x,y))

- I(x:y|z) = E_{z_0} [I(x:y|z=z_0)]

propagate into H's
## Page 9

Proof sketch of round elimination lemma:

- call Alice's first message  $ m = m(x_{1}, \ldots, x_{K}) $

-  $ a = |m| \geq H(m) = \sum_{i=1}^{k} I(x_{i}; m) x_{1}, \ldots, x_{i-1}) $

- "chain rule for information"

- if i is distributed uniformly

then  $ E_{i}\left[\left[I(x_{i}:m)\mid x_{1},\ldots,x_{i-1}\right]\right]=\text{average term in sum} $

 $ \leq H(m)/k \leq a/k $

- intuition: Bob knows  $ x_{1}, \ldots, x_{i-1} $ & receives m

 $ \Rightarrow $ learnus  $ I(x_{i}:m) $ about  $ x_{i} $

- build protocol for  $ f(x) $ as follows:

  - fix  $ x_{1}, \ldots, x_{i-1} $ & i randomly in advance

  - now query x comes along

  - set  $ x_{i}=x $

  - run  $ f^{(k)} $ protocol, starting at second message, assuming first message  $ m=m(x_{1}, \ldots, x_{i-1}, \tilde{x}_{i}, \ldots, \tilde{x}_{k}) $

  - chosen uniformly by Bob

- guess  $ I(x_{i}:m) $ correctly with probability  $ \approx a/k $

- Average Encoding Theorem:

  with probability  $ \geq \sqrt[n]{a/k} $,

   $ 3x_{i+1}, \ldots, x_{k} $ such that  $ m(x_{1}, \ldots, x_{i-1}, \tilde{x}_{i}, \ldots, \tilde{x}_{k}) $

   $ 8m(x_{1}, \ldots, x_{k}) $

  distributed roughly the same

   $ (\Rightarrow \text{error probability } S \text{ preserved}) $
## Page 10

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L14.md


## Page 1

Today: Integer sorting & priority queues

- reduction between them

- survey of sorts

- signature sort: O(n) for w = Ω(lg² + ε n)

- packed sort: O(n) for w = Ω(b lg n lg lg n)

- bits in input integers

- bitonic sort for merging sorted words

Priority_queues:

- O(P(n,w)) priority queue ⇒ O(n P(n,w)) sort

[trivial]

- O(n S(n,w)) sorting algorithm ⇒ [Thorup-J.ACM 2007]

O(S(n,w)) worst-case priority queue

insert_delete_find-min

- O(P(n,w)) priority queue ⇒ [Mendelson, Tarjan,Thorup, Zwick-TALG 2006]

O(P(n,w)+α(n)) melldable priority queue

merge two queues in O(1) am.

OPEN:  $ O(nS(n,w)) $ sorting alg.  $ \Rightarrow $  $ O(S(n,w)) $ delete-min &  $ O(1) $ decrease-key & insert?

Demaine & Patrascu

2005


## Page 2

Integer sorting: sort n w-bit integers

- comparison sort:

- counting sort:

- radio sort:

 $ O(n \lg n) $

 $ O(n+u) $

 $ = O(n) $ for  $ w = \lg n $

 $ O(n \frac{w}{\lg n}) $

 $ = O(n) $ for  $ w = O(\lg n) $



-with more care:

* signature sort:

 $ t_{1} \quad O(n \lg w) $

 $ = O(n \lg \ln n) \quad \text{for } w = \lg^{0(1)} n $

 $ O(n \lg \frac{w}{\lg n}) \quad \text{[Spring'05, PS7]} $

 $ O(n) \quad \text{for } w = \Omega(\lg^{2+\varepsilon} n) \forall \varepsilon > 0 $

 $ O(n \lg \ln n) \quad \text{for all } w $

[Andersson, Hagerup, Nilsson, Rahman-JCSS 1998]

- note: much better than "fusion sort" O(n log w)

- Han [J. Alg. 2001]: O(n log w) deterministic AC

- Han & Thorup [Focs 2002]: O(n√lg w/g) randomized

= O(n√lg g n) for w=lg 0(1) n

⇒ O(n√lg g n) for all w

OPEN: optimal sorting for  $ w = w(\lg n)  $ &  $ o(\lg^{2} + \varepsilon n) $
## Page 3

Signature sort: [Andersson et al. 1998]

- assume w ≥ lg² + £ n · lg lg n (change £)

① break each integer into lg £ n equal-size chunks

② replace each chunk by O(lg n) - bit hash

⇒ n O(lg 1 + £ n) - bit signatures "signature"

- need to be able to hash lg £ n chunks in O(1)

- e.g. multiplication method:

  - just need adjacent blanks

    to prevent overflow collision mask

- so mask & do odds & events separately,

    then OR together

- can compactify via sketch techniques [112]

③ packed sorting sorts them in O(n) time:

n b-bit integers with w=52(b lgn lglgn)

- trouble; hash does not preserve order

④ build compressed trie of sorted signatures:

<div style="text-align: center;"><img src="imgs/img_in_image_box_32_1072_1191_1576.jpg" alt="Image" width="94%" /></div>

## Page 4

Building compressed trie in O(n) time:

(like suffix array→tree conversion [L16])

- for i=1,2n...,n: add ith signature

- compute lcp with (i-1)st signature:

  first 1 bit in XOR (like fusion trees)

  rounded to chunk #

- walk up to appropriate node/compressed edge

- charge distance walked to decrease in

  rightmost path length (potential)

- add new branch from lca/lcp - O(1)

## new OR new

$\Rightarrow O(n)$ total time

~or notice you're just doing an in-order

traversal of the tree to be computed

⑤ recursively sort (node ID, actual chunk, edge index)

Vedge O(lg n) bits w/lg ε n bits O(lg n) bits

⇒ n remains same, b reduces to b/lg ε n + O(lg n)

# bits in an integer

⇒ after  $  \frac{1}{\varepsilon} + 1 = O(1)  $ recursions,

 $  b = O(\lg n + \frac{w}{\lg^{1+\varepsilon}n}) = O(\frac{w}{\lg^{1+\varepsilon}n}) = O(\frac{w}{\lg n \lg \lg n})  $

⇒ packed sort in base case

⑥ scan through & permute each node accordingly

⑦ in-order traversal of leaves
## Page 5

Packed sorting:  $ w \geq 2(b+1) \lg n \lg \lg n $ (for convenience)

⑧ pack lg n lg  $ \lg n $ elements into each word:

 $ \begin{array}{c}

\emptyset - \emptyset - \emptyset - \emptyset \text{elt.} \emptyset \text{elt.} \emptyset \text{elt.} \\

1 \leftarrow b \rightarrow \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \cdots \

① merge pair of sorted words with  $ k \leq \lg n \lg n $ elts. into one sorted word with  $ 2k $ elts. in  $ O(\lg k) $ time -hardest step (To Do) -bitonic sorting + bit tricks

② mergesort k = lg n lg lg n elts, into one word in T(k) = 2T(k/2) + O(lg k)

= O(k) time

O(lg k) ~geometric increase

③ merge two sorted lists of r sorted words into one sorted list of dr sorted words in O(rlgk) time

- like standard merge but with ① as comparator

- merge first word of each list → 2 words

- output first word

- put second word at front of list

- containing max elt in that word

④ mergesort with ③ as merger & ② as base case

⇒ T(n) = 2T(n/2) + O(n/k·lg k)

T(k) = O(k)

⇒ T(n) = O(n/k·lg k·lg n/k

+ n/k·k)

≤ O(n/k·lg k·lg n+n)

O(k) O(k) 3 n/k leaves

- k = lg n·lg lg n ⇒ lg k = ⊕(lg lg n)

⇒ T(n) = O(n)
## Page 6

Bitonic sorting: (from parallel algorithms/networks)

Bitonic sequence = cyclic shift of

nondecreasing + nonincreasing sequences

- i.e.: or or c.

Algorithm: (sorting network)

- put A[i] & A[n/2+i] in right order

  for i = 0, 1, ..., n/2 - 1

- split A in half (at n/2)

- recurse on halves in parallel

82345679

-O(lg n) rounds

Invariant after round: [CLR & CLRS 2e (not 3e)]

- both halves are bitonic

- all elts. in left half < all elts. in right (look at which red comps. straddle peak)
## Page 7

Merging two sorted words of k elts. in O(lg k) time

① reverse order of second word in O(lg k) time

- idea: rev(LR) = rev(R) rev(L)

recurse on halves in parallel

<div style="text-align: center;"><img src="imgs/img_in_image_box_121_277_762_570.jpg" alt="Image" width="52%" /></div>


[(mask L) >> k/2] OR [(mask R) << k/2]

ditto, but shifts of k/4

↓ ↓ ↓

② concatenate two words (shift & or) ⇒ bitonic

③ bitonic sort_ each round in O(1) time:

goal:

<div style="text-align: center;"><img src="imgs/img_in_image_box_287_690_800_788.jpg" alt="Image" width="41%" /></div>


↓

 $ O_{0}^{11}O_{0}^{11}O_{0}^{11}O_{0}^{11} $

small A's small B's smalls

• mask A, OR lead bits

• mask B, shift left

Abstract: O ⇒ B smaller

    1 ⇒ A smaller

mask

shift right

subtract

shift, negate, mask

mask with A, B

shift, OR

(similar)



smalls bigs... OR
## Page 8

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
