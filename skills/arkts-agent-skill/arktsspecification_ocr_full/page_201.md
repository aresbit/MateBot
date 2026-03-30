static, Final Methods for the modifier final, Overriding Methods for the modifier override, and Native Methods for the modifier native).

class Person {
    private _age: number = 0
    get age(): number { return this._age }
    set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        this._age = a
    }
}

A get-accessor (getter) must have an explicit return type and no parameters, or no return type at all on condition it can be inferred from the getter body. A set-accessor (setter) must have a single parameter and no return type. The use of getters and setters looks the same as the use of fields. A compile-time error occurs if:

• Getters or setters are used as methods;

• Getter return type cannot be inferred from the getter body;

• Set-accessor (setter) has a single parameter that is optional (see Optional Parameters):

class Person {
    private _age: number = 0
    get age(): number { return this._age }
    set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        this._age = a
    }
}

let p = new Person()
p.age = 25     // setter is called
if (p.age > 30) { // getter is called
    // do something
}
p.age(17) // Compile-time error: setter is used as a method
let x = p.age() // Compile-time error: getter is used as a method

class X {
    set x (p?: Object) {} // Compile-time error: setter has optional parameter
}

If a getter has no return type specified, then the type is inferred as in Return Type Inference.

class Person {
    private _age: number = 0
    get age() { return this._age } // return type is inferred as number
}

A class can define a getter, a setter, or both with the same name. If both a getter and a setter with a particular name are defined, then both must have the same accessor modifiers. Otherwise, a compile-time error occurs.

Accessors can be implemented by using a private field or fields to store the data as in the example above.
