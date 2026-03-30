let n: number // using identifier as a predefined value type name
let o: Object // using identifier as a predefined class type name
let a: number[] // using array type
let t: [number, number] // using tuple type
let f: ()=>number // using function type
let u: number|string // using union type
let l: "xyz" // using string literal type

class C { n = 1; s = "aa"}
let k: keyof C // using keyof to build union type

Parentheses are used to specify the required type structure if the type is a combination of array, function, or union types. Without parentheses, the symbol ‘|’ that constructs a union type has the lowest precedence as represented by the example below:

// a nullable array with elements of type string:
let a: string[] | null
let s: string[] = []
a = s    // ok
a = null // ok, a is nullable

// an array with elements whose types are string or null:
let b1: (string | null)[]
b1 = null // error, b1 is an array and is not nullable
b1 = ["aa", null] // ok

// string or array of null elements:
let b2: string | null[]
b2 = null // error, b2 - string or array of nulls - not nullable
b2 = [null, null] // ok

// a function type that returns string or null
let c: () => string | null
c = null // error, c is not nullable
c = (): string | null => { return null } // ok

// (a function type that returns string) or null
let d: (() => string) | null
d = null // ok, d is nullable
d = (): string => { return "hi" } // ok

If an annotation is used in front of type in parentheses, then the parentheses become a mandatory part of the annotation to prevent ambiguity.

let var_name1: @my_annotation() (A|B) // OK
let var_name2: @my_annotation (A|B) // Compile-time error
