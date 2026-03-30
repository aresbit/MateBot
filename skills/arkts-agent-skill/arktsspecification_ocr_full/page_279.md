## CONCURRENCY

### 16.1 Introductory Note

Most modern hardware has multiple cores. To achieve maximum performance, the software must be capable of using more than one core in some scenarios (e.g., multimedia processing, data analysis, simulation, modelling, databases etc.).

Providing support to a number of asynchronous APIs at different levels is also crucial.

### 16.2 Concurrency Subsystem Overview

#### 16.2.1 Major Concurrency Features

ArkTS has APIs for asynchronous programming that enables tasks to be suspended and resumed later, and supports coroutines that can run in parallel (implicitly or explicitly). Since the ArkTS coroutines share memory, a developer must be aware about the possible associated issues, and use appropriate functionality to guarantee thread safety.

ArkTS enables both asynchronous programming and parallel-run coroutines, and provides machinery for trustworthy concurrent programs by providing the following:

1. Asynchronous features async / await / Promise;

2. Coroutines (experimental) in Standard Library;

3. Structured concurrency in Standard Library (TaskPool API);

4. Synchronization primitives and “thread”-safe containers in Standard Library.
