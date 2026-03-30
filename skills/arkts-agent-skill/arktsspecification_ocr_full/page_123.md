}
const objects: RefType[] = [new RefType(), new RefType()]
const obj = objects[1]
obj.field = 777 // change the field in the array element
console.log(objects[0].field) // prints 42
console.log(objects[1].field) // prints 777

let an_array = [1, 2, 3]
let element = an_array[3.5] // compile-time error as index is not integer
function foo (index: number) {
    let element = an_array[index] // compile-time error as index is not integer
}

An array indexing expression evaluated at runtime behaves as follows:

• Object reference expression is evaluated first.

• If the evaluation completes abruptly, then so does the indexing expression, and the index expression is not evaluated.

• If the evaluation completes normally, then the index expression is evaluated. The resultant value of the object reference expression refers to an array.

• If the index expression value of an array is less than zero, greater than or equal to that array's length, then RangeError is thrown.

• Otherwise, the result of the array access is a type T variable within the array selected by the value of the index expression.

function setElement(names: string[], i: int, name: string) {
    names[i] = name // runtime error, if 'i' is out of bounds
}

#### 7.12.2 String Indexing Expression

Index expression for string indexing must be of one of integer types, namely byte, short, or int. The same rules apply as in Array Indexing Expression.

If the index expression value of a string is less than zero, greater than or equal to that string's length, then RangeError is thrown.

console.log("abc"[1]]) // prints: b
console.log("abc"[3]]) // runtime exception

The result of a string indexing expression is a value of string type.

Note. String value is immutable, and is not allowed to change a value of a string element by indexing.

let x = "abc"
x[1] = "d" // compile-time error, string value is immutable
