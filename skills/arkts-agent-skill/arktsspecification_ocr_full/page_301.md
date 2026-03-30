(continued from previous page)

interface I4 extends I1, I2 {
    overload foo { f4, f1, f3, f2 } // OK, as new overload is defined
}
interface I5 extends I1, I2 {
    overload foo { f1, f3 } // compile-time error as not all methods are included
}

#### 17.9.4 Constructor Overload Declarations

Constructor overload declaration allows declaring an overload alias and setting an order of constructors for a call in a new expression.

The syntax is presented below:

overloadConstructorDeclaration:
'overload' 'constructor'、「'identifier (',' 'identifier)*', '?' '};

This feature can be used if there are more than one constructors declared in the class, and maximum one of them is anonymous (see Constructor Names).

Only a single constructor overload declaration is allowed in a class. Otherwise, a compile-time error occurs.

Overload alias for constructors is used the same way as anonymous constructor (see New Expressions).

The use of a constructor overload declaration is represented in the example below:

class BigFloat {
    constructor fromNumber(n: number) {/*body1*/}
    constructor fromString(s: string) {/*body2*/}

    overload constructor { fromNumber, fromString }
}

new BigFloat(1) // fromNumber is used
new BigFloat("3.14") // fromString is used

If a class has an anonymous constructor it is implicitly placed at first position in a list of overloaded constructors:

class C {
    constructor () { /*body*/ }
    constructor fromString(s?: string) { /*body*/ }

    overload constructor { fromString }
}

new C() // anonymous constructor is used
new C("abc") // fromString is used
new C.fromString("aa") // fromString is explicitly used
