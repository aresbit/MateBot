In the example above, type Partial<Issue> is transformed to a distinct but analogous type as follows:

interface /*some name*/ {
    title?: string
    description?: string
}

Type T is not assignable to Partial<T> (see Assignability), and variables of Partial<T> are to be initialized with valid object literals.

Note. If class T has a user-defined getter, setter, or both, then none of those is called when object literal is used with Partial<T> variables. Object literal has its own built-in getters and setters to modify its variables. It is represented in the example below:

interface I {
    property: number
}

class A implements I {
    _property: number
    set property(property: number) {
        console.log("Setter called")
        this._property = property
    }
    get property(): number {
        console.log("Getter called");
        return this._property
    }
}

function foo (partial: Partial<A>) {
    partial.property = 42 // setter to be called
    console.log(partial.property) // getter to be called
}

foo ({property: 1}) // No getter or setter from class A is called
// 42 is printed as object literal has its own setter and getter

#### 5.3.4 Required Utility Type

Type Required<T> is opposite to Partial<T>, and constructs a type with all properties of T set to required (i.e., not optional). T must be a class or an interface type, otherwise a compile-time error occurs. No method (not even any getter or setter) of T is part of the Required<T> type. Its usage is represented in the example below:

interface Issue {
    title?: string
    description?: string
}
let c: Required<Issue> = { // CTE: 'description' should be defined

(continues on next page)
