### 3.12 Type undefined

The only value of type undefined is the literal undefined (see Undefined Literal).

Type undefined is a subtype of type void (see Type void).

Using type undefined as type annotation is not recommended, except in nullish types (see Nullish Types).

Type undefined can be used also as type argument to instantiate a generic type as follows:

class A<T> {}
let a = new A<undefined>() // ok, type parameter is irrelevant
function foo<T>(x: T) {}

foo<undefined>(undefined) // ok

### 3.13 Type null

The only value of type null is the literal null (see Null Literal).

Using type null as type annotation is not recommended, except in nullish types (see Nullish Types).

### 3.14 Type string

Type string values are all string literals, e.g., 'abc'. Type string stores sequences of characters as Unicode UTF-16 code units.

A string object is immutable, the value of a string object cannot be changed after the object is created. The value of a string object can be shared.

Type string has dual semantics, i.e.:

• Type string behaves like a reference type (see Reference Types) if created, assigned, or passed as an argument;

• Type string is handled as a value (see Value Types) by all string operations (see String Concatenation, Equality Expressions, and String Relational Operators).

A number of operators can act on string values as follows:

• Accessing the length property returns string length as int type value. String length is a non-negative integer number. String length is set once at runtime and cannot be changed after that.

• Concatenation operator ‘+’ (see String Concatenation) produces a value of type string. If the result is not a constant expression (see Constant Expressions), then the string concatenation operator can implicitly create a new string object;

• Indexing a string value (see String Indexing Expression) returns a value of type string. A new string object can be created implicitly.

A string value can contain any character, i.e., no character can be used to indicate the end of a string. A character with the value '0' is an ordinary character inside a string as represented by the following example:
