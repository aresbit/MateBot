# Chapter 3: Types

Page range: 23-50

## Page 23

### 2.6 Identifiers

Identifier is a sequence of one or more valid Unicode characters. The Unicode grammar of identifiers is based on character properties specified by the Unicode Standard.

The first character in an identifier must be ‘$, ‘_’, or any Unicode code point with the Unicode property ‘ID_Start’². Other characters must be Unicode code points with the Unicode property, or one of the following characters:

• ‘$’(\U+0024),

• 'Zero-Width Non-Joiner' (<ZWNJ>, \U+200C), or

• 'Zero-Width Joiner' (<ZWJ>, \U+200D).

Identifier:
IdentifierStart IdentifierPart*
;
IdentifierStart:
UnicodeIDStart
| ' $ '
| ' _ '
| '\\' EscapeSequence
;
IdentifierPart:
UnicodeIDContinue
| ' $ '
| ZWNJ
| ZWJ
| '\\' EscapeSequence
;
ZWJ:
'\u200C'
;
ZWNJ:
'\u200D'
;
UnicodeIDStart
: Letter
| ['$']
| '\\' UnicodeEscapeSequence;

UnicodeIDContinue
: UnicodeIDStart
| UnicodeDigit
| '\\u200C'
| '\\u200D';

UnicodeEscapeSequence:
'u' HexDigit HexDigit HexDigit HexDigit
| 'u' '{}' HexDigit HexDigit+ '}'

(continues on next page)

## Page 24

Letter
: UNICODE_CLASS_LU
| UNICODE_CLASS_LL
| UNICODE_CLASS_LT
| UNICODE_CLASS_LM
| UNICODE_CLASS_LO
;
UnicodeDigit
: UNICODE_CLASS_ND
;

See Grammar Summary for the Unicode character categories UNICODE_CLASS_LU, UNICODE_CLASS_LL, UNICODE_CLASS_LT, UNICODE_CLASS_LM, UNICODE_CLASS_LO, and UNICODE_CLASS_ND.

### 2.7 Keywords

Keywords are reserved words with meanings permanently predefined in ArkTS. Keywords are case-sensitive, and their exact spelling is presented in the following four tables. The kinds of keywords are discussed below.

1. The following hard keywords are reserved in any context, and cannot be used as identifiers:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>abstract</td><td style='text-align: center; word-wrap: break-word;'>enum</td><td style='text-align: center; word-wrap: break-word;'>let</td><td style='text-align: center; word-wrap: break-word;'>this</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>as</td><td style='text-align: center; word-wrap: break-word;'>export</td><td style='text-align: center; word-wrap: break-word;'>native</td><td style='text-align: center; word-wrap: break-word;'>throw</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>async</td><td style='text-align: center; word-wrap: break-word;'>extends</td><td style='text-align: center; word-wrap: break-word;'>new</td><td style='text-align: center; word-wrap: break-word;'>true</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>await</td><td style='text-align: center; word-wrap: break-word;'>false</td><td style='text-align: center; word-wrap: break-word;'>null</td><td style='text-align: center; word-wrap: break-word;'>try</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>break</td><td style='text-align: center; word-wrap: break-word;'>final</td><td style='text-align: center; word-wrap: break-word;'>overload</td><td style='text-align: center; word-wrap: break-word;'>typeof</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>case</td><td style='text-align: center; word-wrap: break-word;'>for</td><td style='text-align: center; word-wrap: break-word;'>override</td><td style='text-align: center; word-wrap: break-word;'>undefined</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>class</td><td style='text-align: center; word-wrap: break-word;'>function</td><td style='text-align: center; word-wrap: break-word;'>private</td><td style='text-align: center; word-wrap: break-word;'>while</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>const</td><td style='text-align: center; word-wrap: break-word;'>if</td><td style='text-align: center; word-wrap: break-word;'>protected</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>constructor</td><td style='text-align: center; word-wrap: break-word;'>implements</td><td style='text-align: center; word-wrap: break-word;'>public</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>continue</td><td style='text-align: center; word-wrap: break-word;'>import</td><td style='text-align: center; word-wrap: break-word;'>return</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>default</td><td style='text-align: center; word-wrap: break-word;'>in</td><td style='text-align: center; word-wrap: break-word;'>static</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>do</td><td style='text-align: center; word-wrap: break-word;'>instanceof</td><td style='text-align: center; word-wrap: break-word;'>switch</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>else</td><td style='text-align: center; word-wrap: break-word;'>interface</td><td style='text-align: center; word-wrap: break-word;'>super</td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

2. Names and aliases of predefined types are hard keywords, and cannot be used as identifiers:

## Page 25

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Primary name</td><td style='text-align: center; word-wrap: break-word;'>Alias</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Any</td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bigint</td><td style='text-align: center; word-wrap: break-word;'>BigInt</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>Boolean</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>Byte</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char</td><td style='text-align: center; word-wrap: break-word;'>Char</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>double</td><td style='text-align: center; word-wrap: break-word;'>Double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>Float</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>Int</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>Long</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number</td><td style='text-align: center; word-wrap: break-word;'>Number</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Object</td><td style='text-align: center; word-wrap: break-word;'>object</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>Short</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>string</td><td style='text-align: center; word-wrap: break-word;'>String</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>void</td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

3. The following soft keywords have special meaning in certain contexts but are valid identifiers elsewhere:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>catch</td><td style='text-align: center; word-wrap: break-word;'>namespace</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>declare</td><td style='text-align: center; word-wrap: break-word;'>of</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>finally</td><td style='text-align: center; word-wrap: break-word;'>out</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>from</td><td style='text-align: center; word-wrap: break-word;'>readonly</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>get</td><td style='text-align: center; word-wrap: break-word;'>set</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>keyof</td><td style='text-align: center; word-wrap: break-word;'>type</td></tr></table>

4. The following identifiers are also treated as soft keywords reserved for the future use, or currently used in TypeScript:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr><tr><td style='text-align: center; word-wrap: break-word;'>is</td><td style='text-align: center; word-wrap: break-word;'>struct</td><td style='text-align: center; word-wrap: break-word;'>var</td><td style='text-align: center; word-wrap: break-word;'>yield</td></tr></table>

### 2.8 Operators and Punctuators

Operators are tokens that denote various actions to be performed on values: addition, subtraction, comparison, and other. The keywords instanceof and typeof also act as operators.

Punctuators are tokens that separate, complete, or otherwise organize program elements and parts: commas, semicolons, parentheses, square brackets, etc.

The following character sequences represent operators and punctuators:

## Page 26

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>+</td><td style='text-align: center; word-wrap: break-word;'>&amp;</td><td style='text-align: center; word-wrap: break-word;'>+=</td><td style='text-align: center; word-wrap: break-word;'>|=</td><td style='text-align: center; word-wrap: break-word;'>&amp;=</td><td style='text-align: center; word-wrap: break-word;'>&lt;</td><td style='text-align: center; word-wrap: break-word;'>?</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>-</td><td style='text-align: center; word-wrap: break-word;'>|</td><td style='text-align: center; word-wrap: break-word;'>-=</td><td style='text-align: center; word-wrap: break-word;'>^=</td><td style='text-align: center; word-wrap: break-word;'>&amp;&amp;</td><td style='text-align: center; word-wrap: break-word;'>&gt;</td><td style='text-align: center; word-wrap: break-word;'>!</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>*</td><td style='text-align: center; word-wrap: break-word;'>^</td><td style='text-align: center; word-wrap: break-word;'>*=</td><td style='text-align: center; word-wrap: break-word;'>&lt;&lt;=</td><td style='text-align: center; word-wrap: break-word;'>| |</td><td style='text-align: center; word-wrap: break-word;'>===</td><td style='text-align: center; word-wrap: break-word;'>&lt;=</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>/</td><td style='text-align: center; word-wrap: break-word;'>&gt;&gt;</td><td style='text-align: center; word-wrap: break-word;'>/=</td><td style='text-align: center; word-wrap: break-word;'>&gt;&gt;=</td><td style='text-align: center; word-wrap: break-word;'>++</td><td style='text-align: center; word-wrap: break-word;'>===</td><td style='text-align: center; word-wrap: break-word;'>&gt;=</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>%</td><td style='text-align: center; word-wrap: break-word;'>&lt;&lt;</td><td style='text-align: center; word-wrap: break-word;'>%=</td><td style='text-align: center; word-wrap: break-word;'>&gt;&gt;&gt;=</td><td style='text-align: center; word-wrap: break-word;'>--</td><td style='text-align: center; word-wrap: break-word;'>=</td><td style='text-align: center; word-wrap: break-word;'>...</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>(</td><td style='text-align: center; word-wrap: break-word;'>)</td><td style='text-align: center; word-wrap: break-word;'>[</td><td style='text-align: center; word-wrap: break-word;'>]</td><td style='text-align: center; word-wrap: break-word;'>{</td><td style='text-align: center; word-wrap: break-word;'>}</td><td style='text-align: center; word-wrap: break-word;'>??</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>,</td><td style='text-align: center; word-wrap: break-word;'>;</td><td style='text-align: center; word-wrap: break-word;'>.</td><td style='text-align: center; word-wrap: break-word;'>:</td><td style='text-align: center; word-wrap: break-word;'>!=</td><td style='text-align: center; word-wrap: break-word;'>!===</td><td style='text-align: center; word-wrap: break-word;'>**</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>**=</td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td><td style='text-align: center; word-wrap: break-word;'></td></tr></table>

### 2.9 Literals

Literals are values of certain types (see Predefined Types and Literal Types).

Literal:
IntegerLiteral
    FloatLiteral
    BigIntLiteral
    BooleanLiteral
    StringLiteral
    MultilineStringLiteral
    NullLiteral
    UndefinedLiteral
    CharLiteral
;

<div style="text-align: center;">See Character Literals for the experimental char literal.</div>


<div style="text-align: center;">Each literal is described in detail below.</div>


#### 2.9.1 Numeric Literals

Numeric literals include integer and floating-point literals.

#### 2.9.2 Integer Literals

Integer literals represent numbers that have neither a decimal point nor an exponential part. Integer literals can be written with radices 16 (hexadecimal), 10 (decimal), 8 (octal), and 2 (binary) as follows:

IntegerLiteral: DecimalIntegerLiteral

(continues on next page)

## Page 27

(continued from previous page)

| HexIntegerLiteral
| OctalIntegerLiteral
| BinaryIntegerLiteral
;
DecimalIntegerLiteral:
'0'
| DecimalDigitNotZero ('_'? DecimalDigit)*
;
DecimalDigit:
[0-9]
;
DecimalDigitNotZero:
[1-9]
;
HexIntegerLiteral:
'0' [xX] ( HexDigit
| HexDigit (HexDigit | '_')* HexDigit
)
;
HexDigit:
[0-9a-fA-F]
;
OctalIntegerLiteral:
'0' [o0] ( OctalDigit
| OctalDigit (OctalDigit | '_')* OctalDigit )
;
OctalDigit:
[0-7]
;
BinaryIntegerLiteral:
'0' [bB] ( BinaryDigit
| BinaryDigit (BinaryDigit | '_')* BinaryDigit )
;
BinaryDigit:
[0-1]
;

Integral literals with different radices are represented by the examples below:

153 // decimal literal
1_153 // decimal literal
0xBAD3 // hex literal
0xBAD_3 // hex literal

(continues on next page)

## Page 28

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

## Page 29

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

## Page 30

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

## Page 31

(continued from previous page)

;
EscapeSequence:
[''bfnrtv0\\]
| 'x' HexDigit HexDigit
| 'u' HexDigit HexDigit HexDigit HexDigit
| 'u'、「'HexDigit+ '}'
| ~[1-9xu\r\n]
;

Characters in string literals normally represent themselves. However, certain non-graphic characters can be represented by explicit specifications or Unicode codes. Such constructs are called escape sequences.

Escape sequences can represent graphic characters within a string literal, e.g., single quotes “”, double quotes “”, backslashes ‘\’, and some others. An escape sequence always starts with the backslash character ‘\’, followed by one of the following characters:

• " (double quote, U+0022),

• ' (neutral single quote, U+0027),

• b (backspace, U+0008),

• f (form feed, U+000c),

• n (linefeed, U+000a),

• r (carriage return, U+000d),

• t (horizontal tab, U+0009),

• v (vertical tab, U+000b),

• \ (backslash, U+005c),

• x and two hexadecimal digits (like 7F),

• u and four hexadecimal digits (forming a fixed Unicode escape sequence like \u005c),

• u{ and at least one hexadecimal digit followed by } (forming a bounded Unicode escape sequence like \u{5c}), and

• any single character except digits from ‘1’ to ‘9’, and characters ‘x’, ‘u’, ‘CR’, and ‘LF’.

The examples are provided below:

1 {
    let s1 = 'Hello, world!'
    let s2 = "Hello, world!"
    let s3 = "\"
    let s4 = ""
    let s5 = "don't worry, be happy"
    let s6 = 'don\'t worry, be happy'
    let s7 = 'don\u0027t worry, be happy'
}

## Page 32

#### 2.9.7 Multiline String Literal

Multiline strings can contain arbitrary text delimited by backtick characters ‘”。Multiline strings can contain any character, except the escape character ‘\'. Multiline strings can contain newline characters:

MultilineStringLiteral:
    '' (BacktickCharacter)* ' '
;
BacktickCharacter:
~['\\\r\n]
| '\\' EscapeSequence
| LineContinuation
;
LineContinuation:
'\\' [\\r\\u2028\\u2029]+
;

The grammar of embeddedExpression is described in String Interpolation Expressions.

An example of a multiline string is provided below:

let sentence = `This is an example of a multiline string, which should be enclosed in backticks`

MultilineString literals are of the literal type that corresponds to a literal. If an operator is applied to a literal, then the literal type is replaced for string (see Type string).

#### 2.9.8 Null Literal

Null literal is the only literal of type null (see Type null) to denote a reference without pointing at any entity. The null literal is represented by the keyword null:

NullLiteral:
'null'
;

The value is typically used for types like T | null (see Nullish Types).

#### 2.9.9 Undefined Literal

Undefined literal is the only literal of type undefined (see Type undefined) to denote a reference with a value that is not defined. The undefined literal is represented by the keyword undefined:

## Page 33

UndefinedLiteral:
  'undefined'
;

### 2.10 Comments

Comment is a piece of text added in the stream to document and compliment the source code. Comments are insignificant for the syntactic grammar (see Grammar Summary).

Line comments begin with the sequence of characters ‘//’ as in the example below, and end with the line separator character. Any character or sequence of characters between them is allowed but ignored.

// This is a line comment

Multiline comments begin with the sequence of characters ‘\*’ as in the example below, and end with the first subsequent sequence of characters ‘*/’. Any character or sequence of characters between them is allowed but ignored.

1/*
2 This is a multiline comment
3*/

Comments cannot be nested.

### 2.11 Semicolons

Declarations and statements are usually terminated by a line separator (see Line Separators). A semicolon must be used in some cases to separate syntax productions written in one line or to avoid ambiguity.

function foo(x: number): number {
    x++;
    x *= x;
    return x
}

let i = 1
i - i++ // one expression
i; -i++ // two expressions

## Page 34

## Page 35

# TYPES

This chapter introduces the notion of type that is one of the fundamental concepts of ArkTS and other programming languages. Type classification as accepted in ArkTS is discussed below along with all aspects of using types in programs written in the language.

The type of an entity is conventionally defined as the set of values the entity (variable) can take, and the set of operators applicable to the entity of a given type.

ArkTS is a statically typed language. It means that the type of every declared entity and every expression is known at compile time. The type of an entity is either set explicitly by a developer, or inferred implicitly (see Type Inference) by the compiler.

The types integral to ArkTS are called predefined types (see Predefined Types).

The types introduced, declared, and defined by a developer are called user-defined types. All user-defined types must have complete type declarations presented as source code in ArkTS.

ArkTS types are summarized in the table below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Predefined Types</td><td style='text-align: center; word-wrap: break-word;'>User-Defined Types</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte, short, int, long, float, double, number, boolean, char, string, bigint, Any, Object, never, void, undefined, null, Array&lt;T&gt; or T[], FixedArray&lt;T&gt;</td><td style='text-align: center; word-wrap: break-word;'>class types, interface types, array types, fixed array types, tuple types, union types, literal types, function types, type parameters, enumeration types</td></tr></table>

Note. Type number is an alias to double.

Most predefined types have aliases to improve TypeScript compatibility as follows:

## Page 36

<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Primary Name</td><td style='text-align: center; word-wrap: break-word;'>Alias</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number</td><td style='text-align: center; word-wrap: break-word;'>Number</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>Byte</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>Short</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>Int</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>Long</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>Float</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>double</td><td style='text-align: center; word-wrap: break-word;'>Double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>boolean</td><td style='text-align: center; word-wrap: break-word;'>Boolean</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char</td><td style='text-align: center; word-wrap: break-word;'>Char</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>string</td><td style='text-align: center; word-wrap: break-word;'>String</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>bigint</td><td style='text-align: center; word-wrap: break-word;'>BigInt</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>Object</td><td style='text-align: center; word-wrap: break-word;'>object</td></tr></table>

Using primary names of predefined types is recommended in all cases.

### 3.1 Predefined Types

Predefined types include the following:

• Value Types;

• Type Any;

• Type Object;

• Type never;

• Type void;

• Type undefined;

• Type null;

• Type string;

• Type bigint;

• Array Types (Array<T> or T[] or FixedArray<T>).

### 3.2 User-Defined Types

User-defined types include the following:

• Class types (see Classes);

• Interface types (see Interfaces);

• Enumeration types (see Enumerations);

## Page 37

• Function Types;

• Tuple Types:

• Union Types;

• Type Parameters; and

• Literal Types.

### 3.3 Using Types

Source code can refer to a type by using the following:

• Type reference for:

- Named Types, or

- Type aliases (see Type Alias Declaration);

• In-place type declaration for:

- Array Types,

- Tuple Types,

- Function Types,

– Function Types with Receiver,

- Keyof Types,

– Union Types, or

- Type in parentheses.

The syntax of type is presented below:

type:
  annotationUsage?
  ( typeReference
  | 'readonly'? arrayType
  | 'readonly'? tupleType
  | functionType
    | functionTypeWithReceiver
    | unionType
    | keyofType
    | StringLiteral
)
| '(' type ')'
;

The usage of annotations is discussed in Using Annotations.

Types with the prefix reading are discussed in Readonly Array Types and Readonly Triple Types.

The usage of types is represented by the example below:

## Page 38

let n: number // using identifier as a predefined value type name
let o: Object // using identifier as a predefined class type name
let a: number[] // using array type
let t: [number, number] // using tuple type
let f: ()=>number // using function type
let u: number|string // using union type
let l: "xyz" // using string literal type

class C { n = 1; s = "aa"}
let k: keyof C // using keyof to build union type

Parentheses are used to specify the required type structure if the type is a combination of array, function, or union types. Without parentheses, the symbol ‘|’ that constructs a union type has the lowest precedence as represented by the example below:

// a nullable array with elements of type string:
let a: string[] | null
let s: string[] = []
a = s    // ok
a = null // ok, a is nullable

// an array with elements whose types are string or null:
let b1: (string | null)[]
b1 = null // error, b1 is an array and is not nullable
b1 = ["aa", null] // ok

// string or array of null elements:
let b2: string | null[]
b2 = null // error, b2 - string or array of nulls - not nullable
b2 = [null, null] // ok

// a function type that returns string or null
let c: () => string | null
c = null // error, c is not nullable
c = (): string | null => { return null } // ok

// (a function type that returns string) or null
let d: (() => string) | null
d = null // ok, d is nullable
d = (): string => { return "hi" } // ok

If an annotation is used in front of type in parentheses, then the parentheses become a mandatory part of the annotation to prevent ambiguity.

let var_name1: @my_annotation() (A|B) // OK
let var_name2: @my_annotation (A|B) // Compile-time error

## Page 39

### 3.4 Named Types

Named types are classes, interfaces, enumerations, aliases, type parameters, and predefined types (see Predefined Types), except built-in arrays. Other types (i.e., array, function, and union types) are anonymous unless aliased. Respective named types are introduced by the following:

• Class declarations (see Classes),

• Interface declarations (see Interfaces),

• Enumeration declarations (see Enumerations),

• Type alias declarations (see Type Alias Declaration), and

• Type parameter declarations (see Type Parameters).

Classes, interfaces and type aliases with type parameters are generic types (see Generics). Named types without type parameters are non-generic types.

Type references (see Type References) refer to named types by specifying their type names and (where applicable) type arguments to be substituted for the type parameters of a named type.

### 3.5 Type References

Type reference refers to a type by one of the following:

• Simple or qualified type name (see Names),

• Type alias (see Type Alias Declaration).

Type reference that refers to a generic class or to an interface type is valid if it is a valid instantiation of a generic. Its type arguments can be provided explicitly or implicitly based on defaults.

The syntax of type reference is presented below:

typeReference:
    typeReferencePart ('.' typeReferencePart)*
;

typeReferencePart:
    identifier typeArguments?
;

let map: Map<string, number> // Map<string, number> is the type reference

class A<T> {...}

class C<T> {
    field1: A<T> // A<T> is a class type reference - class type reference
    field2: A<number> // A<number> is a type reference - class type reference
    foo (p: T) {} // T is a type reference - type parameter
    constructor () { /* some body to init fields */ }
}

type MyType<T> = A<T>[]

## Page 40

let x: MyType<number> = [new A<number>, new A<number>]
// MyType<number> is a type reference - alias reference
// A<number> is a type reference - class type reference

If type reference refers to a type by a type alias (see Type Alias Declaration), then the type alias is replaced for a non-aliased type in all cases when dealing with types. The replacement is potentially recursive.

type T1 = Object
type T2 = number
function foo(t1: T1, t2: T2) {
    t1 = t2 // Type compatibility test will use Object and number
    t2 = t2 + t2 // Operator validity test will use type number not T2
}

### 3.6 Value Types

Value types are predefined integer types (see Integer Types and Operations), floating-point types (see Floating-Point Types and Operations), the boolean type (see Type boolean), character types (see Type char), and user-defined enumeration types (see Enumerations). The values of such types do not share state with other values.

#### 3.6.1 Numeric Types

Numeric types are integer and floating-point types (see Integer Types and Operations and Floating-Point Types and Operations).

Larger type values include all values of smaller types:

• double > float > long > int > short > byte

A value of a smaller type can be assigned to a variable of a larger type as a consequence (see Widening Numeric Conversions).

In terms of operations available for the numeric types (see Multiplication, Division, Remainder, Additive Expressions) we state that number or double is the largest type and long is larger than int and so on respectively.

Type bigint does not belong to this hierarchy. No implicit conversion from numeric types (see Numeric Types) to bigint occurs in any assignment context (see Assignment-like Contexts). The methods of class BigInt (which is a part of Standard Library) must be used to create bigint values from numeric type values.

## Page 41

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

## Page 42

#### 3.6.3 Floating-Point Types and Operations


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Corresponding Set of Values</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>The set of all IEEE  $ 754^{3} $ 32-bit floating-point numbers</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>number, double</td><td style='text-align: center; word-wrap: break-word;'>The set of all IEEE 754 64-bit floating-point numbers</td></tr></table>

ArkTS provides a number of operators to act on floating-point type values as discussed below.

• Comparison operators that produce a value of type boolean:

- Numeric relational operators ‘<’, ‘<=’, ‘>’, and ‘>=’ (see Numeric Relational Operators);

- Numeric equality operators ‘==’ and ‘!=’ (see Numeric Equality Operators);

• Numeric operators that produce values of type float or double:

– Unary plus ‘+’ and minus ‘-’ operators (see Unary Plus and Unary Minus);

– Multiplicative operators ‘*’, ‘/’, and ‘%’ (see Multiplicative Expressions);

– Additive operators ‘+’ and ‘-’ (see Additive Expressions);

– Increment operator ‘++’ used as prefix (see Prefix Increment) or postfix (see Postfix Increment);

– Decrement operator ‘--’ used as prefix (see Prefix Decrement) or postfix (see Postfix Decrement);

• Numeric operators that produce values of type int or long:

– Signed and unsigned shift operators ‘<<’, ‘>>’, and ‘>>>’ (see Shift Expressions);

– Bitwise complement operator ‘~’ (see Bitwise Complement);

– Integer bitwise operators ‘&', ‘^', and ‘|’ (see Integer Bitwise Operators);

• Ternary conditional operator ‘? : ‘(see Ternary Conditional Expressions);

• The string concatenation operator ‘+’ (see String Concatenation) that, if one operand is of type string and the other is of a floating-point type, converts the floating-point type operand to type string with a value represented in the decimal form (without loss of information), and then creates a concatenation of the two strings as a new string.

An operation is called a floating-point operation if at least one of the operands in a binary operator is of a floating-point type (even if the other operand is integer), and that is not a string concatenation.

If at least one operand of the numeric operator is of type double, then the operation implementation uses the 64-bit floating-point arithmetic. The result of the numeric operator is a value of type double.

If the other operand is not of type double, then the numeric conversion (see Widening Numeric Conversions) is used to widen the operand first to type double.

If neither operand is of type double, then the operation implementation is to use the 32-bit floating-point arithmetic. The result of the numeric operator is a value of type float.

If the other operand is not of type float, then the numeric conversion is used to widen the operator first to type float.

Any floating-point type value can be cast to or from any numeric type (see Numeric Types).

Conversions between floating-point types and type boolean are not allowed. However, the value of floating-point type can be used as a logical condition in some cases (see Extended Conditional Expressions)

## Page 43

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

## Page 44

• Tuple Types;

• Function Types;

• Union Types;

• Literal Types;

• Type Any;

• Type string;

• Type bigint;

• Type never;

• Type null;

• Type undefined;

• Type void; and

• Type Parameters.

### 3.8 Type Any

Type Any is a predefined type which is the supertype of all types. Type Any is a predefined nullish-type (see Nullish Types), i.e., a supertype of Type void and Type null in particular.

Type Any has no methods or fields.

### 3.9 Type Object

Type Object is a predefined class type which is the supertype (see Subtyping) of all types except Type void, Type undefined, Type null, Nullish Types, Type Parameters, and Union Types that contain type parameters. All subtypes of Object inherit the methods of class Object (see Inheritance). All methods of class Object are described in full in Standard Library.

The method toString used in the examples in this document returns a string representation of the object.

The term object is used in the Specification to refer to an instance of any type.

Pointers to objects are called references. Multiple references to an object are possible.

Objects can have states. A state of an object that is a class instance is stored in its fields. A state of an array or tuple object is stored in its elements.

If two variables of any type except Value Types contain references to the same object, and the state of that object is modified in the reference of either variable, then the state so modified can be seen in the reference of the other variable.

## Page 45

### 3.10 Type never

Type never is assignable to any type (see Assignability).

• Return type for functions or methods that never return a value, but throw an error when completing an operation.

Type never has no instance. Type never is used as one of the following:

- Type of variables that never get a value (however, an assignment statement with type never in both left-hand and right-hand sides is valid).

• Type of parameters of a function or a method to prevent the body of that function or method from being executed.

function foo () : never {
    throw new Error("foo() never returns")
}

let x : never = foo() // x will never get a value

function bar (p : never) { // body of this
    // function will never be executed
}

bar (foo()) // neither foo nor bar are executed

### 3.11 Type void

Type void is used as a return type to highlight that a function, a method, or a lambda can contain return Statements with no expression, or no return statement at all:

function foo (): void {} // no return at all

class C {
    bar() : void {
        return // with no expression
    }
}

type FunctionWithNoParametersType = () => void

let funcTypeVariable: FunctionWithNoParametersType = () : void => {}

A compile-time error occurs if:

• Type void is used as type annotation;

• Expression of type void is used as a value.

Type void has no instance by itself. However, that it is a supertype of type undefined (see Type undefined) affects the Assignability as follows:

## Page 46

let x: void = undefined // compile-time error - void used as type annotation

function foo(): void {}
console.log(foo()) // compile-time error - void used as a value

function bar1(): void {
    return void // compile-time error - void used as a value
}

function bar2(): void {
    return undefined // OK as undefined is a subtype of void
}

type aType = void | number // compile-time error - void used as type annotation

Type void can be used as a type argument that instantiates a generic type, function, or method as follows:

class A<T> {
    f: T
    m(): T { return this.f }
    constructor (f: T) { this.f = f }
}
let a1 = new A<void>(undefined) // ok, as undefined is a subtype of void
let a2 = new A<undefined>(undefined) // ok
let a3 = new A<void>(void) // compile-time error: void is used as value

console.log (a1.f, a2.m()) // Output is "undefined" "undefined"

function foo<T>(p: T): T { return p }
foo<void>(undefined) // ok, it returns 'undefined' value
foo<void>(void) // compile-time error: void is used as value

type F1<T> = () => T
const f1: F1<void> = (): void => {}
const f2: F1<void> = () => {}
const f3: F1<void> = (): undefined => { return undefined }

// Array literals can be assigned to the array of void type in any form
type A1<T> = T[]
type A2<T> = Array<T>
const a1: A1<void> = [undefined]
const a2: A2<void> = [undefined, undefined]

let x: void[] // compile-time error - void used as type annotation

## Page 47

### 3.12 Type undefined

The only value of type undefined is the literal undefined (see Undefined Literal).

Type undefined is a subtype of type void (see Type void).

Using type undefined as type annotation is not recommended, except in nullish types (see Nullish Types).

Type undefined can be used also as type argument to instantiate a generic type as follows:

class A<T> {}
let a = new A<undefined>() // ok, type parameter is irrelevant
function foo<T>(x: T) {}

foo<undefined>(undefined) // ok

### 3.13 Type null

The only value of type null is the literal null (see Null Literal).

Using type null as type annotation is not recommended, except in nullish types (see Nullish Types).

### 3.14 Type string

Type string values are all string literals, e.g., 'abc'. Type string stores sequences of characters as Unicode UTF-16 code units.

A string object is immutable, the value of a string object cannot be changed after the object is created. The value of a string object can be shared.

Type string has dual semantics, i.e.:

• Type string behaves like a reference type (see Reference Types) if created, assigned, or passed as an argument;

• Type string is handled as a value (see Value Types) by all string operations (see String Concatenation, Equality Expressions, and String Relational Operators).

A number of operators can act on string values as follows:

• Accessing the length property returns string length as int type value. String length is a non-negative integer number. String length is set once at runtime and cannot be changed after that.

• Concatenation operator ‘+’ (see String Concatenation) produces a value of type string. If the result is not a constant expression (see Constant Expressions), then the string concatenation operator can implicitly create a new string object;

• Indexing a string value (see String Indexing Expression) returns a value of type string. A new string object can be created implicitly.

A string value can contain any character, i.e., no character can be used to indicate the end of a string. A character with the value '0' is an ordinary character inside a string as represented by the following example:

## Page 48

$ \left| \text{console.log("a}\backslash\emptyset b\text{".length)} \right| // output: 3 $

Using string in all cases is recommended, although the name String also refers to type string.

### 3.15 Type bigint

ArkTS has the built-in bigint type that allows handling theoretically arbitrary large integers. Values of type bigint can hold numbers that are larger than the maximum value of type long. Type bigint uses the arbitrary-precision arithmetic. Values of type bigint can be created from the following:

• Bigint literals (see Bigint Literals); or

• Numeric type values, by using a call to the standard library class BigInt methods or constructors (see Standard Library).

Similarly to string, bigint type has dual semantics:

• If created, assigned, or passed as an argument, type bigint behaves like a reference type (see Reference Types).

• All applicable operations handle type bigint as a value type (see Value Types). The operations are described in Integer Types and Operations.

Using bigint is recommended in all cases, although the name BigInt also refers to type bigint. Using BigInt creates new objects and calls to static methods in order to improve TypeScript compatibility.

let b1: bigint = new BigInt(5) // for Typescript compatibility
let b2: bigint = 123n

### 3.16 Literal Types

Literal types are aligned with some ArkTS literals (see Literals). Their names are the same as the names of their values, i.e., literals proper. ArkTS supports only the following literal types:

• String Literal Types,

• null, and

• undefined.

let a: "string literal" = "string literal"
let b: null = null
let c: undefined = undefined

printThem (a, b, c)
function printThem (p1: "string literal", p2: null, p3: undefined) {
    console.log (p1, p2, p3)
}

There are no operations for literal types null and undefined.

## Page 49

#### 3.16.1 String Literal Types

Operations on variables of string literal types are identical to the operations of their supertype string (see Type string). The resulting operation type is the type specified for the operation in the supertype:

let s0: "string literal" = "string literal"
let s1: string = s0 + s0 // + for string returns string

### 3.17 Array Types

Array type is a data structure intended to comprise any number of same-type elements, including zero elements. ArkTS supports the following two predefined array types:

• Resizable Array Types; and

• Fixed-Size Array Types as an experimental feature.

Resizable array types are recommended for most cases. Fixed-size array types can be used where performance is the major requirement.

Fixed-size arrays differ from resizable arrays as follows:

• Fixed-size arrays have their length set only once to achieve a better performance.

• Fixed-Size arrays have no methods defined.

Note. The term array type as used in this Specification applies to both resizable array type and fixed-size array type. The same holds true for array value and array instance. Resizable arrays and fixed-size arrays are not assignable to each other.

#### 3.17.1 Resizable Array Types

Resizable array type is a built-in type characterized by the following:

• Any object of resizable array type contains elements. The number of elements is known as array length, and can be accessed by using the length property.

• Array length is a non-negative integer number.

• Array length can be set and changed at runtime.

- Array element is accessed by its index. The index is an integer number in the range from 0 to array length minus 1.

• Accessing an element by its index is a constant-time operation.

• If passed to non-ArkTS environment, an array is represented as a contiguous memory location.

• Type of each array element is assignable to the element type specified in the array declaration (see Assignability).

## Page 50

Resizable array type with elements of type T can have the following two forms of syntax:

• T[], and

• Array<T>.

The first form uses the following syntax:

arrayType:
type ['']
;

Note. T[] and Array<T> specify identical, i.e., indistinguishable types (see Type Identity).

Two basic operations with array elements take elements out of, and put elements into an array by using the operator ‘[]’.

The same syntax can be used to work with Indexable Types, some of such types are parts of Standard Library.

The number of elements in an array can be obtained by accessing the property length. The length of an array can be set and changed in runtime using the methods defined in Standard Library.

An array can be created by using Array Literal, Resizable Array Creation Expressions, or the constructors defined in Standard Library.

ArkTS allows setting a new value to length to shrink an array and provide better TypeScript compatibility. An error is caused by the following situations:

• The value is of type number or other floating-point type, and the fractional part differs from 0;

• The value is less than zero; or

• The value is greater than previous length.

The above situations cause errors as follows:

• A runtime error, if the situation is identified at runtime, i.e., during program execution; and

• A compile-time error, if the situation is detected during compilation.

Array operations are illustrated below:

let a : number[] = [0, 0, 0, 0, 0]
/* allocate array with 5 elements of type number */
a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
let y = a[4] /* get the last element of array 'a' */
let count = a.length // get the number of array elements
a.length = 3 // shrink array
y = a[2] // OK, 2 is the index of the last element now
y = a[3] // Will lead to runtime error - attempt to access non-existing array element

let b: Array<number> = a // 'b' points to the same array as 'a'

type Matrix = number[][] /* array or array of numbers */

An array as an object is assignable to a variable of type Object:

let a: number[] = [1, 2, 3]
let o: Object = a
