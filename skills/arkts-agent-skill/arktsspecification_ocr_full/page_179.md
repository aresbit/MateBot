## CLASSES

Class declarations introduce new reference types and describe the manner of their implementation.

A class body contains declarations and initializer blocks.

Declarations can introduce class members (see Class Members) or class constructors (see Constructor Declaration).

The body of the declaration of a member comprises the scope of a declaration (see Scopes).

Class members include:

• Fields.

• Methods, and

Class members can be declared or inherited.

• Accessors.

Every member is associated with the class declaration it is declared in.

Field, method, accessor and constructor declarations can have the following access modifiers (see Access Modifiers):

• Public.

• Protected.

• Private.

Every class defines two class-level scopes (see Scopes): one for instance members, and the other for static members. It means that two members of a class can have the same name if one is static while the other is not.

### 9.1 Class Declarations

Every class declaration defines a class type, i.e., a new named reference type.

The class name is specified by an identifier inside a class declaration.

If typeParameters are defined in a class declaration, then that class is a generic class (see Generics).

The syntax of class declaration is presented below:

classDeclaration:

    classModifier? 'class' identifier typeParameters?

    classExtendsClause? implementsClause?

(continues on next page)
