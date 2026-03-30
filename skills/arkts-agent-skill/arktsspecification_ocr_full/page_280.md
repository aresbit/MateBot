### 16.3 Asynchronous API

#### 16.3.1 Async Functions

Async functions are coroutines (i.e., functions which can be suspended and resumed later) that can be called as regular functions. A compile-time error occurs if:

• Async function is called in a static initializer, including module scope;

• Async function has an abstract or a native modifier;

• Return type of an async function is other than Promise<T>.

Type Promise<T> is a library type discussed in detail in the ArkTS Concurrency Specification.

The returning values of both type Promise<T> and type T are allowed inside the async function body (see Return Type Inference).

Using return statement without an expression is allowed if the return type is  $ Promise<void> $. No-argument return statement can be added implicitly as the last statement of the function body if there is no explicit return statement in a function with the return  $ Promise<void> $.

Note. Using type Promise<void> is not recommended as this type is supported for the sake of backward TypeScript compatibility only.

#### 16.3.2 Async Lambdas

A lambda with the modifier async (see Lambda Expressions) is an implicit coroutine that can be called as a regular lambda.

Async lambdas follow the same rules as Async Functions.

#### 16.3.3 Async Methods

A class method with the modifier async (see Method Declarations) is an implicit coroutine that can be called as a regular method.

Async methods follow the same rules as Async Functions.

#### 16.3.4 await

The syntax of await expression is presented below:

awaitExpression:
    'await' expression
;
