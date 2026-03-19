# Tree Queries and Strings

Range minimum query, lowest common ancestor, level ancestors, tries, suffix trees, suffix arrays, and document retrieval.

## Included Lectures
- L15.md
- L16.md

---

## L15.md


## Page 1

TODAY: Constant-time tree queries

- range minimum queries

- lowest common ancestor

- level ancestors

Range Minimum Query (RMQ):

- preprocess array A of n numbers

- query:  $ RMQ(i,j) = (\arg\min\{A[i], A[i+1], \ldots, A[j]\}) = k_n \leq k \leq j $, minimizing A[k]

>range min j

Lowest Common Ancestor (LCA):

- preprocess free T on n nodes

- query: LCA(x,y)

<div style="text-align: center;"><img src="imgs/img_in_image_box_925_858_1116_1010.jpg" alt="Image" width="15%" /></div>


Level Ancestors: (LA)

- preprocess free T on n nodes

- query: LA(x,k) = parent^{k}(x)

Goal: O(1) time/query, O(n) space

[∅(n^{2}) space trivial: store all answers]



<div style="text-align: center;"><img src="imgs/img_in_image_box_966_1035_1095_1235.jpg" alt="Image" width="10%" /></div>


Which of these problems are most similar?

actually RMQ & LCA
## Page 2

[Gabow, Bentley, Tarjan-STOC 1984]

reduction from array A to binary tree T

- root of T = some min. element A[i] in A

- left subtree = Cartesian tree of A[<i]

- right subtree = Cartesian tree of A[≥i]

872869457

A 8

<div style="text-align: center;"><img src="imgs/img_in_image_box_904_426_1192_661.jpg" alt="Image" width="23%" /></div>


- T is a min heap

- in-order traversal of T = A

- LCA(i,j) = RMQ(i,j)

  tree nodes array indices

Linear-time construction algorithm:

- for each item in A: insert into T by

walking up right spine of T&updating edge:

<div style="text-align: center;"><img src="imgs/img_in_image_box_228_1105_745_1323.jpg" alt="Image" width="42%" /></div>


O(1) changes

— charge walk to decrease in right spine len.

⇒ O(n) time (as in L14) [GBT84]

— seven in comparison model
## Page 3

Reverse reduction: from (binary) free T to array A

- in-order traversal of T

- write depth of each node

<div style="text-align: center;"><img src="imgs/img_in_image_box_228_247_686_543.jpg" alt="Image" width="37%" /></div>


21032312

- RMQ(i,j) = LCA(i,j)

↔ index into A ↔ node in T

RMQ universe reduction:

- reduce  $ RMQ \rightarrow LCA \rightarrow RMQ $

- Cartesian in-order depth

-  $ RMQ(i,j) $ answers are preserved

- indices in array (argmin)

- arbitrary ordered universe  $ \rightarrow \{0,1,\ldots,n-1\} $

-  $ O(n) $ time in comparison model
## Page 4

Constant-time LCA ⇒ RMQ: [Harel & Tarjan - SICOMP]

- Simplified by [Bender & Farach-Colton - LATIN 2000]*

- based on PRAM [Berkman et al. - STOC 1989] HERE

① reduce to ±1 RMQ: adjacent values differ by ±1

- Euler tour of tree (depth-first search),

writing depth of each node visited

(instead of in-order traversal)

- e.g. φ 1 2 1 φ 1 2 3 2 3 2 1 2 1 φ

⇒±1: also works for nonbinary trees

- each node stores its first (or any) visit

- each visit stores corresponding node

- LCA(x,y) = RMQ(first(x), first(y))

② O(1) time, O(n) g n) space RMQ: choices:

- store answer from every start point ← n

of interval of length = power of 2 ← gn

- any interval is the (nondisjoint) union of two such intervals:

length k, length

 $ \Rightarrow RMQ = (arg) \min of 2 stored answers $
## Page 5

③ indirection: split array into groups of  $ \frac{1}{2} \lg n $

min  $ \frac{1}{2} \lg n $  $ \frac{1}{2} \lg n $  $ \cdots $  $ \frac{1}{2} \lg n $

⇒ top is O(1) time, O(n) space

- RMQ(i,j) = (arg)min of:

  - RMQ(i,∞) in i's group = [2i/2gn]

  - RMQ(-∞,j) in j's group

  - RMQ(i's group + 1, j's group - 1) in top

④ lookup table for groups:  $ (n' = \frac{1}{2} \lg n) $

- add -A[0] to every value  $ \Rightarrow A'[\emptyset] = \emptyset $

- RMQ(i,j) invariant under such shift

 $ \Rightarrow \# $ possible A' arrays = # ± 1s = 2n' =  $ \sqrt{n} $

-  $ (\frac{1}{2} \lg n)^2 $ possible queries

- O(lg  $ \lg n $) bits to store an answer

 $ \Rightarrow $ lookup table storing all answers

for all possible A' arrays

uses O( $ \sqrt{n} $  $ \lg^2 n $  $ \lg \lg n $) = o(n) bits

- each group just stores index into table

describing A' array  $ \sim O(n) $ words

 $ \Rightarrow O(1) $ query at bottom

- total: O(1) query, O(n) (words of) space

- O(n) bits for LCA & RMQ! [Sadakane-JDA 2007]
## Page 6

Constant-time level ancestors:

[Berkman & Vishkin - JCSS 1994; Dietz - WADS 1991; Alstrup & Holm - ICALP 2000; dynamic trees Bender & Farach-Colton - TCS 2004] *← HERE

① jump pointers: O(n lg n) space, O(lg n) query

- each node stores pointer to  $ 2^{i} $th ancestor for  $ i = 0, 1, \ldots, lg n $ (or less)

extra

- query:  $ x = 2^{\lfloor lg k \rfloor} $ th ancestor of x

   $ k = k - 2^{\lfloor lg k \rfloor} < k/2 \Rightarrow O(\lg n) $

  repeat

② long-path decomposition: O(n) space, O(ln) query

- find longest root-to-leaf path (deepest leaf)

- store nodes on path in depth-ordered array

- each node stores array & index of itself

- recurse on subtrees hanging off path

- query: if  $ k \leq $ index i of node x in its path: return path array[i-k]

else:  $ x = \text{parent}(\text{path} \text{array}[\emptyset]) $

 $ k = k - 1 - i $

extra

- node of height'h is on path of length ≥h

- but can visit ⊙(h) paths:



The image is too blurry to recognize any text content.
## Page 7

③ ladder decomposition: O(n) space, O(lg n) query

- extend each path upward into ladder

of twice the length (→ ladders overlap)

⇒ ≤ double the space of ②

- node stores which ladder contains it

in the lower half (correspond to unique path)

- ladder = array; query uses them as in ②

- node of height h is on ladder of height ≥ 2h

⇒ each step at least doubles height of node

④ combine jump pointers ① & ladder decomp. ③ over time: exp. decr. hops ~ expr. incr. hops

- query: 1 jump pointer → height ≥  $ \frac{k}{2} $ above ×

+ 1 ladder step (ladder height ≥ k above)

⇒ O(1) query, O(nlg n) space

⑤ tune jump pointers: O(n + L(g n) space ladders jump pointers

- each node stores a descendent leaf & how much deeper d it is

⇒ can start query at a leaf (k' = k + d)

⇒ only need jump pointers at leaves
## Page 8

⑥ leaf trimming: (indirection) [Alstrup, Husfeldt, Rauhe-FOCS]

- cut below maximally deep nodes

with  $ \geq \frac{1}{4} $ lg n descendants

 $ \Rightarrow \# $ leaves in top = O(n/lg n)

 $ \Rightarrow $ ⑤ on top uses O(n) space

- query tries in bottom; else uses top

⑦ lookup table for bottom trees with  $ n' < \frac{1}{4} \lg n $

- # rooted trees on  $ n' $ nodes =  $ C_n' \leq 2^{2n'} $

- # queries =  $ (n')^2 = O(\lg^2 n) $ encoding proof:

- answer =  $ \Delta(\lg \lg n) $ encode  $ 2n' $ steps of Euler tour as up/down

- lookup table storing all answers for all possible trees uses  $ O(\sqrt{n} \lg^2 n \lg \lg n) = O(n) $ bits

- bottom tree stores index into table

 $ \Rightarrow O(1) $ query, O(n) space!

Dynamic LCA: [Cole&Hariharan-SCOMP2005]

Dynamic LCA: [Coxe&11
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.

---

## L16.md


## Page 1

TODAY: Strings

- tries & trays

- compressed tries

- suffix trees & arrays

- document retrieval

- linear-time construction

String matching: given text T & pattern P, here both strings over alphabet Σ₁, find some/all occurrences of P in T as substrings

- one-shot: O(T) time [Knuth, Morris, Pratt - 1977?]

  Boyer & Moore - CACM; Karp & Rabin - IBM JRD 1987

- static DS: preprocess T, query = P

- goal: O(P) query

  O(T) space

- other data structures consider when P has wildcards, or when P need not match as an exact substring (Hamming/edit distance) ~ see e.g. [Cole, Gottlieb, Lewenstein - STOC2004] [Maab & Novak - CPM 2005]
## Page 2

Warmup: predecessor among strings  $ T_{1}, \ldots, T_{k} $ (e.g. library search)

 $ \underline{\text{Trie}} $ = rooted tree with child branches

labeled with letters in  $ \Sigma_{i} $



<div style="text-align: center;"><img src="imgs/img_in_image_box_973_231_1206_340.jpg" alt="Image" width="19%" /></div>


to represent strings as

root-to-leaf paths in a trie.

terminate them with a new

letter $ (otherwise can't

distinguish prefixes as

absent or present)

- e.g.: {ana, o

<div style="text-align: center;"><img src="imgs/img_in_image_box_889_378_1192_736.jpg" alt="Image" width="24%" /></div>


{ana, ann, anna, anne}

- in-order traversal of leaves = sorted strings

True representation: T = # nodes in trie ≤ ∑ |T₁|

node stores children: query space

① as array O(P) O(T₂)

→ blank cells store predecessor/successor

② as balanced BST O(P|g∑) O(T)

③ as hash table O(P) O(T)

L>doesn't support predecessor queries/sorting

③.5 as van Emde Boas/y-fast O(PlglgΣi) O(T)

③.75=③+③.5 (only need vEB when fall off) O(P+lglgΣi) O(T)
## Page 3

[Farach-Colton - personal communication, 2012]:

node stores children:

query space

O(P+lg k) O(T)

T # leaves



4) as

4#descendant leaves in I

- split children in left & right

  halves to optimally

  balance sum of weights

⇒ every 2 edges followed either advances P letter

or reduces # candidate T strings to 2/3

⇒ charge to O(P) or Q(kg)

⑤ leaf trimming (indirection) O(P+lgΣ) O(T)

- cut below maximally deep nodes

with ≥|Σ| descendant (leave)s

⇒ # leaves in top trie ≤ |T|/|Σ|

⇒ # branching top nodes ≤ |T|/|Σ|

- use ① on branching top nodes

& ① on top leaves (to find right bottom trie)

& ② on rest of top (≌nonbranching in T)

⇒ O(T) space on top

- bottom trees have < |Σ| descendant (leave)s

⇒ ④ achieves O(P+lgΣ) query time

→ simplification by Farach-Colton of:

⑥ suffix trays

[Cole, Kopelowitz, Lewenstein - ICALP 2006]
## Page 4

Application: sorting strings  $ T_{1} $…… $ T_{k} $

— repeatedly insert into tri/tray

 $ \Rightarrow O(T + k \lg \xi) $

— typically  $ O(T) \& << O(Tk \lg k) $ via comparison

Compressed_trie: contract nonbranching paths to single edge, keyed by first letter of path

<div style="text-align: center;"><img src="imgs/img_in_image_box_191_556_803_907.jpg" alt="Image" width="50%" /></div>


<div style="text-align: center;">TRUE</div>


<div style="text-align: center;"><img src="imgs/img_in_image_box_835_553_1134_909.jpg" alt="Image" width="24%" /></div>


COMPRESSED TRIE

- same representations apply,

with T = # compressed nodes
## Page 5

atfix tree (trie):

compressed trie of all ITI suffixes TIi:7 of T (with $ appended)

- e.g.: b a n a n a $

    ∅ 1 2 3 4 5 6

<div style="text-align: center;"><img src="imgs/img_in_image_box_756_42_1175_486.jpg" alt="Image" width="34%" /></div>


- |T| + 1 leaves

- edge label = substring [i:j]

→ store as two indices (i,j)

⇒ O(T) space

Applications:

- search for P gives subtree whose leaves correspond to all occurrences of P

- O(P) time via hashing

- O(P + lg £i) via trays → leaves sorted in T

- O(P + lg lg £i) via hash + vEB

- list first k occurrences in O(k) more time

- every node points to leftmost descend leaf

- leaves connected via linked list

- # occurrences in O(1) more time (子孙数)



-longest repeated substring in T: O(T) time

  = branching node of maximum "letter depth"

-longest substring match of T[i:] vs. T[j:]

O(1) via LCA query
## Page 6

- all occurrences of T[i:j] = (j-i)th "weighted"

level ancestor of leaf for T[i:j] for compression

- store nodes in long path/ladder of L15 in

van Emde Boas predecessor DS ⇒ O(lg lg T)

- can't afford lookup tables at the bottom...

- use ladder decomposition on bottom trees

⇒ jump to top of O(lg lg n) ladders

(to reach height O(lg n))

- only need predecessor query on last ladder

⇒ O(lg lg T) query & O(T) space

[Abbott, Baron, Demaine, ... - 6.897, Spr. 2005, L19.5]

- multiple documents via mult. $s: T = T_1$ $1 \cdots T_k$ $k$

- count # distinct documents containing P

- store # distinct $s$ below each node

- longest common substring in O(T)

= branching node with ≥2 distinct $s$ below below

- find d distinct documents containing P in O(d) more

"document retrieval problem" [Muthukrishnan-SODA]

- each $i$ stores leaf # of previous $i$

- in interval [l,n] of leaves below a node, $l \cdot m \cdot n$

want first $i, i.e. $i storing <l, for each occ. i

- so find m = RMQ(l,n) on array of stored values

- if stored value at leaf m is <i: [L15]

- found desired $i \sim output$ it

- recurse in intervals [l,m-1] & [m+1,n]

⇒ O(1) time per output (& can stop anytime)
## Page 7

Suffix arrays: sort the suffixes of T just store the indices  $ \Rightarrow O(T) $ space

- e.g. b a n a n a $

    0 1 2 3 4 5 6

- searchable in O(Plg†)

  via binary search

- lcp[i] = length of

  longest common prefix

  of ith & (i+1)st suffix in order

- when binary searching in interval SA[i:j].

  only need to compare from letter RMQlcp(i,j-1)

- via RMQ of L15. O(P+lg†) search [2007, PS4]

Suffix trees ↔ suffix arrays:

- (→) via in-order traversal of leaves

- (←) via Cartesian tree of lcp array

  - put all mins at root (unlike L15)

  - nonleaf child subtrees: recurse

  - suffixes fit in between as leaves

  - lcp value forming a node

  = letter depth of that node

⇒ edge length = child lcp - parent lcp

⇒ can reconstruct labels

- all doable in linear time [L15]

- lcps computable in O(T) from SA [Kasai et al.-2001]

or directly in suffix-array construction below
## Page 8

Constructing suffix array (⇒tree) in O(T+sort(Σi))

[Kärkäinen & Sanders – [CALP 2003], inspired by

[Farach – FOCs; Farach-Colton, Ferragina, Muthukrishnan – JACM]

① sort $\Sigma_{i}$ - initially in sort($\Sigma_{i}$) time (or if don't need children sorted, just number $\Sigma_{i}$ arbitrarily) - later, radix sort in (T) time

@replace each letter by its rank in  $ \Sigma_{1} \Rightarrow \leq|\Sigma| $

(3) form  $ T_{\phi}=\langle(T[3i]_{n}T[3i+1]_{n}T[3i+2])\rangle $ for  $ i=\phi_{n}1_{n}2_{n}\cdots\rangle $

 $ T_{1}=\langle(T[3i+1]_{n}T[3i+2]_{n}T[3i+3])\rangle $ for  $ i=\phi_{n}1_{n}2_{n}\cdots\rangle $

 $ T_{2}=\langle(T[3i+2]_{n}T[3i+3]_{n}T[3i+4])\rangle $ for  $ i=\phi_{n}1_{n}2_{n}\cdots\rangle $

④ recurse on  $ \langle T_{0},T_{1}\rangle $  $ \Rightarrow $  $ \frac{2}{3}|T| $ "letters"  $ \rightarrow $ sorted order & lcps of  $ \cup_{i=0,1} $ suffixes( $ T_{i} $)

⑤ radix sort suffixes(T₂) by writing

T₂[i] ≈ T[3i+2] = <T[3i+2], T[3i+3] > <T[3i+2], T₀[i+1] >

- also get lcps in suffixes(T₂): try to extend by 1

⑥ merge i:0.1 suffixes(T₁) with suffixes(T₂) via:

- T₀[i:] vs. T₂[j:] = T[3i:] vs. T[3j+2:]

  = <T[3i:]、T[3i+1:]> vs. <T[3j+2:]、T[3j+3:]>

  T₁[i:]

- T₁[i:] vs. T₂[j:] = T[3i+1:] vs. T[3j+2:]

  = <T[3i+1:]、T[3i+2:]、T[3i+3:]> → T₀[i+1:]

vs. <T[3j+2:]、T[3j+3:]、T[3j+4:]> → T₁[i+1:]

- also get lcps: try to extend by 1 or ∂

⇒ T(n) = T(2/3·n) + O(n) = O(n)

  (n = |T|)
## Page 9

6.851 Advanced Data Structures

Spring 2012

For information about citing these materials or our Terms of Use, visit: http://ocw.mit.edu/terms.
