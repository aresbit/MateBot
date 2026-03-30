The expression is a subtype of Promise. If expression is  $ Promise<T> $, then type of awaitExpression is  $ Awaited<T> $.

await is used to wait for Promise

If Promise not resolved, then the current coroutine is suspended until it is resolved.

If Promise is rejected, then the reason of the rejection is thrown.

Using await outside of async functions is forbidden.

#### 16.3.5 Promise

The Promise object is introduced to support asynchronous API. It is the object that represents a proxy for the result of an asynchronous operation. The semantics of Promise is similar to the semantics of Promise in JavaScript/TypeScript if it is used in the context of a single coroutine.

Promise object represents the values returned by the call of an async function. Promise object can be used without any qualification as it is defined in the Standard Library.

The Promise lifetime is not limited to the lifetime of the root coroutine as it is created.

Promise is not in general designed to be used concurrently and simultaneously from multiple coroutines. However, it is safe to do the following:

• Pass Promise from one coroutine to another, and avoid using it again in the original coroutine.

• Pass Promise from one coroutine to another, use it in both coroutines, and call then only in one coroutine.

- Pass Promise from one coroutine to another, use it in both coroutines, and call them in both coroutines. The user is to provide custom synchronization to guarantee that there is not called simultaneously for this Promise.

The methods are used as follows:

• then takes two arguments. The first argument is the callback used if the promise is fulfilled. The second argument is used if it is rejected, and returns Promise<U>.

• If then is called from the same parent coroutine several times, then the order of then is the same if called in JavaScript/TypeScript. The callback is called on the coroutine when then called, and if Promise is passed from one coroutine to another and called then in both, then they are called in different coroutines (possibly concurrently). The developer must consider a possible data race, and take appropriate care.

Promise<U>::then<U, E = never>(onFulfilled: ((value: T) => U|PromiseLike<U>
    ←throws)|undefined, onRejected: ((error: Any) => E|PromiseLike<E> throws)|undefined):
    ←Promise<Awaited<U|E>>

• catch takes one argument (the callback called after promise is rejected) and returns Promise<Awaited<U|T>>

Promise<U>::catch<U = never>(onRejected?: (error: Any) => U|PromiseLike<U> throws):_
    →Promise<Awaited<T | U>>

• finally takes one argument (the callback called after promise is either fulfilled or rejected) and returns Promise<Awaited<T>>.

finally(onFinally?: () => void throws): Promise<Awaited<T>>
