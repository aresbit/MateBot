(continued from previous page)

41 | i = x
42 | j = y
43 | // OK, assigning subinterface (J<:I)
44 | i = j
45 |
46 | // CTE, cannot assign superinterface (I>:J)
47 | j = i

• T is type Object (C<:Object) if C <F₁, ..., Fₙ> is either a generic class type with no direct superclasses, or a generic interface type with no direct superinterfaces:

// Object is direct superclass and for C<U,V>
// and direct superinrerface for I<U,V>

class C<U, V> {
    foo(u: U): U { return u }
    bar(v: V): V { return v }
}

interface I<U, V> {
    foo(u: U): U { return u }
    bar(v: V): V { return v }
}

let o: Object = new Object
    let c: C<int, boolean> = new C<int, boolean>
    let i: I<int, boolean>

    // example1 - C<U,V> <: Object
    function example1(o: Object) {}

    // OK, example(Object)
    example1(o)
    // OK, C<int, boolean> <: Object
    example1(c)

    // example2 - I<U,V> <: Object
    function example2(o: Object) {}
    class D<U, V> implements I<U, V> {}
    i = new D<int, boolean>

    // OK, example2(Object)
    example2(o)
    // OK, I<int, boolean> <: Object
    example2(i)

The direct supertype of a type parameter is the type specified as the constraint of that type parameter.

If type parameters of a generic class or an interface have a variance specified (see Type Parameter Variance), then the subtyping for instantiations of the class or interface is determined in accordance with the variance of the appropriate type parameter. For example, with generic class G<in T1, out T2> the G<S, T> <: G<U, V> when S>:U and T<:V

The following code illustrates this:
