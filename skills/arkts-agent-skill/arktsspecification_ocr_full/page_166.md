expressionStatement:
  expression
;

The execution of a statement leads to the execution of the expression. The result of such execution is discarded.

### 8.3 Block

A sequence of statements (see Statements) enclosed in balanced braces forms a block.

The syntax of block statement is presented below:

block:
 '{' statement* '}'
;

The execution of a block means that all block statements, except type declarations, are executed one after another in the textual order of their appearance within the block while an error is thrown (see Errors), or until a return occurs (see return Statements).

If a block is the body of a functionDeclaration (see Function Declarations) or a classMethodDeclaration (see Method Declarations) declared implicitly or explicitly with return type void (see Type void), then the block can contain no return statement at all. Such a block is equivalent to one that ends in a return statement, and is executed accordingly.

### 8.4 Local Declarations

Local declarations define new mutable or immutable variables within the enclosing context.

Let and const declarations have the initialization part that presumes execution, and actually act as statements.

The syntax of local declaration is presented below:

localDeclaration:
    annotationUsage?
    ( variableDeclaration
    | constantDeclaration
)
;
