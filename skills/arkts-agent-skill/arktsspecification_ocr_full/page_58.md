• For any  $ T_{i} $, m is one of the following:
– Method or accessor with an equal signature; or
– Same-type field.

Otherwise, a compile-time error occurs as follows:

class A {
    n = 1
    s = "aa"
    foo() {}
    goo(n: number) {}
    static foo () {}
}

class B {
    n = 2
    s = 3.14
    foo() {}
    goo() {}
    static foo () {}
}

let u: A | B = new A

let x = u.n // ok, common field
u.foo() // ok, common method

console.log(u.s) // compile-time error as field types differ
u.goo() // compile-time error as signatures differ

type AB = A | B
AB.foo() // compile-time error as foo() is a static method

A compile-time error occurs if in some  $ T_{i} $ the name m is overloaded (see Overloading):

class C {
    overload foo { foo1, foo2 }
    foo1(a: number): void {}
    foo2(a: string): void {}
}

class D {
    foo(a: number): void {}
    foo2(a: string): void {}
}

function test(x: C | D) {
    x.foo() // compile-time error, as 'foo' in C is the overload alias
    x.foo2("aa") // ok, as 'foo2' in both C and D is a method
}
