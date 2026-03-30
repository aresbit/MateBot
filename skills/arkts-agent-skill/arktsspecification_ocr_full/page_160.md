#### 7.32.2 Lambda Body

Lambda body can be a single expression or a block (see Block). Similarly to the body of a method or a function, a lambda body describes the code to be executed when a lambda expression call occurs (see Function Call Expression).

The meanings of names, and of the keywords this and super (along with the accessibility of the referred declarations) are the same as in the surrounding context. However, lambda parameters introduce new names.

If any local variable or formal parameter of the surrounding context is used but not declared in a lambda body, then the local variable or formal parameter is captured by the lambda.

If an instance member of the surrounding type is used in the lambda body defined in a method, then this is captured by the lambda.

A compile-time error occurs if a local variable is used in a lambda body but is neither declared in nor assigned before it.

If a lambda body is a single expression, then it is handled as follows:

• If the expression is a call expression with return type void, then the body is equivalent to the block: { expression }.

• Otherwise, the body is equivalent to the block: { return expression }.

If lambda signature return type is not void (see Type void) or never (see Type never), and the execution path of the lambda body has no return statement (see return Statements) or no single expression as a body, then a compile-time error occurs.

#### 7.32.3 Lambda Expression Type

Lambda expression type is a function type (see Function Types) that has the following:

• Lambda parameters (if any) as parameters of the function type; and

• Lambda return type as the return type of the function type.

Note. Lambda return type can be inferred from the lambda body and thus the return type can be dropped off.

const lambda = () => { return 123 } // Type of the lambda is () => int

const int_var: int = lambda()

#### 7.32.4 Runtime Evaluation of Lambda Expressions

The evaluation of a lambda expression itself never causes the execution of the lambda body. If completing normally at runtime, the evaluation of a lambda expression produces a new instance of a function type (see Function Types) that corresponds to the lambda signature. In that case, it is similar to the evaluation of a class instance creation expression (see New Expressions).

If the available space is not sufficient for a new instance to be created, then the evaluation of the lambda expression completes abruptly, and OutOfMemoryError is thrown.

Every time a lambda expression is evaluated, the outer variables referred to by the lambda expression are captured as follows:
