function foo<T1, T2> (p1: T1, p2: T2) {
    let t1: T1 = p1
    let t2: T2 = p2
}

// call contexts:
function foo(s: string) {}
foo("hello")

// composite literal contexts:
let a: number[] = [str.length, 11]

In all these cases, the expression type must be assignable to the target type (see Assignability). Assignability allows using of one of Implicit Conversions. If there is no applicable conversion, then a compile-time error occurs.

### 6.2 String Operator Contexts

String context applies only to a non-string operand of the binary operator ‘+’ if the other operand is string.

String conversion for a non-string operand is evaluated as follows:

• An operand of an integer type (see Integer Types and Operations) is converted to type string with a value that represents the operand in the decimal form.

• An operand of a floating-point type (see Floating-Point Types and Operations) is converted to type string with a value that represents the operand in the decimal form without the loss of information.

• An operand of type boolean is converted to type string with the values true or false.

• An operand of enumeration type (see Enumerations) is converted to type string with the value of the corresponding enumeration constant if values of enumeration are of type string.

• The operand of a nullish type that has a nullish value is converted as follows:

- Operand null is converted to string null.

- Operand undefined is converted to string undefined.

• An operand of a reference type or an enum type with non-string values is converted by applying the method call toString().

If there is no applicable conversion, then a compile-time error occurs.

The target type in this context is always string:

1 console.log(" " + null) // prints "null"
2 console.log("value is " + 123) // prints "value is 123"
3 console.log("BigInt is " + 123n) // prints "BigInt is 123"
4 console.log(15 + " steps") // prints "15 steps"
5 let x: string | null = null
6 console.log("string is " + x) // prints "string is null"
