• Vertical tabulation (U+000B),

• Form feed (U+000C),

• No-break space  $ (U+00A0) $, and

• Zero-width no-break space (U+FEFF).

White spaces improve source code readability and help avoiding ambiguities. White spaces are ignored by the syntactic grammar (see Grammar Summary). White spaces never occur within a single token, but can occur within a comment.

### 2.4 Line Separators

Line separators are lexical input elements that separate tokens from one another and divide sequences of Unicode input characters into lines. Line separators include the following:

• Newline character (U+000A or ASCII <LF>)

• Carriage return character (U+000D or ASCII <CR>)

• Line separator character (U+2028 or ASCII <LS>), and

• Paragraph separator character (U+2029 or ASCII <PS>)

Line separators improve source code readability. Any sequence of line separators is considered a single separator.

Line separators are often treated as white spaces, except where line separators have special meanings. See Semicolons for more details.

### 2.5 Tokens

Tokens form the vocabulary of the language. There are four classes of tokens:

• Identifiers,

• Keywords,

• Operators and Punctuators, and

• Literals.

Token is the only lexical input element that can act as a terminal symbol of the syntactic grammar (see Grammar Summary). In the process of tokenization, the next token is always the longest sequence of characters that form a valid token. Tokens are separated by white spaces (see White Spaces), operators, or punctuators (see Operators and Punctuators). White spaces are ignored by the syntactic grammar (see Grammar Summary).
