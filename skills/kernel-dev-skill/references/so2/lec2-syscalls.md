<div class="wy-grid-for-nav">

<div class="wy-side-scroll">

<div class="wy-side-nav-search">

[The Linux Kernel](../index.html)

<div class="version">

5.10.14

</div>

<div role="search">

</div>

</div>

<div class="wy-menu wy-menu-vertical" data-spy="affix" role="navigation" aria-label="Navigation menu">

  - [Operating Systems 2](index.html)
      - [SO2 - General Rules and Grading](grading.html)
      - [SO2 Lecture 01 - Course overview and Linux kernel introduction](lec1-intro.html)
      - [SO2 Lecture 02 - System calls](#)
          - [Lecture objectives:](#lecture-objectives)
          - [Linux system calls implementation](#linux-system-calls-implementation)
              - [System call table](#system-call-table)
              - [System call parameters handling](#system-call-parameters-handling)
          - [Virtual Dynamic Shared Object (VDSO)](#virtual-dynamic-shared-object-vdso)
          - [Accessing user space from system calls](#accessing-user-space-from-system-calls)
      - [SO2 Lecture 03 - Processes](lec3-processes.html)
      - [SO2 Lecture 04 - Interrupts](lec4-interrupts.html)
      - [SO2 Lecture 05 - Symmetric Multi-Processing](lec5-smp.html)
      - [SO2 Lecture 06 - Address Space](lec6-address-space.html)
      - [SO2 Lecture 07 - Memory Management](lec7-memory-management.html)
      - [SO2 Lecture 08 - Filesystem Management](lec8-filesystems.html)
      - [SO2 Lecture 09 - Kernel debugging](lec9-debugging.html)
      - [SO2 Lecture 10 - Networking](lec10-networking.html)
      - [SO2 Lecture 11 - Architecture Layer](lec11-arch.html)
      - [SO2 Lecture 12 - Virtualization](lec12-virtualization.html)
      - [SO2 Lab 01 - Introduction](lab1-intro.html)
      - [SO2 Lab 02 - Kernel API](lab2-kernel-api.html)
      - [SO2 Lab 03 - Character device drivers](lab3-device-drivers.html)
      - [SO2 Lab 04 - I/O access and Interrupts](lab4-interrupts.html)
      - [SO2 Lab 05 - Deferred work](lab5-deferred-work.html)
      - [SO2 Lab 06 - Memory Mapping](lab6-memory-mapping.html)
      - [SO2 Lab 07 - Block Device Drivers](lab7-block-device-drivers.html)
      - [SO2 Lab 08 - File system drivers (Part 1)](lab8-filesystems-part1.html)
      - [SO2 Lab 09 - File system drivers (Part 2)](lab9-filesystems-part2.html)
      - [SO2 Lab 10 - Networking](lab10-networking.html)
      - [SO2 Lab 11 - Kernel Development on ARM](lab11-arm-kernel-development.html)
      - [SO2 Lab 12 - Kernel Profiling](lab12-kernel-profiling.html)
      - [Collaboration](assign-collaboration.html)
      - [Assignment 0 - Kernel API](assign0-kernel-api.html)
      - [Assignment 1 - Kprobe based tracer](assign1-kprobe-based-tracer.html)
      - [Assignment 2 - Driver UART](assign2-driver-uart.html)
      - [Assignment 3 - Software RAID](assign3-software-raid.html)
      - [Assignment 4 - SO2 Transport Protocol](assign4-transport-protocol.html)
      - [Assignment 7 - SO2 Virtual Machine Manager with KVM](assign7-kvm-vmm.html)

<span class="caption-text">Lectures</span>

  - [Introduction](../lectures/intro.html)
  - [System Calls](../lectures/syscalls.html)
  - [Processes](../lectures/processes.html)
  - [Interrupts](../lectures/interrupts.html)
  - [Symmetric Multi-Processing](../lectures/smp.html)
  - [Address Space](../lectures/address-space.html)
  - [Memory Management](../lectures/memory-management.html)
  - [Filesystem Management](../lectures/fs.html)
  - [Debugging](../lectures/debugging.html)
  - [Network Management](../lectures/networking.html)
  - [Architecture Layer](../lectures/arch.html)
  - [Virtualization](../lectures/virt.html)

<span class="caption-text">Labs</span>

  - [Infrastructure](../labs/infrastructure.html)
  - [Introduction](../labs/introduction.html)
  - [Kernel modules](../labs/kernel_modules.html)
  - [Kernel API](../labs/kernel_api.html)
  - [Character device drivers](../labs/device_drivers.html)
  - [I/O access and Interrupts](../labs/interrupts.html)
  - [Deferred work](../labs/deferred_work.html)
  - [Block Device Drivers](../labs/block_device_drivers.html)
  - [File system drivers (Part 1)](../labs/filesystems_part1.html)
  - [File system drivers (Part 2)](../labs/filesystems_part2.html)
  - [Networking](../labs/networking.html)
  - [Kernel Development on ARM](../labs/arm_kernel_development.html)
  - [Memory mapping](../labs/memory_mapping.html)
  - [Linux Device Model](../labs/device_model.html)
  - [Kernel Profiling](../labs/kernel_profiling.html)

<span class="caption-text">Useful info</span>

  - [Recommended Setup](../info/vm.html)
  - [Virtual Machine Setup](../info/vm.html#virtual-machine-setup)
  - [Customizing the Virtual Machine Setup](../info/extra-vm.html)
  - [Contributing to linux-kernel-labs](../info/contributing.html)

</div>

</div>

<div class="section wy-nav-content-wrap" data-toggle="wy-nav-shift">

** [The Linux Kernel](../index.html)

<div class="wy-nav-content">

<div class="rst-content">

<div role="navigation" aria-label="Page navigation">

  - [](../index.html)
  - [Operating Systems 2](index.html)
  - SO2 Lecture 02 - System calls
  - [View page source](../_sources/so2/lec2-syscalls.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lecture-02-system-calls" class="section">

# SO2 Lecture 02 - System calls[¶](#so2-lecture-02-system-calls "Permalink to this headline")

[View slides](lec2-syscalls-slides.html)

<span class="admonition-so2-lecture-02-system-calls"></span>

<div id="lecture-objectives" class="section">

## Lecture objectives:[¶](#lecture-objectives "Permalink to this headline")

  - Linux system calls implementation
  - VDSO and virtual syscalls
  - Accessing user space from system calls

</div>

<div id="linux-system-calls-implementation" class="section">

## Linux system calls implementation[¶](#linux-system-calls-implementation "Permalink to this headline")

At a high level system calls are "services" offered by the kernel to user applications and they resemble library APIs in that they are described as a function call with a name, parameters, and return value.

 

![../\_images/ditaa-e76e44cad2e92f2134ab77f6a09605b29524d039.png](../_images/ditaa-e76e44cad2e92f2134ab77f6a09605b29524d039.png)

However, on a closer look, we can see that system calls are actually not function calls, but specific assembly instructions (architecture and kernel specific) that do the following:

  - setup information to identify the system call and its parameters
  - trigger a kernel mode switch
  - retrieve the result of the system call

In Linux, system calls are identified by numbers and the parameters for system calls are machine word sized (32 or 64 bit). There can be a maximum of 6 system call parameters. Both the system call number and the parameters are stored in certain registers.

For example, on 32bit x86 architecture, the system call identifier is stored in the EAX register, while parameters in registers EBX, ECX, EDX, ESI, EDI, EBP.

<span class="admonition-linux-system-call-setup"></span>

System libraries (e.g. libc) offers functions that implement the actual system calls in order to make it easier for applications to use them.

When a user to kernel mode transition occurs, the execution flow is interrupted and it is transferred to a kernel entry point. This is similar to how interrupts and exceptions are handled (in fact on some architectures this transition happens as a result of an exception).

The system call entry point will save registers (which contains values from user space, including system call number and system call parameters) on stack and then it will continue with executing the system call dispatcher.

<div class="admonition note">

Note

During the user - kernel mode transition the stack is also switched from the user stack to the kernel stack. This is explained in more details in the interrupts lecture.

</div>

![../\_images/ditaa-eeb919cd078d0ba5021028fa628bb47d7d6866e2.png](../_images/ditaa-eeb919cd078d0ba5021028fa628bb47d7d6866e2.png)

The purpose of the system call dispatcher is to verify the system call number and run the kernel function associated with the system call.

<div class="admonition-linux-system-call-dispatcher highlight-c">

<div class="highlight">

    /* Handles int $0x80 */
    __visible void do_int80_syscall_32(struct pt_regs *regs)
    {
        enter_from_user_mode();
        local_irq_enable();
        do_syscall_32_irqs_on(regs);
    }
    
    /* simplified version of the Linux x86 32bit System Call Dispatcher */
    static __always_inline void do_syscall_32_irqs_on(struct pt_regs *regs)
    {
        unsigned int nr = regs->orig_ax;
    
        if (nr < IA32_NR_syscalls)
            regs->ax = ia32_sys_call_table[nr](regs->bx, regs->cx,
                                               regs->dx, regs->si,
                                               regs->di, regs->bp);
        syscall_return_slowpath(regs);
    }

</div>

</div>

To demonstrate the system call flow we are going to use the virtual machine setup, attach gdb to a running kernel, add a breakpoint to the dup2 system call and inspect the state.

 

In summary, this is what happens during a system call:

  - The application is setting up the system call number and parameters and it issues a trap instruction
  - The execution mode switches from user to kernel; the CPU switches to a kernel stack; the user stack and the return address to user space is saved on the kernel stack
  - The kernel entry point saves registers on the kernel stack
  - The system call dispatcher identifies the system call function and runs it
  - The user space registers are restored and execution is switched back to user (e.g. calling IRET)
  - The user space application resumes

<div id="system-call-table" class="section">

### System call table[¶](#system-call-table "Permalink to this headline")

The system call table is what the system call dispatcher uses to map system call numbers to kernel functions:

<div class="admonition-system-call-table highlight-c">

<div class="highlight">

    #define __SYSCALL_I386(nr, sym, qual) [nr] = sym,
    
    const sys_call_ptr_t ia32_sys_call_table[] = {
      [0 ... __NR_syscall_compat_max] = &sys_ni_syscall,
      #include <asm/syscalls_32.h>
    };

</div>

</div>

<div class="highlight-c">

<div class="highlight">

    __SYSCALL_I386(0, sys_restart_syscall)
    __SYSCALL_I386(1, sys_exit)
    __SYSCALL_I386(2, sys_fork)
    __SYSCALL_I386(3, sys_read)
    __SYSCALL_I386(4, sys_write)
    #ifdef CONFIG_X86_32
    __SYSCALL_I386(5, sys_open)
    #else
    __SYSCALL_I386(5, compat_sys_open)
    #endif
    __SYSCALL_I386(6, sys_close)

</div>

</div>

</div>

<div id="system-call-parameters-handling" class="section">

### System call parameters handling[¶](#system-call-parameters-handling "Permalink to this headline")

Handling system call parameters is tricky. Since these values are setup by user space, the kernel can not assume correctness and must always verify them thoroughly.

Pointers have a few important special cases that must be checked:

  - Never allow pointers to kernel-space
  - Check for invalid pointers

Since system calls are executed in kernel mode, they have access to kernel space and if pointers are not properly checked user applications might get read or write access to kernel space.

For example, let's consider the case where such a check is not made for the read or write system calls. If the user passes a kernel-space pointer to a write system call then it can get access to kernel data by later reading the file. If it passes a kernel-space pointer to a read system call then it can corrupt kernel memory.

<span class="admonition-pointers-to-kernel-space"></span>

Likewise, if a pointer passed by the application is invalid (e.g. unmapped, read-only for cases where it is used for writing), it could "crash" the kernel. Two approaches could be used:

  - Check the pointer against the user address space before using it, or
  - Avoid checking the pointer and rely on the MMU to detect when the pointer is invalid and use the page fault handler to determine that the pointer was invalid

Although it sounds tempting, the second approach is not that easy to implement. The page fault handler uses the fault address (the address that was accessed), the faulting address (the address of the instruction that did the access) and information from the user address space to determine the cause:

> 
> 
> <div>
> 
>   - Copy on write, demand paging, swapping: both the fault and faulting addresses are in user space; the fault address is valid (checked against the user address space)
>   - Invalid pointer used in system call: the faulting address is in kernel space; the fault address is in user space and it is invalid
>   - Kernel bug (kernel accesses invalid pointer): same as above
> 
> </div>

But in the last two cases we don't have enough information to determine the cause of the fault.

In order to solve this issue, Linux uses special APIs (e.g `copy_to_user()`) to accesses user space that are specially crafted:

  - The exact instructions that access user space are recorded in a table (exception table)
  - When a page fault occurs the faulting address is checked against this table

Although the fault handling case may be more costly overall depending on the address space vs exception table size, and it is more complex, it is optimized for the common case and that is why it is preferred and used in Linux.

| Cost            | Pointer checks       | Fault handling         |
| --------------- | -------------------- | ---------------------- |
| Valid address   | address space search | negligible             |
| Invalid address | address space search | exception table search |

</div>

</div>

<div id="virtual-dynamic-shared-object-vdso" class="section">

## Virtual Dynamic Shared Object (VDSO)[¶](#virtual-dynamic-shared-object-vdso "Permalink to this headline")

The VDSO mechanism was born out of the necessity of optimizing the system call implementation, in a way that does not impact libc with having to track the CPU capabilities in conjunction with the kernel version.

For example, x86 has two ways of issuing system calls: int 0x80 and sysenter. The latter is significantly faster so it should be used when available. However, it is only available for processors newer than Pentium II and only for kernel versions greater than 2.6.

With VDSO the system call interface is decided by the kernel:

  - a stream of instructions to issue the system call is generated by the kernel in a special memory area (formatted as an ELF shared object)
  - that memory area is mapped towards the end of the user address space
  - libc searches for VDSO and if present will use it to issue the system call

 

An interesting development of the VDSO is the virtual system calls (vsyscalls) which run directly from user space. These vsyscalls are also part of VDSO and they are accessing data from the VDSO page that is either static or modified by the kernel in a separate read-write map of the VDSO page. Examples of system calls that can be implemented as vsyscalls are: getpid or gettimeofday.

  - "System calls" that run directly from user space, part of the VDSO
  - Static data (e.g. getpid())
  - Dynamic data update by the kernel a in RW map of the VDSO (e.g. gettimeofday(), time(), )

</div>

<div id="accessing-user-space-from-system-calls" class="section">

## Accessing user space from system calls[¶](#accessing-user-space-from-system-calls "Permalink to this headline")

As we mentioned earlier, user space must be accessed with special APIs (`get_user()`, `put_user()`, `copy_from_user()`, `copy_to_user()`) that check whether the pointer is in user space and also handle the fault if the pointer is invalid. In case of invalid pointers, they return a non-zero value.

<div class="admonition-accessing-user-space-from-system-calls highlight-c">

<div class="highlight">

    /* OK: return -EFAULT if user_ptr is invalid */
    if (copy_from_user(&kernel_buffer, user_ptr, size))
        return -EFAULT;
    
    /* NOK: only works if user_ptr is valid otherwise crashes kernel */
    memcpy(&kernel_buffer, user_ptr, size);

</div>

</div>

Let's examine the simplest API, get\_user, as implemented for x86:

<div class="admonition-get-user-implementation highlight-c">

<div class="highlight">

    #define get_user(x, ptr)                                          \
    ({                                                                \
      int __ret_gu;                                                   \
      register __inttype(*(ptr)) __val_gu asm("%"_ASM_DX);            \
      __chk_user_ptr(ptr);                                            \
      might_fault();                                                  \
      asm volatile("call __get_user_%P4"                              \
                   : "=a" (__ret_gu), "=r" (__val_gu),                \
                      ASM_CALL_CONSTRAINT                             \
                   : "0" (ptr), "i" (sizeof(*(ptr))));                \
      (x) = (__force __typeof__(*(ptr))) __val_gu;                    \
      __builtin_expect(__ret_gu, 0);                                  \
    })

</div>

</div>

The implementation uses inline assembly, which allows inserting ASM sequences in C code and also handles access to/from variables in the ASM code.

Based on the type size of the x variable, one of \_\_get\_user\_1, \_\_get\_user\_2 or \_\_get\_user\_4 will be called. Also, before executing the assembly call, ptr will be moved to the first register EAX while after the completion of assembly part the value of EAX will be moved to \_\_ret\_gu and the EDX register will be moved to \_\_val\_gu.

It is equivalent to the following pseudo code:

<div class="admonition-get-user-pseudo-code highlight-c">

<div class="highlight">

    #define get_user(x, ptr)                \
        movl ptr, %eax                      \
        call __get_user_1                   \
        movl %edx, x                        \
        movl %eax, result                   \

</div>

</div>

The \_\_get\_user\_1 implementation for x86 is the following:

<div class="admonition-get-user-1-implementation highlight-none">

<div class="highlight">

    .text
    ENTRY(__get_user_1)
        mov PER_CPU_VAR(current_task), %_ASM_DX
        cmp TASK_addr_limit(%_ASM_DX),%_ASM_AX
        jae bad_get_user
        ASM_STAC
    1:  movzbl (%_ASM_AX),%edx
        xor %eax,%eax
        ASM_CLAC
        ret
    ENDPROC(__get_user_1)
    
    bad_get_user:
        xor %edx,%edx
        mov $(-EFAULT),%_ASM_AX
        ASM_CLAC
        ret
    END(bad_get_user)
    
    _ASM_EXTABLE(1b,bad_get_user)

</div>

</div>

The first two statements check the pointer (which is stored in EDX) with the addr\_limit field of the current task (process) descriptor to make sure that we don't have a pointer to kernel space.

Then, SMAP is disabled, to allow access to user from kernel, and the access to user space is done with the instruction at the 1: label. EAX is then zeroed to mark success, SMAP is enabled, and the call returns.

The movzbl instruction is the one that does the access to user space and its address is captured with the 1: label and stored in a special section:

<div class="admonition-exception-table-entry highlight-c">

<div class="highlight">

    /* Exception table entry */
    # define _ASM_EXTABLE_HANDLE(from, to, handler)           \
      .pushsection "__ex_table","a" ;                         \
      .balign 4 ;                                             \
      .long (from) - . ;                                      \
      .long (to) - . ;                                        \
      .long (handler) - . ;                                   \
      .popsection
    
    # define _ASM_EXTABLE(from, to)                           \
      _ASM_EXTABLE_HANDLE(from, to, ex_handler_default)

</div>

</div>

For each address that accesses user space we have an entry in the exception table, that is made up of: the faulting address(from), where to jump to in case of a fault, and a handler function (that implements the jump logic). All of these addresses are stored on 32bit in relative format to the exception table, so that they work for both 32 and 64 bit kernels.

All of the exception table entries are then collected in the \_\_ex\_table section by the linker script:

<div class="admonition-exception-table-building highlight-c">

<div class="highlight">

    #define EXCEPTION_TABLE(align)                                    \
      . = ALIGN(align);                                               \
      __ex_table : AT(ADDR(__ex_table) - LOAD_OFFSET) {               \
              VMLINUX_SYMBOL(__start___ex_table) = .;                 \
              KEEP(*(__ex_table))                                     \
              VMLINUX_SYMBOL(__stop___ex_table) = .;                  \
      }

</div>

</div>

The section is guarded with \_\_start\_\_\_ex\_table and \_\_stop\_\_\_ex\_table symbols, so that it is easy to find the data from C code. This table is accessed by the fault handler:

<div class="admonition-exception-table-handling highlight-c">

<div class="highlight">

    bool ex_handler_default(const struct exception_table_entry *fixup,
                            struct pt_regs *regs, int trapnr)
    {
        regs->ip = ex_fixup_addr(fixup);
        return true;
    }
    
    int fixup_exception(struct pt_regs *regs, int trapnr)
    {
        const struct exception_table_entry *e;
        ex_handler_t handler;
    
        e = search_exception_tables(regs->ip);
        if (!e)
            return 0;
    
        handler = ex_fixup_handler(e);
        return handler(e, regs, trapnr);
    }

</div>

</div>

All it does is to set the return address to the one in the field of the exception table entry which, in case of the get\_user exception table entry, is bad\_get\_user which return -EFAULT to the caller.

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lec1-intro.html "SO2 Lecture 01 - Course overview and Linux kernel introduction") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lec3-processes.html "SO2 Lecture 03 - Processes")

</div>

-----

<div role="contentinfo">

© Copyright The kernel development community.

</div>

Built with [Sphinx](https://www.sphinx-doc.org/) using a [theme](https://github.com/readthedocs/sphinx_rtd_theme) provided by [Read the Docs](https://readthedocs.org).

</div>

</div>

</div>

</div>
