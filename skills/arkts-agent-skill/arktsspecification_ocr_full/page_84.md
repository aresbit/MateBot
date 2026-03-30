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
