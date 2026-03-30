### 13.1 Import Directives

Import directives make entities exported from other modules (see Modules and Namespaces) available for use in the current module by using different binding forms. These directives have no effect during the program execution.

An import declaration has the following two parts:

• Import path that determines from what module to import;

- Import bindings that define what entities, and in what form (either qualified or unqualified) the current module can use.

The syntax of import directives is presented below:

import Directive:
    'import ' 'type'? bindings 'from' import Path
;

bindings:
    defaultBinding
    | (defaultBinding ',')? allBinding
    | (defaultBinding ',')? selectiveBindings
;

allBinding:
    '*' bindingAlias
;

bindingAlias:
    'as' identifier
;

defaultBinding:
    identifier
;

selectiveBindings:
    nameBinding (',' nameBinding)*
;

nameBinding:
    identifier bindingAlias?
    | 'default' 'as' identifier
;

importPath:
    StringLiteral
;

Each binding adds a declaration or declarations to the scope of a module (see Scopes). Any declaration added so must be distinguishable in the declaration scope (see Declarations).

Import with type modifier is discussed in Import Type Directive.

A compile-time error occurs if:

• Declaration added to the scope of a module by a binding is not distinguishable;
