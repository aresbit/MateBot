#### 4.6.2 Constant Declarations

A constant declaration introduces a named variable with a mandatory explicit value. The value of a constant cannot be changed by an assignment expression (see Assignment). If the constant is an object or array, then object fields or array elements can be modified.

The syntax of constant declarations is presented below:

constantDeclarations:
    'const' constantDeclarationList
;

constantDeclarationList:
    constantDeclaration (',' constantDeclaration)*
;

constantDeclaration:
    identifier (':' type)? initializer
;

The type T of a constant declaration is determined as follows:

• If T is the type specified in a type annotation (if any) of the declaration, then the initializer expression must be assignable to T (see Assignability with Initializer).

• If no type annotation is available, then T is inferred from the initializer expression (see Type Inference from Initializer).

const a: number = 1 // ok
const b = 1 // ok, int type is inferred
const c: number = 1, d = 2, e = "hello" // ok
const x // compile-time error -- initializer is mandatory
const y: number // compile-time error -- initializer is mandatory

#### 4.6.3 Assignability with Initializer

If a variable or constant declaration contains type annotation T and initializer expression E, then the type of E must be assignable to T (see Assignability).

#### 4.6.4 Type Inference from Initializer

The type of a declaration that contains no explicit type annotation is inferred from the initializer expression as follows:

- In a variable declaration (not in a constant declaration, though), if the initializer expression is of a literal type, then the literal type is replaced for its supertype, if any (see Subtyping for Literal Types). If the initializer expression is of a union type that contains literal types, then each literal type is replaced for its supertype (see Subtyping for Literal Types), and then normalized (see Union Types Normalization).

• Otherwise, the type of a declaration is inferred from the initializer expression.
