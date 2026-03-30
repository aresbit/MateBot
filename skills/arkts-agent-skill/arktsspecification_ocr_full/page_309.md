A compile-time error occurs if the name of a function with receiver is the same as the name of an accessible (see Accessible) instance method or field of the receiver type:

class A {
    foo () { ... }
}
function foo(this: A) { ... } // Compile-time error to prevent ambiguity below
(new A).foo()

A compile-time error occurs if an attempt is made to call a function with receiver from a derived class variable:

class B extends A {
    const b = new B
    b.foo()  // Compile-time error
    foo (b)  // OK
}

Function with receiver cannot have the same name as a global function. Otherwise, a compile-time error occurs.

function foo(this: A) { ... }
function foo() { ... } // Compile-time error

Function with receiver can be generic as in the following example:

function foo<T>(this: B<T>, p: T) {
    console.log(p)
}

function demo(p1: B<SomeClass>, p2: B<BaseClass>) {
    p1.foo(new SomeClass())
        // Type inference should determine the instantiating type
    p2.foo<BaseClass>(new DerivedClass())
        // Explicit instantiation
}

Functions with receiver are dispatched statically. What function is being called is known at compile time based on the receiver type specified in the declaration. A function with receiver can be applied to the receiver of any derived class until it is overridden within the derived class:

class Base { ... }
class Derived extends Base { ... }

function foo(this: Base) { console.log("Base.foo is called") }

let b: Base = new Base()

b.foo() // `Base.foo is called` to be printed
b = new Derived()

b.foo() // `Base.foo is called` to be printed

A function with receiver can be defined in a module other than the one that defines the receiver type. This is represented in the following examples:

// file a.ets
class A {
    foo() { ... }
}

(continues on next page)
