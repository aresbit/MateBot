function foo2 (n1: number, n2: string) // non-rest parameters
{ ... }
let a_tuple: [number, string] = [1, "2"]
foo2 (...a_tuple) // compile-time error

### 7.7 Parenthesized Expression

The syntax of parenthesized expression is presented below:

parenthesizedExpression:
    '(' expression ')'
;

Type and value of a parenthesized expression are the same as those of the contained expression.

### 7.8 this Expression

The syntax of this expression is presented below:

thisExpression:
'this'
;

The keyword this can be used as an expression in the body of an instance method of a class (see Method Body) or an interface (see Default Interface Method Declarations). A corresponding class or interface type is the type of this expression. If a method is declared in an object literal (see Object Literal), then the type of the object literal is the type of this.

The keyword  $ \underline{\text{this}} $ can be used in a lambda expression only if it is allowed in the context in which the lambda expression occurs. The type of this is the type of a class or an interface in which it is declared, but not the type of the surrounding object literal type, if any.

The keyword this in a direct call expression this( arguments ) can only be used in an explicit constructor call statement (see Explicit Constructor Call).

The keyword this can also be used in the body of a function with receiver (see Functions with Receiver). The type of this expression is the declared type of the parameter this in a function.

A compile-time error occurs if the keyword this appears elsewhere.

The keyword this used as a primary expression denotes a value that is a reference to the following:

• Object for which the instance method is called; or

• Object being constructed.

The parameter this in a lambda body and in the surrounding context denote the same value.
