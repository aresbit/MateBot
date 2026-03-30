end
end

Checks are represented in the examples below:

call [...1, "str", true], ...[ ...123] // Initial call form

call (1, "str", true, 123) // To be unfolded into the form with no spread expressions

function foo1 (p: Object) {}
    foo1 (1) // Type of '1' must be assignable to 'Object'
    // p becomes 1

function foo2 (...p: Object[]) {}
    foo2 (1, "111") // Types of '1' and "111" must be assignable to 'Object'
    // p becomes array [1, "111"]

function foo31 (...p: (number|string)[]) {}
    foo31 (...[1, "111"]) // Type of array literal [1, "111"] must be assignable to_
    (number|string)[]
    // p becomes array [1, "111"]

function foo32 (...p: [number, string]) {}
    foo32 (...[1, "111"]) // Types of '1' and "111" must be assignable to 'number' and 'string'
    'accordingly
    // p becomes tuple [1, "111"]

function foo4 (...p: number[]) {}
    foo4 (1, ...[2, 3]) //
    // p becomes array [1, 2, 3]

function foo5 (p1: number, ...p2: number[]) {}
    foo5 (...[1, 2, 3]) //
    // p1 becomes 1, p2 becomes array [2, 3]

### 15.7 Type Inference

ArkTS supports strong typing but allows not to burden a programmer with the task of specifying type annotations everywhere. A smart compiler can infer types of some entities and expressions from the surrounding context. This technique called type inference allows keeping type safety and program code readability, doing less typing, and focusing on business logic. Type inference is applied by the compiler in the following contexts:

• Type Inference for Numeric Literals;

• Variable and constant declarations (see Type Inference from Initializer);

• Implicit generic instantiations (see Implicit Generic Instantiations);

• Function, method or lambda return type (see Return Type Inference);
