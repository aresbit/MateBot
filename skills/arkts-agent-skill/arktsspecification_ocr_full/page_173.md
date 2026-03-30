console.log("inner") // get printed only twice

console.log("Outer") // Never reached

} while (false)

### 8.12 return Statements

A return statement can have or not have an expression.

The syntax of return statement is presented below:

returnStatement:
    'return' expression?
;

A return statement with expression can only occur inside a function, a method, or a lambda body with non-void return type.

A return statement (with no expression) can occur inside one of the following:

• Initializer block;

• Constructor body;

• Function, method, or lambda body with return type void (see Type void);

A compile-time error occurs if a return statement is found in:

• Top-level statements (see Top-Level Statements);

• Functions or methods with return type void (see Type void) that have an expression;

• Functions or methods with a non-void return type that have no expression.

The execution of a returnStatement leads to the termination of the surrounding function, method, or initializer. If an expression is provided, the resultant value is the evaluated expression.

In case of constructors, initializer blocks, and top-level statements, the control is transferred out of the scope of the construction, but no result is required. Other statements of the surrounding function, method body, initializer block, or top-level statement are not executed.

### 8.13 switch Statements

A switch statement transfers control to a statement or a block by using the result of successful evaluation of the value of a switch expression.

The syntax of switch statement is presented below:
