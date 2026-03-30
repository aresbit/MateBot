(continued from previous page)

7 }
8
9 let x: Vector = [2, 3, 1]
10 console.log(max(x)) // output: 3

Type aliases can be recursively referenced inside the right-hand side of a type alias declaration.

In a type alias defined as type A = something, A can be used recursively if it is one of the following:

• Array element type: type A = A]; or

• Type argument of a generic type: type A = C<A>.

type A = A[] // ok, used as element type

class C<T> { /*body*/ }
type B = C<B> // ok, used as a type argument

type D = string | Array<D> // ok

Any other use causes a compile-time error, because the compiler does not have enough information about the defined alias:

type E = E // compile-time error
type F = string | E // compile-time error

The same rules apply to a generic type alias defined as type A<T> = something:

type A<T> = Array<A<T>> // ok, A<T> is used as a type argument
type A<T> = string | Array<A<T>> // ok

type A<T> = A<T> // compile-time error

A compile-time error occurs if a generic type alias is used without a type argument:

type A<T> = Array<A> // compile-time error

Note. There is no restriction on using a type parameter T in the right side of a type alias declaration. The following code is valid:

type NodeValue<T> = T | Array<T> | Array<NodeValue<T>>;

### 4.6 Variable and Constant Declarations

A non-ambient variable declaration introduces a new variable which is in fact a named storage location. A declared variable must be assigned an initial value before the first usage. The initial value is assigned either as a part of the declaration or in various forms via initialization.

The syntax of variable declarations is presented below:
