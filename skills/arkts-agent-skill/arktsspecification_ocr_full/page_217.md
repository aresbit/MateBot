enum Commands { Open = "fopen", Close = "fclose" }

### 11.3 Enumeration Operations

The value of an enumeration constant can be converted to type string by using the method toString:

enum Color { Red, Green = 10, Blue }
let c: Color = Color.Green
console.log(c.toString()) // prints: 10

The name of enumeration type can be indexed by the value of this enumeration type to get the name of the constant:

enum Color { Red, Green = 10, Blue }
let c: Color = Color.Green
console.log(Color[c]) // prints: Green

If several enumeration constants have the same value, then the textually last constant has the priority:

enum E { One = 1, one = 1, oNe = 1 }
console.log(E.fromValue(1)) // prints: oNe

Additional methods available for enumeration types and constants are discussed in Enumeration Methods in the chapter Experimental Features.
