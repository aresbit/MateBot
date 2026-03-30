# Kernel Development Source Map

This skill uses local materials already normalized under `references/`.

## Primary content roots

- `references/labs/`: implementation-focused API usage and coding patterns
- `references/lectures/`: subsystem theory, architecture, and debugging model
- `references/so2/`: course-specific variants, assignments, and extra walkthroughs
- `references/info/`: environment and setup notes

## Routing by subsystem

| Subsystem | First file | Second file |
| --- | --- | --- |
| Module lifecycle | `references/labs/kernel_modules.md` | `references/labs/introduction.md` |
| Syscall and user boundary | `references/lectures/syscalls.md` | `references/lectures/processes.md` |
| Process/scheduler | `references/lectures/processes.md` | `references/lectures/smp.md` |
| Interrupt path | `references/labs/interrupts.md` | `references/lectures/interrupts.md` |
| Deferred work | `references/labs/deferred_work.md` | `references/lectures/interrupts.md` |
| SMP and locking | `references/lectures/smp.md` | `references/labs/kernel_api.md` |
| Memory subsystem | `references/lectures/memory-management.md` | `references/labs/memory_mapping.md` |
| Filesystem/VFS | `references/lectures/fs.md` | `references/labs/filesystems_part1.md` |
| Networking | `references/lectures/networking.md` | `references/labs/networking.md` |
| Architecture | `references/lectures/arch.md` | `references/labs/arm_kernel_development.md` |
| Debugging/profiling | `references/lectures/debugging.md` | `references/labs/kernel_profiling.md` |
| Device model | `references/labs/device_model.md` | `references/labs/device_drivers.md` |

## Search anchors

When scanning material quickly, start with these anchors:

- `copy_to_user`, `copy_from_user`
- `request_irq`, `spin_lock`, `mutex`
- `timer`, `workqueue`, `wait_event`
- `vmalloc`, `mmap`
- `struct file_operations`, `kobject`
- `oops`, `KASAN`, `lockdep`

## Usage contract

- Choose one primary subsystem before proposing a patch.
- Cite exact file paths from `references/labs` or `references/lectures`.
- Keep the first fix minimal and verifiable.
