interface I1 {}
interface I2 {}

function equ1 (i1: I1, i2: I2) {
    return i1 == i2 // to be resolved during program execution
}

class A implements I1, I2 {}

const a = new A

equ1 (a, a) // true, the same values

An equality with values of two union types is represented in the example below:

function f1(x: number | string, y: boolean | null): boolean {
    return x == y // compile-time error, always evaluates to false
}

function f2(x: number | string, y: boolean | "abc"): boolean {
    // ok, can be evaluated as true
    return x == y
}

#### 7.25.1 Numeric Equality Operators

Type of each operand in a numeric equality operator must be convertible to a numeric type (see Numeric Types) as described in Numeric Conversions for Relational and Equality Operands. Otherwise, a compile-time error occurs.

A widening conversion can occur (see Widening Numeric Conversions) if type of one operand is smaller than type of the other operand (see Numeric Types).

If the converted type of the operands is int or long, then an integer equality test is performed.

If the converted type is float or double, then a floating-point equality test is performed.

The floating-point equality test must be performed in accordance with the following IEEE 754 standard rules:

• The result of ‘==’ or ‘===’ is false but the result of ‘!=’ is true if either operand is NaN.

The test x != x or x !== x is true only if x is NaN.

• Positive zero equals negative zero.

• Equality operators consider two distinct floating-point values unequal in any other situation.

For example, if one value represents positive infinity, and the other represents negative infinity, then each compares equal to itself and unequal to all other values.

Based on the above presumptions, the following rules apply to integer operands or floating-point operands other than NaN:

• If the value of the left-hand-side operand is equal to that of the right-hand-side operand, then the operator ‘==’ or ‘===’ produces the value true. Otherwise, the result is false.

• If the value of the left-hand-side operand is not equal to that of the right-hand-side operand, then the operator '!=' or '!==' produces the value true. Otherwise, the result is false.
