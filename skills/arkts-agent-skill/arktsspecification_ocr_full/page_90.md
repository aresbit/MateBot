A compile-time error occurs if any other type, or literal of any other type is used in place of this type.

Its usage is represented in the example below:

type R1 = Record<number, Object> // ok
type R2 = Record<boolean, Object> // compile-time error
type R3 = Record<"salary" | "bonus", Object> // ok
type R4 = Record<"salary" | boolean, Object> // compile-time error
type R5 = Record<"salary" | number, Object> // ok
type R6 = Record<string | number, Object> // ok

Type V has no restrictions.

A special form of object literals is supported for instances of type Record (see Object Literal of Record Type).

Access to Record<K, V> values is performed by an indexing expression like r[index], where r is an instance of type Record, and index is the expression of type K (see Record Indexing Expression for detail).

Variables of type Record<K, V> can be initialized by a valid object literal of Record type (see Object Literal of Record Type) where the literal is valid if the type of key expression is compatible with key type K, and the type of value expression is compatible with the value type V.

type Keys = 'key1' | 'key2' | 'key3'

let x: Record<Keys, number> = {
    'key1': 1,
    'key2': 2,
    'key3': 4,
}

console.log(x['key2']) // prints 2
x['key2'] = 8

console.log(x['key2']) // prints 8

In the example above, K is a union of literal types and thus the result of an indexing expression is of type V. In this case it is number.

#### 5.3.7 Utility Type Private Fields

Utility types are built on top of other types. Private fields of the initial type stay in the utility type but they are not accessible (see Accessible) and cannot be accessed in any way. It is represented in the example below:

function foo(): string { // Potentially some side effect
    return "private field value"
}

class A {
    public_field = 444
    private private_field = foo()
}

function bar (part_a: Readonly<A>) {
    console.log(part_a)
}

(continues on next page)
