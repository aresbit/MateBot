The type of unaryExpression is not necessarily the same as the type of the expression provided. Further in the text, the type of unaryExpression is stated explicitly for each unary operator.

#### 7.20.1 Postfix Increment

Postfix increment expression is an expression followed by the increment operator '++'.

The expression must be left-hand-side expression (see Left-Hand-Side Expressions), so it denotes a variable.

A compile-time error occurs if type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a postfix increment expression is the type of the variable. The result of a postfix increment expression is a value, not a variable.

If the evaluation of the operand expression completes normally at runtime, then:

• The value 1 is added to the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the postfix increment expression completes abruptly, and no incrementation occurs.

The value of the postfix increment expression is the value of the variable before a new value is stored.

#### 7.20.2 Postfix Decrement

Postfix decrement expression is an expression followed by the decrement operator ‘--’. The expression must be left-hand-side expression (see Left-Hand-Side Expressions).

A compile-time error occurs if type of the expression is not convertible (see Implicit Conversions) to a numeric type (see Numeric Types).

Type of a postfix decrement expression is the type of the variable. The result of a postfix decrement expression is a value, not a variable.

If evaluation of the operand expression completes at runtime, then:

• The value 1 is subtracted from the value of the variable by using necessary conversions (see Numeric Casting Conversions); and

• The sum is stored back into the variable.

Otherwise, the postfix decrement expression completes abruptly, and no decrementation occurs.

The value of the postfix decrement expression is the value of the variable before a new value is stored.
