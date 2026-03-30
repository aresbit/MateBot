If the type used in the context is a fixed-size array type (see Fixed-Size Array Types), and each initializer expression type is compatible with the array element type, then an array literal is of fixed-size array type.

let array: FixedArray<number> = [1, 2]

If the type used in the context is a readonly array, then an array literal is of readonly array type.

#### 7.4.2 Array Type Inference from Types of Elements

Where no context is set, and thus the type of an array literal cannot be inferred from the context (see Type of Expression), the type of array literal [  $  \text{expr}_1, \ldots, \text{expr}_N  $] is inferred from the initialization expression instead by using the following algorithm:

1. If array literal  $ (N == O) $ includes no element, then the type of the array literal cannot be inferred, and a compile-time error occurs.

2. If at least one element of an expression type cannot be determined, then the type of the array literal cannot be inferred, and a compile-time error occurs.

3. If each initialization expression is of a numeric type (see Numeric Types), then the array literal type is number[].

4. If all initialization expressions are of the same type T, then the array literal type is T[]

5. Otherwise, the array literal type is constructed as the union type T:sub:1 | ... |  $ T_N $, where  $ T_i $ is the type of  $ expr_i $, and then:

• If  $ T_{i} $ is a literal type, then it is replaced for its supertype;

• If  $ T_{i} $ is a union type comprised of literal types, then each constituent literal type is replaced for its supertype.

• Union Types Normalization is applied to the resultant union type after the above replacements.

type A = number
let u : "A" | "B" = "A"

let a = []
let b = ["a"]
let c = [1, 2, 3]
let d = ["a" + "b", 1, 3.14]
let e = [u]
let f = [() : void => {} , new A()] // compile-time error, type cannot be inferred
// type is string[]
// type is number[]
// type is (string | number)[]
// type is string[]
// type is (() => void | A)[]

### 7.5 Object Literal

Object literal is an expression that can be used to create a class instance with methods and fields with initial values. In some cases it is more convenient to use an object literal in place of a class instance creation expression (see New Expressions).

The syntax of object literal is presented below:
