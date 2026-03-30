enum Color { Red, Green, Blue = 5 }
let colors = Color.values()
    //colors[0] is the same as Color.Red

let red = Color.getValueOf("Red")

Color.fromValue(5) // ok, returns Color.Blue
Color.fromValue(6) // throws runtime error

Additional methods for instances of an enumeration type are as follows:

• Method valueOf() returns a numeric or string value of an enumeration constant depending on the type of the enumeration constant.

• Method getName() returns the name of an enumeration constant.

enum Color { Red, Green = 10, Blue }

let c: Color = Color.Green

console.log(c.valueOf()) // prints 10

console.log(c.getName()) // prints Green

Note. Methods c.toString() and c.valueOf().toString() return the same value.

### 17.5 Indexable Types

If a class or an interface declares one or two functions with names $_get and $_set, and signatures (index: Type1): Type2 and (index: Type1, value: Type2) respectively, then an indexing expression (see Indexing Expressions) can be applied to variables of such types:

class SomeClass {
    $_get (index: number): SomeClass { return this }
    $_set (index: number, value: SomeClass) { }
}
let x = new SomeClass
x = x[1] // This notation implies a call: x = x.$_get (1)
x[1] = x // This notation implies a call: x.$_set (1, x)

If only one function is present, then only the appropriate form of indexing expression (see Indexing Expressions) is available:

class ClassWithGet {
    $_get (index: number): ClassWithGet { return this }
}
let getClass = new ClassWithGet
getClass = getClass[0]
getClass[0] = getClass // Error - no $_set function available

class ClassWithSet {
    $_set (index: number, value: ClassWithSet) {}
}

(continues on next page)
