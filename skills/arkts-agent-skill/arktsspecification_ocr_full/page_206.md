#### 9.9.3 Explicit Constructor Call

There are two kinds of explicit constructor calls:

- Superclass constructor calls (used to call a constructor from the direct superclass) that begin with the keyword super.

• Other constructor calls that begin with the keyword this (used to call another same-class constructor).

To call a named constructor (Constructor Names), the name of the constructor must be provided while calling a super-class or another same-class constructor.

A compile-time error occurs if arguments of an explicit constructor call refer to one of the following:

• Any non-static field or instance method; or

• this or super.

// Class declarations without constructors
class Base {
    constructor () {}
    constructor base() {}
}

class Derived1 extends Base {
    constructor () {
        super() // Call Base class constructor
    }
}

class Derived2 extends Base {
    constructor () {
        super.base() // Call Base class named constructor
    }
}

class Derived3 extends Base {
    constructor () {
        this.derived() // Call same class named constructor
    }
    constructor derived() {}
}

#### 9.9.4 Default Constructor

If a class contains no constructor declaration, then a default constructor is implicitly declared. This guarantees that every class effectively has at least one constructor. The form of a default constructor is as follows:

• Default constructor has modifier public (see Access Modifiers).

• The default constructor body contains:

– Call to a superclass constructor with no arguments except the primordial class Object. The default constructor body for the primordial class Object is empty.

– Mandatory execution of field initializers (if any) in the order they appear in a class body.

A compile-time error occurs if a default constructor is implicit, but the superclass has no accessible constructor without parameters (see Accessible).
