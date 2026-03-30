– If the dividend is zero, and the divisor is finite.

• If infinity, zero, or NaN are not involved, then the floating-point remainder  $ r $ from the division of the dividend  $ n $ by the divisor  $ d $ is determined by the mathematical relation  $ r = n - (d \cdot q) $, where  $ q $ is an integer that is only:

– Negative if n/d is negative, or

– Positive if n/d is positive.

• The magnitude of q is the largest possible without exceeding the magnitude of the true mathematical quotient of n and d.

The evaluation of the floating-point remainder operator ‘%’ never throws an error, even if the right-hand operand is zero. Overflow, underflow, or loss of precision cannot occur.

The type of the remainder expression is the 'largest' numeric type (see Numeric Types) of its operands.

#### 7.21.4 Exponentiation

The binary operator ‘**’ yields the result of raising the first operand (base) to the power of the second operand (exponent). The operation returns NaN in the following cases:

• Exponent is NaN;

• Base is NaN, and exponent is not 0;

• Base is  $ \pm1 $, and exponent is  $ \pm\text{Infinity} $; or

• Base is less than 0, and exponent is not an integer.

The binary operator ‘**’ is equivalent to Math.pow(), except it also accepts bigint types as operands.

### 7.22 Additive Expressions

Additive expressions use additive operators '+' and '-'.

The syntax of additive expression is presented below:

additiveExpression:
    expression '+' expression
| expression '-' expression
;

Additive operators group left-to-right.

If either operand of the operator is ‘+’ of type string, then the operation is a string concatenation (see String Concatenation). In all other cases, type of each operand of the operator ‘+’ must be convertible (see Widening Numeric Conversions) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

Type of each operand of the binary operator '-' must be convertible (see Widening Numeric Conversions) to a numeric type (see Numeric Types) in all cases. Otherwise, a compile-time error occurs.

Type of Additive expression is determined as follows:
