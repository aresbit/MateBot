(continued from previous page)

typeParameterDefault:
    '=' typeReference ('[]')?
;

A generic class, interface, type alias, method, or function defines a set of parameterized classes, interfaces, unions, arrays, methods, or functions respectively (see Generic Instantiations). A single type argument can define only one set for each possible parameterization of the type parameter section.

#### 5.1.1 Type Parameter Constraint

If possible instantiations need to be constrained, then an individual constraint can be set for each type parameter after the keyword extends. A constraint can have the form of any type.

If no constraint is specified, then the constraint is Type Any, i.e., the lacking explicit constraint effectively means extends Any. As a consequence, the type parameter is not compatible with Type Object, and has neither methods nor fields available for use.

If type parameter T has type constraint S, then the actual type of the generic instantiation must be a subtype of S (see Subtyping). If the constraint S is a non-nullish type (see Nullish Types), then T is also non-nullish.

class Base {}
class Derived extends Base { }
class SomeType { }

class G<T extends Base> { }

let x = new G<Base> // OK
let y = new G<Derived> // OK
let z = new G<SomeType> // Compile-time : SomeType is not compatible with Base

class H<T extends Base|SomeType> {}
let h1 = new H<Base> // OK
let h2 = new H<Derived> // OK
let h3 = new H<SomeType> // OK
let h4 = new H<Object> // Compile-time : Object is not compatible with Base/SomeType

class Exotic<T extends "aa"| "bb"> {}
let e1 = new Exotic<"aa"> // OK
let e2 = new Exotic<"cc"> // Compile-time : "cc" is not compatible with "aa"| "bb"

class A {
    f1: number = 0
    f2: string = ""
    f3: boolean = false
}
class B <T extends keyof A> {}
let b1 = new B<'f1'> // OK
let b2 = new B<'f0'> // Compile-time error as 'f0' does not fit the constraint
let b3 = new B<keyof A> // OK
