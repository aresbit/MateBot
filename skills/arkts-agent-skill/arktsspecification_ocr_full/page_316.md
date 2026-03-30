If there are optional parameters in front of an optional function type parameter, then calling such a function or method can skip optional arguments and keep the trailing lambda only. This implies that the value of all skipped arguments is undefined.

function foo (p1?: number, p2?: string, f?: ()=>string) {
    console.log (p1, p2, f?.)
}

foo()    // undefined undefined undefined
foo() { return "lambda" }    // undefined undefined lambda
foo(1) { return "lambda" }    // 1 undefined lambda
foo(1, "a") { return "lambda" } // 1 a lambda
