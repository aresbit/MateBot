• lhsExpression is evaluated to produce a variable. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

• If the evaluation completes normally, then the value of lhsExpression is saved, and rhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, then the saved value of the left-hand-side variable, and the value of rhsExpression are used to perform the binary operation as indicated by the compound assignment operator. If the operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, then the result of the binary operation converts to the type of the left-hand-side variable. The result of such conversion is stored into the variable.

2. If lhsExpression is an array reference expression (see Array Indexing Expression), then:

• Array reference subexpression of lhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, the index subexpression, and rhsExpression are not evaluated, and no assignment occurs.

• If the evaluation completes normally, then the index subexpression of lhsExpression is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, rhsExpression is not evaluated, and no assignment occurs.

• If the evaluation completes normally, the value of the array reference subexpression refers to an array, and the value of the index subexpression is less than zero, greater than, or equal to the length of the array, then RangeError is thrown. In that case, no assignment occurs.

• If the evaluation completes normally, then the value of the index subexpression is used to select an array element referred to by the value of the array reference subexpression. The value of this element is saved, and then  $ rhsExpression $ is evaluated. If the evaluation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

• If the evaluation completes normally, consideration must be given to the saved value of the array element selected in the previous step. While this element is a variable of type S, and T is type of lhsExpression of the assignment operator determined at compile time:

– If T is a predefined value type, then S is the same as T.

The saved value of the array element, and the value of rhsExpression are used to perform the binary operation of the compound assignment operator.

If this operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

If this evaluation completes normally, then the result of the binary operation converts to the type of the selected array element. The result of the conversion is stored into the array element.

– If T is a reference type, then it must be string.

S must also be a string because the class string is the final class. The saved value of the array element, and the value of rhsExpression are used to perform the binary operation (string concatenation) of the compound assignment operator ‘+=’. If this operation completes abruptly, then so does the assignment expression. In that case, no assignment occurs.

– If the evaluation completes normally, then the string result of the binary operation is stored into the array element.

3. If lhsExpression is a record access expression (see Record Indexing Expression):
