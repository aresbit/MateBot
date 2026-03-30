• Members inherited from their direct superclass (see Inheritance), except class Object that cannot have a direct superclass.

• Members declared in a direct superinterface (see Superinterfaces and Subinterfaces).

• Members declared in the class body (see Class Members).

Class members declared private are not accessible (see Accessible) to all subclasses of the current class.

Class members declared protected or public are inherited by all subclasses of the class and accessible (see Accessible) for all subclasses.

Constructors and static block are not members, and are not inherited.

Members can be as follows:

• Class fields (see Field Declarations),

• Methods (see Method Declarations), and

• Accessors (see Class Accessor Declarations).

A method is defined by the following:

1. Type parameter, i.e., the declaration of any type parameter of the method member.

2. Argument type, i.e., the list of types of arguments applicable to the method member.

3. Return type, i.e., the return type of the method member.

### 9.5 Access Modifiers

Access modifiers define how a class member or a constructor can be accessed. Accessibility in ArkTS can be of the following kinds:

• Private.

• Protected.

• Public.

The desired accessibility of class members and constructors can be explicitly specified by the corresponding access modifiers.

The syntax of class members or constructors modifiers is presented below:

accessModifier: 'private' | 'protected' | 'public'

If no explicit modifier is provided, then a class member or a constructor is implicitly considered public by default.
