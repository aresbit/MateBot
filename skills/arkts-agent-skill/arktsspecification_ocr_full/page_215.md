## ENUMERATIONS

Enumeration type enum specifies a distinct user-defined type with an associated set of named constants that define its possible values.

The syntax of enumeration declaration is presented below:

enumDeclaration:
    'const'? 'enum' identifier (':' type)? '{' enumConstantList? '}'
;
enumConstantList:
    enumConstant (',' enumConstant)* ','?
;
enumConstant:
    identifier ('=' constantExpression)?
;

Type const enum is supported for source-level compatibility with TypeScript. The modifier const is skipped as it has no impact on enum semantics in ArkTS.

Qualification by type is mandatory to access the enumeration constant, except enumeration constant initialization expressions:

enum Color { Red, Green, Blue }
let c: Color = Color.Red

enum Flags { Read, Write, ReadWrite = Read | Write }
// No need to use Flags.Read | Flags.Write in initialization

If enumeration type is exported, then all enumeration constants are exported along with the mandatory qualification.

For example, if Color is exported, then all constants like Color.Red are exported along with the mandatory qualification Color.

The value of an enum constant can be set as follows:

• Explicitly to a numeric constant expression (expression of type int or long) or to a constant expression of type string; or

• Implicitly by omitting the constant expression.

If constant expression is omitted, then the value of the enum constant is set implicitly to an integer value (see Enumeration Integer Values).

A compile-time error occurs if integer or string type enumeration constants are combined in a single enumeration.
