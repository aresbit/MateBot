### 7.19 Nullish-Coalescing Expression

Nullish-coalescing expression is a binary expression that uses the operator ‘??’.

The syntax of nullish-coalescing expression is presented below:

nullishCoalescingExpression: expression '??' expression ;

A nullish-coalescing expression checks whether the evaluation of the left-hand-side expression equals the nullish value:

• If so, then the right-hand-side expression evaluation is the result of a nullish-coalescing expression.

• If not so, then the result of the left-hand-side expression evaluation is the result of a nullish-coalescing expression, and the right-hand-side expression is not evaluated (the operator ‘??’ is thus lazy).

The type of a nullish-coalescing expression is a normalized union type (see Union Types) formed from the following:

• Non-nullish variant of the type of the left-hand-side expression; and

• Type of the right-hand-side expression.

The semantics of a nullish-coalescing expression is represented in the following example:

let x = lhs_expression ?? rhs_expression

let x$ = lhs_expression

if (x$ == null) {x = rhs_expression} else x = x$!

// Type of x is NonNullishType(LHS_expression) | Type(rhs_expression)

A compile-time error occurs if the nullish-coalescing operator is mixed with conditional-and or conditional-or operators without parentheses.

### 7.20 Unary Expressions

The syntax of unary expression is presented below:

unaryExpression:
  expression '++'
  | expression '--'
  | '++' expression
  | '--' expression
  | '+' expression
  | '-' expression
  | '~' expression
  | '!' expression
;

All expressions with unary operators (except postfix increment and postfix decrement operators) group right-to-left for ‘~+x’ to have the same meaning as ‘~(+)’.
