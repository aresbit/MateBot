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
