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
