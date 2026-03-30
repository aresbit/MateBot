class C {
    native foo1(x: number)
    foo2(x: string) {/*body*/}
    overload foo { foo1, foo2 }
}

An overload alias is used like an ordinary class method except that it is replaced in a call at compile time for one of overloaded methods that use the type of object reference. The overload declaration in subtypes is represented in the example below:

In addition, overriding an overload declaration in a subclass can include new methods and change the order of all methods in the overload declaration.

If a superclass has an overload declaration, then this declaration can be overridden in a subclass. If a subclass does not override an overload declaration, then the declaration from the superclass is inherited.

If a subclass overrides an overload declaration, then this declaration must list all methods of the overload declaration in a superclass. Otherwise, a compile-time error occurs.

class Base {
    overload process { processNumber, processString }
    processNumber(n: number) {/*body*/}
    processString(s: string) {/*body*/}
}

class D1 extends Base {
    // method is overridden
    override processNumber(n: number) {/*body*/}
    // overload declaration is inherited
}

class D2 extends Base {
    // method is added:
    processInt(n: int) {/*body*/}
    // new order for overloaded methods is specified:
    overload process { processInt, processNumber, processString }
}

new D1().process(1) // calls processNumber from D1

new D2().process(1) // calls processInt from D2 (as it is listed earlier)
new D2().process(1.0) // calls processNumber from Base (first appropriate)

Methods with special names (see Indexable Types, Iterable Types, and Callable Types) can be overloaded like ordinary methods:

class C {
    getByNumber(n: number): string {...}
    getByString(s: string): string {...}
    overload $_get { getByNumber, getByString }
}

let c = new C()

(continues on next page)
