class Derived1 extends Base implements Interface {
    // Derived1 is semantically equivalent to Derived2
    class Derived2 extends Base<SomeType> implements Interface<SomeType> {
        function foo<T = number>(input: T): T { return input}
        foo(1) // this call is semantically equivalent to next one
        foo<number>(1)

        class C1 <T1, T2 = number, T3> {
        // That is a compile-time error, as T2 has default but T3 does not

        class C2 <T1, T2 = number, T3 = string> {
            let c1 = new C2<number> // equal to C2<number, number, string>
            let c2 = new C2<number, string> // equal to C2<number, string, string>
            let c3 = new C2<number, Object, number> // all 3 type arguments provided

            function foo <T1 = T2, T2 = T1> () {
                // That is a compile-time error,
                // as T1's default refers to T2, which is defined after the T1
                // T2's default is valid as it refers to already defined type parameter T1
            }
        }
    }
}

#### 5.1.3 Type Parameter Variance

Normally, two different instantiations of the same generic class or interface (like Array<number> and Array<string>) are handled as different and unrelated types. ArkTS supports type parameter variance that allows subtyping relationship between such instantiations (See Subtyping), depending on the subtyping relationship between argument types.

When declaring type parameters of a generic type, special keywords in or out (called variance modifiers) are used to specify the variance of the type parameter (see Invariance, Covariance and Contravariance).

Type parameters with the keyword out are covariant . Covariant type parameters can be used in the out-position only as follows:

• Constructors can have out type parameters as parameters;

• Methods can have out type parameters as return types;

• Fields that have out type parameters as type must be readonly.

• Otherwise, a compile-time error occurs.

Type parameters with the keyword in are contravariant. Contravariant type parameters can be used in the in-position only as follows:

• Methods can have in type parameters as parameter types.

• Otherwise, a compile-time error occurs.

Type parameters with no variance modifier are implicitly invariant, and can occur in any position.

class X<in T1, out T2, T3> {
    (continues on next page)
