function test(a: A) {
    a.foo(new B()) // 'fool' is called as overload from 'A' is used
}

test(new B()) // output: A.foo

let b = new B()
b.foo(b) // output: B.foo, as overload from 'B' is used

### 15.10 Type Erasure

Type erasure is the compilation technique which provides a special handling of certain language types, primarily Generics, when applied to the semantics of the following expressions:

• InstanceOf Expression;

• Cast Expression.

As a result, special types must be used for the execution of such expressions. Certain types in such expressions are handled as their corresponding effective types, while the effective type is defined as type mapping. The effective type of a specific type T is always a supertype of T. As a result, the relationship of an original type and an effective type can have the following two kinds:

• Effective type of T is identical to T, and type erasure has no effect. So, type T is retained.

• If effective type of T is not identical to T, then the type T is considered affected by type erasure, i.e., erased.

In addition, accessing a value of type T, particularly by Field Access Expression, Method Call Expression, or Function Call Expression, can cause ClassCastError thrown if type T and the target type are both affected by type erasure, and the value is produced by a Cast Expression.

class A<T> {
    field?: T

    test(value: Object) {
        return value instanceof T // CTE, T is erased
    }

    cast(value: Object) {
        return value as T // OK, but check is done during execution
    }
}

function castToA(p: Object) {
    p instanceof A<number> // CTE, A<number> is erased

    return p as A<number> // OK, but check is performed against type A, but not A<number>
}

Type mapping determines the effective types as follows:
