function foo(Cond1: boolean) {
    if (Cond1) let x: number = 1
    x = 2 // OK

    if (Cond1) {
        let x: number = 10; // OK, then-block scope
        let y: number = x;
    }
    else {
        let x: number = 20 // OK, no conflict, else-block scope
        y = x; // CTE, no y in scope
    }

    console.log(x) // OK, prints 2
    console.log(y) // CTE, y unknown
}

### 8.6 Loop Statements

ArkTS has four kinds of loops. A loop of each kind can be optionally labelled with an identifier. The identifier can be used only by the break Statements and continue Statements contained in the loop body.

The syntax of loop statements is presented below:

loopStatement:
    (identifier '：')?
    whileStatement
        | doStatement
        | forStatement
        | forOfStatement
    ;

A compile-time error occurs if the label identifier is not used within loopStatement, or is used in lambda expressions (see Lambda Expressions) within a loop body.

label: for (i = 1; i < 10; i++) {
    const f1 = () => {
        while (true) {
            continue label // Compile-time error
        }
    }
    const f2 = () => {
        do
            break label // Compile-time error
        while (true)
    }
}
