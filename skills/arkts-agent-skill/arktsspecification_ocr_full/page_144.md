If the left-hand-side operand is of the promoted type int, then only five lowest-order bits of the right-hand-side operand specify the shift distance (as if using a bitwise logical AND operator ‘&’ with the mask value 0x1f or 0b111111 on the right-hand-side operand). Thus, it is always within the inclusive range of 0 through 31.

If the left-hand-side operand is of the promoted type long, then only six lowest-order bits of the right-hand-side operand specify the shift distance (as if using a bitwise logical AND operator ‘&’ with the mask value 0x3f or 0b111111 the right-hand-side operand). Thus, it is always within the inclusive range of 0 through 63.

Shift operations are performed on the two's-complement integer representation of the value of the left-hand-side operand at runtime.

The value of  $ n \ll s $ is  $ n $ left-shifted by  $ s $ bit positions. It is equivalent to multiplication by two to the power  $ s $ even in case of an overflow.

The value of  $ n \gg s $ is  $ n $ right-shifted by  $ s $ bit positions with sign-extension. The resultant value is  $ floor(n/2s) $. If  $ n $ is non-negative, then it is equivalent to truncating integer division (as computed by the integer division operator by 2 to the power  $ s $).

The value of  $ n \gg \gg $ is n right-shifted by s bit positions with zero-extension, where:

• If n is positive, then the result is the same as that of  $ n \gg s $.

• If $n$ is negative, and type of the left-hand-side operand is int, then the result is equal to that of the expression ($n \gg s$) + (2 \ll \sim s)$.

• If $n$ is negative, and type of the left-hand-side operand is long, then the result is equal to that of the expression $(n>>s)+((2\ as\ long)\ <<\sim s)$.

### 7.24 Relational Expressions

Relational expressions use relational operators ‘<’, ‘>’, ‘<=’, and ‘>=’.

The syntax of relational expression is presented below:

relationalExpression:
    expression <' expression
    | expression '>' expression
    | expression <=' expression
    | expression >=' expression
;

Relational operators group left-to-right.

A relational expression is always of type boolean.

The four kinds of relational expressions are described below. The kind of a relational expression depends on types of operands. It is a compile-time error if at least one type of operands is different from types described below.
