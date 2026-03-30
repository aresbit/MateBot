(continued from previous page)

let setClass = new ClassWithSet
setClass = setClass[0] // Error - no $_get function available
setClass[0] = setClass

Type string can be used as a type of the index parameter:

class SomeClass {
    $_get (index: string): SomeClass { return this }
    $_set (index: string, value: SomeClass) {}
}
let x = new SomeClass
x = x["index string"]
// This notation implies a call: x = x.$_get ("index string")
x["index string"] = x
// This notation implies a call: x.$_set ("index string", x)

Functions $_get and $_set are ordinary functions with compiler-known signatures. The functions can be used like any other function. The functions can be abstract, or defined in an interface and implemented later. The functions can be overridden and provide a dynamic dispatch for the indexing expression evaluation (see Indexing Expressions). The functions can be used in generic classes and interfaces for better flexibility. A compile-time error occurs if these functions are marked as async.

interface ReadonlyIndexable<K, V> {
    $_get (index: K): V
}

interface Indexable<K, V> extends ReadonlyIndexable<K, V> {
    $_set (index: K, value: V)
}

class IndexableByNumber<V> implements Indexable<number, V> {
    private data: V[] = []
    $_get (index: number): V { return this.data [index] }
    $_set (index: number, value: V) { this.data[index] = value }
}

class IndexableByString<V> implements Indexable<string, V> {
    private data = new Map<string, V>
    $_get (index: string): V { return this.data [index] }
    $_set (index: string, value: V) { this.data[index] = value }
}

class BadClass extends IndexableByNumber<boolean> {
    override $_set (index: number, value: boolean) { index / 0 }
}

let x: IndexableByNumber<boolean> = new BadClass
x[42] = true // This will be dispatched at runtime to the overridden
// version of the $_set method
x.$_get (15) // $_get and $_set can be called as ordinary
// methods
