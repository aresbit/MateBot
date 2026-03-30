### 6.4 Implicit Conversions

This section describes all implicit conversions that are allowed. Each conversion is allowed in a particular context (e.g., if an expression that initializes a local variable is subject to Assignment-like Contexts, then the rules of this context define what specific conversion is implicitly chosen for the expression).

#### 6.4.1 Widening Numeric Conversions

Widening numeric conversions convert the following:

• Values of a smaller numeric type to a larger type (see Numeric Types);

• Values of enumeration type (if enumeration constants of this type are of a numeric type) to the same or a larger numeric type.


<table border=1 style='margin: auto; word-wrap: break-word;'><tr><td style='text-align: center; word-wrap: break-word;'>From</td><td style='text-align: center; word-wrap: break-word;'>To</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>byte</td><td style='text-align: center; word-wrap: break-word;'>short, int, long, float, double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>short</td><td style='text-align: center; word-wrap: break-word;'>int, long, float, double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>int</td><td style='text-align: center; word-wrap: break-word;'>long, float, or double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>long</td><td style='text-align: center; word-wrap: break-word;'>float or double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>float</td><td style='text-align: center; word-wrap: break-word;'>double</td></tr><tr><td style='text-align: center; word-wrap: break-word;'>enumeration with numeric constants</td><td style='text-align: center; word-wrap: break-word;'>larger numeric type</td></tr></table>

The above conversions cause no loss of information about the overall magnitude of a numeric value. Some least significant bits of the value can be lost only in conversions from an integer type to a floating-point type if the IEEE 754 round-to-nearest mode is used correctly. The resultant floating-point value is properly rounded to the integer value.

Widening numeric conversions never cause runtime errors.

#### 6.4.2 Enumeration to Constants Type Conversions

The following conversions never cause a runtime error:

• Value of enumeration type without explicit base type is converted to the corresponding integer type (see Enumerations).

enum IntegerEnum { a, b, c}

let int_enum: IntegerEnum = IntegerEnum.a

let int_value: int = int_enum // int_value will get the value of 0

let number_value: number = int_enum

/* number_value will get the value of 0 as a result of conversion sequence: enumeration -> int -> number */

A value of enumeration type with string constants is converted to type string. This conversion never causes a runtime error.
