• If neither NaN nor infinity is involved, then the exact mathematical quotient is computed.

If the magnitude of the product is too large to represent, then the operation overflows, and the result is an appropriately signed infinity.

The quotient is rounded to the nearest value in the chosen value set by using the IEEE 754 round-to-nearest mode. The ArkTS programming language requires gradual underflow support as defined by IEEE 754 (see Floating-Point Types and Operations).

The evaluation of a floating-point division operatorத் /' never throws an error despite possible overflow, underflow, division by zero, or loss of information.

The type of the division expression is the ‘largest’ numeric type (see Numeric Types) of its operands.

#### 7.21.3 Remainder

The binary operator ‘%’ yields the remainder of its operands (dividend as the left-hand-side, and divisor as the right-hand-side operand) from an implied division.

The remainder operator in ArkTS accepts floating-point operands (unlike in C and C++).

The remainder operation on integer operands produces a result value, i.e.,  $ (a/b) * b + (a\%b) $ equals a. Numeric type conversion on remainder operation is discussed in Widening Numeric Conversions.

This equality holds even in the special case where the dividend is a negative integer of the largest possible magnitude of its type, and the divisor is -1 (the remainder is then 0). According to this rule, the result of the remainder operation can only be one of the following:

• Negative if the dividend is negative; or

• Positive if the dividend is positive.

The magnitude of the result is always less than that of the divisor.

If the divisor value of integer remainder operator is detected to be 0 during compilation, then a compile-time error occurs. Otherwise, an ArithmeticError is thrown during execution.

The result of a floating-point remainder operation as computed by the operator %' is different than that produced by the remainder operation defined by IEEE 754. The IEEE 754 remainder operation computes the remainder from a rounding division (not a truncating division), and its behavior is different from that of the usual integer remainder operator. On the contrary, ArkTS presumes that the operator %' behaves on floating-point operations in the same manner as the integer remainder operator (comparable to the C library function fmod). The standard library (see Standard Library) routine Math.IEEEremainder can compute the IEEE 754 remainder operation.

The result of a floating-point remainder operation is determined in compliance with the IEEE 754 arithmetic:

• The result is NaN if:

– Either operand is NaN;

– The dividend is infinity;

– The divisor is zero; or

– The dividend is infinity, and the divisor is zero.

• If the result is not NaN, then the sign of the result is the same as the sign of the dividend.

• The result equals the dividend if:

– The dividend is finite, and the divisor is infinity; or
