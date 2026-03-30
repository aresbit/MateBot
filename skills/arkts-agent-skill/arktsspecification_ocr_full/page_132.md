Expression Type
Code Example

Object
function f(o: Object) {
    typeof o
}

union type
function f(p: A | B) {
    typeof p
}

type parameter
class A<T|null|undefined> {
    f: T
    m() {
        typeof this.f
    }
    constructor(p: T) {
        this.f = p
    }
}

### 7.18 Ensure-Not-Nullish Expression

Ensure-not-nullish expression is a postfix expression with the operator '!'. An ensure-not-nullish expression in the expression e! checks whether e of a nullish type (see Nullish Types) evaluates to a nullish value.

The syntax of ensure-not-nullish expression is presented below:

ensureNotNullishExpression: expression '!'

If the expression e is not of a nullish type, then the operator '!' has no effect.

If the result of the evaluation of e is not equal to null or undefined, then the result of e! is the outcome of the evaluation of e.

If the result of the evaluation of e is equal to null or undefined, then NullPointerError is thrown.

Type of ensure-not-nullish expression is the non-nullish variant of type of e.
