(continued from previous page)

max(1, 2) // max2 is called
max(3, 2, 4) // maxN is called
max("a", "b") // compile-time error, no function to call

maxN(1, 2) // maxN is explicitly called

The semantics of an entity included into an overload set does not change. Such entities follow the ordinary accessibility rules, and can be used separately from an overload alias, e.g., called explicitly as follows:

maxN(1, 2) // maxN is explicitly called
max2(2, 3) // max2 is explicitly called

When calling an overload alias, entities from an overload set are checked in the listed order, and the first entity with an appropriate signature is called (see Overload Resolution for detail). A compile-time error occurs if no entity with an appropriate signature is available:

1  $ \begin{cases} \text{max}(1) & // \text{max}N \text{ is called} \\ \text{max}(1, 2) & // \text{max}2 \text{ is called, as is the first in order} \end{cases} $
2  $ \begin{cases} \text{max}(a", b") & // \text{compile-time error, no function to call} \end{cases} $

It means that exactly one entity is selected for a call at the call site. Otherwise, a compile-time error occurs.

An overloaded entity in an overload declaration can be generic (see Generics).

If during Overload Resolution type arguments are provided explicitly in a call of an overload alias (see Explicit Generic Instantiations), then consideration is given only to the entities that have an equal number of type parameters and type arguments.

If type arguments are not provided explicitly (see Implicit Generic Instantiations), then consideration is given to all entities as represented in the example below:

function foo1(s: string) {}
function foo2<T>(x: T) {}

overload foo { foo1, foo2 }

foo("aa") // foo1 is called
foo(1) // foo2 is called, implicit generic instantiation
foo<string>("aa") // foo2 is called

An entity can be listed in several overload declarations:

function max2i(a: int, b: int): int {
    return a > b ? a : b
}
function maxNi(...a: int[]): int {
    // return max element
}
function maxN(...a: number[]): number {
    // return max element
}

overload maxi { max2i, maxNi }
overload max { max2i, maxNi, maxN }
