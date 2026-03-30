## AMBIENT DECLARATIONS

Ambient declaration specifies an entity that is declared elsewhere. Ambient declarations:

• Provide type information for entities included into a program from external sources.

• Introduce no new entities like regular declarations do.

• Cannot include executable code, and thus have no initializers.

Ambient functions, methods, and constructors have no bodies.

The syntax of ambient declaration is presented below:

ambientDeclaration:
  'declare'
  ( ambientConstantDeclaration
  | ambientFunctionDeclaration
  | overloadFunctionDeclaration
  | ambientClassDeclaration
  | ambientInterfaceDeclaration
  | ambientNamespaceDeclaration
  | ambientAnnotationDeclaration
  | ambientAccessorDeclaration
  | 'const'? enumDeclaration
  | typeAlias
)

An ambient enumeration type declaration can be prefixed by the keyword const for TypeScript compatibility. It has no influence on the declared type.

A compile-time error occurs if the modifier declare is used in a context that is already ambient:

declare namespace A{
    declare function foo(): void // compile-time error
}

A compile-time warning occurs if an ambient declaration is marked with export keyword as all ambient declarations are exported by default:

export declare namespace A{ // compile-time warning
    function foo(): void
}
