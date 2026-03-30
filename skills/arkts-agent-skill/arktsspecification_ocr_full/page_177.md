function ProcessFile(name: string) {
    let r = new SomeResource()
    try {
        // some processing
    }
    finally {
        // finally clause will be executed after try-catch is
        executed normally or abruptly
        r.close()
    }
}

#### 8.15.3 try Statement Execution

1. A try block and the entire try statement complete normally if no catch block is executed. The execution of a try block completes abruptly if an error is thrown inside the try block.

2. The the execution of a try block completes abruptly if error x is thrown inside the try block. If the catch clause is present, and the execution of the body of the catch clause completes normally, then the entire try statement completes normally. Otherwise, the try statement completes abruptly.

3. If no catch clause is in place, then the error is propagated to the surrounding and caller scopes until reaching the scope with the catch clause to handle the error. If there is no such scope, then the whole coroutine stack (see Coroutines (Experimental)) is discarded. Subsequent steps are then defined by the execution environment.

4. If finally clause is in place, and its execution completes abruptly, then the try statement also completes abruptly.
