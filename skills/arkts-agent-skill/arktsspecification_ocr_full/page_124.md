#### 7.12.3 Record Indexing Expression

Indexing expression for a type Record<Key, Value> (see Record Utility Type) allows getting or setting a value of type Value at an index specified by the expression of type Key.

The following two cases are to be considered separately:

2. Other cases.

1. Type Key is a union that contains literal types only;

Case 1. If type Key is a union that contains literal types only, then an index expression can only be one of the literals listed in the type. The result of the indexing expression is of type Value.

type Keys = 'key1' | 'key2' | 'key3'

let x: Record<Keys, number> = {
    'key1': 1,
    'key2': 2,
    'key3': 4,
}

let y = x['key2'] // y value is 2

A compile-time error occurs if an index expression is not a valid literal:

console.log(x['key4']) // compile-time error
x['another key'] = 5 // compile-time error

The compiler guarantees that an object of Record<Key, Value> for this type Key contains values for all Key keys.

Case 2. An index expression has no restriction. The result of an indexing expression is of type Value | undefined.

let x: Record<number, string> = {
    1: "hello",
    2: "buy",
}

function foo(n: number): string | undefined {
    return x[n]
}

function bar(n: number): string {
    let s = x[n]
    if (s == undefined) { return "no" }
    return s!
}

foo(3) // prints "undefined"
bar(3) // prints "no"

let y = x[3]

Type of y in the code above is string | undefined. The value of y is undefined.

An indexing expression evaluated at runtime behaves as follows:
