let array: MyArray<boolean> = [true, false] // Explicit array instantiation, type_
→argument provided

class X <T1, T2> {}
// Different forms of explicit instantiations of class X producing new generic entities
class Y<T> extends X<number, T> { // class Y extends X instantiated with number and T
    f1: X<Object, T> // X instantiated with Object and T
    f2: X<T, string> // X instantiated with T and string
    constructor() {
        this.f1 = new X<Object, T>
        this.f2 = new X<T, string>
    }
}

A compile-time error occurs if type arguments are provided for non-generic class, interface, type alias, method, or function.

In the explicit generic instantiation  $ G < T_1, \ldots, T_n>, G $ is the generic declaration, and  $ <T_1, \ldots, T_n> $ is the list of its type arguments.

If type parameters  $ T_1, \ldots, T_n $ of a generic declaration are constrained by the corresponding  $ C_1, \ldots, C_n $, then  $ T_i $ is assignable to each constraint type  $ C_i $ (see Assignability). All subtypes of the type listed in the corresponding constraint have each type argument  $ T_i $ of the parameterized declaration ranging over them.

A generic instantiation  $ G < T_1, \ldots, T_n> $ is well-formed if all of the following is true:

• The generic declaration name is G;

• The number of type arguments equals the number of type parameters of G; and

• All type arguments are assignable to the corresponding type parameter constraint (see Assignability).

A compile-time error occurs if an instantiation is not well-formed.

Unless explicitly stated otherwise in appropriate sections, this specification discusses generic versions of class type, interface type, or function.

Any two generic instantiations are considered provably distinct if:

• Both are parameterizations of distinct generic declarations; or

• Any of their type arguments is provably distinct.

#### 5.2.3 Implicit Generic Instantiations

In an implicit instantiation, type arguments are not specified explicitly. Such type arguments are inferred (see Type Inference) from the context in which a generic is referred. It is represented in the example below:

function foo <G> (x: G, y: G) {} // Generic function declaration
foo (new Object, new Object) // Implicit generic function instantiation
// based on argument types: the type argument is inferred
function process <P, R> (arg: P, cb?: (p: P) => R): P | R {

(continues on next page)
