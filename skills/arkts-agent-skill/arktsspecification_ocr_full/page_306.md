#### 17.11.3 Constructor Names

A Constructor Declaration allows a developer to set a name used to explicitly specify constructor to call in New Expressions:

class Temperature{
    // use specified scale:
    constructor Celsius(n: double) {/*body1*/}/
    constructor Fahrenheit(n: double) {/*body2*/}/
}

new Temperature.Celsius(0)
new Temperature.Fahrenheit(32)

If a constructor has a name, then using the constructor directly in a new expression implies using the constructor name explicitly:

class X{
    constructor ctor1(p: number) {/*body1*/}
    constructor ctor2(p: string) {/*body2*/}
}

new X(1) // compile-time error
new X("abs") // compile-time error
new X.ctor1(1) // OK
new X.ctor2("abs") // OK

A compile-time error occurs if a constructor name is used as a named reference (see Named Reference) in any expression.

class X{
    constructor foo() {}
}
const func = X.foo // Compile-time error

The feature is also important for Constructor Overload Declarations.

### 17.12 Default Interface Method Declarations

The syntax of interface default method is presented below:

interfaceDefaultMethodDeclaration:
    'private'? identifier signature block
;

A default method can be explicitly declared private in an interface body.

A block of code that represents the body of a default method in an interface provides a default implementation for any class if such a class does not override the method that implements the interface.
