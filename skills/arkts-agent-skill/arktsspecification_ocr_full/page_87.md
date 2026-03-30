(continued from previous page)

function foo <T extends SuperType> (p: Awaited<T>) {}
function bar <T extends SubType> (p: Awaited<T>) {
    foo (p) // is a valid call as Awaited<T extends SubType> <: Awaited<T extends_SuperType>
}

#### 5.3.2 NonNullable Utility Type

Type NonNullable<T> constructs a type by excluding null and undefined types. If type T contains neither null nor undefined, then NonNullable<T> leaves T intact. The use of type NonNullable<T> is represented in the example below:

type X = Object | null | undefined
type Y = NonNullable<X> // type of 'Y' is Object

class A <T> {
    field: NonNullable<T> // This is a non-nullable version of the type parameter
    constructor (field: NonNullable<T>) {
        this.field = field
    }
}

const a = new A<Object|null> (new Object)
a.field // type of field is Object

#### 5.3.3 Partial Utility Type

Type Partial<T> constructs a type with all properties of T set to optional. T must be a class or an interface type. Otherwise, a compile-time error occurs. No method (not even any getter or setter) of T is a part of the Partial<T> type. The use is represented in the example below:

interface Issue {
    title: string
    description: string
}

function process(issue: Partial<Issue>) {
    if (issue.title != undefined) {
        /* process title */
    }
}

process({title: "aa"}) // description is undefined
