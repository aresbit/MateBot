# Kernel Development Checklist

This checklist is for general kernel engineering across subsystems.

## A. Build and interface integrity

- callback signatures match target kernel APIs
- required headers, macros, and helpers are available
- structure field usage matches current definitions

## B. Execution context correctness

- no sleeping in atomic or interrupt context
- user-space access uses kernel copy helpers
- stack usage remains bounded and non-recursive for hot paths

## C. Concurrency and ordering

- shared state is lock-protected in all contexts
- irq/process lock interactions are deadlock-safe
- SMP/preempt assumptions are explicit and verified

## D. Memory subsystem checks

- allocation/free paths are symmetric on success and failure
- mapping assumptions (`mmap`/vm area) are valid for the path
- user/kernel copy boundaries are validated
- lifetime and ownership of pointers are explicit

## E. Subsystem contract checks

- syscall: errno, ABI semantics, user boundary
- process/scheduler: state transition and wake/sleep behavior
- interrupt/deferred: registration, handler safety, deferred handoff
- filesystem: VFS callback contract and object lifetime
- networking: state machine and path transition integrity
- device model: register/probe/remove symmetry

## F. Runtime-first debugging

- oops/panic: resolve crash symbol and call chain first
- hang/deadlock: isolate lock/wait source first
- corruption: run memory/debug tooling path first

## G. Verification gates

- build confirms blocker moved
- one subsystem-specific runtime signal passes
- no new high-severity warning in touched code

## H. Cleanup after stability

- normalize logs and error paths
- remove obsolete compatibility branches carefully
- style cleanup only after behavior is stable
