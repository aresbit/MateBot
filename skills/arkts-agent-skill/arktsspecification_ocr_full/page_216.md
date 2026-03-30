A type to which all enumeration constant values belong is called enumeration base type. This type is int, long or string.

Any enumeration constant is of type enumeration. Implicit conversion (see Enumeration to Constants Type Conversions) of an enumeration constant to numeric types or type string depends on the type of constants.

In addition, all enumeration constant names must be unique. Otherwise, a compile-time error occurs.

enum E1 { A, B = "hello" } // compile-time error
enum E2 { A = 5, B = "hello" } // compile-time error
enum E3 { A = 5, A = 77 } // compile-time error
enum E4 { A = 5, B = 5 } // OK! values can be the same

Empty enum is supported as a corner case for compatibility with TypeScript.

enum Empty {} // OK

### 11.1 Enumeration Integer Values

The integer value of an enum constant is set implicitly if an enumeration constant specifies no value.

A constant expression of type int or long can be used to set the value explicitly:

enum Background { White = 0xFF, Grey = 0x7F, Black = 0x00 }
enum LongEnum { A = 0x7FFF_FFFF_1, B, C }

Choosing which type to use—int or long—is based on the same principle as for integer literals (see Integer Literals).

If all constants have no value, then the first constant is assigned the value zero. The other constant is assigned the value of the immediately preceding constant plus one.

If some but not all constants have their values set explicitly, then the values of the constants are set by the following rules:

• The constant which is the first and has no explicit value gets zero value.

• Constant with an explicit value has that explicit value.

• Constant that is not the first and has no explicit value takes the value of the immediately preceding constant plus one.

In the example below, the value of Red is 0, of Blue, 5, and of Green, 6:

enum Color { Red, Blue = 5, Green }

### 11.2 Enumeration String Values

A string value for enumeration constants must be set explicitly:
