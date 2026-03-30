// Code below prints true 4 times
let byte1: byte = 1
let byte2: byte = 1
let long1: long = 1
let float1: float = 1
let double1: double = 1

let res_byte = byte1 * byte2 // int
console.log(res_byte instanceof int)

let res_long = byte1 * long1 // long
console.log(res_long instanceof long)

let res_float = byte1 * float1 // float
console.log(res_float instanceof float)

let res_double = byte1 * double1 // double
console.log(res_double instanceof double)

The result of a unary bitwise complement expression is a value, not a variable (even if the operand expression is a variable).

#### 7.21.1 Multiplication

The binary operator ‘*’ performs multiplication, and returns the product of its operands.

Multiplication is a commutative operation if operand expressions have no side effects.

Integer multiplication is associative when all operands are of the same type.

Floating-point multiplication is not associative.

Type of a multiplication expression is the ‘largest’ (see Numeric Types) type of its operands.

If overflow occurs during integer multiplication, then:

• The result is the low-order bits of the mathematical product as represented in some sufficiently large two's-complement format.

• The sign of the result can be other than the sign of the mathematical product of the two operand values.

A floating-point multiplication result is determined in compliance with the IEEE 754 arithmetic:

• The result is NaN if:

- Either operand is NaN;

– Infinity is multiplied by zero.

• If the result is not NaN, then the sign of the result is as follows:

– Positive, where both operands have the same sign; and

– Negative, where the operands have different signs.

• If infinity is multiplied by a finite value, then the multiplication results in a signed infinity (the sign is determined by the rule above).
