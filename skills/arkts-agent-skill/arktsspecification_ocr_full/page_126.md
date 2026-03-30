### 7.14 New Expressions

There are two syntactical forms of the new expression:

newExpression:
    newClassInstance
| newArrayInstance
;

Type of a new expression is either class or array.

A new class instance expression creates a new object that is an instance of the specified class and it is described in full details below.

The creation of array instances is an experimental feature discussed in Resizable Array Creation Expressions.

The syntax of new class instance expression is presented below:

newClassInstance:
    'new' typeArguments? typeReference arguments?
;

Class instance creation expression specifies a class to be instantiated. It optionally lists all actual arguments for the constructor.

class A {
    constructor(p: number) {}
}

new A(5) // create an instance and call constructor
const a = new A(6) /* create an instance, call constructor and store
                    created and initialized instance in 'a' */

Class instance creation expression can throw an error (see Error Handling, Constructor Declaration).

When a class instance creation expression refers to classes FixedArray, Array, or derived classes of Array instantiated with an array element type of some class type then it turns out to be a special form of array creation expression. And in case when such array creation expression defines a number of elements of the created array it leads to a compile-time error if the type of an array element:

• refers to a class that contains neither an accessible (see Accessible) parameterless constructor nor a constructor with all parameters of the second form of optional parameters (see Optional Parameters); or

• has no default value.

The same restriction applies to ref:Resizable Array Creation Expressions.

class A<T> {
    foo() {
        const a1 = new Array<T> (5) // Array with 5 elements of type T cannot be created
        const a1 = new FixedArray<T> (5) // Array with 5 elements of type T cannot be created
    }
}

The execution of a class instance creation expression is performed as follows:

• New instance of class is created;
