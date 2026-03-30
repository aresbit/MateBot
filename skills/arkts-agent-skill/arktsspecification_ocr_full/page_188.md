### 9.4 Class Members

A class can contain declarations of the following members:

• Fields.

• Methods.

• Accessors.

• Constructors.

• Method overloads (see Class Method Overload Declarations),

• Constructor overloads (see Constructor Overload Declarations), and

• Single static block for initialization (see Static Initialization).

The syntax is presented below:

classMembers:
    '{}
        classMember* staticBlock? classMember*
    '}'
;

classMember:
    annotationUsage?
    accessModifier?
    ( constructorDeclaration
        | overloadConstructorDeclaration
        | classFieldDeclaration
        | classMethodDeclaration
        | overloadMethodDeclaration
    | classAccessorDeclaration
)
;
staticBlock: 'static' Block;

Declarations can be inherited or immediately declared in a class. Any declaration within a class has a class scope. The class scope is fully defined in Scopes.

Members can be static or non-static as follows:

• Static members that are not part of class instances, and can be accessed by using a qualified name notation (see Names) anywhere the class name is accessible (see Accessible); and

• Non-static, or instance members that belong to any instance of the class.

Names of all static and non-static entities in a class declaration scope (see Scopes) must be unique, i.e., fields, methods, and overloads with the same static or non-static status cannot have the same name.

The use of annotations is discussed in Using Annotations.

Class members are as follows:
