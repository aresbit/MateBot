(continued from previous page)

return res
}

let x: number[] = [1, 2, 3]
sum(...x) // spread an array 'x'
// returns 6

A call of entity with a rest parameter of tuple type  $ [T_1, \ldots, T_n] $ can accept only n arguments of types that are assignable (see Assignability) to the corresponding  $ T_i $:

function sum(...numbers: [number, number, number]): number {
    return numbers[0] + numbers[1] + numbers[2]
}

sum() // compile-time error: wrong number of arguments, 0 instead of 3
sum(1) // compile-time error: wrong number of arguments, 1 instead of 3
sum(1, 2, "a") // compile-time error: wrong type of the 3rd argument
sum(1, 2, 3) // returns 6

It is legal though meaningless to declare a function with an optional parameter followed by a rest parameter of a tuple type. However, use of such function without explicitly set optional and rest parameters will cause compile-time error:

// optional tuple + rest tuple
function g(opt?: [number, string], ...tail: [number, string]) { // OK
    // ...
}

g() // CTE - no rest tuple
g([1, "str"]) // CTE - no rest tuple
g([1, "str"], 1, "str") // OK

If an argument of tuple type  $ [T_1, \ldots, T_n] $ is to be passed to a call of entity with the rest parameter, then a spread expression (see Spread Expression) must have the spread operator ‘...’ as a prefix before the tuple argument:

function sum(...numbers: [number, number, number]): number {
    return numbers[0] + numbers[1] + numbers[2]
}

let x: [number, number, number] = [1, 2, 3]
sum(...x) // spread tuple 'x'
// returns 6

If an argument of fixed-size array type FixedArray<T> is to be passed to a function or a method with the rest parameter, then the spread expression (see Spread Expression) must be used with the spread operator ‘…’ as a prefix before the fixed-size array argument:

function sum(...numbers: Array<number>): number {
    let res = 0
    for (let n of numbers)
        res += n
    return res
}

(continues on next page)
