Resizable array type with elements of type T can have the following two forms of syntax:

• T[], and

• Array<T>.

The first form uses the following syntax:

arrayType:
type ['']
;

Note. T[] and Array<T> specify identical, i.e., indistinguishable types (see Type Identity).

Two basic operations with array elements take elements out of, and put elements into an array by using the operator ‘[]’.

The same syntax can be used to work with Indexable Types, some of such types are parts of Standard Library.

The number of elements in an array can be obtained by accessing the property length. The length of an array can be set and changed in runtime using the methods defined in Standard Library.

An array can be created by using Array Literal, Resizable Array Creation Expressions, or the constructors defined in Standard Library.

ArkTS allows setting a new value to length to shrink an array and provide better TypeScript compatibility. An error is caused by the following situations:

• The value is of type number or other floating-point type, and the fractional part differs from 0;

• The value is less than zero; or

• The value is greater than previous length.

The above situations cause errors as follows:

• A runtime error, if the situation is identified at runtime, i.e., during program execution; and

• A compile-time error, if the situation is detected during compilation.

Array operations are illustrated below:

let a : number[] = [0, 0, 0, 0, 0]
/* allocate array with 5 elements of type number */
a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
let y = a[4] /* get the last element of array 'a' */
let count = a.length // get the number of array elements
a.length = 3 // shrink array
y = a[2] // OK, 2 is the index of the last element now
y = a[3] // Will lead to runtime error - attempt to access non-existing array element

let b: Array<number> = a // 'b' points to the same array as 'a'

type Matrix = number[][] /* array or array of numbers */

An array as an object is assignable to a variable of type Object:

let a: number[] = [1, 2, 3]
let o: Object = a
