### 9.6 Field Declarations

Field declarations represent data members in class instances or static data members (see Static and Instance Fields). Class instance field declarations are its own fields in contrast to the inherited ones. Syntactically, a field declaration is similar to a variable declaration.

classFieldDeclaration:
    fieldModifier*
    identifier
    ('??': 'type initializer?
    | '?? initializer
    | '!! ':' type
)
;
fieldModifier:
    'static' | 'readonly' | 'override'
;

A field with an identifier marked with ‘?’ is called optional field (see Optional Fields). A field with an identifier marked with ‘!’ is called field with late initialization (see Fields with Late Initialization).

A compile-time error occurs if:

• Some field modifier is used more than once in a field declaration.

• Name of a field declared in the body of a class declaration is also used for a method of this class with the same static or non-static status.

• Name of a field declared in the body of a class declaration is also used for another field in the same declaration with the same static or non-static status.

Any static field can be accessed only with the qualification of a superclass name (see Field Access Expression).

A class can inherit more than one field or property with the same name from its superinterfaces, or from both its superclass (see Inheritance) and superinterfaces (see Interface Inheritance. However, an attempt to refer to such a field or property by its simple name within the class body causes a compile-time error.

The same field or property declaration can be inherited from an interface in more than one way. In that case, the field or property is considered to be inherited only once.

#### 9.6.1 Static and Instance Fields

There are two categories of class fields as follows:

• Static fields

Static fields are declared with the modifier static. A static field is not part of a class instance. There is one copy of a static field irrespective of how many instances of the class (even if zero) are eventually created.

Static fields are always accessed by using a qualified name notation wherever the class name is accessible (see Accessible).

• Instance, or non-static fields
