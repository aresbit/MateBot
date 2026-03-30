### 8.14 throw Statements

A throw statement causes an error object to be created and raised (see Error Handling). It immediately transfers control, and can exit multiple statements, constructors, functions, and method calls until a try statement (see try Statements) is found that catches the value thrown. If no try statement is found, then UncaughtExceptionError is thrown.

The syntax of throw statement is presented below:

throwStatement:
    'throw' expression
;

The expression type must be assignable (see Assignability) to type Error. Otherwise, a compile-time error occurs.

This implies that the object thrown is never null.

Errors can be thrown at any place in the code.

### 8.15 try Statements

A try statement runs block of code, and provides optional catch clause to handle errors (see Error Handling) which may occur during block of code execution.

The syntax of try statement is presented below:

tryStatement:
    'try' block catchClause? finallyClause?
;
catchClause:
    'catch' ('identifier ')' block
;
finallyClause:
    'finally' block
;

A try statement must contain either a finally clause, or a catch clause. Otherwise, a compile-time error occurs.

If the try block completes normally, then no action is taken, and no catch clause block is executed.

If an error is thrown in the try block directly or indirectly, then the control is transferred to the catch clause.
