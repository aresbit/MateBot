#### 7.20.3 Prefix Increment

Prefix increment expression is an expression preceded by the operator ‘++’. The expression must be left-hand-side expression (see Left-Hand-Side Expressions).

A compile-time error occurs if the type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a prefix increment expression is the type of the variable. The result of a prefix increment expression is a value, not a variable.

If evaluation of the operand expression completes normally at runtime, then:

• The value 1 is added to the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the prefix increment expression completes abruptly, and no incrementation occurs.

The value of the prefix increment expression is the value of the variable after a new value is stored.

#### 7.20.4 Prefix Decrement

Prefix decrement expression is an expression preceded by the operator ‘--’. The expression must be left-hand-side expression (see Left-Hand-Side Expressions).

A compile-time error occurs if type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a prefix decrement expression is the type of the variable. The result of a prefix decrement expression is a value, not a variable.

If evaluation of the operand expression completes normally at runtime, then:

• The value 1 is subtracted from the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the prefix decrement expression completes abruptly, and no decrementation occurs. The value of the prefix decrement expression remains the value of the variable after a new value is stored.

#### 7.20.5 Unary Plus

Unary plus expression is an expression preceded by the operator ‘+’. Type of the operand expression with the unary operator ‘+’ must be convertible (see Implicit Conversions) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

A numeric types conversion is performed on the operand to ensure that the resultant type is that of the unary plus expression. The result of a unary plus expression is always a value, not a variable (even if the result of the operand expression is a variable).
