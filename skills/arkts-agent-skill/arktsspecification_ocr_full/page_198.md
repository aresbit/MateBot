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
