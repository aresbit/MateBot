let x: void = undefined // compile-time error - void used as type annotation

function foo(): void {}
console.log(foo()) // compile-time error - void used as a value

function bar1(): void {
    return void // compile-time error - void used as a value
}

function bar2(): void {
    return undefined // OK as undefined is a subtype of void
}

type aType = void | number // compile-time error - void used as type annotation

Type void can be used as a type argument that instantiates a generic type, function, or method as follows:

class A<T> {
    f: T
    m(): T { return this.f }
    constructor (f: T) { this.f = f }
}
let a1 = new A<void>(undefined) // ok, as undefined is a subtype of void
let a2 = new A<undefined>(undefined) // ok
let a3 = new A<void>(void) // compile-time error: void is used as value

console.log (a1.f, a2.m()) // Output is "undefined" "undefined"

function foo<T>(p: T): T { return p }
foo<void>(undefined) // ok, it returns 'undefined' value
foo<void>(void) // compile-time error: void is used as value

type F1<T> = () => T
const f1: F1<void> = (): void => {}
const f2: F1<void> = () => {}
const f3: F1<void> = (): undefined => { return undefined }

// Array literals can be assigned to the array of void type in any form
type A1<T> = T[]
type A2<T> = Array<T>
const a1: A1<void> = [undefined]
const a2: A2<void> = [undefined, undefined]

let x: void[] // compile-time error - void used as type annotation
