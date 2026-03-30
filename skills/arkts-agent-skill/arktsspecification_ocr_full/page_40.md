let x: MyType<number> = [new A<number>, new A<number>]
// MyType<number> is a type reference - alias reference
// A<number> is a type reference - class type reference

If type reference refers to a type by a type alias (see Type Alias Declaration), then the type alias is replaced for a non-aliased type in all cases when dealing with types. The replacement is potentially recursive.

type T1 = Object
type T2 = number
function foo(t1: T1, t2: T2) {
    t1 = t2 // Type compatibility test will use Object and number
    t2 = t2 + t2 // Operator validity test will use type number not T2
}

### 3.6 Value Types

Value types are predefined integer types (see Integer Types and Operations), floating-point types (see Floating-Point Types and Operations), the boolean type (see Type boolean), character types (see Type char), and user-defined enumeration types (see Enumerations). The values of such types do not share state with other values.

#### 3.6.1 Numeric Types

Numeric types are integer and floating-point types (see Integer Types and Operations and Floating-Point Types and Operations).

Larger type values include all values of smaller types:

• double > float > long > int > short > byte

A value of a smaller type can be assigned to a variable of a larger type as a consequence (see Widening Numeric Conversions).

In terms of operations available for the numeric types (see Multiplication, Division, Remainder, Additive Expressions) we state that number or double is the largest type and long is larger than int and so on respectively.

Type bigint does not belong to this hierarchy. No implicit conversion from numeric types (see Numeric Types) to bigint occurs in any assignment context (see Assignment-like Contexts). The methods of class BigInt (which is a part of Standard Library) must be used to create bigint values from numeric type values.
