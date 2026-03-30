constructor (p: number) { this.field = p }
}

class Derived extends Base {
    constructor (p: number) { super(p) }
}

A method with the modifier abstract is considered an abstract method (see Abstract Methods). Abstract methods have no bodies, i.e., they can be declared but not implemented.

Only abstract classes can have abstract methods. A compile-time error occurs if a non-abstract class has an abstract method:

class Y {
    abstract method (p: string)
    /* Compile-time error: Abstract methods can only
        be within an abstract class. */
}

A compile-time error occurs if an abstract method declaration contains the modifiers final or override.

abstract class Y {
    final abstract method (p: string)
    // Compile-time error: Abstract methods cannot be final
}

### 9.2 Class Extension Clause

All classes except class Object can contain the extends clause that specifies the base class, or the direct superclass of the current class. In this situation, the current class is a derived class, or a direct subclass. Any class, except class Object that has no extends clause, is assumed to have the extends Object clause.

The syntax of class extension clause is presented below:

classExtendsClause:
    'extends' typeReference
;

A compile-time error occurs if:

• typeReference refers directly to, or is an alias of any non-class type, e.g., of interface, enumeration, union, function, or utility type.

• Class type named by typeReference is not accessible (see Accessible).

• An extends clause appears in the declaration of the class Object.

• The extends graph has a cycle.

Class extension implies that a class inherits all members of the direct superclass.

Note. Private members are inherited from superclasses, but are not accessible (see Accessible) within subclasses:
