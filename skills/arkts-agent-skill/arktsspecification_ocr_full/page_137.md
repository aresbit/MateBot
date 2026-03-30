• long for long and double.

The result of a unary bitwise complement expression is a value, not a variable (even if the result of the operand expression is a variable).

The value of a unary bitwise complement expression at runtime is the bitwise complement of the value of the operand. In all cases,  $ \sim x $ equals  $ (-x)-1 $.

#### 7.20.8 Logical Complement

Logical complement expression is an expression preceded by the operator '!'. Type of the operand expression with the unary '!' operator must be boolean or type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

The unary logical complement expression type is boolean.

The value of a unary logical complement expression is true if the (possibly converted) operand value is false, and false if the operand value (possibly converted) is true.

### 7.21 Multiplicative Expressions

Multiplicative expressions use multiplicative operators ‘*’, ‘/’, and ‘%’.

The syntax of multiplicative expression is presented below:

multiplicativeExpression:
    expression '*' expression
    | expression '/' expression
    | expression '%' expression
    | expression '**' expression
;

Multiplicative operators group left-to-right.

Type of each operand in a multiplicative operator must be convertible (see Numeric Operator Contexts) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

A numeric types conversion (see Widening Numeric Conversions) is performed on both operands to ensure that the resultant type is the type of the multiplicative expression.

The resultant type of an expression is inferred by the largest type after promoting byte and short operands to int:

• double if any operand is double;

• float if any operand is float, and no operand is double;

• long if any operand is long, and no operand is double or float;

• int if all operands are of type byte, short, or int.

This situation is represented in the following example:
