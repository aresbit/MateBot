### 6.3 Numeric Operator Contexts

Numeric contexts apply to the operands of an arithmetic operator. Numeric contexts use numeric types conversions (see Widening Numeric Conversions), and ensure that each argument expression can be converted to target type T while the arithmetic operation for the values of type T is being defined.

An operand of enumeration type (see Enumerations) can be used in a numeric context if enumeration base type is a numeric type. The type of this operand is assumed to be the same as the enumeration base type.

Numeric contexts take the following forms:

• Unary Expressions;

• Multiplicative Expressions;

• Additive Expressions;

• Shift Expressions;

• Relational Expressions;

• Equality Expressions;

• Bitwise and Logical Expressions;

• Conditional-And Expression;

• Conditional-Or Expression.

#### 6.3.1 Numeric Conversions for Relational and Equality Operands

Relational and equality operators (see Relational Expressions and Equality Expressions) allow the following:

• Implicit conversion, where operands are of numeric types but have different sizes (see Widening Numeric Conversions), with their specific details stated in Specifics of Numeric Operator Contexts; and

• Conversion of operands with BigInt() function, where one operand type is bigint and the other is numeric. The situation for the relational operator ‘<’ is represented in the example below:

1 let a: int = 1
2 let b: long = 0
3 let c: bigint = -1n
4
5 if (b<a) { // `a`` converted to `long` prior to comparison
6     ;
7 }
8
9 if (c<b) { // `b` converted to `bigint` prior to comparison
10     ;
11 }
