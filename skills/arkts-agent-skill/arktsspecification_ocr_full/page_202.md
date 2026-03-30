class Person {
    name: string = ""
    surname: string = ""
    get fullName(): string {
        return this.surname + "" + this.name
    }
}
console.log (new Person().fullName)

A name of an accessor cannot be the same as that of a non-static field, or of a method of class or interface. Otherwise, a compile-time error occurs:

class Person {
    name: string = ""
    get name(): string { // Compile-time error: getter name clashes with the field name
        return this.name
    }
    set name(a_name: string) { // Compile-time error: setter name clashes with the field_
        →name
        this.name = a_name
    }
}

In the process of inheriting and overriding (see Overriding), accessors behave as methods. The getter parameter type follows the covariance pattern, and the setter parameter type follows the contravariance pattern (see Override-Compatible Signatures):

class Base {
    get field(): Base { return new Base }
    set field(a_field: Derived) {}
}

class Derived extends Base {
    override get field(): Derived { return new Derived }
    override set field(a_field: Base) {}
}

function foo (base: Base) {
    base.field = new Derived // setter is called
        let b: Base = base.field // getter is called
    }

    foo (new Derived)

### 9.9 Constructor Declaration

Constructors are used to initialize objects that are instances of a class. A constructor declaration starts with the keyword constructor, and has optional name. In any other syntactical aspect, a constructor declaration is similar to a method declaration with no return type:
