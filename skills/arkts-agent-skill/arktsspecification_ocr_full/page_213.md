#### 10.4.1 Required Interface Properties

A required property defined in the form of a field implicitly defines the following:

• Getter, if the property is marked as readonly;

• Otherwise, both a getter and a setter with the same name.

A type annotation for the field defines return type for the getter and type of parameter for the setter.

As a result, the following declarations have the same effect:

interface Style {
    color: string
}

// is the same as
interface Style {
    get color(): string
    set color(s: string)
}

Note. A required property defined in a form of accessors does not define any additional entities in the interface.

A class that implements an interface with properties can also use a field or an accessor notation (see Implementing Required Interface Properties, Implementing Optional Interface Properties).

#### 10.4.2 Optional Interface Properties

An optional property can be defined in two forms:

• Short form identifier '?' '::' T; or

• Explicit form identifier ':' T | undefined.

In both cases, identifier has effective type T | undefined.

The optional property implicitly defines the following:

• A getter (if the property is marked as readonly);

• Otherwise, both a getter and a setter with the same name.

Accessors have implicitly defined bodies, in this aspect they are similar to Default Interface Method Declarations. However, ArkTS does not support explicitly defined accessors with bodies.

The following declaration:

interface I {
    num?: number
}

– implicitly declares two accessors:

interface I {
    get num(): number | undefined { return undefined }
    set num(x: number | undefined) { throw new InvalidStoreAccessError }
}
