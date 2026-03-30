### 3.20 Union Types

Union type is a reference type created as a combination of other types.

The syntax of union type is as follows:

unionType:
    type ('|' type)*
;

A compile-time error occurs if the type in the right-hand side of a union type declaration leads to a circular reference.

Typical usage examples of union types are represented below:

The values of a union type are valid values of all types the union is created from.

type OperationResult = "Done" | "Not done"
function do_action(): OperationResult {
    if (someCondition) {
        return "Done"
    } else {
        return "Not done"
    }
}

class Cat {
    // ...
}

class Dog {
    // ...
}

class Frog {
    // ...
}

type Animal = Cat | Dog | Frog | number
// Cat, Dog, and Frog are some types (class type or interface type)

let animal: Animal = new Cat()
animal = new Frog()
animal = 42
// One may assign the variable of the union type with any valid value

enum StringEnum {One = "One", Two = "Two"}

type Union1 = string | StringEnum // OK, will be reduced during normalization

Values of particular types can be received from a union by using different mechanisms as follows:

class Cat { sleep () {}; meow () {} }
class Dog { sleep () {}; bark () {} }
class Frog { sleep () {}; leap () {} }

type Animal = Cat | Dog | Frog

let animal: Animal = new Cat()

(continues on next page)
