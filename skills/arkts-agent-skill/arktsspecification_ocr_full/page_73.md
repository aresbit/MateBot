If a parameter type is prefixed with `ready`, then there are additional restrictions on the parameter as described in `Readonly Parameters`.

#### 4.7.3 Readonly Parameters

If the parameter type is `readonly` array or `tuple` type, then no assignment and no function or method call can modify elements of this array or `tuple`. Otherwise, a compile-time error occurs:

function foo(array: readonly number[], tuple: readonly [number, string]) {
    let element = array[0] // OK, one can get array element
    array[0] = element // compile-time error, array is readonly

    element = tuple[0] // OK, one can get tuple element
    tuple[0] = element // compile-time error, tuple is readonly
}

Any assignment of readonly parameters and variables must follow the limitations stated in Type of Expression.

#### 4.7.4 Optional Parameters

Optional parameters can be of two forms as follows:

optionalParameter:
    identifier (':' type)?）=' expression
| identifier '?' ':' type
;

The first form contains an expression that specifies a default value. It is called a parameter with default value. The value of the parameter is set to the default value if the argument corresponding to that parameter is omitted in a function or method call:

function pair(x: number, y: number = 7)
{
    console.log(x, y)
}
pair(1, 2) // prints: 1 2
pair(1) // prints: 1 7

The second form is a short-cut notation and identifier '?' ':' type effectively means that identifier has type T | undefined with the default value undefined.

For example, the following two functions can be used in the same way:

function hello1(name: string | undefined = undefined) {}
function hello2(name?: string) {}

hello1() // 'name' has 'undefined' value

(continues on next page)
