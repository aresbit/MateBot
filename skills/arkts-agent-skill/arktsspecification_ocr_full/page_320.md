When using an annotation, the order of values has no significance:

@ClassPreamble({authorName: "John", revision: 2})
// the same as:
@ClassPreamble({revision: 2, authorName: "John"}

When using an annotation, all fields without default values must be listed. Otherwise, a compile-time error occurs:

@ClassPreamble() // compile-time error, authorName is not defined
class C1 {/*body*/}

If a field of an array type for an annotation is defined, then its value is set by using the array literal syntax:

@interface ClassPreamble {
    authorName: string
    revision: number = 1
    reviewers: string[]
}

@ClassPreamble(
    {authorName: "Alice",
    reviewers: ["Bob", "Clara"]
)

class C3 {/*body*/}

If setting annotation properties is not required, then parentheses can be omitted after the annotation name:

@MyAnno
class C4 {/*body*/}

#### 18.2.1 Using Single Field Annotations

If annotation declaration defines only one field, then it can be used with a short notation to specify just one expression instead of an object literal:

@interface deprecated{
    fromVersion: string
}

@deprecated("5.18")
function foo() {}

@deprecated({fromVersion: "5.18”）
function goo() {}

A short notation and a notation with an object literal behave in exactly the same manner.
