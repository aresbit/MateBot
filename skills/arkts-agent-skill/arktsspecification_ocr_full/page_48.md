$ \left| \text{console.log("a}\backslash\emptyset b\text{".length)} \right| // output: 3 $

Using string in all cases is recommended, although the name String also refers to type string.

### 3.15 Type bigint

ArkTS has the built-in bigint type that allows handling theoretically arbitrary large integers. Values of type bigint can hold numbers that are larger than the maximum value of type long. Type bigint uses the arbitrary-precision arithmetic. Values of type bigint can be created from the following:

• Bigint literals (see Bigint Literals); or

• Numeric type values, by using a call to the standard library class BigInt methods or constructors (see Standard Library).

Similarly to string, bigint type has dual semantics:

• If created, assigned, or passed as an argument, type bigint behaves like a reference type (see Reference Types).

• All applicable operations handle type bigint as a value type (see Value Types). The operations are described in Integer Types and Operations.

Using bigint is recommended in all cases, although the name BigInt also refers to type bigint. Using BigInt creates new objects and calls to static methods in order to improve TypeScript compatibility.

let b1: bigint = new BigInt(5) // for Typescript compatibility
let b2: bigint = 123n

### 3.16 Literal Types

Literal types are aligned with some ArkTS literals (see Literals). Their names are the same as the names of their values, i.e., literals proper. ArkTS supports only the following literal types:

• String Literal Types,

• null, and

• undefined.

let a: "string literal" = "string literal"
let b: null = null
let c: undefined = undefined

printThem (a, b, c)
function printThem (p1: "string literal", p2: null, p3: undefined) {
    console.log (p1, p2, p3)
}

There are no operations for literal types null and undefined.
