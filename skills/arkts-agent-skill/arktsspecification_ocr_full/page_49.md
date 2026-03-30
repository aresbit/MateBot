#### 3.16.1 String Literal Types

Operations on variables of string literal types are identical to the operations of their supertype string (see Type string). The resulting operation type is the type specified for the operation in the supertype:

let s0: "string literal" = "string literal"
let s1: string = s0 + s0 // + for string returns string

### 3.17 Array Types

Array type is a data structure intended to comprise any number of same-type elements, including zero elements. ArkTS supports the following two predefined array types:

• Resizable Array Types; and

• Fixed-Size Array Types as an experimental feature.

Resizable array types are recommended for most cases. Fixed-size array types can be used where performance is the major requirement.

Fixed-size arrays differ from resizable arrays as follows:

• Fixed-size arrays have their length set only once to achieve a better performance.

• Fixed-Size arrays have no methods defined.

Note. The term array type as used in this Specification applies to both resizable array type and fixed-size array type. The same holds true for array value and array instance. Resizable arrays and fixed-size arrays are not assignable to each other.

#### 3.17.1 Resizable Array Types

Resizable array type is a built-in type characterized by the following:

• Any object of resizable array type contains elements. The number of elements is known as array length, and can be accessed by using the length property.

• Array length is a non-negative integer number.

• Array length can be set and changed at runtime.

- Array element is accessed by its index. The index is an integer number in the range from 0 to array length minus 1.

• Accessing an element by its index is a constant-time operation.

• If passed to non-ArkTS environment, an array is represented as a contiguous memory location.

• Type of each array element is assignable to the element type specified in the array declaration (see Assignability).
