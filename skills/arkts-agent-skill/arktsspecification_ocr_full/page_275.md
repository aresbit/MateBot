If static initialization routine execution is terminated due to an exception thrown, then the initialization is not complete. Repeating an attempt to execute a static initialization produces an exception again.

Static initialization routine invocation of a concurrent execution (see Coroutines (Experimental)) involves synchronization of all coroutines that try to invoke it. The synchronization is to ensure that the initialization is performed only once, and the operations that require the static initialization to be performed are executed after the initialization completes.

If static initialization routines of two concurrently initialized classes are circularly dependent, then a deadlock can occur.

#### 15.11.1 Static Initialization Safety

A compile-time error occurs if a named reference refers to a not yet initialized entity, including one of the following:

• Variable (see Variable and Constant Declarations) of a module or namespace (see Namespace Declarations);

• Static field of a class (see Static and Instance Fields).

If detecting an access to a not yet initialized entity is not possible, then runtime evaluation is performed as follows:

• Default value is produced if the type of an entity has a default value;

• Otherwise, NullPointerError is thrown.

### 15.12 Dispatch

As a result of assignment (see Assignment) to a variable or call (see Method Call Expression or Function Call Expression), the actual runtime type of a parameter of class or interface can become different from the type explicitly specified or inferred at the point of declaration.

In this situation method calls are dispatched during program execution based on their actual type.

This mechanism is called dynamic dispatch. Dynamic dispatch is used in OOP languages to provide greater flexibility and the required level of abstraction. Unlike static dispatch where the particular method to be called is known at compile time, dynamic dispatch requires additional action during program code execution. Compilation tools can optimize dynamic to static dispatch.

### 15.13 Compatibility Features

Some features are added to ArkTS in order to support smooth TypeScript compatibility. Using these features while doing the ArkTS programming is not recommended in most cases.
