#### 7.24.3 Boolean Relational Operators

Results of all boolean comparisons are defined as follows:

• Operator ‘<’ delivers true if the left-hand-side operand is false, and the right-hand-side operand is true, or false otherwise.

• Operator ‘<=’ delivers:

- true when both operands are true, or the left-hand-side operand is false for any right-hand value;

– false when the left-hand-side operand is true, and the right-hand-side operand is false.

• Operator ‘>’ delivers true if the left-hand-side operand is true, and the right-hand-side operand is false, or false otherwise.

• Operator ‘>=’ delivers:

– true when both operands are false, or the left-hand-side operand is true for any right-hand-side value;

- false when the left-hand-side operand is false, and the right-hand-side operand is true.

#### 7.24.4 Enumeration Relational Operators

If both operands are of the same enumeration type (see Enumerations), then Numeric Relational Operators or String Relational Operators are used depending on the kind of enumeration constant value (Enumeration Integer Values or Enumeration String Values). Otherwise, a compile-time error occurs.

### 7.25 Equality Expressions

Equality expressions use equality operators ‘==’, ‘===’, ‘!=’, and ‘!==’.

The syntax of equality expression is presented below:

equalityExpression:
    expression ('==' | '===' | '!=' | '!=') expression
;

Equality operators group left-to-right. Equality operators are commutative if operand expressions cause no side effects.

Similarly to relational operators, equality operators return true or false. Equality operators have lower precedence than relational operators, for example,  $ a < b == c < d $ is true when both  $ a < b $ and  $ c < d $ are true.

Any equality expression is of type boolean.

The result produced by a != b and !(a == b) is the same in all cases. The result produced by a !== b and !(a === b) is the same.

The result of the operators ‘==’ and ‘===’ is the same in all cases except when comparing the values null and undefined (see Extended Equality with null or undefined).

A comparison that uses the operators ‘==’ and ‘===’ is evaluated to true when

• Operands of Type boolean have the same value;
