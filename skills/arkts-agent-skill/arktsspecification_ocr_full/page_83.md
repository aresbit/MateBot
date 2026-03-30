// T1 can be used in in-position only
foo (p: T1) {} // OK
foo1(p: T1): T1 { return p } // error: T1 in out-position
fldT1: T1 // error: T1 in invariant position

8
9
10
11
12
13
14
15
16

In case of function types (see Function Types), variance interleaving occurs.

class X<in T1, out T2> {
    foo (p: T1): T2 {...} // in - out
    foo (p: (p: T2)=> T1) {...} // out - in
    foo (p: (p: (p: T1)=>T2)=> T1) {...} // in - out - in
    foo (p: (p: (p: T2)=> T1)=>T2)=> T1) {...} // out - in - out - in
    // and further more
}

A compile-time error occurs if function or method type parameters have a variance modifier specified.

### 5.2 Generic Instantiations

As mentioned before, a generic declaration defines a set of corresponding generic or non-generic entities. The process of instantiation is designed to do the following:

• Allow producing new generic or non-generic entities;

- Provide every type parameter with a type argument that can be any kind of type, including the type argument itself.

As a result of the instantiation process, a new class, interface, union, array, method, or function is created.

class A <T> {}
class B <U, V> extends A<U> { // Here A<U> is a new generic type
    field: A<V>     // Here A<V> is a new generic type
    method (p: A<Object>) {} // Here A<Object> is a new non-generic type
}
