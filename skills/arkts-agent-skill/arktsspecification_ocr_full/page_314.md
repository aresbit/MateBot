(continued from previous page)

function foo (i: I) {
    i.lambda(new B) // Argument is to be provided in its usual place
}

#### 17.13.6 Implicit this in Lambda with Receiver Body

Implicit this can be used in the body of lambda expression with receiver when accessing the following:

• Instance methods, fields, and accessors of lambda receiver type (see Receiver Type); or

• Functions with receiver (see Functions with Receiver) of the same receiver type.

In other words, prefix this. in such cases can be omitted. This feature is added to ArkTS to improve DSL support. It is represented in the following examples:

class C {
    name: string = ""
    foo(): void {}
}

function process(context: (this: C) => void) {}

process(
    (this: C): void => {
        this.foo()    // ok - normal call
        foo()    // ok - implicit 'this'
        name = "Bob" // ok - implicit 'this'
    }
)

The same applies if lambda expression with receiver is defined as trailing lambda (see Trailing Lambdas). In this case, lambda signature is inferred from the context:

process() {
    this.foo() // ok - normal call
    foo() // ok - implicit 'this'
}

The example above represents the use of implicit this when calling a function with receiver:

function bar(this: C) {}
function otherBar(this: OtherClass) {}

process() {
    bar()    // ok - implicit 'this'
    otherBar() // compile-time error, wrong type of implicit 'this'
}

If a simple name used in a lambda body can be resolved as instance method, field, or accessor of the receiver type, and as another entity in the current scope at the same time, then a compile-time error occurs to prevent ambiguity and
