declare interface I2 {
    foo () : void // method foo has no default implementation
}
class C2 implements I2 {} // Class C2 is invalid as foo() has no implementation
class C3 implements I2 { foo() {} } // Class C3 is valid as foo() has implementation

### 14.6 Ambient Namespace Declarations

Namespaces are used to logically group multiple entities. ArkTS supports ambient namespaces for better TypeScript compatibility. TypeScript often uses ambient namespaces to specify the platform API or a third-party library API.

The syntax of ambient namespace declaration is presented below:

ambientNamespaceDeclaration:
    'namespace' identifier '{' ambientNamespaceElement* '}'
;
ambientNamespaceElement:
    ambientNamespaceElementDeclaration | exportDirective
;
ambientNamespaceElementDeclaration:
    'export'?
    ( ambientConstantDeclaration
    | ambientFunctionDeclaration
    | ambientClassDeclaration
    | ambientInterfaceDeclaration
    | ambientNamespaceDeclaration
    | ambientAccessorDeclaration
    | 'const'? enumDeclaration
    | typeAlias
)

An enumeration type declaration can be prefixed with the keyword const for TypeScript compatibility. The prefix has no influence on the declared type. Only exported entities can be accessed outside a namespace.

Namespaces can be nested:

declare namespace A {
    export namespace B {
        export function foo(): void;
    }
}

A namespace is not an object but merely a scope for entities that can be accessed by using qualified names only.

If an ambient namespace is imported from a module, then all ambient namespace declarations are accessible (see Accessible) across all declarations and top-level statements of the current module.
