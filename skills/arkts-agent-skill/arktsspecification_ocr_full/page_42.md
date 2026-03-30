#### 3.6.3 Floating-Point Types and Operations


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Corresponding Set of Values</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>The set of all IEEE  $ 754^{3} $ 32-bit floating-point numbers</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number, double</td><td style='text-align: center; word-wrap: break-word;'>The set of all IEEE 754 64-bit floating-point numbers</td></tr></table>

ArkTS provides a number of operators to act on floating-point type values as discussed below.

• Comparison operators that produce a value of type boolean:

- Numeric relational operators ‘<’, ‘<=’, ‘>’, and ‘>=’ (see Numeric Relational Operators);

- Numeric equality operators ‘==’ and ‘!=’ (see Numeric Equality Operators);

• Numeric operators that produce values of type float or double:

– Unary plus ‘+’ and minus ‘-’ operators (see Unary Plus and Unary Minus);

– Multiplicative operators ‘*’, ‘/’, and ‘%’ (see Multiplicative Expressions);

– Additive operators ‘+’ and ‘-’ (see Additive Expressions);

– Increment operator ‘++’ used as prefix (see Prefix Increment) or postfix (see Postfix Increment);

– Decrement operator ‘--’ used as prefix (see Prefix Decrement) or postfix (see Postfix Decrement);

• Numeric operators that produce values of type int or long:

– Signed and unsigned shift operators ‘<<’, ‘>>’, and ‘>>>’ (see Shift Expressions);

– Bitwise complement operator ‘~’ (see Bitwise Complement);

– Integer bitwise operators ‘&', ‘^', and ‘|’ (see Integer Bitwise Operators);

• Ternary conditional operator ‘? : ‘(see Ternary Conditional Expressions);

• The string concatenation operator ‘+’ (see String Concatenation) that, if one operand is of type string and the other is of a floating-point type, converts the floating-point type operand to type string with a value represented in the decimal form (without loss of information), and then creates a concatenation of the two strings as a new string.

An operation is called a floating-point operation if at least one of the operands in a binary operator is of a floating-point type (even if the other operand is integer), and that is not a string concatenation.

If at least one operand of the numeric operator is of type double, then the operation implementation uses the 64-bit floating-point arithmetic. The result of the numeric operator is a value of type double.

If the other operand is not of type double, then the numeric conversion (see Widening Numeric Conversions) is used to widen the operand first to type double.

If neither operand is of type double, then the operation implementation is to use the 32-bit floating-point arithmetic. The result of the numeric operator is a value of type float.

If the other operand is not of type float, then the numeric conversion is used to widen the operator first to type float.

Any floating-point type value can be cast to or from any numeric type (see Numeric Types).

Conversions between floating-point types and type boolean are not allowed. However, the value of floating-point type can be used as a logical condition in some cases (see Extended Conditional Expressions)
