## INTERFACES

An interface declaration declares an interface type, i.e., a reference type that:

• Includes properties and methods as its members;

• Has no instance variables (fields);

• Usually declares one or more methods;

• Allows otherwise unrelated classes to provide implementations for the methods, and so implement the interface.

Creating an instance of interface type is not possible.

An interface can be declared direct extension of one or more other interfaces. If so, the interface inherits all members from the interfaces it extends. Inherited members can be optionally overridden or hidden.

A class can be declared to directly implement one or more interfaces. Any instance of a class implements all methods specified by its interface(s). A class implements all interfaces that its direct superclasses and direct superinterfaces implement. Interface inheritance allows objects to support common behaviors without sharing a superclass.

The value of a variable declared interface type can be a reference to any instance of a class that implements the specified interface. However, it is not enough for a class to implement all methods of an interface. A class or one of its superclasses must be actually declared to implement an interface. Otherwise, the class is not considered to implement the interface.

The rules of subtyping are discussed in detail in Subtyping for Non-Generic Classes and Interfaces and Subtyping for Generic Classes and Interfaces.

### 10.1 Interface Declarations

Interface declaration specifies a new named reference type.

The syntax of interface declarations is presented below:

interfaceDeclaration:
    'interface' identifier typeParameters?
    interfaceExtendsClause? '{' interfaceMember* '}'
;
interfaceExtendsClause:
    'extends' interfaceTypeList
;

(continues on next page)
