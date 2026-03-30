#### 15.2.4 Subtyping for Union Types

A union type U participates in a subtyping relationship (see Subtyping) in the following cases:

1. Union type U (U₁ | ... | Uₙ) is a subtype of type T if each Uᵢ is a subtype of T.

let s1: "1" | "2" = "1"
let s2: string = s1 // ok

let a: string | number | boolean = "abc"
let b: string | number = 42
a = b // OK
b = a // compile-time error, boolean is absent is 'b'

class Base {}
class Derived1 extends Base {}
class Derived2 extends Base {}

let x: Base = ...
let y: Derived1 | Derived2 = ...

x = y // OK, both Derived1 and Derived2 are subtypes of Base
y = x // compile-time error

let x: Base | string = ...
let y: Derived1 | string ...
x = y // OK, Derived1 is subtype of Base
y = x // compile-time error

2. Type T is a subtype of union type U (U1 | ... | Un) if for some i T is a subtype of Ui.

let u: number | string = 1 // ok
u = "aa" // ok
u = 1.0 // ok, 1.0 is of type 'number' (double)
u = 1 // compile-time error, type 'int' is not a subtype of 'number'
u = true // compile-time error

Note. If union type normalization produces a single type, then this type is used instead of the initial set of union types. This concept is represented in the example below:

let u: "abc" | "cde" | string // type of 'u' is string

#### 15.2.5 Subtyping for Function Types

Function type F with parameters  $ FP_1 $,  $ \ldots $,  $ FP_m $ and return type FR is a subtype of function type S with parameters  $ SP_1 $,  $ \ldots $,  $ SP_n $ and return type SR if all of the following conditions are met:

• m ≤ n;

• Parameter type of  $ SP_i $ for each  $ i \leq m $ is a subtype of parameter type of  $ FP_i $ (contravariance), and  $ SP_i $ is: - Rest parameter if  $ FP_i $ is a rest parameter; - Optional parameter if  $ FP_i $ is an optional parameter.

• Type FR is a subtype of SR (covariance).
