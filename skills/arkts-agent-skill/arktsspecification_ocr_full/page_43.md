Operators on floating-point numbers, except the remainder operator (see Remainder), behave in compliance with the IEEE 754 Standard. For example, ArkTS requires the support of IEEE 754 denormalized floating-point numbers and gradual underflow which facilitate proving the desirable properties of a particular numeric algorithm. Floating-point operations do not flush to zero if the calculated result is a denormalized number.

ArkTS requires the floating-point arithmetic to behave as if the floating-point result of every floating-point operator is rounded to the result precision. An inexact result is rounded to a representable value nearest to the infinitely precise result. ArkTS uses the round to nearest principle (the default rounding mode in IEEE 754), and prefers the representable value with the least significant bit zero out of any two equally near representable values.

ArkTS uses round toward zero to convert a floating-point value to an integer value (see Numeric Casting Conversions). In this case it acts as if the number is truncated, and the mantissa bits are discarded. The result of rounding toward zero is the value of the format that is closest to and no greater in magnitude than the infinitely precise result.

A floating-point operation with overflow produces a signed infinity.

A floating-point operation with underflow produces a denormalized value or a signed zero.

A floating-point operation with no mathematically definite result produces NaN.

All numeric operations with a NaN operand result in NaN.

Predefined constructors, methods, and constants for floating-point types are parts of the ArkTS Standard Library.

#### 3.6.4 Type boolean

Type boolean represents logical values true and false.

The boolean operators are as follows:

• Equality operators (see Equality Expressions);

• Logical complement operator '!' (see Logical Complement);

• Logical operators ‘&', ‘^', and ‘|’ (see Boolean Logical Operators);

• Conditional-and operator ‘&&’ (see Conditional-And Expression) and conditional-or operator ‘||’ (see Conditional-Or Expression);

• Ternary conditional operator ‘? : ‘(see Ternary Conditional Expressions);

- String concatenation operator ‘+’ (see String Concatenation) that converts an operand of type boolean to type string (true or false), and then creates a concatenation of the two strings as a new string.

### 3.7 Reference Types

Reference types can be of the following kinds:

• Class types (see Type Object and Classes);

• Interface types (see Interfaces);

• Array Types;

• Fixed-Size Array Types:
