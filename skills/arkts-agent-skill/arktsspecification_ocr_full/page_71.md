If the type of the initializer expression cannot be inferred, then a compile-time error occurs (see Object Literal):

let a = null // type of 'a' is null
let aa = undefined // type of 'aa' is undefined
let arr = [null, undefined] // type of 'arr' is (null | undefined)[]

let cond: boolean = /*some initialization*/

let b = cond ? 1 : 2 // type of 'b' is int
let c = cond ? 3 : 3.14 // type of 'c' is double
let d = cond ? "one" : "two" // type of 'd' is string
let e = cond ? 1 : "one" // type of 'e' is int | string

const bb = cond ? 1 : 2 // type of 'bb' is int
const cc = cond ? 3 : 3.14 // type of 'cc' is double
const dd = cond ? "one" : "two" // type of 'dd' is "one" | "two"
const ee = cond ? 1 : "one" // type of 'ee' is int | "one"

let f = {name: "aa"} // compile-time error: type unknown

declare let x1 = 1 // compile-time error: ambient variable cannot have initializer
declare const x2 = 1 // type of 'x2' is int
let x3 = 1 // type of 'x3' is int
const x4 = 1 // type of 'x4' is int

declare let s1 = "1" // compile-time error: ambient variable cannot have initializer
declare const s2 = "1" // type of 's2' is "1"
let s3 = "1" // type of 's3' is string
const s4 = "1" // type of 's4' is "1"

### 4.7 Function Declarations

Function declarations specify names, signatures, and bodies when introducing named functions. An optional function body is a block (see Block).

The syntax of function declarations is presented below:

functionDeclaration:
    modifiers? 'function' identifier
    typeParameters? signature block?
;

modifiers:
    'native' | 'async'
;

Functions must be declared on the top level (see Top-Level Statements).

If a function is declared generic (see Generics), then its type parameters must be specified.
