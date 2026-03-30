# Chapter 16: Concurrency

Page range: 267-270

## Page 267

public_member()    // All members are public in interfaces
private private_member() {} // Except private methods with default implementation
}

class Derived extends Base implements Interface {
    public override public_member() {}
    // Public member can be overridden and/or implemented by the public one
    public override protected_member() {}
    // Protected member can be overridden by the protected or public one
    override private_member() {}
    // A compile-time error occurs if an attempt is made to override private member
    // or implement the private methods with default implementation
}

The table below represents semantic rules that apply in various contexts:


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>Context</td><td style='text-align: center; word-wrap: break-word;'>Semantic Check</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>An instance method is defined in a subclass with the same name as the instance method in a superclass.</td><td style='text-align: center; word-wrap: break-word;'>If signatures are override-compatible (see Override-Compatible Signatures), then overriding is used. Otherwise, a compile-time error occurs.</td></tr></table>

class Base {
    method_1() {}
    method_2(p: number) {}
}

class Derived extends Base {
    override method_1() {} // overriding
    method_2(p: string) {} // compile-time error
}

A constructor is defined in a subclass.

All base class constructors are available for call in all derived class constructors via super call (see Explicit Constructor Call).

class Base {
    constructor(p: number) {}
}

class Derived extends Base {
    constructor(p: string) {
        super(5)
    }
}

## Page 268

#### 15.8.2 Overriding and Overloading in Interfaces

Context Semantic Check
A method is defined in a subinterface with the same name as the method in the superinterface.
If signatures are override-compatible (see Override-Compatible Signatures), then overriding is used. Otherwise, a compile-time error occurs.
A method is defined in a subinterface with the same name as the private method in the superinterface.
A compile-time error occurs.

interface Base {
    method_1()
    method_2(p: number)
    private foo() {} // private method with implementation body
}

interface Derived extends Base {
    method_1() // overriding
    method_2(p: string) // compile-time error: non-compatible signature
    foo(p: number): void // compile-time error: the same name as private method
}

Two or more methods with the same name are defined in TBD is used. the same interface.

interface anInterface {
    instance_method() // 1st signature
    instance_method(p: number) // 2nd signature
}

#### 15.8.3 Override-Compatible Signatures

If there are two classes Base and Derived, and class Derived overrides the method foo() of Base, then foo() in Base has signature  $ S_1 < V_1 $,  $ \ldots $  $ V_k > (U_1, \ldots, U_n) : U_{n+1} $, and foo() in Derived has signature  $ S_2 < W_1 $,  $ \ldots $  $ W_l > (T_1, \ldots, T_m) : T_{m+1} $ as in the example below:

class Base {
    foo <V1, ... Vk> (p1: U1, ... pn: Un): Un+1
}
class Derived extends Base {
    override foo <W1, ... Wl> (p1: T1, ... pm: Tm): Tm+1
}

The signature  $ S_{2} $ is override-compatible with  $ S_{1} $ only if all of the following conditions are met:

1. Number of parameters of both methods is the same, i.e., n = m.

2. Each parameter type  $ T_i $ is a supertype of  $ U_i $ for  $ i $ in 1..n (contravariance).

## Page 269

3. If return type  $ T_{m+1} $ is this, then  $ U_{n+1} $ is this, or any of superinterfaces or superclass of the current type. Otherwise, return type  $ T_{m+1} $ is a subtype of  $ U_{n+1} $ (covariance).

4. Number of type parameters of either method is the same, i.e., k = 1.

5. Constraints of  $ W_{1}, \ldots, W_{1} $ are to be contravariant (see Invariance, Covariance and Contravariance) to the appropriate constraints of  $ V_{1}, \ldots, V_{k} $.

The following rule applies to generics:

• Derived class must have type parameter constraints to be subtype (see Subtyping) of the respective type parameter constraint in the base type;

• Otherwise, a compile-time error occurs.

class Base {}
class Derived extends Base {}
class A1 <CovariantTypeParameter extends Base> {}
class B1 <CovariantTypeParameter extends Derived> extends A1<CovariantTypeParameter> {}
// OK, derived class may have type compatible constraint of type parameters

class A2 <ContravariantTypeParameter extends Derived> {}
class B2 <ContravariantTypeParameter extends Base> extends A2<ContravariantTypeParameter>
→ {}
// Compile-time error, derived class cannot have non-compatible constraints of type_parameters

The semantics is represented in the examples below:

### 1. Class/Interface Types

interface Base {
    param(p: Derived): void
        ret(): Base
}

interface Derived extends Base {
    param(p: Base): void // Contravariant parameter
        ret(): Derived // Covariant return type
}

### 2. Function Types

interface Base {
    param(p: (q: Base)=>Derived): void
        ret(): (q: Derived)=> Base
}

interface Derived extends Base {
    param(p: (q: Derived)=>Base): void // Covariant parameter type, contravariant_
    →return type
    ret(): (q: Base)=>Derived // Contravariant parameter type, covariant_
    →return type
}

### 3. Union Types

## Page 270

interface BaseSuperType {}
interface Base extends BaseSuperType {
    // Overriding for parameters
    param<T extends Derived, U extends Base>(p: T | U): void

    // Overriding for return type
    ret<T extends Derived, U extends Base>(): T | U
}

interface Derived extends Base {
    // Overriding kinds for parameters, Derived <: Base
    param<T extends Base, U extends Object>(
        p: Base | BaseSuperType // contravariant parameter type: Derived | Base <: Base_
    ) : void
    // Overriding kinds for return type
    ret<T extends Base, U extends BaseSuperType>(): T | U
}

### 4. Type Parameter Constraint

interface Base {
    param<T extends Derived>(p: T): void
        ret<T extends Derived>(); T
}

interface Derived extends Base {
    param<T extends Base>(p: T): void
    →parameters
        ret<T extends Base>(); T
    →return type
}

Override compatibility with Object is represented in the example below:

interface Base {
    kinds_of_parameters<T extends Derived, U extends Base> ( // It represents all_
        →possible kinds of parameter type
        p01: Derived,
        p02: (q: Base)=>Derived,
        p03: number,
        p04: T | U,
        p05: E1,
        p06: Base[],
        p07: [Base, Base]
    ): void
    kinds_of_return_type(): Object // It can be overridden by all subtypes of Object
}
interface Derived extends Base {
    kinds_of_parameters( // Object is a supertype for all class types
        p1: Object,
        p2: Object,
        p3: Object,
    )
}
