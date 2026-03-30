# Kernel Development Quickstart

Use this document for first-pass kernel triage and implementation guidance.

## 1. Establish baseline

- Capture kernel version and architecture.
- Run one full build or capture one full runtime trace.
- Keep raw evidence unchanged for comparison.

## 2. Identify subsystem

Classify the issue into one primary subsystem:

- module
- syscall
- process/scheduler
- interrupt/deferred work
- locking/SMP
- memory subsystem
- filesystem/VFS
- networking
- architecture
- device model
- debugging/profiling

## 3. Pick material

Use `source-map.md` and load one primary file only.
If blocked, load one secondary file.

## 4. Apply smallest fix

- Change one theme at a time.
- Preserve rollback ability.
- Avoid broad refactor during unstable baseline.

## 5. Verify with signal

Every proposed step must include one expected signal:

- compile output movement
- runtime log signal (`dmesg` marker)
- subsystem behavior evidence (e.g., IRQ registration, copy boundary, wake path)

## 6. Deliver minimal report

- subsystem + failure class
- evidence used
- file path(s) consulted under `references/`
- smallest patch sequence
- verification command and expected signal
- one risk/assumption
