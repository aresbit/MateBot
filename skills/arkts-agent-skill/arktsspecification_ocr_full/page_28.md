(continued from previous page)

00777 // octal literal
0b101 // binary literal

The underscore character ‘_’ between successive digits can be used to improve readability. Underscore characters in such positions do not change the values of literals. However, the underscore character must be neither the very first nor the very last symbol of an integer literal.

Type of integer literal is determined by using Type Inference for Numeric Literals if its context allows inferring type. Otherwise, the type is determined as follows:

- int if the literal value can be represented by a non-negative 32-bit number, i.e., the value is in the range 0..max(int); or

• long otherwise.

A compile-time error occurs if an integer literal value is too large for the values of type long. The concept is represented by the examples below:

// literals of type int:
0
1
0x7F
0x7FFF_FFFF // max(int)

// literals of type long:
0x8000_0000
0x7FFF_FFFF_1
9223372036854775807 // max(long)

// compile-time error as value is too large:
9223372036854775808 // max(long) + 1
0xFFFF_FFFF_FFFF_0

#### 2.9.3 Floating-Point Literals

Floating-point literals represent decimal numbers and consist of a whole-number part, a decimal point, a fraction part, an exponent, and a float type suffix as follows:

FloatLiteral:
    DecimalIntegerLiteral '' ' FractionalPart? ExponentPart? FloatTypeSuffix?
    | '.' FractionalPart ExponentPart? FloatTypeSuffix?
    | DecimalIntegerLiteral ExponentPart? FloatTypeSuffix
;
ExponentPart:
    [eE] [+-]? DecimalIntegerLiteral
;
FractionalPart:
    DecimalDigit

(continues on next page)
