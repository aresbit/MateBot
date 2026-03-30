variableDeclarations:
    'let' variableDeclarationList
;
variableDeclarationList:
    variableDeclaration (',' variableDeclaration)*
;
variableDeclaration:
    identifier ':' type initializer?
| identifier initializer
;
initializer:
    '=' expression
;

When a variable is introduced by a variable declaration, type T of the variable is determined as follows:

• T is the type specified in a type annotation (if any) of the declaration.

– If the declaration also has an initializer, then the initializer expression type must be assignable to T (see Assignability with Initializer).

• If no type annotation is available, then T is inferred from the initializer expression (see Type Inference from Initializer).

An ambient variable declaration must have type but has no initializer. Otherwise, a compile-time error occurs.

let a: number // ok
let b = 1 // ok, type 'int' is inferred
let c: number = 6, d = 1, e = "hello" // ok

// ok, type of lambda and type of 'f' can be inferred
let f = (p: number) => b + p
let x // compile-time error -- either type or initializer

Every variable in a program must have an initial value before it can be used:

• If the initializer of a variable is specified explicitly, then its execution produces the initial value for this variable.

• Otherwise, the following situations are possible:

– If the type of a variable is T, and T has a default value (see Default Values for Types), then the variable is initialized with the default value.

– If a variable has no default value, then its value must be set by the Simple Assignment Operator before any use of the variable.

Invalid initialization is represented in the example below:

let a = b // compile-time error: circular dependency
let b = a
