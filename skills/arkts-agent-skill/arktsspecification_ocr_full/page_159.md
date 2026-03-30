The usage of annotations is discussed in Using Annotations.

The examples of usage are presented below:

(x: number): number => { return Math.sin(x) } // block as lambda body
(x: number) => Math.sin(x) // expression as lambda body
e => e // shortest form of lambda

A lambda expression evaluation creates an instance of a function type (see Function Types) as described in detail in Runtime Evaluation of Lambda Expressions.

#### 7.32.1 Lambda Signature

Similarly to function declarations (see Function Declarations), a lambda signature is composed of formal parameters and optional return types. Unlike function declarations, type annotations of formal parameters can be omitted.

function foo<T> (a: (p1: T, ...p2: T[]) => T) {}
// All calls to foo pass valid lambda expressions in different forms
foo (e => e)
foo ((e1, e2) => e1)
foo ((e1, e2: Object) => e1)
foo ((e1: Object, e2) => e1)
foo ((e1: Object, e2, e3) => e1)
foo ((e1: Object, ...e2) => e1)

foo ((e1: Object, e2: Object) => e1)

function bar<T> (a: (...p: T[]) => T) {}
// Type can be omitted for the rest parameter
bar ((...e) => e)

function goo<T> (a: (p?: T) => T) {}
// Type can be omitted for the optional parameter
goo ((e?) => e)

The specification of scope is discussed in Scopes, and shadowing details of formal parameter declarations in Shadowing by Parameter.

A compile-time error occurs if:

• Lambda expression declares two formal parameters with the same name.

• Formal parameter contains no type provided, and type cannot be derived by Type Inference.
