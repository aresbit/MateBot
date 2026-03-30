The type of forVariable declared inside the loop is inferred to be that of the iterated elements, namely:

• T, if Array<T> or FixedArray<T> instance is iterated;

• string, if string value is iterated;

• Type argument of the iterator, if an instance of the iterable type is iterated.

If forVariable is declared outside the loop, then the type of an iterated element must be assignable (see Assignability) to the type of the variable. Otherwise, a compile-time error occurs.

// existing variable 's'
let s : string
for (s of "a string object") {
    console.log(s)
}

// new variable 's', its type is inferred from expression after 'of'
for (let s of "a string object") {
    console.log(s)
}

// new variable 'element', its type is inferred from expression after 'of'.
// as 'const' it cannot be assigned with a new value in the loop body
for (const element of [1, 2, 3]) {
    console.log(element)
    element = 66 // Compile-time error as 'element' is 'const'
}

Explicit type annotation of forVariable is allowed as an experimental feature (see For-of Explicit Type Annotation).

### 8.10 break Statements

A break statement transfers control out of the enclosing loopStatement or switchStatement. If a break statement is used outside a loopStatement or a switchStatement, then a compile-time error occurs.

The syntax of break statement is presented below:

breakStatement:
'break' identifier?
;

A break statement with the label identifier transfers control out of the enclosing statement with the same label identifier. If there is no enclosing loop statement with the same label identifier (within the body of the surrounding function or method), then a compile-time error occurs.

A statement without a label transfers control out of the innermost enclosing switch, while, do, for, or for-of statement. If breakStatement is placed outside loopStatement or switchStatement, then a compile-time error occurs.

Examples of break statements with and without a label are presented below:
