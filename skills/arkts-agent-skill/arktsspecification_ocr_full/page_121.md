• Result of functionCallExpression is not produced as a consequence.

The function call is safe because it handles nullish values properly.

If the form of expression in the call is qualifiedName, and qualifiedName refers an overload declaration (Overload Declarations), then Overload Resolution is used to select the function to call.

A compile-time error occurs if no function is available to call.

A compile-time error occurs if a function has at least one parameter or return type of the type FixedArray parameterized with a type parameter and function call expression leads to instantiation of the type FixedArray with the predefined value type (see Value Types).

Semantic check for call is performed in accordance with Compatibility of Call Arguments.

Various forms of function calls are represented in the example below:

function foo() { console.log("Function foo() is called") }
foo() // function call uses function name to call it

call (foo) // top-level function passed
call ((): void => { console.log("Lambda is called") }) // lambda is passed
call (A.method) // static method
call ((new A).method) // instance method is passed

class A {
    static method() { console.log("Static method() is called") }
    method() { console.log("Instance method() is called") }
}

function call (callee: () => void) {
    callee() // function call uses parameter name to call any functional object passed_
    →as an argument
}

(((): void => { console.log("Lambda is called") })) // function call uses lambda_
→expression to call it

let x = foo() // compile-time error as void cannot be used as type annotation

Type of a function call expression is the return type of the function.

### 7.12 Indexing Expressions

Indexing expressions are used to access elements of arrays (see Array Types), strings (see Type string), and Record instances (see Record Utility Type). Indexing expressions can also be applied to instances of indexable types (see Indexable Types).

The syntax of indexing expression is presented below:

indexingExpression:
    expression ('?.')? [' expression '']
;
