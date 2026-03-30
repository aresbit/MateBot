#### 7.5.1 Object Literal of Class Type

If class type C is inferred from the context, then type of an object literal is C:

class Person {
    name: string = ""
    age: number = 0
}

function foo(p: Person) { /*some code*/ }
// ...
let p: Person = {name: "Bob", age: 25} /* ok, variable type is used */
foo({name: "Alice", age: 18}) // ok, parameter type is used

An identifier in each name-value pair must name a field of class C, or a field of any superclass of class C.

A compile-time error occurs if the identifier does not name an accessible member field (see Accessible) in type C:

class Friend {
    name: string = ""
    private nick: string = ""
    age: number
    sex?: "male"|"female"
}

// compile-time error, nick is private:
let f: Friend = {name: "Alexander", age: 55, nick: "Alex"}

A compile-time error occurs if type of an expression in a name-value pair is not assignable (see Assignability) to the field type:

let f: Friend = {name: 123} /* compile-time error - type of right hand-side is not assignable to the type of the left hand-side */

If some class fields have default values (see Default Values for Types) or explicit initializers (see Variable and Constant Declarations), then such fields can be skipped in the object literal.

let f: Friend = {} /* OK, as name, nick, age, and sex have either default value or explicit initializer */

If an object literal is to use class C, then class C must have a parameterless constructor (explicit or default) that is accessible (see Accessible) in the class-composite context.

A compile-time error occurs if:

• C contains no parameterless constructor; or

• No constructor is accessible (see Accessible).

These situations are presented in the examples below:

class C {
    constructor (x: number) {}
}

// ...
let c: C = {} /* compile-time error - no parameterless
    constructor */
