### 14.1 Ambient Constant Declarations

The syntax of ambient constant declaration is presented below:

ambientConstantDeclaration:
    'const' ambientConstList；《
    ;

ambientConstList:
    ambientConst（'，' ambientConst）*
;

ambientConst:
    identifier（('：' type）|（'='）
→(IntegerLiteral|FloatLiteral|StringLiteral|MultilineStringLiteral)))
;

An initializer expression for an ambient constant must be a numeric or string literal. The meaning of the literal is to define the type of the ambient constant, while the actual value must be provided when a non-ambient declaration is available.

### 14.2 Ambient Function Declarations

The syntax of ambient function declaration is presented below:

ambientFunctionDeclaration: 'function' identifier typeParameters? signature;

A compile-time error occurs if explicit return type for an ambient function declaration is not specified.

declare function foo(x: number): void // ok
declare function bar(x: number) // compile-time error

Ambient functions cannot have parameters with default values but can have optional parameters.

Ambient function declarations cannot specify function bodies.

declare function foo(x?: string): void // ok
declare function bar(y: number = 1): void // compile-time error

Note. The modifier async cannot be used in an ambient context.
