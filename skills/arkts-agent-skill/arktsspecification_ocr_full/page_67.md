### 4.5 Type Declarations

An interface declaration (see Interfaces), a class declaration (see Classes), an enum declaration (see Enumerations), or a type alias (see Type Alias Declaration) are type declarations.

The syntax of type declaration is presented below:

typeDeclaration:
    classDeclaration
    | interfaceDeclaration
    | enumDeclaration
    | typeAlias
    ;

#### 4.5.1 Type Alias Declaration

Type aliases enable using meaningful and concise notations by providing the following:

• Names for anonymous types (array, function, and union types); or

• Alternative names for existing types.

Scopes of type aliases are module or namespace level scopes. Names of all type aliases must follow the uniqueness rules of Declarations in the current context.

The syntax of type alias is presented below:

typeAlias:
    'type' identifier typeParameters? '=' type
;

Meaningful names can be provided for anonymous types as follows:

type Matrix = number[][]
type Handler = (s: string, no: number) => string
type Predicate<T> = (x: T) => boolean
type NullableNumber = number | null

If the existing type name is too long, then a shorter new name can be introduced by using type alias (particularly for a generic type).

type Dictionary = Map<string, string>
type MapOfString<T> = Map<T, string>

A type alias acts as a new name only. It neither changes the original type meaning nor introduces a new type.

type Vector = number[]
function max(x: Vector): number {
    let m = x[0]
    for (let v of x)
        if (v > m) m = v
        return m

(continues on next page)
