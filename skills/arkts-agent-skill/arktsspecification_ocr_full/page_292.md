class C {
    data: string[] = ['a', 'b', 'c');
    [Symbol.iterator]() {
        return new CIterator(this)
    }
}

The use of the name [Symbol.iterator] is considered deprecated. It can be removed in the future versions of the language.

### 17.7 Callable Types

A type is callable if the name of the type can be used in a call expression. A call expression that uses the name of a type is called a type call expression. Only class type can be callable. To make a type callable, a static method with the name $_invoke or $_instantiate must be defined or inherited:

class C {
    static $_invoke() { console.log("invoked") }
}
C() // prints: invoked
C.$_invoke() // also prints: invoked

In the above example, C() is a type call expression. It is the short form of the normal method call C.$_invoke(). Using an explicit call is always valid for the methods $_invoke and $_instantiate.

Note. Only a constructor—not the methods $_invoke or $_instantiate—is called in a new expression:

class C {
    static $_invoke() { console.log("invoked") }
    constructor() { console.log("constructed") }
}
let x = new C() // constructor is called

The methods $_invoke and $_instantiate are similar but have differences as discussed below.

A compile-time error occurs if a callable type contains both methods invoke and $_instantiate.

#### 17.7.1 Callable Types with $_invoke Method

The static method $_invoke can have an arbitrary signature. The method can be used in a type call expression in either case above. If the signature has parameters, then the call must contain corresponding arguments.

class Add {
    static $_invoke(a: number, b: number): number {
        return a + b
    }
}

(continues on next page)
