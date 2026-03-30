## GRAMMAR SUMMARY

literal: Literal;
identifier: Identifier;

indexType: 'number';

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

typeReference:
  typeReferencePart ('.' typeReferencePart)*
;

typeReferencePart:
  identifier typeArguments?
;

arrayType:
  type '[' '']
;
