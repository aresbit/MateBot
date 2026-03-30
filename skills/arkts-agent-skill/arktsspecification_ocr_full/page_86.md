7 // return the data itself or if the processing function provided the
8 // result of processing
9 return cb != undefined ? cb(arg): arg
10 }
11 process (123, () => {}) // P is inferred as 'int', while R is 'void'

### 5.3 Utility Types

ArkTS supports several embedded types, called utility types. Utility types allow constructing new types by adjusting properties of initial types, for which purpose notations identical to generics are used. If the initial types are class or interface, then the resultant utility types are also handled as class or interface types. All utility type names are accessible as simple names (see Accessible) in any module across all its scopes. Using these names as user-defined entities causes a compile-time error in accordance with Declarations. An alphabetically sorted list of utility types is provided below.

#### 5.3.1 Awaited Utility Type

Implicit instantiation is only possible for generic functions and methods.

Type Awaited<T> constructs a type which includes no type Promise. It is similar to await in async functions, or to the method .then() in Promises. Any occurrence of type Promise is recursively removed until a generic, a function, an array, or a tuple type is detected. If type Promise is not a part of a type T declaration, then Awaited<T> leaves T intact.

If T in Awaited<T> is a type parameter, then subtyping for Awaited<T> is based on the subtyping for T. In other words, Awaited<T> is a subtype of Awaited<U> if T is a subtype of U. The use of type Awaited<T> is represented in the example below:

type A = Awaited<Promise<string>> // type A is string

type B = Awaited<Promise<promise<number>> // type B is number

type C = Awaited<boolean | Promise<number>> // type C is boolean | number

type D = Awaited <Object> // type D is Object

type E = Awaited<Promise<promise<number>> | Promise<string> | Promise<boolean>> // type E is number | string | boolean

type F = Awaited<Promise<(p: Promise<string>) => Promise<number>> // type F is (p: Promise<string>) => Promise<number>>

type G = Awaited<Promise<Array<promise<number>>>>> // type G is Array<promise<number>>
