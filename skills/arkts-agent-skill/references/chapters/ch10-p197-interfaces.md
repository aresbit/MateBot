# Chapter 10: Interfaces

Page range: 197-202

## Page 197

#### 9.7.1 Static Methods

A method declared in a class with the modifier static is a static method.

A compile-time error occurs if:

• The method declaration contains another modifier (abstract, final, or override) along with the modifier static.

Static methods are always called without reference to a particular object. As a result, a compile-time error occurs if the keywords this or super are used inside a static method.

Static methods can be inherited from a superclass or shadowed by name regardless of the their signature:

• The header or body of a class method includes the name of a type parameter of the surrounding declaration.

class Base {
    static foo() { console.log("static foo() from Base") }
    static bar() { console.log("static foo() from Base") }
}

class Derived extends Base {
    static foo(p: string) { console.log("static foo() from Derived") }
}

Base.foo() // Output: static foo() from Base
Base.bar() // Output: static foo() from Base
Derived.bar() // Output: static foo() from Base, bar() is inherited
Derived.foo("a string") // Output: static foo() from Derived, foo() is shadowed
Derived.foo() // compile-time error as foo() in Derived has shadowed Base.
→foo()

Note: class static methods may access protected or private members of the same class type or derived one represented as parameters or local variables:

class C {
    protected count1: number
    private count2: number
    static getCount(c: C): number {
        const local_c = new C
        return c.count1 + c.count2 + local_c.count1 + local_c.count2 // OK
    }
    static handleDerived (b: B) {
        b.count1 + b.count2 // OK
    }
}
class B extends C {
    static dealWithProtected (b: B) {
        b.count1 // OK
        b.count2 // compile-time error
    }
}
C.getCount (new C) // will return the sum of counts
C.handleDerived (new B) // will work with protected and private fields

## Page 198

#### 9.7.2 Instance Methods

A method that is not declared static is called non-static method, or instance method.

An instance method is always called with respect to an object that becomes the current object which the keyword this refers to during the execution of the method body.

#### 9.7.3 Abstract Methods

An abstract method declaration introduces the method as a member along with its signature but without implementation. An abstract method is declared with the modifier abstract in the declaration.

Non-abstract methods can be referred to as concrete methods.

A compile-time error occurs if:

• An abstract method is declared private.

• The method declaration contains another modifier (static, final, native, or async) along with the modifier abstract.

• The declaration of an abstract method m does not appear directly within abstract class A.

• Any non-abstract subclass of A (see Abstract Classes) does not provide implementation for m.

An abstract method declaration provided by an abstract subclass can override another abstract method. An abstract method can also override non-abstract methods inherited from base classes or base interfaces as follows:

class C {
    foo() {}
}
interface I {
    foo() {} // default implementation
}
abstract class X extends C implements I {
    abstract foo(): void /* Here abstract foo() overrides both foo() coming from class C and interface I */
}

#### 9.7.4 Async Methods

Async methods are discussed in Async Methods.

## Page 199

#### 9.7.5 Overriding Methods

The override modifier indicates that an instance method in a superclass is overridden by the corresponding instance method from a subclass (see Overriding).

The usage of the modifier override is optional but strongly recommended as it makes the overriding explicit.

A compile-time error occurs if:

• Method marked with the modifier override overrides no method from a superclass.

• Method declaration contains modifier static along with the modifier override.

If the signature of an overridden method contains parameters with default values (see Optional Parameters), then the overriding method must always use the same default parameter values for the overridden method. Otherwise, a compile-time error occurs.

More details on overriding are provided in Overriding in Classes and Overriding and Overloading in Interfaces.

#### 9.7.6 Native Methods

Native methods are discussed in Native Methods.

#### 9.7.7 Method Body

Method body is a block of code that implements a method. A semicolon or an empty body (i.e., no body at all) indicates the absence of implementation.

An abstract or native method must have an empty body.

In particular, a compile-time error occurs if:

• The body of an abstract or native method declaration is a block.

• The method declaration is neither abstract nor native, but its body is either empty

The rules that apply to return statements in a method body are discussed in return Statements.

A compile-time error occurs if a method is declared to have a return type, but its body can complete normally (see Normal and Abrupt Statement Execution).

#### 9.7.8 Methods Returning this

A return type of an instance method can be this. It means that the return type is the class type to which the method belongs. It is the only place where the keyword this can be used as type annotation (see Signatures and Return Type).

The only result that is allowed to be returned from such a method is this:

## Page 200

class C {
    foo(): this {
        return this
    }
}

The return type of an overridden method in a subclass must also be this:

class C {
    foo(): this {
        return this
    }
}

class D extends C {
    foo(): this {
        return this
    }
}

let x = new C().foo() // type of 'x' is 'C'
let y = new D().foo() // type of 'y' is 'D'

Otherwise, a compile-time error occurs.

### 9.8 Class Accessor Declarations

Class accessors are often used instead of fields to add additional control for operations of getting or setting a field value. An accessor can be either a getter or a setter.

The syntax of class accessor declarations is presented below:

class AccessorDeclaration:
    class AccessorModifier*
    ( 'get' identifier '(' ')' returnType? block?
    | 'set' identifier '(' parameter ')' block?
)
;
class AccessorModifier:
    'abstract'
| 'static'
| 'final'
| 'override'
| 'native'
;

Accessor modifiers are a subset of method modifiers. The allowed accessor modifiers have exactly the same meaning as the corresponding method modifiers (see Abstract Methods for the modifier abstract, Static Methods for the modifier

## Page 201

static, Final Methods for the modifier final, Overriding Methods for the modifier override, and Native Methods for the modifier native).

class Person {
    private _age: number = 0
    get age(): number { return this._age }
    set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        this._age = a
    }
}

A get-accessor (getter) must have an explicit return type and no parameters, or no return type at all on condition it can be inferred from the getter body. A set-accessor (setter) must have a single parameter and no return type. The use of getters and setters looks the same as the use of fields. A compile-time error occurs if:

• Getters or setters are used as methods;

• Getter return type cannot be inferred from the getter body;

• Set-accessor (setter) has a single parameter that is optional (see Optional Parameters):

class Person {
    private _age: number = 0
    get age(): number { return this._age }
    set age(a: number) {
        if (a < 0) { throw new Error("wrong age") }
        this._age = a
    }
}

let p = new Person()
p.age = 25     // setter is called
if (p.age > 30) { // getter is called
    // do something
}
p.age(17) // Compile-time error: setter is used as a method
let x = p.age() // Compile-time error: getter is used as a method

class X {
    set x (p?: Object) {} // Compile-time error: setter has optional parameter
}

If a getter has no return type specified, then the type is inferred as in Return Type Inference.

class Person {
    private _age: number = 0
    get age() { return this._age } // return type is inferred as number
}

A class can define a getter, a setter, or both with the same name. If both a getter and a setter with a particular name are defined, then both must have the same accessor modifiers. Otherwise, a compile-time error occurs.

Accessors can be implemented by using a private field or fields to store the data as in the example above.

## Page 202

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
