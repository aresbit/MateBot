interface I {}
const i: I = { foo(): void {} } // compile-time error

If an interface has accessors (see Interface Properties) for some property, and the property is used in an object literal, then a compile-time error occurs:

interface I1 {
    set attr (attr: number)
}
const a: I1 = {attr: 42} /* compile-time error - 'attr' cannot be used in object literal */
interface I2 {
    get attr(): number
}
const b: I2 = {attr: 42} /* compile-time error - 'attr' cannot be used in object literal */

#### 7.5.3 Object Literal of Record Type

Generic type Record<Key, Value>(see Record Utility Type) is used to map properties of a type (type Key) to another type (type Value). A special form of object literal is used to initialize the value of such type:

The syntax of record literal is presented below:

recordLiteral:
    {'keyValueSequence?'}
;
keyValueSequence:
    keyValue(','keyValue)*','?
;
keyValue:
    expression:'expression';

The first expression in keyValue denotes a key and must be of type Key. The second expression denotes a value and must be of type Value:

let map: Record<string, number> = {
    "John": 25,
    "Mary": 21,
}

console.log(map["John"]) // prints 25

interface PersonInfo {
    age: number

(continues on next page)
