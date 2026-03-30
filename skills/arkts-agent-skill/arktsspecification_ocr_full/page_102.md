let readonly_array: readonly number[] = [1, 2, 3]

foo1(readonly_array) // OK

foo2(readonly_array) // compile-time error

function foo1 (p: readonly number[]) {}

function foo2 (p: number[]) {}

let writable_array: number [] = [1, 2, 3]

foo1 (读写able_array) // OK, as always safe

#### 7.1.2 Normal and Abrupt Completion of Expression Evaluation

Each expression in a normal mode of evaluation requires certain computational steps. Normal modes of evaluation for each kind of expression are described in the following sections.

An expression evaluation completes normally if all computational steps are performed without throwing an error.

On the contrary, an expression evaluation completes abruptly if an error is thrown in the process. The information on the cause of an abrupt completion is provided in the value attached to the error object.

Runtime errors can occur as a result of expression or operator evaluation as follows:

• If the value of an array index expression is negative, or greater than, or equal to the length of the array, then an array indexing expression (see Array Indexing Expression) throws RangeError.

• If the type of a value being assigned to a fixed-size array element is not a subtype of an array element type, then an Assignment throws ArrayStoreError.

• If a Cast Expression conversion cannot be performed at runtime, then it throws ClassCastError.

• If a right-hand expression has the zero value, then the integer division or integer remainder (see Division and Remainder) operator throws ArithmeticError.

An error during the evaluation of an expression can be caused by a possible hard-to-predict and hard-to-handle linkage and virtual machine error.

Abrupt completion of the evaluation of a subexpression results in the following:

• Immediate abrupt completion of an expression that contains the subexpression (if the evaluation of the contained subexpression is required for the evaluation of the entire expression); and

• Cancellation of all subsequent steps of the normal mode of evaluation.

The terms complete normally and complete abruptly can also denote normal and abrupt completion of the execution of a statement (see Normal and Abrupt Statement Execution). A statement can complete abruptly for many reasons in addition to an error being thrown.
