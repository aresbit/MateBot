enum StringEnum { a = "a", b = "b", c = "c"}
let string_enum: StringEnum = StringEnum.a
let a_string: string = string_enum // a_string will get the value of "a"

A value of enumeration type with an explicitly declared type of constants is converted to the declared type. This conversion never causes a runtime error.

enum DoubleEnum: double {a = 1.0, b = 2.0, c = 3.141592653589}
let dbl_enum: DoubleEnum = DoubleEnum.a
let dbl_value: double = dbl_enum // dbl_value will get the value of 1.0

### 6.5 Numeric Casting Conversions

A numeric casting conversion occurs if the target type and the expression type are both numeric. The context for a numeric casting conversion is where conversion methods are used as defined in the standard library (see Standard Library).

The explicit use of methods for numeric cast conversions is represented in the following example:

function process_int(an_int: int) { /* ... */ }

let pi = 3.14
process_int(pi.toInt())

A numeric casting conversion never causes a runtime error.

Numeric casting conversion of an operand of type double to target type float is performed in compliance with the IEEE 754 rounding rules. This conversion can lose precision or range, resulting in the following:

• Float zero from a nonzero double; and

• Float infinity from a finite double.

Double NaN is converted to float NaN.

Double infinity is converted to the same-signed floating-point infinity.

A numeric conversion of a floating-point type operand to target types long or int is performed by the following rules:

• If the operand is NaN, then the result is 0 (zero).

• If the operand is positive infinity, or if the operand is too large for the target type, then the result is the largest representable value of the target type.

• If the operand is negative infinity, or if the operand is too small for the target type, then the result is the smallest representable value of the target type.

• Otherwise, the result is the value that rounds toward zero by using IEEE 754 round-toward-zero mode.

A numeric casting conversion of a floating-point type operand to types byte or short is performed in two steps as follows:

• The casting conversion to int is performed first (see above);

• Then, the int operand is cast to the target type.
