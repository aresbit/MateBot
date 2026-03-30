The syntax of annotation declaration is presented below:

annotationDeclaration:
  '@interface ' identifier '{' annotationField* '}'
;
annotationField:
  identifier ':' type const Initializer?
;
const Initializer:
  =' constantExpression
;

As any other declared entity, an annotation can be exported by using the keyword export.

Type in the annotation field is restricted (see Types of Annotation Fields).

The default value of an annotation field can be specified by using `initializer` as `constant` expression. A compile-time error occurs if the value of this expression cannot be evaluated at compile time.

Annotation must be defined at the top level. Otherwise, a compile-time error occurs.

Annotation cannot be extended as inheritance is not supported.

The name of an annotation cannot coincide with the name of another entity:

@interface Position {/*properties*/}

class Position {/*body*/} // compile-time error: duplicate identifier

An annotation declaration defines no type, and no type alias can be applied to the annotation or used as an interface:

@interface Position {}
type Pos = Position // compile-time error

class A implements Position {} // compile-time error

#### 18.1.1 Types of Annotation Fields

The choice of types for annotation fields is limited to the following:

• Numeric Types:

• Type boolean (see Type boolean);

• Type string;

• Enumeration types (see Enumerations);

• Array of the above types (e.g., string[]), including arrays of arrays (e.g., string[][]).

A compile-time error occurs if any other type is used as the type of an annotation field.
