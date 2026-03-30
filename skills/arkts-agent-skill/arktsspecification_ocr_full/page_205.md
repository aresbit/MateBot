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
