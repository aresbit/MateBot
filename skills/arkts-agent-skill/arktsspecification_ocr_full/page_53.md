(continued from previous page)

'...' ftParameter
;
ftReturnType:
'=>' type
;

let binaryOp: (x: number, y: number) => number
function evaluate(f: (x: number, y: number) => number) { }

The rest parameter is described in Rest Parameter.

A type alias can set a name for a function type (see Type Alias Declaration):

type BinaryOp = (x: number, y: number) => number
let op: BinaryOp

If a function type has the ‘?’ mark for a parameter name, then this parameter and all parameters that follow (if any) are optional. Otherwise, a compile-time error occurs. The actual type of the parameter is then a union of the parameter type and type undefined. This parameter has no default value.

type FuncTypeWithOptionalParameters = (x?: number, y?: string) => void
let foo: FuncTypeWithOptionalParameters
    = ():void => {} // OK: as arguments are just ignored
foo = (p: number):void => {} // CTE as call with zero arguments is invalid
foo = (p?: number):void => {} // OK: as call with zero or one argument is valid
foo = (p1: number, p2?: string):void => {} // Compile-time error: as call with zero__
arguments is invalid
foo = (p1?: number, p2?: string):void => {} // OK

foo()
foo(undefined)
foo(undefined, undefined)
foo(42)
foo(42, undefined)
foo(42, "a string")

type IncorrectFuncTypeWithOptionalParameters = (x?: number, y: string) => void
// compile-time error: no mandatory parameter can follow an optional parameter

function bar (
    p1?: number,
    p2: number | undefined
) {
    p1 = p2 // OK
    p2 = p1 // OK
    // Types of p1 and p2 are identical
}

More details on function types assignability are provided in Subtyping for Function Types.
