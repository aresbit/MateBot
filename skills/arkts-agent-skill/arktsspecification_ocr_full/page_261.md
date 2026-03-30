Note. If a generic class or an interface has a type parameter T while its method has its own type parameter T, then the two types are different and unrelated.

class A<T> {
    data: T
    constructor (p: T) { this.data = p } // OK, as here 'T' is a class type parameter
    method <T>(p: T) {
        this.data = p // compile-time error as 'T' of the class is different from 'T' of the_method
    }
}

### 15.4 Assignability

Type  $ T_{1} $ is assignable to type  $ T_{2} $ if:

•  $ T_{1} $ is type never;

 $ T_{1} $ is identical to  $ T_{2} $ (see Type Identity);

• T1 is a subtype of T2 (see Subtyping); or

• Implicit conversion (see Implicit Conversions) is present that allows converting a value of type T1 to type T2.

Assignability relationship is asymmetric, i.e., that T1 is assignable to T2 does not imply that T2 is assignable to type T1.

### 15.5 Invariance, Covariance and Contravariance

Variance is how subtyping between types relates to subtyping between derived types, including generic types (See Generics), member signatures of generic types (type of parameters, return type), and overriding entities (See Override-Compatible Signatures). Variance can be of three kinds:

• Covariance,

• Contravariance, and

• Invariance.

Covariance means it is possible to use a type which is more specific than originally specified.

Contravariance means it is possible to use a type which is more general than originally specified.

Invariance means it is only possible to use the original type, i.e., there is no subtyping for derived types.

Valid and invalid usages of variance are represented in the examples below. If class Base is defined as follows:

class Base {
    method_one(p: Base): Base {}
    method_two(p: Derived): Base {}
    method_three(p: Derived): Derived {}
}
