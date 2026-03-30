## ANNOTATIONS

Annotation is a special language element that changes the semantics of the declaration to which it is applied by adding metadata.

Declaring and using an annotation is represented in the example below:

// Annotation declaration:
@interface ClassAuthor {
    authorName: string
}

// Annotation use:
@ClassAuthor({authorName: "Bob"}
class MyClass {/*body*/}

The annotation ClassAuthor in the example above adds metadata to the class declaration.

An annotation must be placed immediately before the declaration to which it is applied. An annotation can include arguments as in the example above.

For an annotation to be used, the name of the annotation must be prefixed with the character ‘@’ (e.g., @MyAnno). No white space and line separator is allowed between the character ‘@’ and the name:

ClassAuthor({authorName: "Bob"}) // compile-time error, no '@'
@ ClassAuthor({authorName: "Bob"}) // compile-time error, space is forbidden

A compile-time error occurs if the annotation name is not accessible (see Accessible) at the place of use. An annotation declaration can be exported and used in other modules.

Multiple annotations can be applied to a single declaration:

@MyAnno()
@ClassAuthor({authorName: "John Smith”）
class MyClass {/*body*/}

### 18.1 Declaring Annotations

Declaring an annotation is similar to declaring an interface where the keyword interface is prefixed with the character '@'.
