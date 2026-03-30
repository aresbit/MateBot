Any indexing expression has two subexpressions as follows:

• Object reference expression before the left bracket; and

• Index expression inside the brackets.

If the operator '?.' (see Chaining Operator) is present in an indexing expression, then:

• It an object reference expression is not of a nullish type, then the chaining operator has no effect.

• Otherwise, object reference expression must be checked to nullish value. If the value is undefined or null, then the evaluation of the entire surrounding primary expression stops. The result of the entire primary expression is then undefined.

If no ‘?.’ is present in an indexing expression, then object reference expression must be of array type or Record type. Otherwise, a compile-time error occurs.

#### 7.12.1 Array Indexing Expression

Index expression for array indexing must be one of integer types, namely byte, short, or int. Otherwise, a compile-time error occurs.

The conversion of byte and short types (see Widening Numeric Conversions) is performed on an index expression to ensure that the resultant type is int. Otherwise, a compile-time error occurs.

Other numeric types (long, float, and double/number) must be converted explicitly by applying the methods defined in the classes of the Standard Library.

const a = ["Alice", "Bob", "Carol"]
function demo (l: long, f: float, d: double, n: number) {
    console.log(
        a[l.toInt()], a[f.toInt()],
        a[d.toInt()], a[n.toInt()]
    ) // OK to access array using index expression conversion methods
}

If the chaining operator ‘? .’ (see Chaining Operator) is present, and after its application the type of object reference expression is an array type, then it makes a valid array reference expression, and the type of the array indexing expression is T.

The result of an array indexing expression is a variable of type T (i.e., an element of the array selected by the value of that index expression).

It is essential that, if type T is a reference type, then the fields of array elements can be modified by changing the resultant variable fields:

let names: string[] = ["Alice", "Bob", "Carol"]
console.log(names[1]) // prints Bob
names[1] = "Martin"
console.log(names[1]) // prints Martin

console.log(names["1"]) // compile-time error as index of non-numeric type

class RefType {
    field: number = 42
