// Subtyping illustration for generic with parameter variance

// U1 <: U0
class U0 {}
class U1 extends U0 {}

// Generic with contravariant parameter
class E<in T> {}

let e0: E<U0> = new E<U1> // CTE, E<U0> is subtype of E<U1>
let e1: E<U1> = new E<U0> // OK, E<U1> is supertype for E<U0>

// Generic with covariant parameter
class F<out T> {}

let f0: F<U0> = new F<U1> // OK, F<U0> is supertype for F<U1>
let f1: F<U1> = new F<U0> // CTE, F<U1> is subtype of F<U0>

#### 15.2.3 Subtyping for Literal Types

Any string literal type (see String Literal Types) is subtype of type string. It affects overriding as shown in the example below:

class Base {
    foo(p: "1"): string { return "42" }
}
class Derived extends Base {
    override foo(p: string): "1" { return "1" }
}
// Type "1" <: string

let base: Base = new Derived
let result: string = base.foo("1")
/* Argument "1" (value) is compatible to type "1" and to type string in the overridden method
    Function result of type string accepts "1" (value) of literal type "1"
*/

Literal type null (see Literal Types) is a subtype and a supertype to itself. Similarly, literal type undefined is a subtype and a supertype to itself.
