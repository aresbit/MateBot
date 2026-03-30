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
