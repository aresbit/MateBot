code is called before any use of namespace members (see Static Initialization for detail).

The usage of a namespace is represented in the example below:

namespace NS1 {
    export function foo() { }
    export let variable = 1234
    export const constant = 1234
    export let someVar: string

    // Will be called before any use of NS1 members
    static {
        someVar = "some string"
        console.log("Init for NS1 done")
    }
    export function bar() {}
}

namespace NS2 {
    export const constant = 1
    // Will never be called since NS2 members are never used
    static {
        console.log("Init for NS2 done")
    }
    export function bar() {}
}

export function bar() {} // That is a different bar()

if (NS1.variable == NS1.constant) {
    NS1.variable = 4321
}

NS1.bar() // namespace bar() is called
bar() // top-level bar() is called

Note. An exported namespace entity can be used in the form of a qualifiedName outside a namespace in the same module. Any namespace entity can be and typically is used inside a namespace without qualification, i.e., without a namespace name. A qualifiedName inside a namespace can be used for a namespace entity only when the entity is exported. Using a qualifiedName for non-exported entity both inside and outside a namespace causes a compile-time error:

namespace NS {
    export let a: number = 1
    let b = 2

    export function foo() {
        let v: number
        v = a // OK, no qualification
        v = NS.a // OK, `a` exported
    }

    export function bar() {
        let v: number
        v = b // OK, no qualification

(continues on next page)
