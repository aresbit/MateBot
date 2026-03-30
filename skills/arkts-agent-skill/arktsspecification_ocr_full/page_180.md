(continued from previous page)

classMembers
;

classModifier:
'abstract' | 'final'
;

Classes with the final modifier are an experimental feature discussed in Final Classes.

The scope of a class declaration is specified in Scopes.

An example of a class is presented below:

class Point {
    public x: number
    public y: number
    public constructor(x : number, y : number) {
        this.x = x
        this.y = y
    }
    public distanceBetween(other: Point): number {
        return Math.sqrt(
            (this.x - other.x) * (this.x - other.x) +
            (this.y - other.y) * (this.y - other.y)
        )
    }
    static origin = new Point(0, 0)
}

#### 9.1.1 Abstract Classes

A class with the modifier abstract is known as abstract class. An abstract class is a class that cannot be instantiated, i.e., no objects of this type can be created. It serves as a blueprint for other classes by defining common fields and methods that subclasses must implement. Abstract classes can contain both abstract and concrete methods.

A compile-time error occurs if an attempt is made to create an instance of an abstract class:

abstract class X {
    field: number
    constructor (p: number) { this.field = p }
}
let x = new X(42)
// Compile-time error: Cannot create an instance of an abstract class.

Subclasses of an abstract class can be abstract or non-abstract. A non-abstract subclass of an abstract superclass can be instantiated. As a result, a constructor for the abstract class, and field initializers for non-static fields of that class are executed:

abstract class Base {
    field: number

(continues on next page)
