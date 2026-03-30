Instance fields belong to each instance of the class. An instance field is created for, and associated with a newly-created instance of a class, or of its superclass. An instance field is accessible (see Accessible) via the instance name.

#### 9.6.2 Readonly (Constant) Fields

A field with the modifier `readonly` is a `readonly` field. Changing the value of a `readonly` field after `initialization` is not allowed. Both static and non-static fields can be declared `readonly` fields.

#### 9.6.3 Optional Fields

Optional field f?: T = expr effectively means that the type of f`is `T | undefined. If an initializer is absent in a field declaration, then the default value undefined (see Default Values for Types) is used as the initial value of the field.

For example, the following two fields are actually defined the same way:

class C {
    f?: string
    g: string | undefined = undefined
}

#### 9.6.4 Field Initialization

All fields except Fields with Late Initialization are initialized by using the default value (see Default Values for Types) or a field initializer (see below). Otherwise, the field can be initialized in one of the following:

• Initializer block of a static field (see Static Initialization), or

• Class constructor of a non-static field (see Constructor Declaration).

Field initializer is an expression that is evaluated at compile time or runtime. The result of successful evaluation is assigned into the field. The semantics of field initializers is therefore similar to that of assignments (see Assignment). Each initializer expression evaluation and the subsequent assignment are only performed once.

Readonly fields initialization never uses default values (see Default Values for Types).

The initializer of a non-static field declaration is evaluated at runtime. The assignment is performed each time an instance of the class is created.

The instance field initializer expression cannot use the following directly in any form:

• super; or

• this.
