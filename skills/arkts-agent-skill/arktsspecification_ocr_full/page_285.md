### 17.2 Fixed-Size Array Types

Fixed-size array type, written as FixedArray<T>, is the built-in type characterized by the following:

• Any instance of array type contains elements. The number of elements is known as array length, and can be accessed by using the length property.

• Array length is a non-negative integer number.

• Array length is set once at runtime and cannot be changed after that.

• Array element is accessed by its index. Index is an integer number starting from 0 to array length minus 1.

• Accessing an element by its index is a constant-time operation.

• If passed to a non-ArkTS environment, an array is represented as a contiguous memory location.

• Type of each array element is assignable to the element’s type specified in the array declaration (see Assignability).

Fixed-size arrays differ from resizable arrays as follows:

• Fixed-size array length is set once to achieve better performance;

• Fixed-size arrays have no methods defined;

• Fixed-size arrays have several constructors (see Fixed-Size Array Creation);

• Fixed-size arrays are not compatible with resizable arrays.

Incompatibility between a resizable array and a fixed-size array is represented by the example below:

function foo(a: FixedArray<number>, b: Array<number>) {
    a = b // compile-time error
    b = a // compile-time error
}

#### 17.2.1 Fixed-Size Array Creation

Fixed-size array can be created by using Array Literal or constructors defined for type FixedArray<T>, where T must be a concrete type. A compile time error occurs if T is a type parameter.

Using an array literal to create an array is represented in the example below:

let a : FixedArray<number> = [1, 2, 3]
/* create array with 3 elements of type number */
a[1] = 7 /* put 7 as the 2nd element of the array, index of this element is 1 */
let y = a[2] /* get the last element of array 'a' */
let count = a.length // get the number of array elements
y = a[3] // Will lead to runtime error - attempt to access non-existing array element

Several constructors can be called to create a FixedArray<T> instance as follows:

• constructor(len: int), if type T has either a default value (see Default Values for Types) or a constructor that can be called with no argument provided:
