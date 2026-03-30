• Local variable or parameter of the surrounding function or method.

If not a simple name, qualifiedName refers to the following:

• Entity imported from a module.

• Entity exported from a namespace, or

• Member of some class or interface, or

• Special syntax form of Record Indexing Expression.

If typeArguments are provided, then qualifiedName is a valid instantiation of the generic method or function. Otherwise, a compile-time error occurs.

A compile-time error also occurs if a name referred by qualifiedName is one of the following:

• Undefined or inaccessible;

• Named constructor (see Constructor Names).

Type of a named reference is the type of an expression.

If a named reference refers to a function name, it is called Function Reference. If a named reference refers to a method name, it is called Method Reference.

#### 7.3.1 Function Reference

A function reference refers to a declared or imported function. Type of a function reference is derived from the function signature:

function foo(n: number): string { return n.toString() }
let func = foo // type of func is '(n: number) => string'
let x = func(1) // foo() called via reference

A function reference can refer to a generic function but only if Explicit Generic Instantiations is present, otherwise a compile-time error occurs:

function gen<T> (x: T) {}

let a = gen<string> // ok
let b = gen // compile-tin

function gen<T>
 $ \text{ants} $

A compile-time error occurs if an overload alias is used in a named reference:

function foo1(n: number) {}
function foo2(s: string) {}
overload foo { foo1, foo2 }

foo(1) // OK, overload call
let x = foo // Error: ref to overload
let y = foo2 // ok, ref to foo2
