#### 3.6.2 Integer Types and Operations


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Corresponding Set of Values</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>All signed 8-bit integers  $ (-2^{7} \text{ to } 2^{7} - 1) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>All signed 16-bit integers  $ (-2^{15} \text{ to } 2^{15} - 1) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>All signed 32-bit integers  $ (-2^{31} \text{ to } 2^{31} - 1) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>All signed 64-bit integers  $ (-2^{63} \text{ to } 2^{63} - 1) $</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bigint</td><td style='text-align: center; word-wrap: break-word;'>All integers with no limits</td></tr></table>

ArkTS provides a number of operators to act on integer values as discussed below.

• Comparison operators that produce a value of type boolean:

- Numeric relational operators ‘<’, ‘<=’, ‘>’, and ‘>=’ (see Numeric Relational Operators);

- Numeric equality operators ‘==’ and ‘!=’ (see Numeric Equality Operators);

• Numeric operators that produce values of types int, long, or bigint:

– Unary plus ‘+’ and minus ‘-’ operators (see Unary Plus and Unary Minus);

– Multiplicative operators ‘*’, ‘/’, and ‘%’ (see Multiplicative Expressions);

– Additive operators ‘+’ and ‘-’ (see Additive Expressions);

– Increment operator ‘++’ used as prefix (see Prefix Increment) or postfix (see Postfix Increment);

- Decrement operator ‘--’ used as prefix (see Prefix Decrement) or postfix (see Postfix Decrement);

- Signed and unsigned shift operators ‘<<’, ‘>>’, and ‘>>>’ (see Shift Expressions);

– Bitwise complement operator ‘~’ (see Bitwise Complement);

– Integer bitwise operators ‘&’, ‘^’, and ‘|’ (see Integer Bitwise Operators);

• Ternary conditional operator '?' : ' (see Ternary Conditional Expressions);

- String concatenation operator ‘+’ (see String Concatenation) that, if one operand is string and the other is of an integer type, converts the integer operand to string with the decimal form, and then creates a concatenation of the two strings as a new string.

If either operand of a binary integer operation except Shift Expressions is of type long and the other operand is of a lesser type, then numeric conversion (see Widening Numeric Conversions) is used to widen the second operand first to type long. In this case:

• Operation implementation uses 64-bit precision; and

• Result of the numeric operator is of type long.

If otherwise neither operand is of type long and any operand is of a type other than int, then numeric conversion is used to widen the latter first to type int. In this case:

• Operation implementation uses 32-bit precision; and

• Result of the numeric operator is of type int.

Conversions between integer types and type boolean are not allowed. However, the value of integer type can be used as a logical condition in some cases (see Extended Conditional Expressions)

The integer operators cannot indicate an overflow or an underflow.

An integer operator can throw ArithmeticError if the right-hand-side operand of an integer division operator ‘/’ (see Division) and an integer remainder operator ‘%’ (see Remainder) is zero. The situation is discussed in Error Handling.

Predefined constructors, methods, and constants for integer types are parts of the ArkTS Standard Library.
