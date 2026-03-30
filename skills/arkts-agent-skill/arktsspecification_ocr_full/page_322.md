An ambient annotation and the annotation that implements it must be exactly identical, including field initialization:

// a.d.ets
export declare @interface NameAnno{name: string = ""}

// a.ets
export @interface NameAnno{name: string = ""} // ok

The code in the example below is incorrect because the ambient declaration is not identical to the annotation declaration:

// a.d.ets
export declare @interface VersionAnno{version: number} // initialization is missing

// a.ets
export @interface VersionAnno{version: number = 1}

An ambient declaration can be imported and used in exactly the same manner as a regular annotation:

// a.d.ets
export declare @interface MyAnno {}

// b.ets
import { MyAnno } from "./a"

@MyAnno
class C {/*body*/}

If an annotation is applied to an ambient declaration in the .d.ets file (see the example below), then the annotation is to be applied to the implementation declaration manually, because the annotation is not automatically applied to the declaration that implements the ambient declaration:

// a.d.ets
export declare @interface MyAnno {}

@MyAnno
declare class C {}

### 18.5 Standard Annotations

Standard annotation is an annotation that is defined in Standard Library, or implicitly defined in the compiler (built-in annotation). Standard annotation is usually known to the compiler. It modifies the semantics of the declaration it is applied to.

An annotation that annotates a declaration of another annotation is called meta-annotation.
