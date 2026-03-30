#### 7.24.1 Numeric Relational Operators

Type of each operand in a numeric relational operator must be convertible to a numeric type (see Numeric Types). Otherwise, a compile-time error occurs.

Depending on the converted type of operands, a comparison is performed as follows:

• Signed integer comparison, if the converted operand type is int or long.

• Floating-point comparison, if the converted operand type is float or double.

he comparison of floating-point values drawn from any value set must be accurate.

A floating-point comparison must be performed in accordance with the IEEE 754 standard specification as follows:

• The result of a floating-point comparison is false if either operand is NaN.

• All values other than NaN must be ordered with the following:

– Negative infinity less than all finite values; and

– Positive infinity greater than all finite values.

• Positive zero equals negative zero.

Based on the above presumption, the following rules apply to integer, floating-point, or bigint operands other than NaN:

• The value produced by the operator ‘<’ is true if the value of the left-hand-side operand is less than that of the right-hand-side operand. Otherwise, the value is false.

• The value produced by the operator ‘<=’ is true if the value of the left-hand-side operand is less than or equal to that of the right-hand-side operand. Otherwise, the value is false.

• The value produced by the operator ‘>’ is true if the value of the left-hand-side operand is greater than that of the right-hand-side operand. Otherwise, the value is false.

• The value produced by the operator ‘>=’ is true if the value of the left-hand-side operand is greater than or equal to that of the right-hand-side operand. Otherwise, the value is false.

#### 7.24.2 String Relational Operators

Results of all string comparisons are defined as follows:

• Operator ‘<’ delivers true if the string value of the left-hand-side operand is lexicographically less than the string value of the right-hand-side operand, or false otherwise.

• Operator ‘<=’ delivers true if the string value of the left-hand-side operand is lexicographically less than or equal to the string value of the right-hand-side operand, or false otherwise.

• Operator ‘>’ delivers true if the string value of the left-hand-side operand is lexicographically greater than the string value of the right-hand-side operand, or false otherwise.

• Operator ‘>=’ delivers true if the string value of the left-hand-side operand is lexicographically greater than or equal to the string value of the right-hand operand, or false otherwise.
