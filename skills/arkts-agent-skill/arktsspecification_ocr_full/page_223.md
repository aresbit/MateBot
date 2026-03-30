• Module imports itself directly: importPath refers to the file in which the current module is stored; or

#### 13.1.1 Bind All with Qualified Access

Import binding * as A binds the single named entity A to the declaration scope of the current module.

A qualified name consisting of A and the name of entity A.name is used to access any entity exported from the module as defined by the import path.

Import Usage
import * as Math from "..."
    let x = Math.sin(1.0)

This form of import is recommended because it simplifies the reading and understanding of the source code when all exported entities are prefixed with the name of the imported module.

#### 13.1.2 Default Import Binding

Default import binding allows importing a declaration exported from a module as default export. Knowing the actual name of a declaration is not required as the new name is given at importing. A compile-time error occurs if another form of import is used to import an entity initially exported as default.

There are two forms of default import binding:

• Single identifier;

• Special form of selective import with the keyword default.

import DefaultExportedItemBindedName from ".../someFile"
import {default as DefaultExportedItemNewName} from ".../someFile"
function foo() {
    let v1 = new DefaultExportedItemBindedName()
    // instance of class 'SomeClass' to be created here
    let v2 = new DefaultExportedItemNewName()
    // instance of class 'SomeClass' to be created here
}

// SomeFile
export default class SomeClass {}

// Or
class SomeClass {}
export default SomeClass
