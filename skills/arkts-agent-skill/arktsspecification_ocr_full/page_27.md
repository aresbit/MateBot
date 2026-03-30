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
