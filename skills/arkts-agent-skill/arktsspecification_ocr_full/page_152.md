### 7.28 Conditional-Or Expression

The conditional-or operator ‘||’ is similar to ‘|’ (see Integer Bitwise Operators) but evaluates its right-hand-side operand only if the value of its left-hand-side operand is false.

The syntax of conditional-or expression is presented below:

conditionalOrExpression:
expression '||' expression
;

A conditional-or operator groups left-to-right.

A conditional-or operator is fully associative as regards both the result value and side effects (i.e., the evaluations of the expressions ((a) || (b)) || (c) and (a) || ((b) || (c)) produce the same result, and the same side effects occur in the same order for any a, b, and c).

A conditional-or expression is always of type boolean except the extended semantics (see Extended Conditional Expressions). A conditional-or expression with extended semantics can be of the first expression type.

Each operand of the conditional-or operator must be of type boolean or type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

The left-hand-side operand expression is first evaluated at runtime.

If the resultant value is true, then the value of the conditional-or expression is true, and the evaluation of the right-hand-side operand expression is omitted.

If the resultant value is false, then the right-hand-side expression is evaluated. The resultant value is the value of the conditional-or expression.

The computation results of ‘||’ and ‘|’ on boolean operands are the same, but the right-hand-side operand in ‘||’ cannot be evaluated.

### 7.29 Assignment

All assignment operators group right-to-left (i.e., a = b = c means a = (b = c). The value of c is thus assigned to b, and then the value of b to a).

The syntax of assignment expression is presented below:

assignmentExpression:
lhsExpression assignmentOperator rhsExpression
;
assignmentOperator
: '='
| '+=' | '-=' | '*=' | '=' | '%=' | '**=' | '=/='
| '<<=' | '>>>=' | '>>>='
| '&=' | '|=' | '^='

(continues on next page)
