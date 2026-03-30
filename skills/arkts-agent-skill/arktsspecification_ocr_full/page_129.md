let a = [1, 2] as double[] // ok, [1.0, 2.0]
let b = [1, 2] as double // compile-time error, wrong target type
let c = [1, "cc"] as double[] // compile-time error, wrong element type
let d = [1, "cc"] as [double, string] // ok, cast to the tuple type
let e = [1.0, "cc"] as [int, string] // compile-time error, wrong element type

Note. Assignability check is applied to the elements of an array literal.

Examples with object literals are provided in Object Literal.

#### 7.16.2 Runtime Checking in Cast Expression

If none of the previous kinds of cast expression can be applied, then expr as target checks if the type of expr is a subtype of target (see Subtyping).

If the actual type of expr is a subtype of target (see Subtyping), then the result of an as expression is the result of the evaluated expr. Otherwise, ClassCastError is thrown.

If target type is not preserved by Type Erasure, then the check is performed against an effective type of the target type. As the effective type is less specific than target in the case described, the usage of the resulting value can cause type violation, and ClassCastError is thrown as a consequence (see Type Erasure for detail).

Semantically, a cast expression of this kind is coupled tightly with InstanceOf Expression as follows:

• If the result of x instanceof T is true, then x as T never causes a runtime error;

• If x instanceof T causes a compile-time error as a result of Type Erasure, then x as T also causes a compile-time error.

• If otherwise the result of x instanceof T is false, then x as T causes ClassCastError thrown at runtime.

This situation is represented in the following example:

function foo (x: Object) {
    x as string
}

foo("aa") // OK
foo(1) // runtime error is thrown in foo by 'as' operator application

InstanceOf Expression can be used to prevent runtime errors. Moreover, the InstanceOf Expression makes cast conversion unnecessary in many cases as smart cast is applied (see Smart Types):

class Person {
    name: string
    constructor (name: string) { this.name = name }
}

function printName(x: Object) {
    if (x.instanceof Person) {
        // no need to cast, type of 'x' is 'Person' here
        console.log(x.name)
    } else {

(continues on next page)
