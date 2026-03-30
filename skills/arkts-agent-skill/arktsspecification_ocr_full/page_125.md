• Object reference expression is evaluated first.

• If the evaluation completes abruptly, then so does the indexing expression, and the index expression is not evaluated.

• If the evaluation completes normally, then the index expression is evaluated. The resultant value of the object reference expression refers to a record instance.

• If the record instance contains a key defined by the index expression, then the result is the value mapped to the key.

• Otherwise, the result is the literal undefined.

### 7.13 Chaining Operator

The chaining operator ‘?.’ is used to effectively access values of nullish types. It can be used in the following contexts:

• Field Access Expression.

• Method Call Expression.

• Function Call Expression.

• Indexing Expressions.

If the value of the expression to the left of ‘?.’ is undefined or null, then the evaluation of the entire surrounding primary expression stops. The result of the entire primary expression is then undefined. Thus the type of the entire primary expression is the union undefined | non-nullish type of the entire primary expression:

class Person {
    name: string
    spouse?: Person = undefined
    constructor(name: string) {
        this.name = name
    }
}

let bob = new Person("Bob")
console.log(bob.spouse?.name) // prints "undefined"
// type of bob.spouse?.name is undefined|string

bob.spouse = new Person("Alice")
console.log(bob.spouse?.name) // prints "Alice"
// type of bob.spouse?.name is undefined|string

If an expression is not of a nullish type, then the chaining operator has no effect.

A compile-time error occurs if a chaining operator is placed in the context where a variable is expected, e.g., in the left-hand-side expression of an assignment (see Assignment) or expression (see Postfix Increment, Postfix Decrement, Prefix Increment or Prefix Decrement).
