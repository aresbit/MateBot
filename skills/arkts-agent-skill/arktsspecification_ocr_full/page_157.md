A compile-time error occurs if the first expression is not of type boolean, or a type mentioned in Extended Conditional Expressions.

Type of the ternary conditional expression is determined as the union of types of the second and the third expressions further normalized in accordance with the process discussed in Union Types Normalization. If the second and the third expressions are of the same type, then this is the type of the conditional expression.

The following steps are performed as the evaluation of a ternary conditional expression occurs at runtime:

1. The first operand (condition) of a ternary conditional expression is evaluated first.

2. If the value of the first operand is true, then the second operand expression (whenTrue) is evaluated. Otherwise, the third operand expression (whenFalse) is evaluated. The result of successful evaluation is the result of the ternary conditional expression.

The examples below represent different scenarios with standalone expressions:

class A {}
class B extends A {}

condition ? new A() : new B() // A | B => A

condition ? 5 : 6 // int

condition ? "5" : 6 // "5" | int

### 7.31 String Interpolation Expressions

'String interpolation expression' is a multiline string literal, i.e., a string literal delimited with backticks (see Multiline String Literal for detail) that contains at least one embedded expression.

The syntax of string interpolation expression is presented below:

stringInterpolation:
    ''' (BacktickCharacter | embeddedExpression)* ' '
;
embeddedExpression:
    '${' expression ' }'
;

An ‘embedded expression’ is an expression specified inside curly braces preceded by the dollar sign ‘$’. A string interpolation expression is of type string (see Type string).

When evaluating a string interpolation expression, the result of each embedded expression substitutes that embedded expression. An embedded expression must be of type string. Otherwise, the implicit conversion to string takes place in the same way as with the string concatenation operator (see String Concatenation):

let a = 2
let b = 2
console.log('The result of ${a} * ${b} is ${a * b}')
// prints: The result of 2 * 2 is 4
