#### 15.1.4 Specifics of Numeric Operator Contexts

The postfix and prefix increment and decrement operators evaluate byte and short operands without widening. It is also true for an assignment operator (considering assignment as a binary operator).

For other numeric operators, the operands of unary and binary numeric expressions are widened to a larger numeric type. The minimum type is int. None of those operators evaluates values of types byte and short without widening. Details of specific operators are discussed in corresponding sections of the Specification.

#### 15.1.5 Specifics of String Operator Contexts

If one operand of the binary operator '+' is of type string, then the string conversion applies to another non-string operand to convert it to string (see String Concatenation and String Operator Contexts).

#### 15.1.6 Other Contexts

The only semantic rule for all other contexts, and specifically for Overriding, is to use Subtyping.

#### 15.1.7 Specifics of Type Parameters

If the type of a left-hand-side expression in assignment-like context is a type parameter, then it provides no additional information for type inference even where a type parameter constraint is set.

If the target type of an expression is a type parameter, then the type of the expression is inferred as the type of a standalone expression.

The semantics is represented in the example below:

class C<T extends number> {
    constructor (x: T) {}
}

new C(1) // compile-time error

The type of ‘1’ in the example above is inferred as int (default type of an integer literal). The expression is considered new C<int>(1) and causes a compile-time error because int is not a subtype of number (type parameter constraint).

Explicit type argument new C<number>(1) must be used to fix the code.
