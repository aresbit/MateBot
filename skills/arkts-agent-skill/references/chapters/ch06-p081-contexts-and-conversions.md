# Chapter 6: Contexts and Conversions

Page range: 81-86

## Page 81

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

## Page 82

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

## Page 83

// T1 can be used in in-position only
foo (p: T1) {} // OK
foo1(p: T1): T1 { return p } // error: T1 in out-position
fldT1: T1 // error: T1 in invariant position

8
9
10
11
12
13
14
15
16

In case of function types (see Function Types), variance interleaving occurs.

class X<in T1, out T2> {
    foo (p: T1): T2 {...} // in - out
    foo (p: (p: T2)=> T1) {...} // out - in
    foo (p: (p: (p: T1)=>T2)=> T1) {...} // in - out - in
    foo (p: (p: (p: T2)=> T1)=>T2)=> T1) {...} // out - in - out - in
    // and further more
}

A compile-time error occurs if function or method type parameters have a variance modifier specified.

### 5.2 Generic Instantiations

As mentioned before, a generic declaration defines a set of corresponding generic or non-generic entities. The process of instantiation is designed to do the following:

• Allow producing new generic or non-generic entities;

- Provide every type parameter with a type argument that can be any kind of type, including the type argument itself.

As a result of the instantiation process, a new class, interface, union, array, method, or function is created.

class A <T> {}
class B <U, V> extends A<U> { // Here A<U> is a new generic type
    field: A<V>     // Here A<V> is a new generic type
    method (p: A<Object>) {} // Here A<Object> is a new non-generic type
}

## Page 84

#### 5.2.1 Type Arguments

Type arguments are non-empty lists of types that are used for instantiation.

The syntax of type arguments is presented below:

typeArguments:
    '<' type (',' type)* '>';

The example below represents instantiations with different forms of type arguments:

Array<number> // instantiated with type number
Array<number|string> // instantiated with union type
Array<number[]> // instantiated with array type
Array|[number, string, boolean]> // instantiated with tuple type
Array<()=>void> // instantiated with function type

A compile-time error occurs if a generic instantiation leads to instantiation of the type FixedArray with the predefined value type (see Value Types).

class A <T> {
    foo (p: FixedArray<T>) {}
}
A<int> // compile-time error as such instantiation leads to method foo()
    // of class A to have type FixedArray<int> in it.

    // The actual code could be like code below - all these fragments result in a compile-
    time error
    new A<int>
    let a: A<int>|undefined
    function foo (p: A<int>) {}

#### 5.2.2 Explicit Generic Instantiations

An explicit generic instantiation is a language construct, which provides a list of type arguments (see Type Arguments) that specify real types or type parameters to substitute corresponding type parameters of a generic:

class G<T> {} // Generic class declaration
let x: G<number> // Explicit class instantiation, type argument provided

class A {
    method <T> () {} // Generic method declaration
}
let a = new A()
a.method<string> () // Explicit method instantiation, type argument provided

function foo <T> () {} // Generic function declaration
foo <string> () // Explicit function instantiation, type argument provided

type MyArray<T> = T[] // Generic type declaration

## Page 85

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

## Page 86

7 // return the data itself or if the processing function provided the
8 // result of processing
9 return cb != undefined ? cb(arg): arg
10 }
11 process (123, () => {}) // P is inferred as 'int', while R is 'void'

### 5.3 Utility Types

ArkTS supports several embedded types, called utility types. Utility types allow constructing new types by adjusting properties of initial types, for which purpose notations identical to generics are used. If the initial types are class or interface, then the resultant utility types are also handled as class or interface types. All utility type names are accessible as simple names (see Accessible) in any module across all its scopes. Using these names as user-defined entities causes a compile-time error in accordance with Declarations. An alphabetically sorted list of utility types is provided below.

#### 5.3.1 Awaited Utility Type

Implicit instantiation is only possible for generic functions and methods.

Type Awaited<T> constructs a type which includes no type Promise. It is similar to await in async functions, or to the method .then() in Promises. Any occurrence of type Promise is recursively removed until a generic, a function, an array, or a tuple type is detected. If type Promise is not a part of a type T declaration, then Awaited<T> leaves T intact.

If T in Awaited<T> is a type parameter, then subtyping for Awaited<T> is based on the subtyping for T. In other words, Awaited<T> is a subtype of Awaited<U> if T is a subtype of U. The use of type Awaited<T> is represented in the example below:

type A = Awaited<Promise<string>> // type A is string

type B = Awaited<Promise<promise<number>> // type B is number

type C = Awaited<boolean | Promise<number>> // type C is boolean | number

type D = Awaited <Object> // type D is Object

type E = Awaited<Promise<promise<number>> | Promise<string> | Promise<boolean>> // type E is number | string | boolean

type F = Awaited<Promise<(p: Promise<string>) => Promise<number>> // type F is (p: Promise<string>) => Promise<number>>

type G = Awaited<Promise<Array<promise<number>>>>> // type G is Array<promise<number>>
