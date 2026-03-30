(continued from previous page)

7 overload foo { fooDerived, fooBase }

8 function too() {
    let a: Base = new Base
    foo (a) // fooBase will be called
    let b: Base = new Derived
    foo (b) // as smart type of 'b' is Derived, fooDerived will be called
}

Particular cases supported by the compiler are determined by the compiler implementation.

### 15.8 Overriding

Method overriding is the language feature closely connected with inheritance. It allows a subclass or a subinterface to offer a specific implementation of a method already defined in its supertype optionally with modified signature.

The actual method to be called is determined at runtime based on object type. Thus, overriding is related to runtime polymorphism.

ArkTS uses the override-compatibility rule to check the correctness of overriding. The overriding is correct if method signature in a subtype (subclass or subinterface) is override-compatible with the method defined in a supertype (see Override-Compatible Signatures).

An implementation is forced to Make a Bridge Method for Overriding Method in some cases of method overriding.

#### 15.8.1 Overriding in Classes

Note. Only accessible (see Accessible) methods are subjected to overriding. The same rule applies to accessors in case of overriding.

An overriding member can keep or extend an access modifier (see Access Modifiers) of a member that is inherited or implemented. Otherwise, a compile-time error occurs.

A compile-time error occurs if an attempt is made to do the following:

• Override a private method of a superclass; or

- Declare a method with the same name as that of a private method with default implementation from any super-interface.

class Base {
    public public_member() {}
    protected protected_member() {}
    private private_member() {}
}

interface Interface {
