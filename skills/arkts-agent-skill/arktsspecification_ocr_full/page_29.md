(continued from previous page)

| DecimalDigit (DecimalDigit | '_\')* DecimalDigit
;
FloatTypeSuffix:
'f'
;

The concept is represented by the examples below:

1 3.14
2 3.14f
3 3.141_592
4 .5
5 1234f
6 1e10
7 1e10f

The underscore character ‘_’ between successive digits can be used to improve readability. Underscore characters in such positions do not change the values of literals. However, the underscore character must be neither the very first nor the very last symbol of a literal.

Floating-point literals are of floating-point types that match literals as follows:

• float if float type suffix is present; or

• float or double that is inferred using Type Inference for Numeric Literals if its context allows to infer type; or

• double otherwise (type number is an alias to double).

A compile-time error occurs if a floating-point literal is too large for its type:

// compile-time error as value is too large for type float:
3.4e39f

// compile-time error as value is too large for type double:
1.7e309

#### 2.9.4 Bigint Literals

Bigint literals represent integer numbers with an unlimited number of digits.

Bigint literals are always of type bigint (see Type bigint).

A bigint literal is an integer literal followed by the symbol 'n':

BigIntLiteral:
'0n'
| [1-9] ('_'? [0-9])* 'n';

The concept is represented by the examples below:
