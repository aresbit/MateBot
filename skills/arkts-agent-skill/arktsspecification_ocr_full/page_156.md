- The object reference subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, the index subexpression and rhsExpression are not evaluated, and no assignment occurs.

• If this evaluation completes normally, then the index subexpression of lhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

• If this evaluation completes normally, the value of the object reference subexpression and the value of index subexpression are saved, then  $ rhsExpression $ is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If this evaluation completes normally, the saved values of the object reference subexpression and index subexpression (as the key) are used to get the value that is mapped to the key (see Record Indexing Expression), then this value and the value of rhsExpression are used to perform the binary operation as indicated by the compound assignment operator. If the operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, then the result of the binary operation is stored as the key-value pair in the record instance (as in Simple Assignment Operator).

#### 7.29.3 Left-Hand-Side Expressions

Left-hand-side expression is an expression that is one of the following:

• Named variable;

• Field or setter resultant from a field access (see Field Access Expression); or

• Array or record element access (see Indexing Expressions).

A compile-time error occurs in the following situations:

• Expression contains the chaining operator ‘?.’ (see Chaining Operator);

• Result of expression is not a variable.

### 7.30 Ternary Conditional Expressions

The ternary conditional expression ‘condition?whenTrue:whenFalse’ uses the boolean value of the first expression (condition) to decide which of other two expressions to evaluate:

ternaryConditionalExpression:
    expression '?' expression ':' expression
;

The ternary conditional operator groups right-to-left (i.e., the meaning of a?b : c?d : e?f : g and a?b : (c?d : (e?f : g)) is the same).

The ternary conditional operator 'condition?whenTrue:whenFalse' consists of three operand expressions with the separators '?' between the first and the second expression, and '?' between the second and the third expression.
