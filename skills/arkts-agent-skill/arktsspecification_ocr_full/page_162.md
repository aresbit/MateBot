### 7.33 Constant Expressions

Constant expressions are expressions with values that can be evaluated at compile time.

The syntax of constant expression is presented below:

constantExpression: expression
;

A constant expression is an expression of a value type (see Value Types), or of type string that completes normally while being composed only of the following:

• Literals of a predefined value types, and literals of type string (see Literals);

• Enumeration type constants;

• Unary operators ‘+’, ‘-’, ‘~’, and ‘!’, but not ‘++’ or ‘--’ (see Unary Plus, Unary Minus, Prefix Increment, and Prefix Decrement);

• Casting conversions to numeric types (see Cast Expression);

• Multiplicative operators ‘*’, ‘/’, and ‘%’ (see Multiplicative Expressions);

• Additive operators ‘+’ and ‘-’ (see Additive Expressions);

• Shift operators ‘<<’, ‘>>’, and ‘>>>’ (see Shift Expressions);

• Relational operators ‘<', ‘<=', ‘>', and ‘>=' (see Relational Expressions);

• Equality operators ‘==’ and ‘!=’ (see Equality Expressions);

• Bitwise and logical operators ‘&', ‘^', and ‘|’ (see Bitwise and Logical Expressions);

• Conditional-and operator ‘&&’ (see Conditional-And Expression), and conditional-or operator ‘||’ (see Conditional-Or Expression);

• Ternary conditional operator 'condition?whenTrue:whenFalse' (see Ternary Conditional Expressions);

• Parenthesized expressions (see Parenthesized Expression) that contain constant expressions;

• Simple names or qualified names that refer to constants (see Constant Declarations) with constant expressions as initializers, declared in the same module.

The examples of constant expressions are presented below:

const a = 2

// Constant expressions:
1 + 2
a + 1
"aa" + "bb"
(a < 0) || (a > 5)

Note. The following expressions are not constant expressions:
