import Usage

import {sin, PI} from "..."
    let x = sin(PI)

import {sin as Sine, PI}
    let x = Sine(PI)
    ...
    ...

Complex cases with several bindings mixed on one import path are discussed below in Several Bindings for One Import Path.

#### 13.1.4 Import Type Directive

An import directive can have a type modifier exclusively for a better syntactic compatibility with TypeScript (also see Export Type Directive). ArkTS supports no additional semantic checks for entities imported by using import type directives.

The semantic checks performed by the compiler in TypeScript but not in ArkTS are represented by the following code:

// File module.ets
console.log("Module initialization code")

export class Class1 {/*body*/}

class Class2 {}
export type {Class2}

// MainProgram.ets
import {Class1} from "./module.ets"
import type {Class2} from "./module.ets"

let c1 = new Class1() // OK
let c2 = new Class2() // Compile-time error in Typescript, OK in ArkTS

#### 13.1.5 Import Path

Import path is a string literal that determines where and how an imported module is to be searched for.

Import path can include the following:

• Initial dot ‘.’ or two dots ‘..’ followed by the slash character ‘/’.
