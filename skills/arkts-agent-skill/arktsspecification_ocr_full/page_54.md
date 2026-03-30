#### 3.19.1 Type Function

Type Function is a predefined type that is a direct superinterface of any function type.

A value of type Function cannot be called directly. A developer must use the unsafeCall method instead. This method checks the arguments of type Function, and calls the underlying function value if the number and types of the arguments are valid.

function foo(n: number) {}

let f: Function = foo

f(1) // compile-time error: cannot be called

f.unsafeCall(3.14) // correct call and execution
f.unsafeCall() // runtime error: wrong number of arguments

Another important property of type Function is name. It is a string that contains the name associated with the function object in the following way:

• If a function or a method is assigned to a function object, then the associated name is that of the function or of the method;

• If a lambda is assigned to a variable of Function type, then the associated name is that of the variable;

• Otherwise, the string is empty.

function print_name (f: Function) {
    console.log(f.name)
}

function foo() {}
print_name(foo) // output: "foo"

class A {
    static sm() {}
    m() {}
}

print_name(A.sm) // output: "sm"
print_name(new A().m) // output: "m"

let x: Function = (): void => {}
print_name(x) // output: "x"

let y = x
print_name(y) // output: "x"

print_name ((): void=>{}) // output: ""

The declarations of the unsafeCall method, name property, and all other methods and properties of type Function are included in the ArkTS Standard Library.
