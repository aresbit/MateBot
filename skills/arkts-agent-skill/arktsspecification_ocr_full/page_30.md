153n // bigint literal
1_153n // bigint literal
-153n // negative bigint literal

The underscore character ‘_’ between successive digits can be used to improve readability. Underscore characters in such positions do not change the values of literals. However, the underscore character must be neither the very first nor the very last symbol of a bigint literal.

Strings that represent numbers or any integer value can be converted to bigint by using built-in functions as follows:

BigInt(other: string): bigint
BigInt(other: long): bigint

Two methods allow taking bitsCount lower bits of a bigint number and return them as a result. Signed and unsigned versions are both possible as follows:

asIntN(bitsCount: long, bigIntToCut: bigint): bigint
asUintN(bitsCount: long, bigIntToCut: bigint): bigint

#### 2.9.5 Boolean Literals

The two boolean literal values are represented by the keywords true and false.

BooleanLiteral:
'true' | 'false'
;

Boolean literals are of the boolean type.

#### 2.9.6 String Literals

String literals consist of zero or more characters enclosed between single or double quotes. A special form of string literals is multiline string literal (see Multiline String Literal).

String literals are of the literal type that corresponds to the literal. If an operator is applied to the literal, then the literal type is replaced for string (see Type string).

StringLiteral:
'"' DoubleQuoteCharacter* '"'
| '\'' SingleQuoteCharacter* ''\'
;

DoubleQuoteCharacter:
~["\\\r\n]
| ''\' EscapeSequence
;

SingleQuoteCharacter:
~['\\\r\n]
| ''\' EscapeSequence

(continues on next page)
