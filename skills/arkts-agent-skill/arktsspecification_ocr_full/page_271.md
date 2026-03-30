p4: Object,
p5: Object,
p6: Object,
p7: Object
): void
}
interface Derived1 extends Base {
    kinds_of_return_type(): Base // Valid overriding
}
interface Derived2 extends Base {
    kinds_of_return_type(): (q: Derived) => Base // Valid overriding
}
interface Derived3 extends Base {
    kinds_of_return_type(): number // Valid overriding
}
interface Derived4 extends Base {
    kinds_of_return_type(): number | string // Valid overriding
}
interface Derived5 extends Base {
    kinds_of_return_type(): E1 // Valid overriding
}
interface Derived6 extends Base {
    kinds_of_return_type(): Base[] // Valid overriding
}
interface Derived7 extends Base {
    kinds_of_return_type(): [Base, Base] // Valid overriding
}

### 15.9 Overloading

Overloading is the language feature that allows to use the same name to call several functions, or methods, or constructors with different signatures.

The actual function, method, or constructor to be called is determined at compile time. Thus, overloading is compile-time polymorphism by name.

ArkTS supports the following two overloading mechanisms:

• Conventional overloading TBD; and

• Innovative managed overloading (see Overload Declarations).

Overload resolution is used to select one entity to call from a set of candidates if the name to call refers to an overload declaration (see Overload Resolution).

Both mechanisms of resolution use the first-match textual order to streamline the resolution process.

TBD: A compile-time warning is issued if the order of entities in an overload declaration implies that some overloaded entities can never be selected for a call.
