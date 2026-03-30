### 7.16 Cast Expression

The syntax of cast expression is as follows:

castExpression: expression 'as' type ;

Cast expression in the form expr as target applies the cast operator as to expr by issuing the value of a specified target type. Thus, the type of a cast expression is always the target type.

class X {}

let x1 : X = new X()
let ob : Object = x1 as Object // Object is the target type
let x2 : X = ob as X // X is the target type

A compile-time error occurs if the target type is type never:

1 as never // compile-time error

A compile-time error occurs if target type is not preserved by Type Erasure.

Two specific cases of a cast expression are described in the sections below:

- Type Inference in Cast Expression if expr is a numeric literal (see Numeric Literals), an Array Literal, or an Object Literal;

• Runtime Checking in Cast Expression otherwise.

If none of conditions stated in these sections are satisfied, then a compile-time error occurs.

#### 7.16.1 Type Inference in Cast Expression

The following combinations of expr and target are considered for the expr as target expression:

• expr is a numeric literal, see Type Inference for Numeric Literals for detail;

- expr is an Array Literal, and target is an array type or a tuple type (see Array Literal Type Inference from Context for detail);

- expr is an Object Literal, and target is class type, interface type, or Record Utility Type (see the subsections of Object Literal for detail).

This kind of a cast expression results in inferring the target type for expr. A compile-time error can occur when processing a cast expression (see corresponding sections for detail), but this expression never causes a runtime error by itself. However, the evaluation of array literal elements or object literal properties can cause a runtime error.

Casting for numeric literals is represented in the example below:

let x = 1 as byte // ok
let y = 128 as byte // compile-time error

Casting for array literals is represented in the example below:
