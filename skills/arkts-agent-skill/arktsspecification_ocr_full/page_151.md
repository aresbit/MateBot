The resultant value of ‘&’ is the bitwise AND of the operand values.

The resultant value of ‘^’ is the bitwise exclusive OR of the operand values.

The resultant value of ‘|’ is the bitwise inclusive OR of the operand values.

#### 7.26.2 Boolean Logical Operators

Boolean logical operators are ‘&’, ‘^’, and ‘|’ applied to operands of type boolean.

If both operand values are true, then the resultant value of ‘&’ is true. Otherwise, the result is false. If the operand values are different, then the resultant value of ‘^’ is true. Otherwise, the result is false. If both operand values are false, then the resultant value of ‘|’ is false. Otherwise, the result is true. Thus, boolean logical expression is of the boolean type.

### 7.27 Conditional-And Expression

The conditional-and operator ‘&&’ is similar to ‘&’ (see Bitwise and Logical Expressions) but evaluates its right-hand-side operand only if the value of the left-hand-side operand is true.

The computation results of ‘&&’ and ‘&’ on boolean operands are the same. The right-hand-side operand of ‘&&’ is not necessarily evaluated.

The syntax of conditional-and expression is presented below:

conditionalAndExpression:
expression '&&' expression
;

A conditional-and operator groups left-to-right.

A conditional-and operator is fully associative as regards both the result value and side effects (i.e., the evaluations of the expressions ((a) && (b)) && (c) and (a) && ((b) && (c)) produce the same result, and the same side effects occur in the same order for any a, b, and c).

A conditional-and expression is always of type boolean except the extended semantics (see Extended Conditional Expressions). A conditional-and expression with extended semantics can be of the first expression type.

Each operand of the conditional-and operator must be of type boolean, or of a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

The left-hand-side operand expression is first evaluated at runtime.

If the resultant value is false, then the value of the conditional-and expression is false. The evaluation of the right-hand-side operand expression is omitted.

If the value of the left-hand-side operand is true, then the right-hand-side expression is evaluated. The resultant value is the value of the conditional-and expression.
