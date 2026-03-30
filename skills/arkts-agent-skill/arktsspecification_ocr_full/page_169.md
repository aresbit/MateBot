### 8.7 while Statements and do Statements

A while statement and a do statement evaluate an expression and execute the statement repeatedly till the expression value is true. The key difference is that a whileStatement starts from evaluating and checking the expression value, and a doStatement starts from executing the statement.

The syntax of while and do statements is presented below:

whileStatement:
    'while' ('expression') statement
;
doStatement
    : 'do' statement 'while' ('expression')
;

Type of expression must be boolean, or a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

### 8.8 for Statements

The syntax of for statements is presented below:

forStatement:
    'for ' (' forInit? '; ' forContinue? '; ' forUpdate? ')' statement
;
forInit:
    expressionSequence
| variableDeclarations
;
forContinue:
    expression
;
forUpdate:
    expressionSequence
;

Type of forContinue expression must be boolean, or a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

// existing variable is used as a loop index variable
let i: number
for (i = 1; i < 10; i++) {

(continues on next page)
