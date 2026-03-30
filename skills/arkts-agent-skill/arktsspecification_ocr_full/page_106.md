#### 7.3.2 Method Reference

A method reference refers to a static or instance method of a class or an interface. Type of a method reference is derived from the method signature:

class C {
    static foo(n: number) {}
    bar (s: string): boolean { return true }
}

// Method reference to a static method
const m1 = C.foo  // type of 'm1' is (n: number) => void

// Method reference to an instance method
const m2 = new C().bar  // type of 'm1' is (s: string) => boolean

If method reference refers to an instance method, that the named reference is bounded with the used instance of that class or interface.

class C {
    field = 123
    method(): number { return this.field }
}

let c1 = new C
let c2 = new C
let m1 = c1.method // 'c1' is bounded
let m2 = c2.method // 'c2' is bounded
c1.field = 42
console.log(m1(), m2()) // Outputs: 42 123

A method reference can refer to a generic method only if a generic instantiation is explicitly present (see Explicit Generic Instantiations). Otherwise, a compile-time error occurs:

class C {
    gen<T> (x: T) {}
}

let a = new C().gen<string> // ok
let b = new C().gen // compile-time error: no explicit type arguments

A compile-time error occurs if a method overload alias is used in a named reference:

class C {
    foo1(n: number) {}
    foo2(s: string) {}
    overload foo { foo1, foo2 }
}

let f = new C().foo // compile-time error
