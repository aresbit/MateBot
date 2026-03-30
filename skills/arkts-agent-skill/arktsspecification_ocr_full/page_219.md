## ERROR HANDLING

ArkTS is designed to provide first-class support in responding to, and recovering from different error situations in a program. Normal program execution can be interrupted by the occurrence of situations of two kinds:

• Runtime errors (e.g., null pointer dereferencing, array bounds checking, or division by zero);

• Operation completion failures (e.g., the task of reading and processing data from a file on disk can fail if the file does not exist on a specified path, read permissions are not available, or else).

The term error in this Specification denotes all kinds of error situations.

### 12.1 Errors

Error is the base class of all error situations. Defining a new error class is normally not required because essential error classes for various cases (e.g., RangeError) are defined in the standard library (see Standard Library).

However, a developer can handle a new error situation by using Error class itself, or by a subclass of Error. An example of error handling is provided below:

class UnknownError extends Error { // User-defined error class
    error: Error
    constructor (error: Error) {
        super()
        this.error = error
    }
}

function get_array_element<T>(array: T[], index: number): T | null {
    try {
        return array[index] // access array
    }
    catch (error) {
        if (error instanceof RangeError) // invalid index detected
            return null
        }
    }
}
