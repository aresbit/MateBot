### 3.10 Type never

Type never is assignable to any type (see Assignability).

• Return type for functions or methods that never return a value, but throw an error when completing an operation.

Type never has no instance. Type never is used as one of the following:

- Type of variables that never get a value (however, an assignment statement with type never in both left-hand and right-hand sides is valid).

• Type of parameters of a function or a method to prevent the body of that function or method from being executed.

function foo () : never {
    throw new Error("foo() never returns")
}

let x : never = foo() // x will never get a value

function bar (p : never) { // body of this
    // function will never be executed
}

bar (foo()) // neither foo nor bar are executed

### 3.11 Type void

Type void is used as a return type to highlight that a function, a method, or a lambda can contain return Statements with no expression, or no return statement at all:

function foo (): void {} // no return at all

class C {
    bar() : void {
        return // with no expression
    }
}

type FunctionWithNoParametersType = () => void

let funcTypeVariable: FunctionWithNoParametersType = () : void => {}

A compile-time error occurs if:

• Type void is used as type annotation;

• Expression of type void is used as a value.

Type void has no instance by itself. However, that it is a supertype of type undefined (see Type undefined) affects the Assignability as follows:
