### 14.3 Ambient Overload Function Declarations

The syntax of ambient overload function declaration is identical to that of Function Overload Declarations. The semantics of such declarations is defined by the same rules.

// Top-level functions are overloaded
declare function foo1(p: string): void
declare function foo2(p: number): void
declare overload foo {foo1, foo2}

// Namespace functions are overloaded
declare namespace N {
    function foo1(p: string): void
    function foo2(p: number): void
    overload foo {foo1, foo2}
}

// All calls are valid
foo("a string")
foo(5)
N.foo("a string")
N.foo(5)

### 14.4 Ambient Class Declarations

The syntax of ambient class declaration is presented below:

ambientClassDeclaration:
  'class' | 'struct' identifier typeParameters?
  classExtendsClause? implementsClause?
  '{' ambientClassMember* '}'
;
ambientClassMember:
  ambientAccessModifier?
  ( ambientFieldDeclaration
  | ambientConstructorDeclaration
  | ambientMethodDeclaration
  | overloadMethodDeclaration
  | ambientClassAccessorDeclaration
  | ambientIndexerDeclaration
  | ambientCallSignatureDeclaration
  | ambient 词性
  )
  ;
ambientAccessModifier:
  'public' | 'protected'
;
