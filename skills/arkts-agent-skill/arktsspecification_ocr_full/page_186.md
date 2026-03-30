(continued from previous page)

function write_into_read_only (s: Style) {
    s.color = "Black"
    s.可可
    s.可可
}
write_into_read_only (new StyleClassTwo)

If a property is defined in the  $ \underline{\text{readonly}} $ form, then the implementation of the property can either keep the  $ \underline{\text{readonly}} $ form or extend it to a  $ \underline{\text{writable}} $ form as follows:

interface Style {
    get color(): string
    readonly readable: number
}

class StyleClassThree implements Style {
    get color(): string { return "Black" }
    set color(s: string) {} // OK!
    readable: number = 0 // OK!
}

function how_to_write (s: Style) {
    s.color = "Black" // compile-time error
    s.readable = 42 // compile-time error
    if (s.instanceof StyleClassThree) {
        let s1 = s as StyleClassThree
        s1.color = "Black" // OK!
        s1.readable = 42 // OK!
    }
}

how_to_write (new StyleClassThree)

#### 9.3.3 Implementing Optional Interface Properties

A class can implement Optional Interface Properties) from superinterfaces or use implicitly defined accessors from an interface.

The use of accessors implicitly defined in the interface is represented in the example below:

interface I {
    n?: number
}
class C implements I {}

let c = new C()
console.log(c.n) // Output: undefined
c.n = 1 // runtime error is thrown
