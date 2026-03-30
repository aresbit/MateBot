function f1 (p: number) {}
function f2 (p: string) {}
function f3 (p: number|string) {}
overload foo {f1, f2, f3} // f3 will never be called as foo()

foo (5) // f1() is called
foo ("5") // f2() is called

#### 15.9.1 Overload Resolution

Overload declaration defines an ordered set of entities, and the first entity from this set that is accessible and has an appropriate signature is used to call at the call site. This approach is called managed overloading because the first-match algorithm provides full control for a developer to select a specific entity to call. This developer control over calls is represented in the following example:

function max2i(a: int, b: int): int
    return a > b ? a : b
}
function max2d(a: double, b: double): double {
    return a > b ? a : b
}
function maxN(...a: double[]): double {
    // returns max element in array 'a'
}
overload max {max2i, max2d, maxN}
let i = 1
let j = 2
let pi = 3.14

max(i, j) // max2i is used
max(i, pi) // max2d is used
max(i, pi, 4) // maxN is used
max(1) // maxN is used
max(false, true) // compile-time error, no appropriate signature

Overload resolution for an instance method overload (see Class Method Overload Declarations) always uses the type of the object reference known at compile time. It can be either the type used in a declaration, or a smart type (see Smart Types) as represented in the example below:

class A {
    foo1(x: A) { console.log("A.foo") }
    overload foo { foo1 }
}

class B extends A {
    foo2(x: B) { console.log("B.foo") }
    overload foo { foo2, foo1 }
}

(continues on next page)
