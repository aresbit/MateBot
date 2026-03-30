#### 3.17.2 Readonly Array Types

Readonly array type is immutable, i.e.:

• Length of a variable of a readonly array type cannot be changed;

• Elements of a reasonably array type cannot be modified after the initial assignment directly nor through a function or method call.

Otherwise, a compile-time error occurs.

let x: readonly number [] = [1, 2, 3]
x[0] = 42 // compile-time error as array itself is readonly

Readonly array type with elements of type T can have the following two syntax forms:

• readonly T[] and

• ReadonlyArray<T>.

Both forms specify identical (indistinguishable) types (see Type Identity).

Note. In arrays of arrays, all arrays are readonly.

### 3.18 Tuple Types

Tuple type is a reference type created as a fixed set of other types.

The syntax of tuple type is presented below:

tupleType:
  '[' (type (',' type)* ',?)?' ]'
;

The value of a tuple type is a group of values of types that comprise the tuple type. The number of values in the group equals the number of types in a tuple type declaration. The order of types in a tuple type declaration specifies the type of the corresponding value in the group.

It implies that each element of a tuple has its own type. The operator ‘[]’ (square brackets) is used to access the elements of a tuple in a manner similar to accessing the elements of an array.

An index expression must be of integer type. The index of the first tuple element is 0. Only constant expressions can be used as the index providing access to tuple elements:

let tuple: [number, number, string, boolean, Object] =
[6, 7, "abc", true, 42]
tuple[0] = 42
console.log(tuple[0], tuple[4]) // `42 42` be printed

A tuple does not have length property so the legal TypeScript code like below issues compile-time error in ArkTS:
