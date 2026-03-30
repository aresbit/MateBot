The usage of annotations is discussed in Using Annotations.

Interface members include:

• Members declared explicitly in the interface declaration;

• Members inherited from a direct superinterface (see Superinterfaces and Subinterfaces).

A compile-time error occurs if the method explicitly declared by the interface has the same name as the Object's public method.

interface I {
    toString (p: number): void // Compile-time error
    toString(): string { return "some string" } // Compile-time error
}

An interface inherits all members of the interfaces it extends (see Interface Inheritance).

A name in a declaration scope must be unique, i.e., the names of properties and methods of an interface type must not be the same (see Interface Declarations).

### 10.4 Interface Properties

Interface property can be defined in the form of a field or an accessor (a getter or a setter).

The syntax of interface property is presented below:

interfaceProperty:
  'readonly'? identifier '?' '?' '': 'type
  | 'get' identifier '(' ')' returnType
  | 'set' identifier '(' parameter ')'
;

An interface property is a required property (see Required Interface Properties) if it is one of the following:

• Explicit accessor, i.e., a getter or a setter; or

• Form of a field that has no ‘?’.

Otherwise, it is an optional property (see Optional Interface Properties).

If ‘?’ is used after the name of the property, then the property type is semantically equivalent to type | undefined.

interface I {
    property?: Type
}
// is the same as
interface I {
    property: Type | undefined
}
