• Lambda expression parameter type (see Lambda Signature);

• Array literal type inference (see Array Literal Type Inference from Context, and Array Type Inference from Types of Elements);

• Object literal type inference (see Object Literal);

• Smart types (see Smart Types).

#### 15.7.1 Type Inference for Numeric Literals

The type of expression of a numeric type for Constant Expressions is first evaluated from the expression as follows:

• Type of an integer literal is the default type of the literal: int or long (see Integer Literals);

• Type of a floating-point literal is the default type of the literal: double or float (see Floating-Point Literals);

• Type of a named constant is specified in the constant declaration;

• Result type of an operator is evaluated according to the rules of the operator;

• Type of a Cast Expression is specified in the expression target type.

The evaluated numeric result type can be inferred to a numeric target type from the context on condition that:

1. Last executed operator in the expression is not a cast operator as;

2. Target type is a numeric type larger than the evaluated result type; or

3. The evaluated result type is an integer type, the target type is a smaller integer type with the value of the expression fitting into its range; or

4. The target type is float, the evaluated result type is double and the value of the expression fits into the range of type float.

A compile-time error occurs if the context is a union type, and the evaluated value can be treated as value of several of union component types.

Valid and invalid narrowing is represented in the examples below:

let b: byte = 127 // ok, int -> byte narrowing
b = 64 + 63 // ok, int -> byte narrowing
b = 128 // compile-time-error, value is out of range
b = 1.0 // compile-time-error, floating-point value cannot be narrowed
b = 1 as short // // compile-time-error, cast expression fixes 'short' type

let s: short = 32768 // compile-time-error, value is out of range

let u: byte | int = 1 // compile-time error, ambiguity
