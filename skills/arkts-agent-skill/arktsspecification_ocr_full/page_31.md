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
