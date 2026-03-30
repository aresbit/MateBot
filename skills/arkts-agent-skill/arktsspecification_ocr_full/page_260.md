function foo (ca: FixedArray<C>) {
    ca[0] = new C() // ArrayStoreError if ca refers to FixedArray<D>
}

let da: FixedArray<D> = [new D()]

foo(da) // leads to runtime error in 'foo'

#### 15.2.7 Subtyping for Intersection Types

Intersection type I defined as  $ (I_1 \& \ldots \mid I_n) $ is a subtype of type T if  $ I_i $ is a subtype of T for some  $ i $.

Type T is a subtype of intersection type  $ (I_1 \& \ldots \mid I_n) $ if T is a subtype of each  $ I_i $.

#### 15.2.8 Subtyping for Difference Types

Difference type A - B is a subtype of T if A is a subtype of T.

Type T is a subtype of the difference type A - B if T is a subtype of A, and no value belongs both to T and B (i.e., T & B = never).

### 15.3 Type Identity

Identity relation between two types means that the types are indistinguishable. Identity relation is symmetric and transitive. Identity relation for types A and B is defined as follows:

• Array types A = T1[] and B = Array<T2> are identical if T1 and T2 are identical.

• Tuple types  $ A = [T_1, T_2, \ldots, T_n] $ and  $ B = [U_1, U_2, \ldots, U_m] $ are identical on condition that:

- n is equal to m, i.e., the types have the same number of elements;

– Every  $ T_i $ is identical to  $ U_i $ for any  $ i $ in 1 … n.

• Union types  $ A = T_1 \mid T_2 \mid \ldots \mid T_n $ and  $ B = U_1 \mid U_2 \mid \ldots \mid U_m $ are identical on condition that:

– n is equal to m, i.e., the types have the same number of elements;

-  $ U_i $ in U undergoes a permutation after which every  $ T_i $ is identical to  $ U_i $ for any  $ i $ in 1 ... n.

• Types A and B are identical if A is a subtype of B (A<:B), and B is at the same time a subtype of A (A:>B).

Note. Type Alias Declaration creates no new type but only a new name for the existing type. An alias is indistinguishable from its base type.
