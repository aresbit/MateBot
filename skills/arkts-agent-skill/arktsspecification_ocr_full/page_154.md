3. If the evaluation completes normally, then  $ rhsExpression $ is evaluated. If this evaluation completes abruptly, then so does the assignment expression, and no assignment occurs.

4. If the evaluation completes normally, but the value of the index subexpression is less than zero, or greater than, or equal to the length of the array, then RangeError is thrown, and no assignment occurs.

5. If lhsExpression denotes indexing of fixed-size array, and the type of rhsExpression is not a subtype of array element type, then ArrayStoreError is thrown, and no assignment occurs.

6. Otherwise, the value of the index subexpression is used to select an element of the array referred to by the value of the array reference subexpression and the value of rhsExpression is converted to the type of the array element. In that case, the result of the conversion is assigned to the array element.

3. If lhsExpression is a record access expression (see Record Indexing Expression), possibly enclosed in parentheses, then:

1. Object reference subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression and the index subexpression are not evaluated, and no assignment occurs.

2. If the evaluation completes normally, the index subexpression of lhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

3. If the evaluation completes normally, rhsExpression is evaluated. If this evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

4. Otherwise, the value of the index subexpression is used as the key, and the value of rhsExpression converted to the type of the record value is used as the value. In that case, the assignment results in storing the key-value pair in the record instance.

If none of the above is true, then the following three steps are performed:

1. lhsExpression is evaluated to produce a variable. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

2. If the evaluation completes normally, then  $ rhsExpression $ is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

3. If that evaluation completes normally, then the value of  $ rhsExpression $ is converted to the type of the left-hand-side variable. In that case, the result of the conversion is assigned to the variable.

#### 7.29.2 Compound Assignment Operators

A compound assignment expression in the form:

lhsExpression op= rhsExpression

is equivalent to

lhsExpression = ((lhsExpression) op (rhsExpression)) as T

where T is type of lhsExpression, except that lhsExpression is evaluated only once.

While the nullish-coalescing assignment (??=) only evaluates the right operand, and assigns to the left operand if the left operand is null or undefined.

An assignment expression can be evaluated at runtime in one of the following ways:

1. If lhsExpression is not an indexing expression:
