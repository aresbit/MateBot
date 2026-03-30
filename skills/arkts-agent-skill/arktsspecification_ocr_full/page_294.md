#### 17.8.1 For-of Explicit Type Annotation

An explicit type annotation is allowed for a ForVariable (see for-of Statements):

// explicit type is used for a new variable,
let x: number[] = [1, 2, 3]
for (let n: number of x) {
    console.log(n)
}

Type of elements in a for-of expression must be assignable (see Assignability) to the type of the variable. Otherwise, a compile-time error occurs.

### 17.9 Overload Declarations

ArkTS supports both the conventional overloading and an innovative form of managed overloading that allows a developer to fully control the order of selecting a specific entity to call from several overloaded entities Overloading.

The actual entity to be called is determined at compile time. Thus, overloading is related to the compile-time polymorphism by name. The semantic details are discussed in Overloading.

An overload declaration is used in managed overloading to define a set and an order of the overloaded entities (functions, methods, or constructors).

An overload declaration can be used for:

• Functions (see Function Declarations), including functions in namespaces;

• Class or interface methods (see Method Declarations and Interface Method Declarations); and

• Ambient Declarations.

An overload declaration starts with the keyword overload and declares an overload alias for a set of explicitly listed entities as follows:

function max2(a: number, b: number): number {
    return a > b ? a : b
}
function maxN(...a: number[]): number {
    // return max element
}
// declare 'max' as an ordered set of functions max2 and maxN
overload max { max2, maxN }
