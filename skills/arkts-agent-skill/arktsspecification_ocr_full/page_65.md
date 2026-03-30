/* compile-time error: Name of the declaration clashes with the predefined type or standard library entity name. */
let number: number = 1
let String = true
function Record () {}
interface Object {}
let Array = 42

/* compile-time error: ambient and non-ambient declarations refer to the same entity in a single module
*/
declare function foo()
function foo() {}

### 4.3 Scopes

Different entity declarations introduce new names in different scopes. Scope is the region of program text where an entity is declared, along with other regions it can be used in. The following entities are always referred to by their qualified names only:

• Class and interface members (both static and instance ones);

• Entities imported via qualified import; and

• Entities declared in namespaces (see Namespace Declarations).

Other entities are referred to by their simple (unqualified) names.

Entities within the scope are accessible (see Accessible).

The scope level of an entity depends on the context the entity is declared in:

- Module level scope is applicable to modules only. Constants and variables are accessible (see Accessible) from their respective points of declaration to the end of the module. Other entities are accessible through the entire scope level. If exported, a name can be accessed in other modules.

• Namespace level scope is applicable to namespaces only. Constants and variables are accessible (see Accessible) from their respective points of declaration to the end of the namespace including all embedded namespaces. Other entities are accessible through the entire namespace scope level including embedded namespaces. If exported, a name can be accessed outside the namespace with mandatory namespace name qualification.

• A name declared inside a class (class level scope) is accessible (see Accessible) in the class and sometimes, depending on the access modifier (see Access Modifiers), outside the class, or by means of a derived class.

Access to names inside the class is qualified with one of the following:

- Keywords this or super;

– Class instance expression for the names of instance entities; or

- Name of the class for static entities.

Outside access is qualified with one of the following:
