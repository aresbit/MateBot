### 13.7 Program Entry Point

Modules can act as programs (applications). Program execution starts from the execution of a program entry point which can be of the following two kinds:

• Top-level statements for modules (see Top-Level Statements); or

• Sole top-level statement (the first statement in the top-level statements acts as the entry point);

• Entry point function (see below).

- Both top-level statement and entry point function (same as above, plus the function called after the top-level statement execution is completed).

Entry point functions have the following features:

A module can have the following forms of entry point:

• Any exported top-level function can be used as an entry point. An entry point is selected by the compiler, the execution environment, or both;

• Sole entry point function (main or other as described below);

• Entry point function must either have no parameters, or have one parameter of type string[] that provides access to the arguments of a program command line;

• Entry point function return type is either void (see Type void) or int;

• Entry point function cannot have overloading;

• Entry point function is called main by default.

The example below represents different forms of valid and invalid entry points:

function main() {
    // Option 1: a return type is inferred from the body of main().
    // It will be 'int' if the body has 'return' with the integer expression
    // and 'void' if no return at all in the body
}

function main(): void {
    // Option 2: explicit :void - no return in the function body required
}

function main(): int {
    // Option 3: explicit :int - return is required
    return 0
}

function main(): string { // compile-time error: incorrect main signature
    return ""
}

function main(p: number) { // compile-time error: incorrect main signature
}

// Option 4: top-level statement is the entry point
console.log("Hello, world!")

// Option 5: top-level exported function

(continues on next page)
