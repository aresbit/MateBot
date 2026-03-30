hello1("John") // 'name' has a string value
hello2() // 'name' has 'undefined' value
hello2("John") // 'name' has a string value

function foo1 (p?: number) {}
function foo2 (p: number | undefined = undefined) {}

foo1() // 'p' has 'undefined' value
foo1(5) // 'p' has a numeric value
foo2() // 'p' has 'undefined' value
foo2(5) // 'p' has a numeric value

#### 4.7.5 Rest Parameter

Rest parameters allow functions, methods, constructors, or lambdas to take arbitrary numbers of arguments. Rest parameters have the spread operator ‘...’ as a prefix before the parameter name.

The syntax of rest parameter is presented below:

restParameter:
    annotationUsage? '...' identifier ':' type
;

A compile-time error occurs if a rest parameter:

• Is not the last parameter in a parameter list;

• Has a type that is not an array type, a tuple type, nor a type parameter constrained by an array or a tuple type.

A call of entity with a rest parameter of array type T[] (or FixedArray<T>) can accept any number of arguments of types that are assignable (see Assignability) to T:

function sum(...numbers: number[]): number {
    let res = 0
    for (let n of numbers)
        res += n
    return res
}

sum() // returns 0
sum(1) // returns 1
sum(1, 2, 3) // returns 6

If an argument of array type T[] is to be passed to a call of entity with the rest parameter, then the spread expression (see Spread Expression) must be used with the spread operator ‘...’ as a prefix before the array argument:

function sum(...numbers: number[]): number {
    let res = 0
    for (let n of numbers)
        res += n

(continues on next page)
