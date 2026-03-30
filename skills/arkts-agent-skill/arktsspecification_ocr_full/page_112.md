class C {
    private constructor () {}
}

// ...
let c: C = {} /* compile-time error - constructor is not accessible */

If a class has accessors (see Class Accessor Declarations) for a property, and its setter is provided, then this property can be used as a part of an object literal. Otherwise, a compile-time error occurs:

class OK {
    set attr (attr: number) {}
}
const a: OK = {attr: 42} // OK, as the setter be called

class Err {
    get attr (): number { return 42 }
}
const b: Err = {attr: 42} // compile-time error - no setter for 'attr'

#### 7.5.2 Object Literal of Interface Type

If an interface type I is inferred from the context, then type of an object literal is an anonymous class implicitly created for interface I:

interface Person {
    name: string
    age: number
}
let b: Person = {name: "Bob", age: 25}

In the example above, type of b is an anonymous class that contains the same fields as the interface I properties.

Any properties that are optional can be skipped in an object literal. The values of such optional properties are set to undefined as follows:

interface Person {
    name: string
    age: number
    sex?: "male"|"female"
}
let b: Person = {name: "Bob", age: 25}
    // 'sex' field will have 'undefined' value

Properties that are non-optional cannot be skipped in an object literal, despite some property types having default values (see Default Values for Types). If a non-optional property (e.g., age in the example above) is skipped, then a compile-time error occurs.

A compile-time error occurs if an object literal of interface type introduces a new method:
