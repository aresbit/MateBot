## LEXICAL ELEMENTS

This chapter discusses the lexical structure of the ArkTS programming language.

### 2.1 Use of Unicode Characters

1ne ArkTS programming language uses characters of the Unicode Character set $ ^{1} $ as its terminal symbols. It uses the Unicode UTF-16 encoding to represent text in sequences of 16-bit code units.

The term Unicode code point is used in this specification only where such representation is relevant to refer the reader to Unicode Character set and UTF-16 encoding. Where such representation is irrelevant to the discussion, the generic term character is used.

### 2.2 Lexical Input Elements

The language has the following types of lexical input elements:

• White Spaces.

• Line Separators.

• Tokens, and

• Comments.

### 2.3 White Spaces

White spaces are lexical input elements that separate tokens from one another. White spaces include the following:

• Space (U+0020),

• Horizontal tabulation (U+0009),
