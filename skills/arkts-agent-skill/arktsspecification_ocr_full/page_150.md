function foo(x: Object | null, y: Object | null | undefined) {
    console.log(x == y, x === y)
}

foo(null, undefined) // output: true, false
foo(null, null) // output: true, true

Comparison the values null and undefined directly is also allowed:

console.log(null == undefined) // output: true
console.log(null === undefined) // output: false

### 7.26 Bitwise and Logical Expressions

The bitwise operators and logical operators are as follows:

• AND operator ‘&’;

• Exclusive OR operator ‘^’; and

• Inclusive OR operator '|'.

The syntax of bitwise and logical expression is presented below:

bitwiseAndLogicalExpression:
    expression '&' expression
    | expression '^' expression
    | expression '|' expression
;

These operators have different precedence. The operator '&' has the highest, while '|' has the lowest precedence.

Operators group left-to-right. Each operator is commutative if the operand expressions have no side effects, and associative.

The bitwise and logical operators can compare two operands of a numeric type, or two operands of the boolean type. Otherwise, a compile-time error occurs.

#### 7.26.1 Integer Bitwise Operators

Integer bitwise operators are ‘&’, ‘^’, and ‘|’ applied to operands of numeric types or type bigint.

If the type of one or both operands is double or float, then the operand or operands are truncated first to the appropriate integer type. If the type of any operand is byte or short, then the operand is converted to int. If operands are of different integer types, then the operand of a smaller type is converted to a larger type (see Numeric Types) by using Widening Numeric Conversions. If both operands are of type bigint, then no conversion is required. A compile-time error occurs if one operand of type bigint, and the other operand is of a numeric type.

The resultant type of the bitwise operator is the type of its operands.
