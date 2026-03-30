### 18.2 Using Annotations

The following syntax is used to apply an annotation to a declaration, and to define the values of annotation fields:

annotationUsage:
    '@' qualifiedName annotationValues?
    ;
annotationValues:
    '( ' (objectLiteral | constantExpression)？ ')'
    ;

An annotation declaration is represented in the example below:

@interface ClassPreamble {
    authorName: string
    revision: number = 1
}
@interface MyAnno{}

In general, annotation field values are set by an object literal. In a special case, annotation field values are set by using an expression (see Using Single Field Annotations).

All values in an object literal must be constant expressions. Otherwise, a compile-time error occurs.

The use of annotation is presented in the example below. The annotations in this example are applied to class declarations:

@ClassPreamble({authorName: "John", revision: 2})
class C1 {/*body*/}

@ClassPreamble({authorName: "Bob"}) // default value for revision = 1
class C2 {/*body*/}

@MyAnno()
class C3 {/*body*/}

Annotations can be applied to the following:

• Top-Level Declarations;

• Class members (see Class Members) or interface members (see Interface Members);

• Type usage (see Using Types);

• Parameters (see Parameter List and Optional Parameters);

• Lambda expression (see Lambda Expressions and Lambda Expressions with Receiver);

• Local Declarations.

Otherwise, a compile-time error occurs:

function foo () @MyAnno() {} // wrong target for annotation

Repeatable annotations are not supported, i.e., an annotation can be applied to an entity no more than once:

@ClassPreamble({authorName: "John"})
@ClassPreamble({authorName: "Bob"}) // compile-time error
class C {/*body*/}
