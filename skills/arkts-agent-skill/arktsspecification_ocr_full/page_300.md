(continued from previous page)

bar(n?: string): void
  overload goo { foo, bar }
}

function example(i: I) {
  i.goo()     // calls i.foo()
  i.goo("hello")  // calls i.bar("hello")
  i.bar()       // explicit call: i.bar(undefined)
}

An overload alias is used like an ordinary interface method, except that in a call it is replaced at compile time by one of overloaded methods by using the type of object reference.

A class that implements an interface with an overload alias usually implements all interface methods, except those having a default body (see Default Interface Method Declarations):

// Using interface overload declaration
class C implements I {
    foo(): void {/*body*/}
    bar(n?: string): void {/*body*/}
}

let c = new C()
c.goo() // calls c.foo()

An interface overload alias can be overridden in a class. In this case, the overload declaration in the class must contain all methods overloaded in the interface. Otherwise, a compile-time error occurs.

class D implements I {
    foo(): void {/*body*/}
    bar(n?: string): void {/*body*/}
    overload goo(bar, foo) // order is changes
}

let d = new D()
d.goo() // d.bar(undefined) is used, as it is the first appropriate method

An overload alias defined in a superinterface can be overridden in a subinterface. In this case, the overload declaration of the subinterface must contain all methods overloaded in superinterface. Otherwise, a compile-time error occurs.

The overload alias defined in superinterfaces must be overridden in a subinterface if several overload declarations for the same alias are inherited into the interface, otherwise a compile-time error occurs.

interface I1 {
    overload foo {f1, f2}
    // f1 and f2 are declared in I1
}

interface I2 {
    overload foo {f3, f4}
    // f3 and f4 are declared in I2
}

interface I3 extends I1, I2 {
    // compile-time error as no new overload for 'foo' is defined
}

(continues on next page)
