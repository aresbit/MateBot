(continued from previous page)

interface SomeInterface {}
let type_of_interface: Type = Type.from<SomeInterface>()

If type T used as type argument is affected by Type Erasure, then the function returns value of type Type for effective type of T but not for T itself:

let type_of_array1: Type = Type.from<int[]>( ) // value of Type for Array<>
let type_of_array2: Type = Type.from<Array<number>>() // the same Type value

### 20.4 Ensuring Module Initialization

The ArkTS standard library (see Standard Library) provides a top-level function initModule() with one parameter of string type. A call to this function ensures that the module referred by the argument is available, and that its initialization (see Static Initialization) is performed. An argument must be a string literal. Otherwise, a compile-time error occurs.

The current module has no access to the exported declarations of the module referred by the argument. If such module is not available or any other runtime issue occurs then a proper exception is thrown.

initModule (@ohos/library/src/main/ets/pages/Index")

### 20.5 Generic and Function Types Peculiarities

The current compiler and runtime implementations use type erasure. Type erasure affects the behavior of generics and function types. It is expected to change in the future. A particular example is provided in the last bullet point in the list of compile-time errors in InstanceOf Expression.

### 20.6 Keyword struct and ArkUI

The current compiler reserves the keyword struct because it is used in legacy ArkUI code. This keyword can be used as a replacement for the keyword class in Class Declarations. Class declarations marked with the keyword struct are processed by the ArkUI plugin and replaced with class declarations that use specific ArkUI types.
