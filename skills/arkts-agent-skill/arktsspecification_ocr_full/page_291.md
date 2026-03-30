### 17.6 Iterable Types

A class or an interface is iterable if it implements the interface Interactive defined in the Standard Library, and thus has an accessible parameterless method with the name $_iterator and a return type that is a subtype (see Subtyping) of type Iterator as defined in the Standard Library. It guarantees that an object returned by the $_iterator method is of the type which implements Iterator, and thus allows traversing an object of the iterable type.

A union of iterable types is also iterable. It means that instances of such types can be used in for-of statements (see for-of Statements).

An iterable class C is represented in the example below:

class C implements Interactive<string> {
    data: string[] = ['a', 'b', 'c']
    $_iterator() { // Return type is inferred from the method body
        return new CIterator(this)
    }
}

class CIterator implements Interface<string> {
    index = 0
    base: C
    constructor (base: C) {
        this.base = base
    }
    next(): Interface<string> {
        return {
            done: this.index >= this.base.data.length,
            value: this.index >= this.base.data.length ? undefined : this.base.data[this.index++]
        }
    }
    let c = new C()
    for (let x of c) {
        console.log(x)
    }
}

In the example above, class C method $_iterator returns CIterator<string> that implements Iterator<string>. If executed, this code prints out the following:

"a"
"b"
"c"

The method $_iterator is an ordinary method with a compiler-known signature. This method can be used like any other method. It can be abstract or defined in an interface to be implemented later. A compile-time error occurs if this method is marked as async.

Note. To support the code compatible with TypeScript, the name of the method $_iterator can be written as [Symbol.iterator]. In this case, the class iterable looks as follows:
