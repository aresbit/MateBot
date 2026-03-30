Future compiler implementations are to infer the return type in more cases. Type inference is represented in the example below:

// Explicit return type
function foo(): string { return "foo" }

// Implicit return type inferred as string
function goo() { return "goo" }

class Base {}
class Derived1 extends Base {}
class Derived2 extends Base {}

function bar (condition: boolean) {
    if (condition)
        return new Derived1()
    else
        return new Derived2()
}

// Return type of bar will be Derived1/Derived2 union type
function boo (condition: boolean) {
    if (condition) return 1
}

// That is a compile-time error as there is an execution path with no return

If the compiler fails to recognize a particular type inference case, then a corresponding compile-time error occurs.
