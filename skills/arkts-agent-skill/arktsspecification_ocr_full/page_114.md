(continued from previous page)

salary: number
}
let map: Record<string, PersonInfo> = {
    "John": { age: 25, salary: 10},
    "Mary": { age: 21, salary: 20}
}

If a key is a union of literal types, then all variants must be listed in the object literal. Otherwise, a compile-time error occurs:

let map: Record<"aa" | "bb", number> = {
    "aa": 1,
} // compile-time error: "bb" key is missing

#### 7.5.4 Object Literal Evaluation

The evaluation of an object literal of type C (where C is either a named class type or an anonymous class type created for the interface) is to be performed by the following steps:

• A parameterless constructor is executed to produce an instance x of class C. The execution of the object literal completes abruptly if so does the execution of the constructor.

- Name-value pairs of the object literal are then executed from left to right in the textual order they occur in the source code. The execution of a name-value pair includes the following:

- Evaluation of the expression; and

– Assignment of the value of expression to the corresponding field of x as its initial value. This rule also applies to reading fields.

The execution of an object literal completes abruptly if so does the execution of a name-value pair.

An object literal completes normally with the value of a newly initialized class instance if so do all name-value pairs.

### 7.6 Spread Expression

Spread expression can be used only within an array literal (see Array Literal) or argument passing. The expression must be of array type (see Array Types) or tuple type (see tuple Types). Otherwise, a compile-time error occurs.

The syntax of spread expression is presented below:

spreadExpression:
    ...' expression
;

A spread expression for arrays or tuples can be evaluated as follows:

• By the compiler at compile time if expression is constant (see Constant Expressions);
