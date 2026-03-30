• Constructor of class is called to fully initialize the created instance.

The validity of the constructor call is similar to the validity of the method call as discussed in Step 2: Selection of Method, except the cases discussed in Constructor Body.

A compile-time error occurs if typeReference is a type parameter.

Note. If a class instance creation expression with no argument is used as object reference in a method call expression, then empty parentheses ‘()’ are to be used.

class A { method() {} }

new A.method() // compile-time error
new A().meth
(new

### 7.15 Instance0f Expression

The syntax of instanceof expression is presented below:

instanceOfExpression:
    expression 'instanceof' type
;

Any instance of expression in the form expr instanceof T is of type boolean.

The result of an instance of expression is true if the actual type of evaluated expr is a subtype of T (see Subtyping). Otherwise, the result is false.

A compile-time error occurs if type T is not retained by Type Erasure.

Generic type (see Generics) in the form of type name (see Type References) can be used as T operand of an instance of expression. In this case, the check is performed against the type name, and type parameters are ignored. Instantiated generic types (see Explicit Generic Instantiations) cannot be used because the T operand of an instance of must be retained by Type Erasure.

class C<T> {
    foo() {
        console.log(this.instanceof C) // true
        console.log(this.instanceof C<T>) // compile-time error
    }
}

let c = new C<number>
c.foo()

The type of an instance of expression is used for smart cast (see Smart Types) if applicable.
