class A {...}

type FA = (this: A) => boolean
type FN = (this: number[], max: number) => number

Function type with receiver can be generic as in the following example:

class B<T> {...}

type FB<T> = (this: B<T>, x: T): void
type FBS = (this: B<string>, x: string): void

The usual rule of function type compatibility (see Subtyping for Function Types) is applied to function type with receiver, and parameter names are ignored.

class A {...}

type F1 = (this: A) => boolean
type F2 = (a: A) => boolean

function foo(this: A): boolean {}
function goo(a: A): boolean {}

let f1: F1 = foo // ok
f1 = goo // ok

let f2: F2 = goo // ok
f2 = foo // ok
f1 = f2 // ok

The sole difference is that only an entity of function type with receiver can be used in Method Call Expression. The declarations from the previous example are reused in the example below:

let a = new A()
a.f1() // ok, function type with receiver
f1(a) // ok

a.f2() // compile-time error
f2(a) // ok

#### 17.13.5 Lambda Expressions with Receiver

Lambda expression with receiver defines an instance of a function type with receiver (see Function Types with Receiver). It looks almost the same as an ordinary lambda expression (see Lambda Expressions), except that the first parameter is mandatory, and the keyword this is used as its name:

The syntax of lambda expression with receiver is presented below:

lambdaExpressionWithReceiver:
    annotationUsage?

(continues on next page)
