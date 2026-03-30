(continued from previous page)

[' expression '']
;
arrayElement:
(' expression '')
;

let x = new number[2][2] // create 2x2 matrix

Array creation expression creates an object that is a new array with the elements of the type specified by arrayElementType.

The type of each dimension expression must be assignable (see Assignability) to an int type. Otherwise, a compile-time error occurs.

A compile-time error occurs if any dimension expression is a constant expression that is evaluated to a negative integer value at compile time.

If the type of any dimension expression is number or other floating-point type, and its fractional part is other than '0', then errors occur as follows:

• Compile-time error, if the situation is identified during compilation; and

• Runtime error, if the situation is identified during program execution.

If arrayElement is provided, then the type of the expression can be as follows:

• Type of array element denoted by arrayElementType, or

• Lambda function with the return type equal to the type of array element denoted by arrayElementType and the parameters of type int, and the number of parameters equal to the number of array dimensions.

Otherwise, a compile-time error occurs.

let x = new number[-3] // compile-time error

let y = new number[3.141592653589] // compile-time error

foo (3.141592653589)
function foo (size: number) {
    let y = new number[size] // runtime error
}

A compile-time error occurs if arrayElementType refers to a class that does not contain an accessible (see Accessible) parameterless constructor, or constructor with all parameters of the second form of optional parameters (see Optional Parameters), or if type has no default value:

class C{
    constructor (n: number) {}
}
let x = new C[3] // compile-time error: no parameterless constructor

class A {
    constructor (p1?: number, p2?: string) {}
}
let y = new A[2] // OK, as all 3 elements of array will be filled with
// new A() objects
