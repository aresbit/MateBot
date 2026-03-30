console.log(i)

// new variable is declared as a loop index variable with its type
// explicitly specified
for (let i: number = 1; i < 10; i++) {
    console.log(i)
}

// new variable is declared as loop index variable with its type
// inferred from its initialization part of the declaration
for (let i = 1; i < 10; i++) {
    console.log(i)
}

A variable declared in the forInit-part has the loop scope. It can be used in a forContinue expression, a forUpdate expression, a single-body statement, or in a body block if enclosed in parentheses:

// forInit declaration and no body block
let k: number = 0
for (let i: number = 1; i < 10; i++)
    k += i
console.log(k)
// i = k // CTE when uncommented
let i: number = k // OK

### 8.9 for-of Statements

A for-of loop iterates elements of array or string, or an instance of iterable class or interface (see Iterable Types).

The syntax of for-of statements is presented below:

forOfStatement:
    'for' ('forVariable 'of' expression ')' statement
;

forVariable:
    identifier | ('let' | 'const') identifier (':' type)?
;

A compile-time error occurs if the type of an expression is not array, string, or an iterable type.

The execution of a for-of loop starts from the evaluation of expression. If the evaluation is successful, then the resultant expression is used for loop iterations (execution of the statement). On each iteration, forVariable is set to successive elements of the array, string, or the result of class iterator advancement.

If forVariable has the modifiers let or const, then a new variable is declared in the loop scope. The new variable is accessible only inside the loop body. Otherwise, the variable is as declared above. The modifier const prohibits assignments into forVariable, while let allows modifications.
