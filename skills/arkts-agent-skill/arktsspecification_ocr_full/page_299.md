(continued from previous page)

c[1] // getByNumber is used
c["abc"] // getByString is used

If a class implements some interfaces with overload declarations for the same alias, then a new overload declaration must include all overloaded methods. Otherwise, a compile-time error occurs.

interface I1 {
    overload foo {f1, f2}
    // f1 and f2 are declared in I1
}

interface I2 {
    overload foo {f3, f4}
    // f3 and f4 are declared in I2
}

class C implements I1, I2 {
    // compile-time error as no new overload is defined
}

class D implements I1, I2 {
    overload foo {f2, f3, f1, f4} // OK, as new overload is defined
}

class E implements I1, I2 {
    overload foo {f2, f4} // compile-time error as not all methods are used
}

const i1: I1 = new D

i1.foo(<arguments>) // call is valid if arguments fit first signature of {f1, f2} set

const i2: I2 = new D

i2.foo(<arguments>) // call is valid if arguments fit first signature of {f3, f4} set

const d: D = new D

d.foo(<arguments>) // call is valid if arguments fit first signature of {f2, f3, f1, f4}
→ set

#### 17.9.3 Interface Method Overload Declarations

Interface method overload declaration allows declaring an overload alias as an interface member (see Interface Members) for a set of interface methods (see Interface Method Declarations).

The syntax is presented below:

overloadInterfaceMethodDeclaration:
'overload' identifier '{' identifier (',' identifier)* ','? '}';

The use of a method overload declaration is represented in the example below:

interface I {
    foo(): void

(continues on next page)
