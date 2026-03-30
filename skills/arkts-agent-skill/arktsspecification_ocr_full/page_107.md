### 7.4 Array Literal

Array literal is an expression that can be used to create an array or tuple in some cases, and to provide some initial values.

The syntax of array literal is presented below:

arrayLiteral:
    [' expressionSequence? '']
;
expressionSequence:
    expression (',' expression)* ','?
;

An array literal is a comma-separated list of initializer expressions enclosed in square brackets ‘[’ and ‘]’. A trailing comma after the last expression in an array literal is ignored:

let x = [1, 2, 3] // ok
let y = [1, 2, 3, ] // ok, trailing comma is ignored

The number of initializer expressions enclosed in square brackets of the array initializer determines the length of the array to be constructed.

If memory is allocated as required for an array literal, then an array of the specified length is created, and all elements of the array are initialized to the values specified by initializer expressions.

On the contrary, the evaluation of an array literal expression completes abruptly if:

• Not enough memory is available for a new array, and OutOfMemoryError is thrown; or

• Some initialization expression completes abruptly.

Initializer expressions are executed from left to right. The  $ n' $th expression specifies the value of the  $ n-1' $th element of the array.

Array literals can be nested (i.e., the initializer expression that specifies an array element can be an array literal if that element is of array type).

Type of an array literal expression is inferred by the following rules:

• If a context is available, then type is inferred from the context. If successful, then type of an array literal is the inferred type T[], Array<T>, or tuple.

• Otherwise, type is inferred from the types of array literal elements.

More details of both cases are presented below.

#### 7.4.1 Array Literal Type Inference from Context

Type of an array literal can be inferred from the context, including explicit type annotation of a variable declaration, left-hand part type of an assignment, call parameter type, or type of a cast expression:

let a: number[] = [1, 2, 3] // ok, variable type is used
a = [4, 5] // ok, variable type is used

(continues on next page)
