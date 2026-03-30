#### 3.20.1 Union Types Normalization

Union types normalization allows minimizing the number of types within a union type, while keeping type safety. Some types can also be replaced for more general types.

Union type  $ T_1 \mid \ldots \mid T_N $, where  $ N > 1 $, can be formally reduced to type  $ U_1 \mid \ldots \mid U_M $, where  $ M \leq N $, or even to a non-union type  $ V $. In this latter case  $ V $ can be a predefined value type or a literal type.

The normalization process presumes that the following steps are performed one after another:

1. All nested union types are linearized.

2. All type aliases (if any and except recursive ones) are recursively replaced for non-alias types.

3. Identical types within a union type are replaced for a single type with account to the readonly type flag priority.

4. If at least one type in a union is Any, then all other types are removed.

5. If positioned among union types, type never is removed.

6. If one type in a union is string, then all string literal types (if any) are removed.

This procedure is performed recursively until none of the above steps can be performed again.

The normalization process results in a normalized union type. The process is represented by the examples below:

( T1 | T2) | (T3 | T4) // normalized as T1 | T2 | T3 | T4. Linearization
type A = A[] | string // No changes. Recursive type alias is kept
type B = number
type C = string
type D = B | C // normalized as number | string. Type aliases are unfolded
number | number // normalized as number. Identical types elimination
(number[]) | (readonly number[]) // normalized as readonly number[]. Readonly version_
→wins
"1" | string | number // normalized as string | number. Literal type value belongs to_
→another type values
class Base {}
class Derived extends Base {}
Base | Derived // normalized as Base | Derived (no change)

The ArkTS compiler applies normalization while processing union types and handling type inference for array literals (see Array Type Inference from Types of Elements).

#### 3.20.2 Access to Common Union Members

Where u is a variable of union type  $ T_1 \mid ... \mid T_N $, ArkTS supports access to a common member of u.m if the following conditions are fulfilled:

• Each  $ T_{i} $ is an interface or class type;

• Each  $ T_{i} $ has a non-static member with the name m; and
