Numeric widening occurs on the expression before a unary plus operator is applied. The type of the unary plus is determined as follows:

• Type of result is int for byte, short, and int;

• Type of result is the same as that of the initial expression for long, float, and double.

#### 7.20.6 Unary Minus

Unary minus expression is an expression preceded by the operator '-'. Type of the operand expression with the unary operator '-' must be convertible (see Widening Numeric Conversions) to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

Numeric widening occurs on the expression before a unary minus operator is applied. The type of the unary minus is determined as follows:

• Type of result is int for byte, short, and int;

• Type of result is the same as that of the initial expression for long, float, and double.

The result of a unary minus expression is a value, not a variable (even if the result of the operand expression is a variable).

The unary negation operation is always performed on, and the result is drawn from the same value set as the promoted operand value.

Further value set conversions are then performed on the same result.

The value of a unary minus expression at runtime is the arithmetic negation of the promoted value of the operand.

The negation of integer values is the same as subtraction from zero. The ArkTS programming language uses two's-complement representation for integers. The range of two's-complement value is not symmetric. The same maximum negative number results from the negation of the maximum negative int or long. In that case, an overflow occurs but throws no error. For any integer value x, -x is equal to  $ (\sim x)+1 $.

The negation of floating-point values is not the same as subtraction from zero (if x is +0.0, then 0.0-x is +0.0, however -x is -0.0).

A unary minus merely inverts the sign of a floating-point number. Special cases to consider are as follows:

• Operand NaN results in NaN (NaN has no sign).

• Operand infinity results in the infinity of the opposite sign.

• Operand zero results in zero of the opposite sign.

#### 7.20.7 Bitwise Complement

Bitwise complement operator ‘~’ is applied to an operand of a numeric type or type bigint.

If the type of the operand is double or float, then it is truncated first to long or int, respectively. If the type of the operand is byte or short, then the operand is widened to int. If the type of the operand is bigint, then no conversion is required. Type of result is determined as follows:

• int for byte, short, int, and float.
