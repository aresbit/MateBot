• Operands of Type string or string literal type (see String Literal Types) have the same contents;

• Operands after a numeric conversion are of Type bigint (see Numeric Conversions for Relational and Equality Operands) and have the same value;

• Operands after a numeric conversion (see Widening Numeric Conversions, Numeric Conversions for Relational and Equality Operands) are of Numeric Types of the same value except NaN (see Numeric Equality Operators for detail);

• Operands of Type char have the same value (both operands represent the same Unicode code point);

• Operands of the same enumeration type (see Enumerations) have the same numeric values or the same string contents, depending on the type of enumeration constant values;

• Function references that refer to the same functional object (see Function Type Equality Operators for detail).

In all other cases, if types A and B do not overlap (and therefore an expression always evaluated to false at compile time), then:

• if each of A and B is either a predefined type or a union of predefined types, a compile-time-error is issued..

• in all other cases, a compile-time warning is issued.

Note. There are two main reasons why compiler do not use always a compile-time error:

• Compatibility with TypeScript code base

• The inferred smart type (see Smart Types) could lead in some cases to triggering the error even in the case when it is impossible at runtime (see an example below):

class B {
    f(): B|undefined { return undefined }
}
class D extends B {
    f(): D { return this }
}
function f(c: B) {
    if (c.instanceof D) {
        // smart type causes compile-time warning
        c.f() == undefined
    }
}

An evaluation of equality expressions always uses the actual types of operands as in the example below:

function equ(a: Object, b: Object): boolean {
    return a == b
}

equ(1, 1) // true, values are compared
equ(1, 2) // false, value are compared

equ("aa", "aa") // true, string contexts are compared
equ(1, "aa") // false, not compatible types

(continues on next page)
