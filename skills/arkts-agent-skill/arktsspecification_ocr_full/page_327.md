## IMPLEMENTATION DETAILS

Important implementation details are discussed in this section.

### 20.1 Import Path Lookup

If an import path <some path>/name is resolved to a path in the folder 'name', then the compiler executes the following lookup sequence:

• If the folder contains the file index.ets, then this file is imported as a module written in ArkTS;

• If the folder contains the file index.ts, then this file is imported as a module written in TypeScript.

### 20.2 Modules in Host System

Modules are created and stored in a manner that is determined by the host system. The exact manner modules are stored in a file system is determined by a particular implementation of the compiler and other tools.

A simple implementation stores every module in a single file.

### 20.3 Getting Type Via Reflection

The ArkTS standard library (see Standard Library) provides a pseudogeneric static method Type.from<T>() to be processed by the compiler in a specific way during compilation. A call to this method allows getting a value of type Type that represents type T at runtime.

let type_of_int: Type = Type.from<int>()
    let type_of_string: Type = Type.from<string>()
    let type_of_number: Type = Type.from<number>()
    let type_of_Object: Type = Type.from<Object>()

class UserClass {}
let type_of_user_class: Type = Type.from<UserClass>()

(continues on next page)
