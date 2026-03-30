// type "number" has a default value:
let a = new FixedArray<number>(3) // creates array [0.0, 0.0, 0.0]

class C {
    constructor (n?: number) {}
}
let b = new FixedArray<C>(2) // creates array [new C(), new C()]

• constructor(len: int, elem: T) for any T. The constructor creates an array instance filled with a single value elem:

let a = new FixedArray<string>(3, "a") // creates array ["a", "a", "a"]

• constructor(len: int, elems: (inx: int) => T) for any T. The constructor creates an array instance where each i element is evaluated as a result of the elems call with argument i:

let a = new FixedArray<int>(3, (inx: int) => 3 - inx)
// creates array [3, 2, 1]

New Expressions cannot use generic parameters to create a Fixed-size array. Attempting to do so causes a compile-time error as in the following example:

function f<T>(): T {
    let ret = new FixedArray<T>(3) // compile-time error, generic parameter T
    return ret
}

### 17.3 Resizable Array Creation Expressions

Array creation expression creates new objects that are instances of resizable arrays (see Resizable Array Types). An array instance can be created alternatively by using Array Literal.

The syntax of array creation expression is presented below:

newArrayInstance:
    'new' arrayElementType dimensionExpression+ (arrayElement)?
;

arrayElementType:
    typeReference
| '(' type ')'
;

dimensionExpression:

(continues on next page)
