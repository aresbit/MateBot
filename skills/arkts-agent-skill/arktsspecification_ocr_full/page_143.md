• The sum of two zeros of opposite sign is positive zero.

• The sum of two zeros of the same sign is zero of that sign.

• The sum of zero and a nonzero finite value is equal to the nonzero operand.

• The sum of two nonzero finite values of the same magnitude and opposite sign is positive zero.

• If infinity, zero, or  $ \mathrm{NaN} $ are not involved, and the operands have the same sign or different magnitudes, then the exact sum is computed mathematically.

If the magnitude of the sum is too large to represent, then the operation overflows. The result is an appropriately signed infinity.

Otherwise, the sum is rounded to the nearest value within the chosen value set by using the IEEE 754 round-to-nearest mode. The ArkTS programming language requires gradual underflow support as defined by IEEE 754 (see Floating-Point Types and Operations).

When applied to two numeric type operands (see Numeric Types), the binary operator '-' performs subtraction, and returns the difference of such operands (minuend as left-hand-side, and subtrahend as the right-hand-side operand).

The result of a-b is always the same as that of  $ a+(-b) $ in both integer and floating-point subtraction.

The subtraction from zero for integer values is the same as negation. However, the subtraction from zero for floating-point operands and negation is not the same (if x is +0.0, then 0.0-x is +0.0; however -x is -0.0).

The evaluation of a numeric additive operator never throws an error despite possible overflow, underflow, or loss of information.

### 7.23 Shift Expressions

Shift expressions use shift operators ‘<<’ (left shift), ‘>>’ (signed right shift), and ‘>>>’ (unsigned right shift). The value to be shifted is the left-hand-side operand in a shift operator, and the right-hand-side operand specifies the shift distance.

The syntax of shift expression is presented below:

shiftExpression:
    expression '<<' expression
    | expression '>>' expression
    | expression '>>>' expression
;

Shift operators group left-to-right.

Both operands of a shift expression must be of numeric types or type bigint.

If the type of one or both operands is double or float, then the operand or operands are truncated first to long or int, respectively. If the type of the left-hand-side operand is byte or short, then the operand is converted to int. If both operands are of type bigint, then no conversion is required. A compile-time error occurs if one operand is type bigint, and the other one is a numeric type. Also, a compile-time error occurs if ‘>>>’ (unsigned right shift) is applied to operands of type bigint.

The result of a shift expression is of the type to which its first operand converted.
