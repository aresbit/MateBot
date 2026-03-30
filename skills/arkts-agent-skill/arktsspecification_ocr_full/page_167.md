The visibility of a local declaration name is determined by the surrounding function or method, and by the block scope rules (see Scopes). In order to avoid ambiguous interpretation, appropriate sections of this Specification are dedicated to a detailed discussion of the following entities:

• if Statements,

• for Statements,

• for-of Statements.

The usage of annotations is discussed in Using Annotations.

### 8.5 if Statements

An if statement allows executing alternative statements (if provided) under certain conditions.

The syntax of if statement is presented below:

ifStatement:
    'if '(' expression ')' thenStatement
    ('else' elseStatement)?
;
thenStatement:
statement
;
elseStatement:
statement
;

Type of expression must be boolean, or a type mentioned in Extended Conditional Expressions. Otherwise, a compile-time error occurs.

If an expression is successfully evaluated as true, then a thenStatement is executed. Otherwise, an elseStatement is executed (if provided).

Any else corresponds to the nearest preceding if of an if statement:

if (Cond1)
    if (Cond2) statement1
    else statement2 // Executes only if: Cond1 && !Cond2

A Block can be used to combine the else part with the initial if as follows:

if (Cond1) {
    if (Cond2) statement1
}
else statement2 // Executes if: !Cond1

If thenStatement or elseStatement is any kind of a statement but not a block (see Block), then no block scope (see Scopes) is created for such a statement.
