• string if any operand is of type string;

• Type inferred after widening operands of numeric types by the rules explained in the example in Multiplicative Expressions.

#### 7.22.1 String Concatenation

If one operand of an expression is of type string, then the string conversion (see String Operator Contexts) is performed on the other operand at runtime to produce a string.

String concatenation produces a reference to a string object that is a concatenation of two operand strings. The left-hand-side operand characters precede the right-hand-side operand characters in a newly created string.

If the expression is not a constant expression (see Constant Expressions), then a new string object is created (see New Expressions).

#### 7.22.2 Additive Operators for Numeric Types

A numeric types conversion (see Widening Numeric Conversions) performed on a pair of operands ensures that both operands are of a numeric type. If the conversion fails, then a compile-time error occurs.

The binary operator ‘+’ performs addition and produces the sum of such operands.

The binary operator ‘-’ performs subtraction and produces the difference of two numeric operands.

Type of an additive expression performed on numeric operands is the largest type (see Numeric Types) to which operands of that expression are converted (see Multiplicative Expressions for an example).

If the promoted type is int or long, then integer arithmetic is performed. If the promoted type is float or double, then floating-point arithmetic is performed.

If operand expressions have no side effects, then addition is a commutative operation.

If all operands are of the same type, then integer addition is associative.

Floating-point addition is not associative.

If overflow occurs on an integer addition, then:

• Result is the low-order bits of the mathematical sum as represented in a sufficiently large two's-complement format.

• Sign of the result is opposite to that of the mathematical sum of the operands' values.

The result of a floating-point addition is determined in compliance with the IEEE 754 arithmetic as follows:

• The result is NaN if:

– Either operand is NaN; or

– The operands are two infinities of the opposite signs.

• The sum of two infinities of the same sign is the infinity of that sign.

• The sum of infinity and a finite value equals the infinite operand.
