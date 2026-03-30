<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Type</td><td style='text-align: center; word-wrap: break-word;'>Type&#x27;s Set of Values</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>char (32-bits)</td><td style='text-align: center; word-wrap: break-word;'>Symbols with codes from U+0000 to U+10FFFF (maximum valid Unicode code point) inclusive</td></tr></table>

Predefined constructors, methods, and constants for char type are parts of the ArkTS Standard Library.

#### 17.1.1 Character Literals

Character literal represents the following:

• Value consisting of a single character; or

- Single escape sequence preceded by the characters single quote (U+0027) and ‘c’ (U+0063), and followed by a single quote U+0027).

The syntax of character literal is represented below:

CharLiteral:
    'c\' SingleQuoteCharacter '\\'
;

SingleQuoteCharacter:
~[\\\\r\n]
| '\\' EscapeSequence
;

The examples are presented below:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>1</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;a&#x27;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>2</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;\n&#x27;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>3</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;\x7F&#x27;</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>4</td><td style='text-align: center; word-wrap: break-word;'>c&#x27;\u0000&#x27;</td></tr></table>

<div style="text-align: center;">Character literals are of type char.</div>


#### 17.1.2 Character Equality Operators

Value equality is used for operands of type char.

If both operands represent the same Unicode code point, then the result of ‘==’ or ‘===’ is true. Otherwise, the result is false.
