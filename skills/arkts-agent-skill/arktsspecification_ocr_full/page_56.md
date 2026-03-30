if (animal.instanceof Frog) {
    // animal is of type Frog here, conversion can be used:
    let frog: Frog = animal as Frog
    frog.leap()
}
animal.sleep() // Any animal can sleep

(continued from previous page)

Predefined types are represented by the following example:

type Predefined = number | boolean
let p: Predefined = 7
if (p instanceof number) {
    // type of 'p' is number here
}

Literal types are represented by the following example:

type BMW_ModelCode = "325" | "530" | "735"
let car_code: BMW_ModelCode = "325"
if (car_code == "325") {
    car_code = "530"
} else if (car_code == "530") {
    car_code = "735"
} else {
    // pension :-)
}

Note. A compile-time error occurs if an expression of a union type is compared to a literal value or a constant that does not belong to the values of the union type:

type BMW_ModelCode = "325" | "530" | "735"
let car_code: BMW_ModelCode = "325"
if (car_code == "234") { ... }
/*
compile-time error as "234" does not belong to values of literal type BMW_ModelCode
*/
function model_code_test (code: string) {
    if (car_code == code) { ... }
    // This test is to be resolved during program execution
}
