A type parameter of a generic can depend on another type parameter of the same generic.

If S constrains T, then the type parameter T directly depends on the type parameter S, while T directly depends on the following:

• S; or

• Type parameter U that depends on S.

A compile-time error occurs if a type parameter in the type parameter section depends on itself.

class Base {}
class Derived extends Base {}
class SomeType {}

class G<T, S extends T> {}

let x: G<Base, Derived> // correct: the second argument directly
    // depends on the first one
let y: G<Base, SomeType> // error: SomeType does not depend on Base

class A0<T> {
    data: T
    constructor (p: T) { this.data = p }
    foo () {
        let o: Object = this.data // error: T not compatible with Object
        console.log (this.data.toString()) // error: T has no methods or fields
    }
}

class A1<T extends Object> extends A0<T> {
    constructor (p: T) { super(p); this.data = p }
    override foo () {
        let o: Object = this.data // OK!
        console.log (this.data.toString()) // OK!
    }
}

#### 5.1.2 Type Parameter Default

Type parameters of generic types can have defaults. This situation allows dropping a type argument when a particular type of instantiation is used. However, a compile-time error occurs if:

• A type parameter without a default type follows a type parameter with a default type in the declaration of a generic type;

• Type parameter default refers to a type parameter defined after the current type parameter.

The application of this concept to both classes and functions is presented in the examples below:

class SomeType {}
interface Interface <T1 = SomeType> { }
class Base <T2 = SomeType> { }

(continues on next page)
