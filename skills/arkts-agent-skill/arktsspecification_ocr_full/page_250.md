#### 15.1.2 Specifics of Assignment-like Contexts

Assignment-like context (see Assignment-like Contexts) can be considered as an assignment x = expr, where x is a left-hand-side expression, and expr is a right-hand-side expression. E.g., there is an implicit assignment of expr to the formal parameter foo in the call foo(expr), and implicit assignments to elements or properties in Array Literal and Object Literal.

Assignment-like context is specific in that the type of a left-hand-side expression is known, but the type of a right-hand-side expression is not necessarily known in the context as follows:

• If the type of a right-hand-side expression is known from the expression itself, then the Assignability check is performed as in the example below:

function foo(x: string, y: string) {
    x = y // ok, assignability is checked
}

• Otherwise, an attempt is made to apply the type of the left-hand-side expression to the right-hand-side expression. A compile-time error occurs if the attempt fails as in the example below:

function foo(x: int, y: double[]) {
    x = 1 // ok, type of '1' is inferred from type of 'x'
    y = [1, 2] // ok, array literal is evaluated as [1.0, 2.0]
}

#### 15.1.3 Specifics of Variable Initialization Context

If the variable or a constant declaration (see Variable and Constant Declarations) has an explicit type annotation, then the same rules as for assignment-like contexts apply. Otherwise, there are two cases for let x = expr (see Type Inference from Initializer) as follows:

• The type of the right-hand-side expression is known from the expression itself, then this type becomes the type of the variable as in the example below:

function foo(x: int) {
    let y = x // type of 'y' is 'int'
}

• Otherwise, the type of expr is evaluated as type of a standalone expression as in the example below:

function foo() {
    let x = 1 // x is of type 'int' (default type of '1')
    let y = [1, 2] // x is of type 'number[]'
}
