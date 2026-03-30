<div id="slide_container" class="section slides layout-regular">

## Introduction

  - Basic operating systems terms and concepts
  - Overview of the Linux kernel

## User vs Kernel

  - Execution modes
      - Kernel mode
      - User mode
  - Memory protection
      - Kernel-space
      - User-space

## Typical operating system architecture

![../\_images/ditaa-48374873962ca32ada36c14ab9a83b60f112a1e0.png](../_images/ditaa-48374873962ca32ada36c14ab9a83b60f112a1e0.png)

## Monolithic kernel

![../\_images/ditaa-3dc899167df5e16a230c434cf5d6964cb5868482.png](../_images/ditaa-3dc899167df5e16a230c434cf5d6964cb5868482.png)

## Micro-kernel

![../\_images/ditaa-c8a3d93d0109b7be6f608871d16adff4aaa933da.png](../_images/ditaa-c8a3d93d0109b7be6f608871d16adff4aaa933da.png)

## Monolithic kernels *can* be modular

  - Components can enabled or disabled at compile time
  - Support of loadable kernel modules (at runtime)
  - Organize the kernel in logical, independent subsystems
  - Strict interfaces but with low performance overhead: macros, inline functions, function pointers

## "Hybrid" kernels

Many operating systems and kernel experts have dismissed the label as meaningless, and just marketing. Linus Torvalds said of this issue:

"As to the whole 'hybrid kernel' thing - it's just marketing. It's 'oh, those microkernels had good PR, how can we try to get good PR for our working kernel? Oh, I know, let's use a cool name and try to imply that it has all the PR advantages that that other system has'."

## Address space

  - Physical address space
      - RAM and peripheral memory
  - Virtual address space
      - How the CPU sees the memory (when in protected / paging mode)
      - Process address space
      - Kernel address space

## User and kernel sharing the virtual address space

![../\_images/ditaa-a5f93e0d17ccdc2ba24828b620d7227f7fc75e33.png](../_images/ditaa-a5f93e0d17ccdc2ba24828b620d7227f7fc75e33.png)

## Execution contexts

  - Process context
      - Code that runs in user mode, part of a process
      - Code that runs in kernel mode, as a result of a system call issued by a process
  - Interrupt context
      - Code that runs as a result of an interrupt
      - Always runs in kernel mode

## Multi-tasking

  - An OS that supports the "simultaneous" execution of multiple processes
  - Implemented by fast switching between running processes to allow the user to interact with each program
  - Implementation:
      - Cooperative
      - Preemptive

## Preemptive kernel

Preemptive multitasking and preemptive kernels are different terms.

A kernel is preemptive if a process can be preempted while running in kernel mode.

However, note that non-preemptive kernels may support preemptive multitasking.

## Pageable kernel memory

A kernel supports pageable kernel memory if parts of kernel memory (code, data, stack or dynamically allocated memory) can be swapped to disk.

## Kernel stack

Each process has a kernel stack that is used to maintain the function call chain and local variables state while it is executing in kernel mode, as a result of a system call.

The kernel stack is small (4KB - 12 KB) so the kernel developer has to avoid allocating large structures on stack or recursive calls that are not properly bounded.

## Portability

  - Architecture and machine specific code (C & ASM)
  - Independent architecture code (C):
      - kernel core (further split in multiple subsystems)
      - device drivers

## Asymmetric MultiProcessing (ASMP)

![../\_images/ditaa-cb16db58a2489307b74d4f70256a48c81c65f6c6.png](../_images/ditaa-cb16db58a2489307b74d4f70256a48c81c65f6c6.png)

## Symmetric MultiProcessing (SMP)

![../\_images/ditaa-08aff771b3ff7a5525df7b0c090e28c836502788.png](../_images/ditaa-08aff771b3ff7a5525df7b0c090e28c836502788.png)

## CPU Scalability

  - Use lock free algorithms when possible
  - Use fine grained locking for high contention areas
  - Pay attention to algorithm complexity

## Linux development model

  - Open source, GPLv2 License
  - Contributors: companies, academia and independent developers
  - Development cycle: 3 – 4 months which consists of a 1 - 2 week merge window followed by bug fixing
  - Features are only allowed in the merge window
  - After the merge window a release candidate is done on a weekly basis (rc1, rc2, etc.)

## Maintainer hierarchy

  - Linus Torvalds is the maintainer of the Linux kernel and merges pull requests from subsystem maintainers
  - Each subsystem has one or more maintainers that accept patches or pull requests from developers or device driver maintainers
  - Each maintainer has its own git tree, e.g.:
      - Linux Torvalds: git://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux-2.6.git
      - David Miller (networking): git://git.kernel.org/pub/scm/linux/kernel/git/davem/net.git/
  - Each subsystem may maintain a -next tree where developers can submit patches for the next merge window

## Linux source code layout

![../\_images/ditaa-f45246aade5ecc7cfb71f7f103a57f95fc7c2b9e.png](../_images/ditaa-f45246aade5ecc7cfb71f7f103a57f95fc7c2b9e.png)

## Linux kernel architecture

[![../\_images/ditaa-b9ffae65be16d30be11b5eca188a7a143b1b8227.png](../_images/ditaa-b9ffae65be16d30be11b5eca188a7a143b1b8227.png)](../_images/ditaa-b9ffae65be16d30be11b5eca188a7a143b1b8227.png)

## arch

  - Architecture specific code
  - May be further sub-divided in machine specific code
  - Interfacing with the boot loader and architecture specific initialization
  - Access to various hardware bits that are architecture or machine specific such as interrupt controller, SMP controllers, BUS controllers, exceptions and interrupt setup, virtual memory handling
  - Architecture optimized functions (e.g. memcpy, string operations, etc.)

## Device drivers

  - Unified device model
  - Each subsystem has its own specific driver interfaces
  - Many device driver types (TTY, serial, SCSI, fileystem, ethernet, USB, framebuffer, input, sound, etc.)

## Process management

  - Unix basic process management and POSIX threads support
  - Processes and threads are abstracted as tasks
  - Operating system level virtualization
      - Namespaces
      - Control groups

## Memory management

  - Management of the physical memory: allocating and freeing memory
  - Management of the virtual memory: paging, swapping, demand paging, copy on write
  - User services: user address space management (e.g. mmap(), brk(), shared memory)
  - Kernel services: SL\*B allocators, vmalloc

## Block I/O management

[![../\_images/ditaa-0a96997f269a7a9cd0cdc9c9125f6e62e549be94.png](../_images/ditaa-0a96997f269a7a9cd0cdc9c9125f6e62e549be94.png)](../_images/ditaa-0a96997f269a7a9cd0cdc9c9125f6e62e549be94.png)

## Virtual Filesystem Switch

[![../\_images/ditaa-afa57a07e21b1b842554278abe30fea575278452.png](../_images/ditaa-afa57a07e21b1b842554278abe30fea575278452.png)](../_images/ditaa-afa57a07e21b1b842554278abe30fea575278452.png)

## Networking stack

[![../\_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png](../_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png)](../_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png)

## Linux Security Modules

  - Hooks to extend the default Linux security model
  - Used by several Linux security extensions:
      - Security Enhancened Linux
      - AppArmor
      - Tomoyo
      - Smack

</div>

<div id="slide_notes" class="section">

</div>
