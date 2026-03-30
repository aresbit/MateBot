(continued from previous page)

'from' importPath
;

An importPath cannot refer to the file the current module is stored in. Otherwise, a compile-time error occurs.

If re-exported declarations are not distinguishable (see Declarations) within the scope of the current module, then a compile-time error occurs.

The re-exporting practices are represented in the following examples:

export * from "path_to_the_module" // re-export all exported declarations
export * as qualifier from "path_to_the_module"
// re-export all exported declarations with qualification
export { d1, d2 as d3 } from "path_to_the_module"
// re-export particular declarations some under new name
export {default} from "path_to_the_module"
// re-export default declaration from the other module
export {default as name} from "path_to_the_module"
// re-export default declaration from the other module under 'name'

### 13.6 Top-Level Statements

A module can contain sequences of statements that logically comprise one sequence of statements.

The syntax of top-level statements is presented below:

topLevelStatements: statement*
;

A module can contain any number of top-level statements that logically merge into a single sequence in the textual order:

statements_1
/* top-declarations except constant and variable declarations */
statements_2

The sequence above is equal to the following:

/* top-declarations except constant and variable declarations */
statements_1; statements_2

This situation is represented by the example below:

// The actual text combination of the statements and declarations
console.log("Start of top-level statements")
type A = number | string
let a: A = 56
function foo() {
    console.log(a)

(continues on next page)
