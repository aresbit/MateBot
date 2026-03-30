# NAMES, DECLARATIONS AND SCOPES

This chapter introduces the following three mutually-related notions:

• Names.

• Declarations, and

• Scopes.

Each entity in an ArkTS program—a variable, a constant, a class, a type, a function, a method, etc.—is introduced via a declaration. An entity declaration defines a name of the entity. The name is used to refer to the entity further in the program text. The declaration binds the entity name with the scope (see Scopes). The scope affects the accessibility of a new entity, and how it can be referred to by its qualified or simple (unqualified) name.

### 4.1 Names

A name is a sequence of one or more identifiers. A name allows referring to any declared entity. Names can have two syntactical forms:

• Simple name that consists of a single identifier;

• Qualified name that consists of a sequence of identifiers with the token ‘.’ as separator.

Both situations are covered by the below syntax rule:

qualifiedName:
    identifier ('.' identifier )*
;

In a qualified name N.x (where N is a simple name, and x is an identifier that can follow a sequence of identifiers separated with ‘.’ tokens), N can name the following:

• Name of a module (see Modules and Namespaces) that is introduced as a result of import * as N (see Bind All with Qualified Access) with x to name the exported entity;

• A class or interface type (see Classes, Interfaces) with x to name its static member;

• A class or interface type variable with x to name its instance member.
