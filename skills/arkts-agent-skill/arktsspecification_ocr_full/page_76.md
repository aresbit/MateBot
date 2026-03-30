(continued from previous page)

let x: FixedArray<number> = [1, 2, 3]
sum(...x) // spread an fixed-size array 'x'
// returns 6

If constrained by an array or a tuple type, a type parameter can be used with generics as a rest parameter.

function sum<T extends Array<number>>(...numbers: T): number {
    let res = 0
    for (let n of numbers)
        res += n
    return res
}

Note. Any call to a function, method, constructor, or lambda with a rest parameter implies that a new array or tuple is created from the arguments provided.

function foo(...array_parameter: number[], ...tuple_parameter: [number, string]) {
    // array_parameter is a new array created from the arguments passed
    // tuple_parameter is a new tuple created from the arguments passed
    array_parameter[0] = 1234
    tuple_parameter[0] = 1234
    console.log(array_parameter[0], tuple_parameter[0]) // 1234 1234 is the output
}

const array_argument: number[] = [1,2,3,4]
const tuple_argument: [number, string] = [1,"234"]

console.log(array_argument[0], tuple_argument[0]) // 11 is the output

foo(...array_argument, ...tuple_argument)
    // array_argument is spread into a sequence of its elements
    // tuple_argument is spread into a sequence of its elements

console.log(array_argument[0], tuple_argument[0]) // 11 is the output

#### 4.7.6 Shadowing by Parameter

If the name of a parameter is identical to the name of a top-level variable accessible (see Accessible) within the body of a function or a method with that parameter, then the name of the parameter shadows the name of the top-level variable within the body of that function or method:

let x: number = 1
function foo (x: string) {
    // 'x' refers to the parameter and has type string
}
class SomeClass {
    method (x: boolean) {
        // 'x' refers to the method parameter and has type boolean
    }
}
