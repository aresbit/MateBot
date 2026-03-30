#### 18.5.1 Retention Annotation

@Retention is a standard meta-annotation that is used to annotate a declaration of another annotation. A compile-time error occurs if it is used in other places.

The annotation has a single field policy of type string. It is typically used as follows:

@Retention({policy: "RUNTIME"})
@interface MyAnno {} // this annotation uses "RUNTIME" policy
@MyAnno //
class C {}

The value of this field determines at which point an annotation is used, and discarded after use. The retention policies can be of three types:

• “SOURCE”

Annotations that use “SOURCE” policy are processed at compile time, and are discarded after compilation;

• "BYTECODE"

Metadata specified in annotations that use “BYTECODE” policy are saved into the bytecode file, but are discarded at runtime.

• "RUNTIME"

Metadata specified in annotations that use “RUNTIME” policy are saved into the bytecode file, are retained and can be accessed at runtime.

The default retention policy is “BYTECODE”.

A compile-time error occurs if any other string literal is used as the value of policy field.

As @Retention has a single field, it can be used with a short notation (see Using Single Field Annotations) as follows:

@Retention("SOURCE")
@interface Author {name: string} // this annotation uses "SOURCE" policy

### 18.6 Runtime Access to Annotations

For an annotation with retention policy (see Retention Annotation) BYTECODE or RUNTIME an abstract class with the name of the annotation is implicitly declared. All fields of this class are reasonably. If a field is of an array type, the array type is also readonly.

For the following annotation:

@Retention("RUNTIME")
@interface MyAnno {
    name: string
    attrs: number[]
}

—the abstract class is declared:
