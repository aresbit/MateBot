#### 16.3.6 Unhandled Rejected Promises

In case of an unhandled rejection of Promise, either the custom handler provided for Promise rejection is called, or the default Promise rejection handler is called upon the entire program completion.

### 16.4 Coroutines (Experimental)

A function or lambda can be a coroutine. ArkTS supports basic coroutines and structured coroutines. Basic coroutines are used to create and launch a coroutine. The result is then to be awaited. Details are provided in Standard Library.
