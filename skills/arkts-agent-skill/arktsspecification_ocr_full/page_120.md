• If the method call has the form expression.identifier, then the method must not be declared static. Otherwise, a compile-time error occurs.

• If the method call has the form super.identifier, then the method must not be declared abstract or static. Otherwise, a compile-time error occurs.

A compile-time error occurs if a method has at least one parameter or return type of the type FixedArray parameterized with a type parameter and method call expression leads to instantiation of the type FixedArray with the predefined value type (see Value Types).

#### 7.10.4 Type of Method Call Expression

Type of a method call expression is the return type of the method.

class A {
    static method() { console.log("Static method() is called") }
    method() { console.log("Instance method() is called") }
}

let x = A.method() // compile-time error as void cannot be used as type annotation
A.method() // OK
let y = new A().method() // compile-time error as void cannot be used as type annotation
new A().method() // OK

### 7.11 Function Call Expression

Function call expression is used to call a function (see Function Declarations), a variable of a function type (Function Types), or a lambda expression (see Lambda Expressions).

The syntax of function call expression is presented below:

functionCallExpression:
    expression ('?.' | typeArguments)? arguments block?
;

A special syntactic form that contains a block associated with the function call is called trailing lambda call (see Trailing Lambdas for details).

A compile-time error occurs if the expression type is one of the following:

• Different than the function type;

• Nullish type without ‘?.’ (see Chaining Operator).

If the operator ‘? .’ (see Chaining Operator) is present, and the expression evaluates to a nullish value, then:

• Arguments are not evaluated;

• Call is not performed; and
