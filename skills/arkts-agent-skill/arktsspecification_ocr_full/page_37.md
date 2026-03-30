• Function Types;

• Tuple Types:

• Union Types;

• Type Parameters; and

• Literal Types.

### 3.3 Using Types

Source code can refer to a type by using the following:

• Type reference for:

- Named Types, or

- Type aliases (see Type Alias Declaration);

• In-place type declaration for:

- Array Types,

- Tuple Types,

- Function Types,

– Function Types with Receiver,

- Keyof Types,

– Union Types, or

- Type in parentheses.

The syntax of type is presented below:

type:
  annotationUsage?
  ( typeReference
  | 'readonly'? arrayType
  | 'readonly'? tupleType
  | functionType
    | functionTypeWithReceiver
    | unionType
    | keyofType
    | StringLiteral
)
| '(' type ')'
;

The usage of annotations is discussed in Using Annotations.

Types with the prefix reading are discussed in Readonly Array Types and Readonly Triple Types.

The usage of types is represented by the example below:
