function min(x: number[]): number {
    let m = x[0]
    for (let v of x)
        if (v < m)
            m = v
    return m
}

min([1., 3.14, 0.99]); // ok, parameter type is used

// Array of array initialization
type Matrix = number[][]
let m: Matrix = [[1, 2], [3, 4], [5, 6]]

class aClass {
    let b1: Array <aClass> = [new aClass, new aClass]
    let b2: Array <number> = [1, 2, 3]
    let b3: FixedArray<number> = [1, 2]

    /* Type of literal is inferred from the context
     taken from b1, b2 and b3 declarations */
}

Possible kinds of context are represented in the following example:

let array: number[] = [1, 2, 3] // assignment context
function foo (array: number[]) {}
foo ([1, 2, 3]) // call context
let b = [1, 2, 3] as number[] // casting conversion

All valid conversions are applied to the initializer expression, i.e., each initializer expression type must be assignable (see Assignability) to the array element type. Otherwise, a compile-time error occurs.

let value: number = 2
let list: Object[] = [1, value, "hello", new Error()] // ok

If the type used in the context is a tuple type (see Tuple Types), and types of all literal expressions are compatible with tuple type elements at respective positions, then an array literal is of tuple type.

let tuple: [number, string] = [1, "hello"] // ok
let incorrect: [number, string] = ["hello", 1] // compile-time error

If the type used in the context is a union type (see Union Types), then it is necessary to try inferring the type of the array literal from its elements (see Array Type Inference from Types of Elements). If successful, then the type so inferred must be compatible with one of the types that form the union type. Otherwise, a compile-time error occurs:

let union_of_arrays_int: int[] | string[] = [1, 2] // OK, literal is int[]
    // Compatible with union
let union_of_arrays: number[] | string[] = [1, 2] // Error, literal is int[]
    // incompatible with union
let incorrect_union_of_arrays: number[] | string[] = [1, 2, "string"]
/* Error: (number|string)[] (type of the literal) is not compatible with number[] | string[] (type of the variable)
*/
