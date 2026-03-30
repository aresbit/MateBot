• If neither NaN nor infinity is involved, then the exact mathematical product is computed.

The product is rounded to the nearest value in the chosen value set by using the IEEE 754 round-to-nearest mode. The ArkTS programming language requires gradual underflow support as defined by IEEE 754 (see Floating-Point Types and Operations).

If the magnitude of the product is too large to represent, then the operation overflows, and the result is an appropriately signed infinity.

The evaluation of a multiplication operator ‘*’ never throws an error despite possible overflow, underflow, or loss of information.

#### 7.21.2 Division

The binary operatorத் /’ performs division and returns the quotient of its left-hand-side and right-hand-side expressions (dividend and divisor respectively).

Integer division rounds toward 0, i.e., the quotient of integer operands n and d, after a numeric types conversion on both (see Widening Numeric Conversions for details), is the integer value q with the largest possible magnitude that satisfies  $ |d \cdot q| \leq |n| $.

Note. The integer value q is:

• Positive, where  $ |n| \geq |d| $, and  $ n $ and  $ d $ have the same sign; but

• Negative, where  $ |n| \geq |d| $, and  $ n $ and  $ d $ have opposite signs.

The only one special case that does not comply with this rule is where integer overflow occurs. The result equals the dividend if the dividend is a negative integer of the largest possible magnitude for its type, while the divisor is -1. No error is thrown in this case despite the overflow.

However, if the divisor value of integer division is detected to be 0 during compilation, then a compile-time error occurs. Otherwise, an ArithmeticError is thrown during execution.

The result of a floating-point division is determined in compliance with the IEEE 754 arithmetic:

• The result is NaN if:

- Either operand is NaN;

– Both operands are infinity; or

- Both operands are zero.

• If the result is not NaN, then the sign of the result is:

– Positive, where both operands have the same sign; or

– Negative, where the operands have different signs.

• Division produces a signed infinity (the sign is determined by the rule above) if:

– Infinity is divided by a finite value; and

– A nonzero finite value is divided by zero.

• Division produces a signed zero (the sign is determined by the rule above) if:

– A finite value is divided by infinity; and

- Zero is divided by any other finite value.
