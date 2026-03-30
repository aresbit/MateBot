#### 17.10.2 Native Methods

Native method is a method marked with the keyword native (see Method Declarations).

Native methods are the methods implemented in a platform-dependent code written in another programming language (e.g., C).

A compile-time error occurs if:

• Method declaration contains the keyword abstract along with the keyword native.

• Native method has a body (see Method Body) that is a block instead of a simple semicolon or empty body.

#### 17.10.3 Native Constructors

Native constructor is a constructor marked with the keyword native (see Constructor Declaration).

Native constructors are the constructors implemented in a platform-dependent code written in another programming language (e.g., C).

A compile-time error occurs if a native constructor has a non-empty body (see Constructor Body).

### 17.11 Classes Experimental

#### 17.11.1 Final Classes

A class can be declared final to prevent extension, i.e., a class declared final can have no subclasses. No method of a final class can be overridden.

If a class type F expression is declared final, then only a class F object can be its value.

A compile-time error occurs if the extends clause of a class declaration contains another class that is final.

#### 17.11.2 Final Methods

A method can be declared final to prevent it from being overridden (see Overriding Methods) in subclasses.

A compile-time error occurs if:

• The method declaration contains the keyword abstract or static along with the keyword final.

• A method declared final is overridden.
