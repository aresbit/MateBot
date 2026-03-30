## CONTEXTS AND CONVERSIONS

This Chapter defines expression contexts and conversions that can be applied to expressions in different contexts. Contexts can be of the following kinds:

• Assignment-like Contexts:

• String Operator Contexts with string concatenation (operator ‘+’);

• Numeric Operator Contexts with all numeric operators ('+', '-', etc.).

### 6.1 Assignment-like Contexts

Assignment-like contexts include the following:

• Declaration contexts that allow setting an initial value to a variable (see Variable Declarations), a constant (see Constant Declarations), or a field (see Field Declarations) with an explicit type annotation;

• Assignment contexts that allow assigning (see Assignment) an expression value to a variable;

• Call contexts that allow assigning an argument value to a corresponding formal parameter of a function, method, constructor or lambda call (see Function Call Expression, Method Call Expression, Explicit Constructor Call, and New Expressions);

• Return contexts (see return Statements) the allow specifying a resultant value of a function, method or lambda call;

• Composite literal contexts that allow setting an expression value to an array element (see Array Literal Type Inference from Context), a class, or an interface field (see Object Literal);

The examples are presented below:

// declaration contexts:
let x: number = 1
const str: string = "done"
class C {
    f: string = "aa"
}

// assignment contexts:
x = str.length
new C().f = "bb"
