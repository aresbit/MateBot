Ambient field declarations have no initializers.

The syntax of ambient field declaration is presented below:

ambientFieldDeclaration:
    ambientFieldModifier* identifier : 'type
;
ambientFieldModifier:
    'static' | 'readonly'
;

Ambient constructor, method, and accessor declarations have no bodies.

Their syntax is presented below:

ambientConstructorDeclaration:
    'constructor' parameters
;
ambientMethodDeclaration:
    ambientMethodModifier* identifier signature
;
ambientMethodModifier:
    'static'
;
ambientClassAccessorDeclaration:
    ambientMethodModifier*
( 'get' identifier '(' ')' returnType
| 'set' identifier '(' parameter ')'
)
;

Ambient methods can be overloaded similarly to non-ambient methods with the same syntax and semantics (see Class Method Overload Declarations).

// Class methods are overloaded
declare class A {
    foo1(p: string): void
    foo2(p: number): void
    overload foo {foo1, foo2}
}

// All methods calls are valid
function demo (a: A) {
    a.foo("a string")
    a.foo(5)
}
