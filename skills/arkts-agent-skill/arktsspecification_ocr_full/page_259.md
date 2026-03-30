class Base {}
class Derived extends Base {}

function check(
    bb: (p: Base) => Base,
    bd: (p: Base) => Derived,
    db: (p: Derived) => Base,
    dd: (p: Derived) => Derived
) {
    bb = bd
    /* OK: identical parameter types, and covariant return type */
    bb = dd
    /* Compile-time error: parameter type are not contravariant */
    db = bd
    /* OK: contravariant parameter types, and covariant return type */

    let f: (p: Base, n: number) => Base = bb
    /* OK: subtype has less parameters */

    let g: () => Base = bb
    /* Compile-time error: less parameters than expected */
}

let foo: (x?: number, y?: string) => void = (): void => {} // OK: ``m <= n``
foo = (p?: number): void => {} // OK: ``m <= n``
foo = (p1?: number, p2?: string): void => {} // OK: Identical types
foo = (p: number): void => {}
    // Compile-time error: 1st parameter in type is optional but mandatory in lambda
    foo = (p1: number, p2?: string): void => {}
    // Compile-time error: 1st parameter in type is optional but mandatory in lambda

#### 15.2.6 Subtyping for Fixed-Size Array Types

Subtyping for fixed-size array types is based on subtyping of their element types. It is formally defined as follows:

FixedSize<B> <: FixedSize<A> if B <: A.

The situation is represented in the following example:

let x: FixedArray<number> = [1, 2, 3]
let y: FixedArray<Object> = x // ok, as number <: Object
x = y // compile-time error

Such subtyping allows array assignments that can lead to ArrayStoreError at runtime if a value of a type which is not a subtype of an element type of one array is put into that array by using the subtyping of another array element type. Type safety is ensured by runtime checks performed by the runtime system as represented in the example below:

class C {}
class D extends C {}

(continues on next page)
