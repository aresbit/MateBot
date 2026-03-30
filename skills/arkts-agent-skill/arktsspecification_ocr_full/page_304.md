class C {
    foo(n: number): number {/*body*/}
}

class D implements C {
    fooString(s: number): string {/*body*/}
    overload foo { foo, fooString }
}

let d = new D()
let c: C = d

let func1 = c.foo // method 'foo' is used
let func2 = d.foo // method 'foo' is used, not overload alias

A compile-time error occurs if the name of an overload alias is the same as the name of a method (with the same static or non-static modifier) that is not listed as an overloaded method as follows:

class C {
    foo(n: number) {/*body*/}
    fooString(s: number) {/*body*/}
    fooBoolean(b: boolean) {/*body*/}

    overload foo { // compile-time error
        fooBoolean, fooString
    }
}

### 17.10 Native Functions and Methods

#### 17.10.1 Native Functions

Native function is a function marked with the keyword native (see Function Declarations).

Native function implemented in a platform-dependent code is typically written in another programming language (e.g., C). A compile-time error occurs if a native function has a body.
