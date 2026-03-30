export v
let v = 1

The directive in the example below exports class ‘A’ by its name as default export:

class A {}
export default A
export {A as default} // such syntax is also acceptable

The directive in the example below exports a constant variable anonymously:

class A {}
export default new A

Single export directive acts as re-export when the declaration referred to by identifier is imported.

import {v} from "some location"
export v

#### 13.5.3 Export Type Directive

An export directive can have a type modifier exclusively for a better syntactic compatibility with TypeScript (also see Import Type Directive).

The export type directive syntax is presented below:

exportTypeDirective:
    'export' 'type' selectiveBindings
;

ArkTS supports no additional semantic checks for entities exported by using export type directives.

#### 13.5.4 Re-Export Directive

In addition to exporting what is declared in the module, it is possible to re-export declarations that are part of other modules' export. A particular declaration or all declarations can be re-exported from a module. When re-exporting, new names can be given. This action is similar to importing but has the opposite direction.

The syntax of re-export directive is presented below:

reExportDirective:
'export'
('*' bindingAlias?
| selectiveBindings
| '{' 'default' bindingAlias? '}'
)

(continues on next page)
