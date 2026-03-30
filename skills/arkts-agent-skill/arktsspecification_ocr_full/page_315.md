improve readability.

### 17.14 Trailing Lambdas

The trailing lambda is a special form of notation for function or method call when the last parameter of a function or a method is of function type, and the argument is passed as a lambda using the Block notation. The trailing lambda syntactically looks as follows:

class A {
    foo (f: ()=>void) { ... }
}

let a = new A()
a.foo() { console.log ("method lambda argument is activated") }
// method foo receives last argument as the trailing lambda

The syntax of trailing lambda is presented below:

trailingLambdaCall:
    (objectReference '' identifier typeArguments?)
    | expression ('?.' | typeArguments)?
)
arguments block
;

Currently, no parameter can be specified for the trailing lambda, except a receiver parameter (see Lambda Expressions with Receiver). Otherwise, a compile-time error occurs.

A block immediately after a call is always handled as trailing lambda. A compile-time error occurs if the last parameter of the called entity is not of a function type.

The semicolon ‘;’ separator can be used between a call and a block to indicate that the block does not define a trailing lambda. When calling an entity with the last optional parameter (see Optional Parameters), it means that the call must use the default value of the parameter.

function foo (f := >void) { ... }

foo() { console.log("trailing lambda") }
// 'foo' receives last argument as the trailing lambda

function bar(f?: () => void) { ... }

bar() { console.log("trailing lambda") }
// function 'bar' receives last argument as the trailing lambda,
bar(); { console.log("that is the block code") }
// function 'bar' is called with parameter 'f' set to 'undefined'

function goo(n: number) { ... }

goo() { console.log("aa") } // compile-time error as goo() requires an argument
goo(); { console.log("aa") } // compile-time error as goo() requires an argument
