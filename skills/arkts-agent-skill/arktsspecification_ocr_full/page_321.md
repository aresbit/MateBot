### 18.3 Exporting and Importing Annotations

An annotation can be exported and imported. However, a few forms of export and import directives are supported.

An annotation declaration to be exported must be marked with the keyword export as follows:

// a.ets
export @interface MyAnno {}

If an annotation is imported as a part of an imported module, then the annotation is accessed by its qualified name:

// b.ets
import * as ns from "./a"

@ns.MyAnno
class C {/*body*/}

Unqualified import is also allowed:

// b.ets
import { MyAnno } from "./a"

@MyAnno
class C {/*body*/}

An annotation is not a type. Using export type or import type notations to export or import annotations is forbidden:

import type { MyAnno } from "./a" // compile-time error

Annotations are forbidden in the following cases:

• Export default,

• Import default,

• Rename in export, and

• Rename in import.

import {MyAnno as Anno} from "./a" // compile-time error

### 18.4 Ambient Annotations

The syntax of ambient annotations is presented below:

ambientAnnotationDeclaration:
'declare' annotationDeclaration
;

Such a declaration does not introduce a new annotation but provides type information that is required to use the annotation. The annotation itself must be defined elsewhere. A runtime error occurs if no annotation corresponds to the ambient annotation used in the program.
