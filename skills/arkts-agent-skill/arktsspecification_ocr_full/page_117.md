The class of the actual object referred to at runtime can be T if T is a class type, or a subclass of T (see Subtyping).

The semantics of this in different contexts is represented in the example below:

interface anInterface {
    method() {
        this // type of 'this' is anInterface
    }
}

class aClass implements anInterface {
    method() {
        this // type of 'this' is aClass
    }
    field = (): void => {
        this // type of 'this' is aClass
    }
}

class AnotherClass {
    anotherMethod() {
        const obj: aClass = { // Object literal
            method() {
                this // type of 'this' is aClass
            },
            field: (): void => {
                this // type of 'this' is AnotherClass
            }
        }
    }
}

### 7.9 Field Access Expression

Field access expression can access a field of an object to which an object reference refers. The object reference can have different forms as described in detail in Accessing Current Object Fields and in Accessing SuperClass Properties.

The syntax of field access expression is presented below:

fieldAccessExpression:
    objectReference ('.' | '?.') identifier
;

A field access expression that contains ‘?.’ (see Chaining Operator) is called safe field access because it handles nullish object references safely.

If object reference evaluation completes abruptly, then so does the entire field access expression.

An object reference used to access a field must be a non-nullish reference type T. Otherwise, a compile-time error occurs.

A field access expression is valid if the identifier refers to an accessible member field (see Accessible) in type T. A compile-time error occurs otherwise.
