(continued from previous page)

{
    }
}

new Derived()

/* Output:
    Field initialization in C
    Field initialization in Derived
*/

A compile-time error occurs if a field is not declared as `ready` in a `superclass`, while an `overriding` field is marked as `ready`:

class C {
    field = 1
}
class D extends C {
    readonly field = 2 // compile-time error, wrong overriding
}

A compile-time error occurs if a field overrides getter or setter in a superclass:

class C {
    get num(): number { return 42 }
    set num(x: number) {}
}
class D extends C {
    num: number = 2 // compile-time error, wrong overriding
}

The same compile-time error occurs in more complex case, where a field simultaneously overrides a field from a superclass and implements a property from a superinterface:

class C {
    num: number = 1
}
interface I {
    num: number
}
class D extends C implements I {
    num: number = 2 // compile-time error, conflict in overriding
}

The overriding conflict occurs as num in D, and must be both:

• Field to override a field inherited from the superclass C; and

• Two accessors (see Class Accessor Declarations) to implement a property from the superinterface ‘I’ (see Implementing Required Interface Properties).

Overriding a field by an accessor also causes a compile-time error as follows:

class C {
    num: number = 1
}
class D extends C {

(continues on next page)
