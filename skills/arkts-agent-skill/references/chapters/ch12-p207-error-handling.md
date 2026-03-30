# Chapter 12: Error Handling

Page range: 207-208

## Page 207

// Class declarations without constructors
class Obj_no_ctor {}
class Base_no_ctor {}
class Derived_no_ctor extends Base_no_ctor {}

// Class declarations with default constructors declared implicitly
class Obj {
    constructor () {} // Empty body - as there is no superclass
}

// Default constructors added
class Base { constructor () { super () } }
class Derived extends Base { constructor () { super () } }

// Example of an error case
class A {
    private constructor () {}
}

class B0 extends A {} // OK. No constructor in B
    // During compilation of B
class B1 extends A {
    constructor () { // Default constructor added
        // that leads to compile-time error
        // as default constructor calls super()
        // which is private and inaccessible
    }
}

### 9.10 Inheritance

Class C inherits all accessible members from its direct superclass and direct superinterfaces (see Accessible), and optionally overrides or shadows some of the inherited members.

If C is not abstract, then it must implement all inherited abstract methods. The method of each inherited abstract method must be defined with override-compatible signatures (see Override-Compatible Signatures).

Semantic checks for inherited method and accessors are described in Overriding in Classes.

Constructors from the direct superclass of C are not subject of overriding because such constructors are not accessible (see Accessible) in C directly, and can only be called from a constructor of C (see Constructor Body).

## Page 208
