(continued from previous page)

title: "aa"
}

In the example above, type Required<Issue> is transformed to a distinct but analogous type as follows:

interface /*some name*/ {
    title: string
    description: string
}

Type T is not assignable (see Assignability) to Required<T>, and variables of Required<T> are to be initialized with valid object literals.

#### 5.3.5 Readonly Utility Type

Type `Readonly<T>` constructs a type with all properties of T set to `readonly`. It means that the properties of the constructed value cannot be reassigned. T must be a class or an interface type, otherwise a compile-time error occurs. No method (not even any `getter` or `setter`) of T is part of the `Readonly<T>` type. Its usage is represented in the example below:

interface Issue {
    title: string
}

const myIssue: Readonly<Issue> = {
    title: "One"
};

myIssue.title = "Two" // compile-time error: readonly property

Type T is assignable (see Assignability) to Readonly<T>, and allows assignments as a consequence:

class A {
    f1: string = ""
    f2: number = 1
    f3: boolean = true
}
let x = new A
let y: Readonly<A> = x // OK

#### 5.3.6 Record Utility Type

Type Record<K, V> constructs a container that maps keys (of type K) to values of type V.

Type K is restricted to numeric types (see Numeric Types), type string, string literal types and union types constructed from these types.
