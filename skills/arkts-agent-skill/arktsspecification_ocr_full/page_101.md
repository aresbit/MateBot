• Value (results found elsewhere).

A variable or a value are equally considered the value of the expression if such a value is required for further evaluation.

The type of an expression is determined at compile time (see Type of Expression).

Expressions can contain assignments, increment operators, decrement operators, method calls, and function calls. The evaluation of an expression can produce side effects as a result.

Constant expressions (see Constant Expressions) are the expressions with values that can be determined at compile time.

#### 7.1.1 Type of Expression

Every expression in the ArkTS programming language has a type. The type of an expression is determined at compile time.

In most contexts, an expression must be compatible with the type expected in a context. This type is called target type. If no target type is available in a context, then the expression is called a standalone expression:

let a = expr // no target type is available

function foo() {
    expr // no target type is available
}

Otherwise, the expression is non-standalone:

let a: number = expr // target type of 'expr' is number

function foo(s: string) {}
foo(expr) // target type of 'expr' is string

In some cases, the type of an expression cannot be inferred (see Type Inference) from the expression itself (see Object Literal as an example). If such an expression is used as a standalone expression, then a compile-time error occurs:

class P { x: number, y: number }

let x = { x: 10, y: 10 } // standalone object literal - compile time error
let y: P = { x: 10, y: 10 } // OK, type of object literal is inferred

The evaluation of an expression type requires completing the following steps:

1. Collect information for type inference (type annotation, generic constraints, etc);

2. Perform Type Inference;

3. If the expression type is not yet inferred at a previous step, and the expression is a literal in the general sense, including Array Literal, then an attempt is made to evaluate the type from the expression itself.

A compile-time error occurs if none of these steps produces an appropriate expression type.

If the expression type is  $ \underline{\text{readonly}} $, then the target type must also be  $ \underline{\text{readonly}} $. Otherwise, a compile-time error occurs:
