#### 8.15.1 catch Clause

A catch clause consists of two parts:

• A catch identifier that provides access to an object associated with the error thrown; and

• A block of code that handles the error.

The type of catch identifier inside the block is Error (see Error Handling).

class ZeroDivisor extends Error {}

function divide(a: number, b: number): number {
    if (b == 0)
        throw new ZeroDivisor()
    return a / b
}

function process(a: number, b: number): number {
    try {
        let res = divide(a, b)
        // further processing ...
        return res
    }
    catch (e) {
        return e instanceof ZeroDivisor? -1 : 0
    }
}

A catch clause handles all errors at runtime. It returns '-1' for the ZeroDivisor, and '0' for all other errors.

#### 8.15.2 finally Clause

A finally clause defines the set of actions in the form of a block to be executed without regard to whether a try-catch completes normally or abruptly.

The syntax of finally clause is presented below:

finallyClause:
'finally' block
;

A finally block is executed without regard to how (by reaching return or try-catch end or raising new error) the program control is transferred out. The finally block is particularly useful to ensure proper resource management.

Any required actions (e.g., flush buffers and close file descriptors) can be performed while leaving the try-catch:

class SomeResource {
    // some API
    // ...
    close() {}
}

(continues on next page)
