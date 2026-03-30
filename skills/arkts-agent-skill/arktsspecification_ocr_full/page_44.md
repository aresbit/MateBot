• Tuple Types;

• Function Types;

• Union Types;

• Literal Types;

• Type Any;

• Type string;

• Type bigint;

• Type never;

• Type null;

• Type undefined;

• Type void; and

• Type Parameters.

### 3.8 Type Any

Type Any is a predefined type which is the supertype of all types. Type Any is a predefined nullish-type (see Nullish Types), i.e., a supertype of Type void and Type null in particular.

Type Any has no methods or fields.

### 3.9 Type Object

Type Object is a predefined class type which is the supertype (see Subtyping) of all types except Type void, Type undefined, Type null, Nullish Types, Type Parameters, and Union Types that contain type parameters. All subtypes of Object inherit the methods of class Object (see Inheritance). All methods of class Object are described in full in Standard Library.

The method toString used in the examples in this document returns a string representation of the object.

The term object is used in the Specification to refer to an instance of any type.

Pointers to objects are called references. Multiple references to an object are possible.

Objects can have states. A state of an object that is a class instance is stored in its fields. A state of an array or tuple object is stored in its elements.

If two variables of any type except Value Types contain references to the same object, and the state of that object is modified in the reference of either variable, then the state so modified can be seen in the reference of the other variable.
