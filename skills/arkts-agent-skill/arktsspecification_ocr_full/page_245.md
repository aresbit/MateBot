#### 14.4.1 Ambient Indexer

Ambient indexer declarations specify the indexing of a class instance in an ambient context. The feature is provided for TypeScript compatibility:

The syntax of ambient indexer declaration is presented below:

ambientIndexerDeclaration:
    'readonly'? ['identifier': 'indexType'] 'returnType';
indexType: 'number';

The following restriction applies: Only one ambient indexer declaration is allowed in an ambient class declaration.

declare class C {
    [index: number]: number
}

Note. Ambient indexer declaration is supported in ambient contexts only. If written in ArkTS, ambient class implementation must conform to Indexable Types.

#### 14.4.2 Ambient Call Signature

Ambient call signature declarations are used to specify callable types in an ambient context. The feature is provided for TypeScript compatibility:

The syntax of ambient call signature declaration is presented below:

ambientCallSignatureDeclaration:
signature
;

declare class C {
    (someArg: number): boolean
}

Note. Ambient class signature declaration is supported in ambient contexts only. If written in ArkTS, ambient class implementation must conform to Callable Types with $_invoke Method.

#### 14.4.3 Ambient Iterable

Ambient秤able declaration indicates that a class instance is iterable in an ambient context. The feature is provided for TypeScript compatibility:

The syntax of ambient iterable declaration is presented below:

ambient 词性限定

'[Symbol.iterator]' '(' ')' returnType
;
