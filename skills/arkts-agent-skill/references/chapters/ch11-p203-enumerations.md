# Chapter 11: Enumerations

Page range: 203-206

## Page 203

constructorDeclaration:
    'native'? 'constructor' identifier? parameters constructorBody?
;

An optional identifier in constructor declaration is an experimental feature discussed in Constructor Names. Constructors are called by the following:

• Class instance creation expressions (see New Expressions); and

• Explicit constructor calls from other constructors (see Constructor Body).

Access to constructors is governed by access modifiers (see Access Modifiers and Scopes). Declaring a constructor inaccessible prevents class instantiation from using this constructor. If the only constructor is declared inaccessible, then no class instance can be created.

A native constructor (an experimental feature described in Native Constructors) must have no constructorBody. Otherwise, a compile-time error occurs.

A non-native constructor must have constructorBody. Otherwise, a compile-time error occurs.

A compile-time error occurs if more than one non-native anonymous constructors are defined in a class:

class C {
    constructor (s: string) {}
    constructor () {} // compile-time error: multiple anonymous constructors
}

#### 9.9.1 Formal Parameters

The syntax and semantics of a constructor’s formal parameters are identical to those of a method.

#### 9.9.2 Constructor Body

Constructor body is a block of code that implements a constructor.

The syntax of constructor body is presented below:

constructorBody:
    '{' statement* '}'
;

The constructor body must provide correct initialization of new class instances. Constructors have two variations:

• Primary constructor that initializes instance own fields directly;

• Secondary constructor that uses another same-class constructor to initialize its instance fields.

The high-level sequence of a primary constructor body includes the following:

1. Mandatory call to a superconstructor (see Explicit Constructor Call) if a class has an extension clause (see Class Extension Clause) on all execution paths of the constructor body.

## Page 204

2. Mandatory execution of field initializers (if any) in the order they appear in a class body implicitly added by the compiler.

3. Optional arbitrary code that avoids usage of non-initialized fields.

4. Optional code that ensures all object fields to be initialized.

• If the compiler can detect that a non-initialized field is accessed during compilation, then a compile-time error occurs;

As step 4 above cannot be guaranteed at compile time in all possible cases, the following strategy is to be taken:

• Otherwise, it is a responsibility of the runtime system to detect such cases and handle them with a runtime exception.

5. Optional arbitrary code.

class Base {
    x: Object
    constructor() {
        this.x = new Object // Base object is fully initialized
        crash_this (this)
    }
}

class Derived {
    y: Object
    constructor () {
        super() // mandatory call to base class constructor
        this.y = new Object
    }
}

function crash_this (b: Base) {
    if (b instanceof Derived) { // If b is of type Derived, then
        console.log ((b as Derived).y) // Access y field of Derived object
        // Depending on the compilation context, either the compiler reports
        // a compile-time error, or the runtime system is to detect the case
    }
}

The example below represents primary constructors:

class Point {
    x: number
    y: number
        constructor(x: number, y: number) {
            this.x = x
            this.y = y
        }
}

class ColoredPoint extends Point {
    static readonly WHITE = 0
    static readonly BLACK = 1
    color: number
        constructor(x: number, y: number, color: number) {
            super(x, y) // calls base class constructor
            this.color = color
        }
    }
}

(continues on next page)

## Page 205

(continued from previous page)

(continued from previous page)

7

8

The high-level sequence of a secondary constructor body includes the following:

1. Call to another same-class constructor that uses the keyword this (see Explicit Constructor Call) on all execution paths of the constructor body.

The example below represents primary and secondary constructors:

2. Optional arbitrary code.

class Point {
    x: number
    y: number
    constructor(x: number, y: number) {
        this.x = x
        this.y = y
    }
}

class ColoredPoint extends Point {
    static readonly WHITE = 0
    static readonly BLACK = 1
    color: number

    // primary constructor:
    constructor(x: number, y: number, color: number) {
        super(x, y) // calls base class constructor as class has 'extends'
        this.color = color
    }
    // secondary constructor:
    constructor zero(color: number) {
        this(0, 0, color)
    }
}

A compile-time error occurs if a constructor calls itself, directly or indirectly through a series of one or more explicit constructor calls using this.

A constructor body looks like a method body (see Method Body), except for the semantics as described above. Explicit return of a value (see return Statements) is prohibited. On the opposite, a constructor body can use a return statement without an expression.

A constructor body can have no more than one call to the current class or direct superclass constructor. Otherwise, a compile-time error occurs.

## Page 206

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
