• At runtime otherwise.

An array or tuple object referred by the expression is broken by the evaluation into a sequence of values. This sequence is used where a spread expression is used. It can be an assignment, a call of a function, method, or constructor. A sequence of types of these values is the type of the spread expression.

A spread expression for arrays is represented in the example below:

let array1 = [1, 2, 3]
let array2 = [4, 5]
let array3 = [...array1, ...array2] // spread array1 and array2 elements
    // while building new array literal at compile time
console.log(array3) // prints [1, 2, 3, 4, 5]

function foo (...array: number[]) {
    console.log(array)
}

foo (...array2) // spread array2 elements into arguments of the foo() call

function run_time_spread_application1 (a1: number[], a2: number[]) {
    console.log([...a1, 42, ...a2])
    // array literal will be built at runtime
}

run_time_spread_application1 (array1, array2) // prints [1, 2, 3, 42, 4, 5]

A spread expression for tuples is represented in the example below:

let tuple1: [number, string, boolean] = [1, "2", true]
let tuple2: [number, string] = [4, "5"]
// spread tuple1 and tuple2 elements
let tuple3: [number, string, boolean, number, string] = [...tuple1, ...tuple2]
// while building new tuple object at compile time
console.log(tuple3) // prints [1, 2, true, 4, 5]

function bar (...tuple: [number, string]) {
    console.log(tuple)
}
bar (...tuple2) // spread tuple2 elements into arguments of the foo() call

function run_time_spread_application2 (a1: [number, string, boolean], a2: [number, _, string]) {
    console.log([...a1, 42, ...a2])
    // such array literal will be built at runtime
}
run_time_spread_application2 (tuple1, tuple2) // prints [1, 2, true, 42, 4, "5"]

Note. If an argument is spread at the call site, then an appropriate parameter must be of the rest kind (see Rest Parameter). A compile-time error occurs if an argument is spread into a sequence of ordinary non-optional parameters as follows:

function foo1 (n1: number, n2: number) // non-rest parameters
{ ... }
let an_array = [1, 2]
foo1 (...an_array) // compile-time error

(continues on next page)
