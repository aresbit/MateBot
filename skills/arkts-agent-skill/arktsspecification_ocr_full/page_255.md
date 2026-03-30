let t: T<int, boolean> = new T<int, boolean>
    let c: C<int, boolean> = new C<int, boolean>

// OK, assigning to direct superclass
t = new C<int, boolean>

// CTE, cannot assign to subclass
c = new T<int, boolean>

• T is one of direct superinterfaces of C <F1, ..., Fn> (see Superinterfaces and Subinterfaces):

// Interface I<U, V> is direct superinterface
// of J<U, V>, X<U, V>

interface I<U, V> {
    foo(u: U): U;
    bar(v: V): V;
}

// J<U, V> <: I<U, V>
// since J extebdss I
interface J<U, V> extends I<U, V>
{
    foo(u: U): U
        bar(v: V): V
        foo1(p: U|V): U|V
    }

    // X<U, V> <: I<U, V>
    // since X implements I
    class X<U, V> implements I<U, V> {
        foo(u: U): U { return u }
        bar(v: V): V { return v }
    }

    // Y<U, V> <: J<U, V> (directly)
    // Also Y<U, V> <: I<U, V> (transitively)
    class Y<U, V> implements J<U, V> {
        foo(u: U): U { return u }
        bar(v: V): V { return v }
    }

    fool(p: U|V): U|V { return p }
}

let i: I<int, boolean>
    let j: J<int, boolean>
    let x = new X<int, boolean>
    let y = new Y<int, boolean>

    // OK, assigning to direct supertypes

(continues on next page)
