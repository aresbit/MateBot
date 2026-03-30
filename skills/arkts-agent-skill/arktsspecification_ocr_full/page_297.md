class Processor {
    overload process { processNumber, processString }
    processNumber(n: number) {/*body*/}
    processString(s: string) {/*body*/}
}

let c = new C()
c.process(42) // calls processNumber
c.process("aa") // calls processString

Static overload alias is represented in the example below:

class C {
    static one(n: number) {/*body*/}
    static two(s: string) {/*body*/}
    static overload foo { one, two }
}

A compile-time error occurs if:

• Method modifier is used more than once in an method overload declaration;

• Overload alias is:

• Identifier in the overloaded method list does not refer to an accessible method (either declared or inherited) of the current class;

– Static but the overloaded method is not;

– Non-static but the overloaded method is not;

– Marked async but the overloaded method is not; or

– Not async but the overloaded method is.

Overload alias and overloaded methods can have different access modifiers. A compile-time error occurs if the overload alias is:

• public but at least one overloaded method is not public;

• protected but at least one overloaded method is private.

Valid and invalid overload declarations are represented in the example below:

class C {
    private foo1(x: number) {/*body*/}
    protected foo2(x: string) {/*body*/}
    public foo3(x: boolean) {/*body*/}
    foo4() {/*body*/} // implicitly public

    public overload foo { foo3, foo4 } // ok
    protected overload bar { foo2, foo3 } // ok
    private overload goo { foo1, foo2, foo3 } // ok

    public overload err1 {foo2, foo3} // compile-time error, foo2 is not public
    protected overload err2 {foo2, foo1} // compile-time error, foo1 is private
}

Some or all overloaded functions can be native as follows:
