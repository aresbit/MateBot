objectLiteral:
    {'objectLiteralMembers?'}'
;
objectLiteralMembers:
    objectLiteralMember(',' objectLiteralMember)*','?
;
objectLiteralMember:
    objectLiteralField
;
objectLiteralField:
    identifier ':' expression
;

An object literal field consists of an identifier and an expression as follows:

class Person {
    name: string = ""
    age: number = 0
}

let b: Person = {name: "Bob", age: 25}

let : Person = {name: "Alice", age: 18, } //ok, trailing comma is ignored

let c: Person | number = {name: "Mary", age: 17} // literal will be of type Person

An object literal method is a complete declaration of a public method. Examples of object literals with methods are provided in Object Literal of Interface Type.

Type of an object literal expression is always some class C that is inferred from the context. A type inferred from the context can be either a class (see Object Literal of Class Type), or an anonymous class created for the inferred interface type (see Object Literal of Interface Type).

A compile-time error occurs if:

• Type of an object literal cannot be inferred from the context (see Type of Expression for an example);

• Inferred type is not a class or interface type, or is an abstract class type (see Abstract Classes);

• Inferred type is not an interface type, and an object literal contains methods;

• Context is a union type, and an object literal can be treated as the value of several union component types.

let p = {name: "Bob", age: 25}
    // compile-time error, type cannot be inferred

class A { field = 1 }
class B { field = 2 }

let q: A | B = {field: 6}
    // compile-time error, type cannot be inferred as the literal
    // fits both A and B
