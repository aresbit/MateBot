constructorDeclaration:
    'native'? 'constructor' identifier? parameters constructorBody?
;

An optional identifier in constructor declaration is an experimental feature discussed in Constructor Names. Constructors are called by the following:

• Class instance creation expressions (see New Expressions); and

• Explicit constructor calls from other constructors (see Constructor Body).

Access to constructors is governed by access modifiers (see Access Modifiers and Scopes). Declaring a constructor inaccessible prevents class instantiation from using this constructor. If the only constructor is declared inaccessible, then no class instance can be created.

A native constructor (an experimental feature described in Native Constructors) must have no constructorBody. Otherwise, a compile-time error occurs.

A non-native constructor must have constructorBody. Otherwise, a compile-time error occurs.

A compile-time error occurs if more than one non-native anonymous constructors are defined in a class:

class C {
    constructor (s: string) {}
    constructor () {} // compile-time error: multiple anonymous constructors
}

#### 9.9.1 Formal Parameters

The syntax and semantics of a constructor’s formal parameters are identical to those of a method.

#### 9.9.2 Constructor Body

Constructor body is a block of code that implements a constructor.

The syntax of constructor body is presented below:

constructorBody:
    '{' statement* '}'
;

The constructor body must provide correct initialization of new class instances. Constructors have two variations:

• Primary constructor that initializes instance own fields directly;

• Secondary constructor that uses another same-class constructor to initialize its instance fields.

The high-level sequence of a primary constructor body includes the following:

1. Mandatory call to a superconstructor (see Explicit Constructor Call) if a class has an extension clause (see Class Extension Clause) on all execution paths of the constructor body.
