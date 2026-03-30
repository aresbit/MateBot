### 4.2 Declarations

A declaration introduces a named entity in an appropriate declaration scope (see Scopes), see

• Type Declarations;

• Variable and Constant Declarations;

• Function Declarations;

• Classes;

• Interfaces;

• Enumerations:

• Local Declarations;

• Top-Level Declarations;

• Overload Declarations;

• Annotations;

• Ambient Declarations.

Each declaration in the declaration scope must be distinguishable. Declarations are distinguishable if they have different names.

Distinguishable declarations are represented by the examples below:

const PI = 3.14
const pi = 3
function Pi() {}
type IP = number[]
class A {
    static method() {}
    method() {}
    field: number = PI
    static field: number = PI + pi
}

A compile-time error occurs if a declaration is not distinguishable:

// compile-time error: The constant and the function have the same name
const PI = 3.14
function PI() { return 3.14 }

// compile-time error: The type and the variable have the same name.
class Person {}
let Person: Person

// compile-time error: The field and the method have the same name.
class C {
    counter: number
    counter(): number {
        return this.counter
    }
}

(continues on next page)
