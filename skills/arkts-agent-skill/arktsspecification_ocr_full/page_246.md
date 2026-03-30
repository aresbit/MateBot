The following restrictions apply:

• returnType must be a type that implements Interface defined in Standard Library.

• Only one ambient iterable declaration is allowed in an ambient class declaration.

declare class C {
    [Symbol.iterator](); CIterator
}

### 14.5 Ambient Interface Declarations

The syntax of ambient interface declaration is presented below:

Note. Ambient秤的 $ ^{1} $is supported in ambient contexts only. If written in ArkTS, ambient class implementation must conform to Iterable Types.

ambientInterfaceDeclaration:
    'interface' identifier typeParameters?
    interfaceExtendsClause?
    '{' ambientInterfaceMember* '}'
;
ambientInterfaceMember
    : interfaceProperty
    | ambientInterfaceMethodDeclaration
    | ambientIndexerDeclaration
    | ambientIterableDeclaration
;
ambientInterfaceMethodDeclaration:
    'default'? identifier signature
;

Ambient interface can contain additional members in the same manner as an ambient class (see Ambient Indexer, and Ambient Iterable).

If an interface method declaration is marked with the keyword default, then a non-ambient interface must contain the default implementation for the method as follows:

declare interface I1 {
    default foo (): void // method foo will have the default implementation
}
class C1 implements I1 {} // Class C1 is valid as foo() has the default implementation

interface I1 {
    // If such interface is used as I1 it will be runtime error as there is
    // no default implementation for foo()
    foo (): void
}
