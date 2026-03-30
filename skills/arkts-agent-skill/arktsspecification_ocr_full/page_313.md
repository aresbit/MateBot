(continued from previous page)

(' receiverParameter (',' lambdaParameterList?) '')
returnType? '=>' lambdaBody
;

The usage of annotations is discussed in Using Annotations.

The keyword this can be used inside a lambda expression with receiver, It corresponds to the first parameter:

class A { name = "Bob" }

let show = (this: A): void {
    console.log(this.name)
}

Lambda can be called in two syntactical ways represented by the example below:

class A {
    name: string
    constructor (n: string) {
        this.name = n
    }
}

function foo(aa: A[], f: (this: A) => void) {
    for (let a of aa) {
        a.f() // first way
        f(a) // second way
    }
}

let aa: A[] = [new A("aa"), new A("bb"))
foo(aa, (this: A) => { console.log(this.name)}) // output: "aa" "bb"

Note. If lambda expression with receiver is declared in a class or interface, then this use in the lambda body refers to the first lambda parameter and not to the surrounding class or interface. Any lambda call outside a class has to use the ordinary syntax of arguments as represented by the example below:

class B {
    foo() { console.log("foo() from B is called") }
}
class A {
    foo() { console.log("foo() from A is called") }
    bar() {
        let lambda1 = (this: B): void => { this.foo() } // local lambda new B().lambda1()
    }
    lambda2 = (this: B): void => { this.foo() } // class field lambda
}
new A().bar() // Output is 'foo() from B is called'
new A().lambda2 (new B) // Argument is to be provided in its usual place

interface I {
    lambda: (this: B) => void // Property of the function type

(continues on next page)
