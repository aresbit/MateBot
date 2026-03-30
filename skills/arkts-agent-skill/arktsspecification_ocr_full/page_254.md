function foo(t: T) {}
    let t: T
    let s: S

    // Using T
    class A implements T {}
    t = new A
    foo(t)

    // Using S (S<: T)
    class B implements S {}
    s = new B
    foo(s)

• Interface S is a direct subtype of class Object (S<:Object) if S has no extends clause (see Superinterfaces and Subinterfaces).

// Illustrating subinterface of Object
interface S {}
function foo(o: Object) {}

// Using Object
foo(new Object)

// Using subinterface of Object
class A implements S {}
let s: S = new A;
foo(s)

#### 15.2.2 Subtyping for Generic Classes and Interfaces

A generic class or generic interface is declared as C <F₁, ..., Fₙ>, where n>0 is a direct subtype of another generic class or interface T, if one of the following conditions is true:

• T is a direct superclass of C <F₁, ..., Fᵢ> mentioned in the extends clause of C:

// T<U, V> is direct superclass of C<U,V>
// T<U, V>>: C<U, V>

class T<U, V> {
    foo(p: U|V): U|V { return p }
}

class C<U, V> extends T<U, V> {
    bar(u: U): U { return u }
}

// OK, exact match

(continues on next page)
