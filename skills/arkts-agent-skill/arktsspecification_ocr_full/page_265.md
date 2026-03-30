#### 15.7.2 Smart Types

Data entities like local variables (see Variable and Constant Declarations) and parameters (see Parameter List), if not captured in a lambda body and modified by the lambda code, are subjected to smart typing.

Every data entity has a static type, which is specified explicitly or inferred at the point of declaration. This type defines the set of operations that can be applied to the entity (namely, what methods can be called, and what other entities can be accessed if the entity acts as a receiver of the operation):

let a = new Object
a.toString() // entity 'a' has method toString()

If an entity is class type (see Classes), interface type (see Interfaces), or union type (see Union Types), then the compiler can narrow (smart cast) a static type to a more precise type (smart type), and allow operations that are specific to the type so narrowed:

function boo() {
    let a: number | string = 42
    a++ /* Smart type of 'a' is number and number-specific operations are type-safe */
}

class Base {}
class Derived extends Base { method () {} }
function goo() {
    let b: Base = new Derived
    b.method () /* Smart type of 'b' is Derived and Derived-specific operations can be applied in type-safe way */
}

Other examples are explicit calls to instanceof (see InstanceOf Expression) or checks against null (see Equality Expressions) as parts of if statements (see if Statements) or ternary conditional expressions (see Ternary Conditional Expressions):

function foo (b: Base, d: Derived|null) {
    if (b.instanceof Derived) {
        b.method()
    }
    if (d != null) {
        d.method()
    }
}

In like cases, a smart compiler requires no additional checks or casts (see Cast Expression) to deduce a smart type of an entity.

Overloading (see Overload Declarations) can cause tricky situations when a smart type results in calling an entity that suits the smart type rather than a declared type of an argument (see Overload Resolution):

class Base {b = 1}
class Derived extends Base{d = 2}

function fooBase (p: Base) {}
function fooDerived (p: Derived) {}

(continues on next page)
