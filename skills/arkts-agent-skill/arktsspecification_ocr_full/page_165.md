## STATEMENTS

Statements are designed to control execution.

The syntax of statements is presented below:

statement:
    expressionStatement
    | block
    | localDeclaration
    | ifStatement
    | loopStatement
    | breakStatement
    | continueStatement
    | returnStatement
    | switchStatement
    | throwStatement
    | tryStatement
;

### 8.1 Normal and Abrupt Statement Execution

The actions that every statement performs in a normal mode of execution are specific for the particular kind of statement. Normal modes of evaluation for each kind of statement are described in the following sections.

A statement execution is considered to complete normally if the desired action is performed without an error being thrown. On the contrary, a statement execution is considered to complete abruptly if it causes an error thrown.

### 8.2 Expression Statements

Any expression can be used as a statement.

The syntax of expression statement is presented below:
