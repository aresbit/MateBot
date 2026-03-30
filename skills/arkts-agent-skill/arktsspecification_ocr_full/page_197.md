#### 9.7.1 Static Methods

A method declared in a class with the modifier static is a static method.

A compile-time error occurs if:

• The method declaration contains another modifier (abstract, final, or override) along with the modifier static.

Static methods are always called without reference to a particular object. As a result, a compile-time error occurs if the keywords this or super are used inside a static method.

Static methods can be inherited from a superclass or shadowed by name regardless of the their signature:

• The header or body of a class method includes the name of a type parameter of the surrounding declaration.

class Base {
    static foo() { console.log("static foo() from Base") }
    static bar() { console.log("static foo() from Base") }
}

class Derived extends Base {
    static foo(p: string) { console.log("static foo() from Derived") }
}

Base.foo() // Output: static foo() from Base
Base.bar() // Output: static foo() from Base
Derived.bar() // Output: static foo() from Base, bar() is inherited
Derived.foo("a string") // Output: static foo() from Derived, foo() is shadowed
Derived.foo() // compile-time error as foo() in Derived has shadowed Base.
→foo()

Note: class static methods may access protected or private members of the same class type or derived one represented as parameters or local variables:

class C {
    protected count1: number
    private count2: number
    static getCount(c: C): number {
        const local_c = new C
        return c.count1 + c.count2 + local_c.count1 + local_c.count2 // OK
    }
    static handleDerived (b: B) {
        b.count1 + b.count2 // OK
    }
}
class B extends C {
    static dealWithProtected (b: B) {
        b.count1 // OK
        b.count2 // compile-time error
    }
}
C.getCount (new C) // will return the sum of counts
C.handleDerived (new B) // will work with protected and private fields
