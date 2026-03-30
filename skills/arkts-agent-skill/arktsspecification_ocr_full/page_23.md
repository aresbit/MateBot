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
