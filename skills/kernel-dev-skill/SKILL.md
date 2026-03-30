---
name: kernel-dev-skill
description: Linux kernel development skill grounded in local references/labs and references/lectures materials. Use for kernel modules, system calls, process scheduling, interrupts, locking, memory management, filesystems, networking, architecture, debugging, profiling, and device model work.
---

# Linux Kernel Development

Core rule: `simple is superior to everything`.

This skill is for practical kernel engineering. Use it to analyze failures, choose the smallest relevant subsystem material, make minimal verifiable changes, and validate with evidence.

## Use this skill when

- Kernel code fails to build or run on a target kernel
- A module, subsystem patch, or lab skeleton needs implementation
- You need help on process, syscall, interrupt, SMP, memory, filesystem, networking, or architecture topics
- You are decoding oops/panic, lock bugs, memory bugs, or performance regressions
- You are working on device-model or driver-adjacent kernel paths

## Scope

Includes:

- kernel modules and build flow
- kernel API and execution context rules
- system calls and process interactions
- interrupts and deferred work
- SMP and synchronization
- memory management and mapping
- filesystems and VFS-facing logic
- networking stack and net path basics
- architecture layer and portability concerns
- debugging and profiling
- device and driver model

## Coverage contract

When responding, ensure the chosen path explicitly maps to one of these kernel components:

- module lifecycle
- syscall boundary
- process/scheduler path
- interrupts/deferred work
- locking/SMP behavior
- memory subsystem (allocation, mapping, lifetime, reclaim-facing assumptions)
- filesystem/VFS path
- networking path
- architecture portability
- debugging/profiling or device model

If the issue touches memory, call out which memory aspect is involved:

- allocation/lifetime (`kmalloc`, `vmalloc`, `kzalloc`, free path symmetry)
- user/kernel copy boundary
- mapping or virtual memory behavior (`mmap`, vm area assumptions)
- context safety (sleeping/atomic constraints)

Excludes:

- pure user-space programs
- generic Linux administration without kernel code

## Required inputs

Collect minimal hard evidence before proposing a patch:

- target kernel version, distro, architecture
- source path and build entry (`Makefile` / `Kbuild` / target)
- first failing build log or runtime log
- subsystem guess: module, syscall, process, irq, memory, fs, net, arch, driver, or unknown
- desired outcome: compile fix, runtime fix, behavior change, or learning implementation

## Workflow

1. Freeze baseline.
   Run one build or collect one complete runtime failure trace.
2. Classify failure.
   Place blockers into one class: API break, context violation, concurrency, memory, lifecycle, functional bug, or performance issue.
3. Route to one reference first.
   Use [references/source-map.md](references/source-map.md) to pick the smallest matching file from `references/labs` or `references/lectures`.
4. Patch one theme per step.
   Avoid mixing unrelated refactors.
5. Verify immediately.
   Rebuild and run one focused check that proves the specific blocker moved.
6. Expand only after proof.
   After the first fix is validated, handle next blocker.

## Hard rules

- Minimal, reversible, evidence-based changes.
- No API claims without code/log evidence.
- Do not redesign architecture while baseline is broken.
- Do not hide uncertainty; label assumptions and provide next confirming command.
- Keep recommendations subsystem-specific, not generic Linux advice.

## Command set

```bash
make -C /lib/modules/$(uname -r)/build M=$PWD V=1 modules
make -C /lib/modules/$(uname -r)/build M=$PWD W=1 C=1 modules
dmesg -T | tail -n 200
scripts/checkpatch.pl --strict -f path/to/file.c
```

Add subsystem commands only when they directly test the current blocker.

## Subsystem verification rule

For the selected subsystem, include at least one verification step with an expected signal:

- memory: allocator path, user-copy return handling, or mapping behavior check
- interrupts: handler registration and interrupt-path signal in logs
- process/scheduler: task state transition or wake/sleep behavior evidence
- filesystem: VFS callback path evidence
- networking: packet path or interface state transition evidence
- syscall boundary: errno and copy boundary behavior evidence

## Output format

```text
1. Subsystem and failure class
2. Evidence used
3. Relevant local material
4. Smallest patch sequence
5. Verification step and expected signal
6. Risks / assumptions
```

Output must satisfy all items:

- name one primary kernel component from the coverage contract
- cite the local material file used for that component (`references/labs/*.md` or `references/lectures/*.md`)
- provide one concrete verification step with expected signal
- if subsystem is unknown, state the shortest command to disambiguate it

## Fast mode

For firefighting requests:

- show top 3 blockers only
- map each blocker to one local reference
- provide smallest next patch and one verification step

## References

- [references/source-map.md](references/source-map.md)
- [references/getting-started.md](references/getting-started.md)
- [references/api-migration-checklist.md](references/api-migration-checklist.md)
