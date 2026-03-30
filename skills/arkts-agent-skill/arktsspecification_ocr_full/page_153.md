lhsExpression:
  expression
;
rhsExpression:
  expression
;

The first operand in an assignment operator represented by lhsExpression must be left-hand-side expression (see Left-Hand-Side Expressions). This first operand denotes a variable.

Type of the variable is the type of the assignment expression.

The result of the assignment expression at runtime is not a variable itself but the value of a variable after the assignment.

#### 7.29.1 Simple Assignment Operator

The form of a simple assignment expression is lhsExpression = rhsExpression.

A compile-time error occurs in the following situations:

• Type of rhsExpression is not assignable (see Assignability) to the type of the variable; or

• Type of lhsExpression is one of the following:

– readonly array (see Readonly Parameters), while the converted type of rhsExpression is a non-readonly array;

– readonly tuple (see Readonly Parameters), while the converted type of rhsExpression is a non-readonly tuple.

Otherwise, the assignment expression is evaluated at runtime in one of the following ways:

1. If lhsExpression is a field access expression e.f (see Field Access Expression), possibly enclosed in parentheses, then:

1. lhsExpression e is evaluated: if the evaluation of e completes abruptly, then so does the assignment expression.

2. rhsExpression is evaluated: if the evaluation completes abruptly, then so does the assignment expression.

3. If that evaluation completes normally, then the value of  $ rhsExpression $ is converted to the type of the field. In that case, the result of the conversion is assigned to the field.

2. If the lhsExpression is an array reference expression (see Array Indexing Expression), possibly enclosed in parentheses, then:

1. Array reference subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression and the index subexpression are not evaluated, and no assignment occurs.

2. If the evaluation completes normally, then the index subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.
