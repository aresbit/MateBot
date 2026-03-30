// Single iteration
while (true) {
    console.log("iteration") // get printed exactly once
    break;
}

let a: number = 0
outer:
do {
    for (a = 0; a < 10; a++) {
        if (a == 1) break outer
            console.log("inner") // get printed only once
        }
        console.log(a) // Never reached
    } while (true) // condition never used

### 8.11 continue Statements

A continue statement stops the execution of the current loop iteration, and transfers control to the next iteration. Appropriate checks of loop exit conditions depend on the kind of the loop.

The syntax of continue statement is presented below:

continueStatement:
    'continue' identifier?
;

A continue statement with no label transfers control to the next iteration of the enclosing loop statement. If there is no enclosing loop statement within the body of the surrounding function or method, then a compile-time error occurs.

A continue statement with the label identifier transfers control to the next iteration of the enclosing loop statement with the same label identifier. If there is no enclosing loop statement with the same label identifier (within the body of the surrounding function or method), then a compile-time error occurs.

Examples of continue statements with and without a label are presented below:

// continue    // would cause CTE if uncommented

// continue without label
// will print 0, 1, 2, 4 (3 skipped)
for (let a: number = 0; a < 5; a++) {
    if (a == 3) continue
        console.log("a = " + a)
}

let a: number
outer:
    do {
        for (a = 0; a < 10; a++) {
            if (a > 1) continue outer

(continues on next page)
