#### 13.1.3 Selective Binding

Selective binding allows to bind an entity exported as identifier, or an entity exported by default (see Default Import Binding).

Binding with identifier binds an exported entity with the name identifier to the declaration scope of the current module. If no binding alias is present, then the entity is added to the declaration scope under the original name. Otherwise, the identifier specified in binding alias is used. In the latter case, the bounded entity is no longer accessible (see Accessible) under the original name.

If an identifier denotes an overload alias (see Function Overload Declarations), then all its accessible overloaded functions, either imported or not, are considered in the process of Overload Resolution for call validity.

// File1
export function f1(p: number) {}
export function f2(p: string) {}
export overload foo {f1, f2}

// File2
import {foo} from "File1" // Note: f1 and f2 are not mandatory imported
foo(5) // f1() is called
foo("a string") // f2() is called

// File3
import {foo, f1} from "File1" // Note: f1 is accessible as well
f1(5) // f1() is called
foo(6) // f1() is called
foo("a string") // f2() is called

Selective binding that uses exported entities is represented in the examples below:

export const PI = 3.14
export function sin(d: number): number {}

Note. The import path of the module is irrelevant and replaced for ‘​…’ in the examples below:

import {sin}

A single import statement can list several names as follows:
