(continued from previous page)

}
console.log(Add(2, 2)) // prints: 4

That a type contains the instance method $_invoke does not make the type callable.

#### 17.7.2 Callable Types with $_instantiate Method

The static method $_instantiate can have an arbitrary signature by itself. If it is to be used in a type call expression, then its first parameter must be a factory (i.e., it must be a parameterless function type returning some class type). The method can have or not have other parameters, and those parameters can be arbitrary.

In a type call expression, the argument corresponding to the factory parameter is passed implicitly:

class C {
    static $_instantiate(factory: () => C): C {
        return factory()
    }
}
let x = C() // factory is passed implicitly
// Explicit call of：‘_instantiate' requires explicit 'factory':
let y = C.$_instantiate(() => { return new C() })

If the method $_instantiate has additional parameters, then the call must contain corresponding arguments:

class C {
    name = ""
    static $_instantiate(factory: () => C, name: string): C {
        let x = factory()
        x.name = name
        return x
    }
}
let x = C("Bob") // factory is passed implicitly

A compile-time error occurs in a type call expression with type T, if:

• T has neither method $_invoke nor method $_instantiate; or

• T has the method $_instantiate but its first parameter is not a factory.

class C {
    static $_instantiate(factory: string): C {
        return factory()
    }
}
let x = C() // compile-time error, wrong $_instantiate' 1st parameter

That a type contains the instance method $_instantiate does not make the type callable.
