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
      - [SO2 Lecture 02 - System calls](lec2-syscalls.html)
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
      - [SO2 Lab 01 - Introduction](#)
          - [Lab objectives](#lab-objectives)
          - [About this laboratory](#about-this-laboratory)
          - [References](#references)
          - [Documentation](#documentation)
          - [Kernel Modules Overview](#kernel-modules-overview)
          - [An example of a kernel module](#an-example-of-a-kernel-module)
          - [Compiling kernel modules](#compiling-kernel-modules)
          - [Loading/unloading a kernel module](#loading-unloading-a-kernel-module)
          - [Kernel Module Debugging](#kernel-module-debugging)
              - [objdump](#objdump)
              - [addr2line](#addr2line)
              - [minicom](#minicom)
              - [netconsole](#netconsole)
              - [Printk debugging](#printk-debugging)
              - [Dynamic debugging](#dynamic-debugging)
              - [KDB: Kernel debugger](#kdb-kernel-debugger)
          - [Exercises](#exercises)
              - [Remarks](#remarks)
              - [1. Kernel module](#kernel-module)
              - [2. Printk](#printk)
              - [3. Error](#error)
              - [4. Sub-modules](#sub-modules)
              - [5. Kernel oops](#kernel-oops-1)
              - [6. Module parameters](#module-parameters)
              - [7. Proc info](#proc-info-1)
          - [Good to know](#good-to-know-1)
          - [Source code navigation](#source-code-navigation)
              - [cscope](#cscope)
              - [clangd](#clangd)
              - [Kscope](#kscope)
              - [LXR Cross-Reference](#lxr-cross-reference)
              - [SourceWeb](#sourceweb)
          - [Kernel Debugging](#kernel-debugging)
              - [gdb (Linux)](#gdb-linux)
              - [Getting a stack trace](#getting-a-stack-trace)
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
  - SO2 Lab 01 - Introduction
  - [View page source](../_sources/so2/lab1-intro.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lab-01-introduction" class="section">

# SO2 Lab 01 - Introduction[¶](#so2-lab-01-introduction "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

  - presenting the rules and objectives of the Operating Systems 2 lab
  - introducing the lab documentation
  - introducing the Linux kernel and related resources
  - creating simple modules
  - describing the process of kernel module compilation
  - presenting how a module can be used with a kernel
  - simple kernel debugging methods

</div>

<div id="about-this-laboratory" class="section">

## About this laboratory[¶](#about-this-laboratory "Permalink to this headline")

The Operating Systems 2 lab is a kernel programming and driver development lab. The objectives of the laboratory are:

  - deepening the notions presented in the course
  - presentation of kernel programming interfaces (kernel API)
  - gaining documenting, development and debugging skills on a freestanding environment
  - acquiring knowledge and skills for drivers development

A laboratory will present a set of concepts, applications and commands specific to a given problem. The lab will start with a presentation (each lab will have a set of slides) (15 minutes) and the remaining time will be allocated to the lab exercises (80 minutes).

For best laboratory performance, we recommend that you read the related slides. To fully understand a laboratory, we recommend going through the lab support. For in-depth study, use the supporting documentation.

</div>

<div id="references" class="section">

## References[¶](#references "Permalink to this headline")

  - Linux
      - [Linux Kernel Development, 3rd Edition](http://www.amazon.com/Linux-Kernel-Development-Robert-Love/dp/0672329468/)
      - [Linux Device Drivers, 3rd Edition](http://free-electrons.com/doc/books/ldd3.pdf)
      - [Essential Linux Device Drivers](http://www.amazon.com/Essential-Device-Drivers-Sreekrishnan-Venkateswaran/dp/0132396556)
  - General
      - [mailing list](http://cursuri.cs.pub.ro/cgi-bin/mailman/listinfo/pso) ([searching the mailing list](http://blog.gmane.org/gmane.education.region.romania.operating-systems-design))

</div>

<div id="documentation" class="section">

## Documentation[¶](#documentation "Permalink to this headline")

Kernel development is a difficult process, compared to user space programming. The API is different and the complexity of the subsystems in kernel requires additional preparation. The associated documentation is heterogeneous, sometimes requiring the inspection of multiple sources to have a more complete understanding of a certain aspect.

The main advantages of the Linux kernel are the access to sources and the open development system. Because of this, the Internet offers a larger number of documentation for the kernel.

A few links related to the Linux kernel are shown bellow:

  - [KernelNewbies](http://kernelnewbies.org)
  - [KernelNewbies - Kernel Hacking](http://kernelnewbies.org/KernelHacking)
  - [Kernel Analysis - HOWTO](http://www.tldp.org/HOWTO/KernelAnalysis-HOWTO.html)
  - [Linux Kernel Programming](http://web.archive.org/web/20090228191439/http://www.linuxhq.com/lkprogram.html)
  - [Linux kernel - Wikibooks](http://en.wikibooks.org/wiki/Linux_kernel)

The links are not comprehensive. Using [The Internet](http://www.google.com) and [kernel source code](http://lxr.free-electrons.com/) is essential.

</div>

<div id="kernel-modules-overview" class="section">

## Kernel Modules Overview[¶](#kernel-modules-overview "Permalink to this headline")

A monolithic kernel, though faster than a microkernel, has the disadvantage of lack of modularity and extensibility. On modern monolithic kernels, this has been solved by using kernel modules. A kernel module (or loadable kernel mode) is an object file that contains code that can extend the kernel functionality at runtime (it is loaded as needed); When a kernel module is no longer needed, it can be unloaded. Most of the device drivers are used in the form of kernel modules.

For the development of Linux device drivers, it is recommended to download the kernel sources, configure and compile them and then install the compiled version on the test /development tool machine.

</div>

<div id="an-example-of-a-kernel-module" class="section">

## An example of a kernel module[¶](#an-example-of-a-kernel-module "Permalink to this headline")

Below is a very simple example of a kernel module. When loading into the kernel, it will generate the message `"Hi"`. When unloading the kernel module, the `"Bye"` message will be generated.

<div class="highlight-c">

<div class="highlight">

    #include <linux/kernel.h>
    #include <linux/init.h>
    #include <linux/module.h>
    
    MODULE_DESCRIPTION("My kernel module");
    MODULE_AUTHOR("Me");
    MODULE_LICENSE("GPL");
    
    static int dummy_init(void)
    {
            pr_debug("Hi\n");
            return 0;
    }
    
    static void dummy_exit(void)
    {
            pr_debug("Bye\n");
    }
    
    module_init(dummy_init);
    module_exit(dummy_exit);

</div>

</div>

The generated messages will not be displayed on the console but will be saved in a specially reserved memory area for this, from where they will be extracted by the logging daemon (syslog). To display kernel messages, you can use the **dmesg** command or inspect the logs:

<div class="highlight-bash">

<div class="highlight">

    # cat /var/log/syslog | tail -2
    Feb 20 13:57:38 asgard kernel: Hi
    Feb 20 13:57:43 asgard kernel: Bye
    
    # dmesg | tail -2
    Hi
    Bye

</div>

</div>

</div>

<div id="compiling-kernel-modules" class="section">

## Compiling kernel modules[¶](#compiling-kernel-modules "Permalink to this headline")

Compiling a kernel module differs from compiling an user program. First, other headers should be used. Also, the module should not be linked to libraries. And, last but not least, the module must be compiled with the same options as the kernel in which we load the module. For these reasons, there is a standard compilation method (`kbuild`). This method requires the use of two files: a `Makefile` and a `Kbuild` file.

Below is an example of a `Makefile`:

<div class="highlight-bash">

<div class="highlight">

    KDIR = /lib/modules/`uname -r`/build
    
    kbuild:
            make -C $(KDIR) M=`pwd`
    
    clean:
            make -C $(KDIR) M=`pwd` clean

</div>

</div>

And the example of a `Kbuild` file used to compile a module:

<div class="highlight-bash">

<div class="highlight">

    EXTRA_CFLAGS = -Wall -g
    
    obj-m        = modul.o

</div>

</div>

As you can see, calling **make** on the `Makefile` file in the example shown will result in the **make** invocation in the kernel source directory (``/lib/modules/`uname -r`/build``) and referring to the current directory (`` M = `pwd` ``). This process ultimately leads to reading the `Kbuild` file from the current directory and compiling the module as instructed in this file.

<div class="admonition note">

Note

For labs we will configure different **KDIR**, according to the virtual machine specifications:

<div class="last highlight-bash">

<div class="highlight">

    KDIR = /home/student/src/linux
    [...]

</div>

</div>

</div>

A `Kbuild` file contains one or more directives for compiling a kernel module. The easiest example of such a directive is `obj-m = module.o`. Following this directive, a kernel module (`ko` - kernel object) will be created, starting from the `module.o` file. `module.o` will be created starting from `module.c` or `module.S`. All of these files can be found in the `Kbuild`'s directory.

An example of a `Kbuild` file that uses several sub-modules is shown below:

<div class="highlight-bash">

<div class="highlight">

    EXTRA_CFLAGS = -Wall -g
    
    obj-m        = supermodule.o
    supermodule-y = module-a.o module-b.o

</div>

</div>

For the example above, the steps to compile are:

> 
> 
> <div>
> 
>   - compile the `module-a.c` and `module-b.c` sources, resulting in module-a.o and module-b.o objects
>   - `module-a.o` and `module-b.o` will then be linked in `supermodule.o`
>   - from `supermodule.o` will be created `supermodule.ko` module
> 
> </div>

The suffix of targets in `Kbuild` determines how they are used, as follows:

> 
> 
> <div>
> 
>   - M (modules) is a target for loadable kernel modules
>   - Y (yes) represents a target for object files to be compiled and then linked to a module (`$(mode_name)-y`) or within the kernel (`obj-y`)
>   - any other target suffix will be ignored by `Kbuild` and will not be compiled
> 
> </div>

<div class="admonition note">

Note

These suffixes are used to easily configure the kernel by running the **make menuconfig** command or directly editing the `.config` file. This file sets a series of variables that are used to determine which features are added to the kernel at build time. For example, when adding BTRFS support with **make menuconfig**, add the line `CONFIG_BTRFS_FS = y` to the `.config` file. The BTRFS kbuild contains the line `obj-$(CONFIG_BTRFS_FS):= btrfs.o`, which becomes `obj-y:= btrfs.o`. This will compile the `btrfs.o` object and will be linked to the kernel. Before the variable was set, the line became `obj:=btrfs.o` and so it was ignored, and the kernel was build without BTRFS support.

</div>

For more details, see the `Documentation/kbuild/makefiles.txt` and `Documentation/kbuild/modules.txt` files within the kernel sources.

</div>

<div id="loading-unloading-a-kernel-module" class="section">

## Loading/unloading a kernel module[¶](#loading-unloading-a-kernel-module "Permalink to this headline")

To load a kernel module, use the **insmod** utility. This utility receives as a parameter the path to the `*.ko` file in which the module was compiled and linked. Unloading the module from the kernel is done using the **rmmod** command, which receives the module name as a parameter.

<div class="highlight-bash">

<div class="highlight">

    $ insmod module.ko
    $ rmmod module.ko

</div>

</div>

When loading the kernel module, the routine specified as a parameter of the `module_init` macro will be executed. Similarly, when the module is unloaded the routine specified as a parameter of the `module_exit` will be executed.

A complete example of compiling and loading/unloading a kernel module is presented below:

<div class="highlight-bash">

<div class="highlight">

    faust:~/lab-01/modul-lin# ls
    Kbuild  Makefile  modul.c
    
    faust:~/lab-01/modul-lin# make
    make -C /lib/modules/`uname -r`/build M=`pwd`
    make[1]: Entering directory `/usr/src/linux-2.6.28.4'
      LD      /root/lab-01/modul-lin/built-in.o
      CC [M]  /root/lab-01/modul-lin/modul.o
      Building modules, stage 2.
      MODPOST 1 modules
      CC      /root/lab-01/modul-lin/modul.mod.o
      LD [M]  /root/lab-01/modul-lin/modul.ko
    make[1]: Leaving directory `/usr/src/linux-2.6.28.4'
    
    faust:~/lab-01/modul-lin# ls
    built-in.o  Kbuild  Makefile  modul.c  Module.markers
    modules.order  Module.symvers  modul.ko  modul.mod.c
    modul.mod.o  modul.o
    
    faust:~/lab-01/modul-lin# insmod modul.ko
    
    faust:~/lab-01/modul-lin# dmesg | tail -1
    Hi
    
    faust:~/lab-01/modul-lin# rmmod modul
    
    faust:~/lab-01/modul-lin# dmesg | tail -2
    Hi
    Bye

</div>

</div>

Information about modules loaded into the kernel can be found using the **lsmod** command or by inspecting the `/proc/modules`, `/sys/module` directories.

</div>

<div id="kernel-module-debugging" class="section">

## Kernel Module Debugging[¶](#kernel-module-debugging "Permalink to this headline")

Troubleshooting a kernel module is much more complicated than debugging a regular program. First, a mistake in a kernel module can lead to blocking the entire system. Troubleshooting is therefore much slowed down. To avoid reboot, it is recommended to use a virtual machine (qemu, virtualbox, vmware).

When a module containing bugs is inserted into the kernel, it will eventually generate a [kernel oops](https://en.wikipedia.org/wiki/Linux_kernel_oops). A kernel oops is an invalid operation detected by the kernel and can only be generated by the kernel. For a stable kernel version, it almost certainly means that the module contains a bug. After the oops appears, the kernel will continue to work.

Very important to the appearance of a kernel oops is saving the generated message. As noted above, messages generated by the kernel are saved in logs and can be displayed with the **dmesg** command. To make sure that no kernel message is lost, it is recommended to insert/test the kernel directly from the console, or periodically check the kernel messages. Noteworthy is that an oops can occur because of a programming error, but also a because of hardware error.

If a fatal error occurs, after which the system can not return to a stable state, a [kernel panic](https://en.wikipedia.org/wiki/Linux_kernel_panic) is generated.

Look at the kernel module below that contains a bug that generates an oops:

<div class="highlight-c">

<div class="highlight">

    /*
     * Oops generating kernel module
     */
    
    #include <linux/kernel.h>
    #include <linux/module.h>
    #include <linux/init.h>
    
    MODULE_DESCRIPTION ("Oops");
    MODULE_LICENSE ("GPL");
    MODULE_AUTHOR ("PSO");
    
    #define OP_READ         0
    #define OP_WRITE        1
    #define OP_OOPS         OP_WRITE
    
    static int my_oops_init (void)
    {
            int *a;
    
            a = (int *) 0x00001234;
    #if OP_OOPS == OP_WRITE
            *a = 3;
    #elif OP_OOPS == OP_READ
            printk (KERN_ALERT "value = %d\n", *a);
    #else
    #error "Unknown op for oops!"
    #endif
    
            return 0;
    }
    
    static void my_oops_exit (void)
    {
    }
    
    module_init (my_oops_init);
    module_exit (my_oops_exit);

</div>

</div>

Inserting this module into the kernel will generate an oops:

<div class="highlight-bash">

<div class="highlight">

    faust:~/lab-01/modul-oops# insmod oops.ko
    [...]
    
    faust:~/lab-01/modul-oops# dmesg | tail -32
    BUG: unable to handle kernel paging request at 00001234
    IP: [<c89d4005>] my_oops_init+0x5/0x20 [oops]
      *de = 00000000
    Oops: 0002 [#1] PREEMPT DEBUG_PAGEALLOC
    last sysfs file: /sys/devices/virtual/net/lo/operstate
    Modules linked in: oops(+) netconsole ide_cd_mod pcnet32 crc32 cdrom [last unloaded: modul]
    
    Pid: 4157, comm: insmod Not tainted (2.6.28.4 #2) VMware Virtual Platform
    EIP: 0060:[<c89d4005>] EFLAGS: 00010246 CPU: 0
    EIP is at my_oops_init+0x5/0x20 [oops]
    EAX: 00000000 EBX: fffffffc ECX: c89d4300 EDX: 00000001
    ESI: c89d4000 EDI: 00000000 EBP: c5799e24 ESP: c5799e24
     DS: 007b ES: 007b FS: 0000 GS: 0033 SS: 0068
    Process insmod (pid: 4157, ti=c5799000 task=c665c780 task.ti=c5799000)
    Stack:
     c5799f8c c010102d c72b51d8 0000000c c5799e58 c01708e4 00000124 00000000
     c89d4300 c5799e58 c724f448 00000001 c89d4300 c5799e60 c0170981 c5799f8c
     c014b698 00000000 00000000 c5799f78 c5799f20 00000500 c665cb00 c89d4300
    Call Trace:
     [<c010102d>] ? _stext+0x2d/0x170
     [<c01708e4>] ? __vunmap+0xa4/0xf0
     [<c0170981>] ? vfree+0x21/0x30
     [<c014b698>] ? load_module+0x19b8/0x1a40
     [<c035e965>] ? __mutex_unlock_slowpath+0xd5/0x140
     [<c0140da6>] ? trace_hardirqs_on_caller+0x106/0x150
     [<c014b7aa>] ? sys_init_module+0x8a/0x1b0
     [<c0140da6>] ? trace_hardirqs_on_caller+0x106/0x150
     [<c0240a08>] ? trace_hardirqs_on_thunk+0xc/0x10
     [<c0103407>] ? sysenter_do_call+0x12/0x43
    Code: <c7> 05 34 12 00 00 03 00 00 00 5d c3 eb 0d 90 90 90 90 90 90 90 90
    EIP: [<c89d4005>] my_oops_init+0x5/0x20 [oops] SS:ESP 0068:c5799e24
    ---[ end trace 2981ce73ae801363 ]---

</div>

</div>

Although relatively cryptic, the message provided by the kernel to the appearance of an oops provides valuable information about the error. First line:

<div class="highlight-bash">

<div class="highlight">

    BUG: unable to handle kernel paging request at 00001234
    EIP: [<c89d4005>] my_oops_init + 0x5 / 0x20 [oops]

</div>

</div>

Tells us the cause and the address of the instruction that generated the error. In our case this is an invalid access to memory.

Next line

> 
> 
> <div>
> 
> `Oops: 0002 [# 1] PREEMPT DEBUG_PAGEALLOC`
> 
> </div>

Tells us that it's the first oops (\#1). This is important in the context that an oops can lead to other oopses. Usually only the first oops is relevant. Furthermore, the oops code (`0002`) provides information about the error type (see `arch/x86/include/asm/trap_pf.h`):

> 
> 
> <div>
> 
>   - Bit 0 == 0 means no page found, 1 means protection fault
>   - Bit 1 == 0 means read, 1 means write
>   - Bit 2 == 0 means kernel, 1 means user mode
> 
> </div>

In this case, we have a write access that generated the oops (bit 1 is 1).

Below is a dump of the registers. It decodes the instruction pointer (`EIP`) value and notes that the bug appeared in the `my_oops_init` function with a 5-byte offset (`EIP: [<c89d4005>] my_oops_init+0x5`). The message also shows the stack content and a backtrace of calls until then.

If an invalid read call is generated (`#define OP_OOPS OP_READ`), the message will be the same, but the oops code will differ, which would now be `0000`:

<div class="highlight-bash">

<div class="highlight">

    faust:~/lab-01/modul-oops# dmesg | tail -33
    BUG: unable to handle kernel paging request at 00001234
    IP: [<c89c3016>] my_oops_init+0x6/0x20 [oops]
      *de = 00000000
    Oops: 0000 [#1] PREEMPT DEBUG_PAGEALLOC
    last sysfs file: /sys/devices/virtual/net/lo/operstate
    Modules linked in: oops(+) netconsole pcnet32 crc32 ide_cd_mod cdrom
    
    Pid: 2754, comm: insmod Not tainted (2.6.28.4 #2) VMware Virtual Platform
    EIP: 0060:[<c89c3016>] EFLAGS: 00010292 CPU: 0
    EIP is at my_oops_init+0x6/0x20 [oops]
    EAX: 00000000 EBX: fffffffc ECX: c89c3380 EDX: 00000001
    ESI: c89c3010 EDI: 00000000 EBP: c57cbe24 ESP: c57cbe1c
     DS: 007b ES: 007b FS: 0000 GS: 0033 SS: 0068
    Process insmod (pid: 2754, ti=c57cb000 task=c66ec780 task.ti=c57cb000)
    Stack:
     c57cbe34 00000282 c57cbf8c c010102d c57b9280 0000000c c57cbe58 c01708e4
     00000124 00000000 c89c3380 c57cbe58 c5db1d38 00000001 c89c3380 c57cbe60
     c0170981 c57cbf8c c014b698 00000000 00000000 c57cbf78 c57cbf20 00000580
    Call Trace:
     [<c010102d>] ? _stext+0x2d/0x170
     [<c01708e4>] ? __vunmap+0xa4/0xf0
     [<c0170981>] ? vfree+0x21/0x30
     [<c014b698>] ? load_module+0x19b8/0x1a40
     [<c035d083>] ? printk+0x0/0x1a
     [<c035e965>] ? __mutex_unlock_slowpath+0xd5/0x140
     [<c0140da6>] ? trace_hardirqs_on_caller+0x106/0x150
     [<c014b7aa>] ? sys_init_module+0x8a/0x1b0
     [<c0140da6>] ? trace_hardirqs_on_caller+0x106/0x150
     [<c0240a08>] ? trace_hardirqs_on_thunk+0xc/0x10
     [<c0103407>] ? sysenter_do_call+0x12/0x43
    Code: <a1> 34 12 00 00 c7 04 24 54 30 9c c8 89 44 24 04 e8 58 a0 99 f7 31
    EIP: [<c89c3016>] my_oops_init+0x6/0x20 [oops] SS:ESP 0068:c57cbe1c
    ---[ end trace 45eeb3d6ea8ff1ed ]---

</div>

</div>

<div id="objdump" class="section">

### objdump[¶](#objdump "Permalink to this headline")

Detailed information about the instruction that generated the oops can be found using the **objdump** utility. Useful options to use are **-d** to disassemble the code and **-S** for interleaving C code in assembly language code. For efficient decoding, however, we need the address where the kernel module was loaded. This can be found in `/proc/modules`.

Here's an example of using **objdump** on the above module to identify the instruction that generated the oops:

<div class="highlight-bash">

<div class="highlight">

    faust:~/lab-01/modul-oops# cat /proc/modules
    oops 1280 1 - Loading 0xc89d4000
    netconsole 8352 0 - Live 0xc89ad000
    pcnet32 33412 0 - Live 0xc895a000
    ide_cd_mod 34952 0 - Live 0xc8903000
    crc32 4224 1 pcnet32, Live 0xc888a000
    cdrom 34848 1 ide_cd_mod, Live 0xc886d000
    
    faust:~/lab-01/modul-oops# objdump -dS --adjust-vma=0xc89d4000 oops.ko
    
    oops.ko:     file format elf32-i386
    
    
    Disassembly of section .text:
    
    c89d4000 <init_module>:
    #define OP_READ         0
    #define OP_WRITE        1
    #define OP_OOPS         OP_WRITE
    
    static int my_oops_init (void)
    {
    c89d4000:       55                      push   %ebp
    #else
    #error "Unknown op for oops!"
    #endif
    
            return 0;
    }
    c89d4001:       31 c0                   xor    %eax,%eax
    #define OP_READ         0
    #define OP_WRITE        1
    #define OP_OOPS         OP_WRITE
    
    static int my_oops_init (void)
    {
    c89d4003:       89 e5                   mov    %esp,%ebp
            int *a;
    
            a = (int *) 0x00001234;
    #if OP_OOPS == OP_WRITE
            *a = 3;
    c89d4005:       c7 05 34 12 00 00 03    movl   $0x3,0x1234
    c89d400c:       00 00 00
    #else
    #error "Unknown op for oops!"
    #endif
    
            return 0;
    }
    c89d400f:       5d                      pop    %ebp
    c89d4010:       c3                      ret
    c89d4011:       eb 0d                   jmp    c89c3020 <cleanup_module>
    c89d4013:       90                      nop
    c89d4014:       90                      nop
    c89d4015:       90                      nop
    c89d4016:       90                      nop
    c89d4017:       90                      nop
    c89d4018:       90                      nop
    c89d4019:       90                      nop
    c89d401a:       90                      nop
    c89d401b:       90                      nop
    c89d401c:       90                      nop
    c89d401d:       90                      nop
    c89d401e:       90                      nop
    c89d401f:       90                      nop
    
    c89d4020 <cleanup_module>:
    
    static void my_oops_exit (void)
    {
    c89d4020:       55                      push   %ebp
    c89d4021:       89 e5                   mov    %esp,%ebp
    }
    c89d4023:       5d                      pop    %ebp
    c89d4024:       c3                      ret
    c89d4025:       90                      nop
    c89d4026:       90                      nop
    c89d4027:       90                      nop

</div>

</div>

Note that the instruction that generated the oops (`c89d4005` identified earlier) is:

> 
> 
> <div>
> 
> `C89d4005: c7 05 34 12 00 00 03 movl $ 0x3,0x1234`
> 
> </div>

That is exactly what was expected - storing value 3 at 0x0001234.

The `/proc/modules` is used to find the address where a kernel module is loaded. The **--adjust-vma** option allows you to display instructions relative to `0xc89d4000`. The **-l** option displays the number of each line in the source code interleaved with the assembly language code.

</div>

<div id="addr2line" class="section">

### addr2line[¶](#addr2line "Permalink to this headline")

A more simplistic way to find the code that generated an oops is to use the **addr2line** utility:

<div class="highlight-bash">

<div class="highlight">

    faust:~/lab-01/modul-oops# addr2line -e oops.o 0x5
    /root/lab-01/modul-oops/oops.c:23

</div>

</div>

Where `0x5` is the value of the program counter (`EIP = c89d4005`) that generated the oops, minus the base address of the module (`0xc89d4000`) according to `/proc/modules`

</div>

<div id="minicom" class="section">

### minicom[¶](#minicom "Permalink to this headline")

**Minicom** (or other equivalent utilities, eg **picocom**, **screen**) is a utility that can be used to connect and interact with a serial port. The serial port is the basic method for analyzing kernel messages or interacting with an embedded system in the development phase. There are two more common ways to connect:

  - a serial port where the device we are going to use is `/dev/ttyS0`
  - a serial USB port (FTDI) in which case the device we are going to use is `/dev/ttyUSB`.

For the virtual machine used in the lab, the device that we need to use is displayed after the virtual machine starts:

<div class="highlight-bash">

<div class="highlight">

    char device redirected to /dev/pts/20 (label virtiocon0)

</div>

</div>

Minicom use:

<div class="highlight-bash">

<div class="highlight">

    #for connecting via COM1 and using a speed of 115,200 characters per second
    minicom -b 115200 -D /dev/ttyS0
    
    #For USB serial port connection
    minicom -D /dev/ttyUSB0
    
    #To connect to the serial port of the virtual machine
    minicom -D /dev/pts/20

</div>

</div>

</div>

<div id="netconsole" class="section">

### netconsole[¶](#netconsole "Permalink to this headline")

**Netconsole** is a utility that allows logging of kernel debugging messages over the network. This is useful when the disk logging system does not work or when serial ports are not available or when the terminal does not respond to commands. **Netconsole** comes in the form of a kernel module.

To work, it needs the following parameters:

> 
> 
> <div>
> 
>   - port, IP address, and the source interface name of the debug station
>   - port, MAC address, and IP address of the machine to which the debug messages will be sent
> 
> </div>

These parameters can be configured when the module is inserted into the kernel, or even while the module is inserted if it has been compiled with the `CONFIG_NETCONSOLE_DYNAMIC` option.

An example configuration when inserting **netconsole** kernel module is as follows:

<div class="highlight-bash">

<div class="highlight">

    alice:~# modprobe netconsole netconsole=6666@192.168.191.130/eth0,6000@192.168.191.1/00:50:56:c0:00:08

</div>

</div>

Thus, the debug messages on the station that has the address `192.168.191.130` will be sent to the `eth0` interface, having source port `6666`. The messages will be sent to `192.168.191.1` with the MAC address `00:50:56:c0:00:08`, on port `6000`.

Messages can be played on the destination station using **netcat**:

<div class="highlight-bash">

<div class="highlight">

    bob:~ # nc -l -p 6000 -u

</div>

</div>

Alternatively, the destination station can configure **syslogd** to intercept these messages. More information can be found in `Documentation/networking/netconsole.txt`.

</div>

<div id="printk-debugging" class="section">

### Printk debugging[¶](#printk-debugging "Permalink to this headline")

`The two oldest and most useful debugging aids are Your Brain and Printf`.

For debugging, a primitive way is often used, but it is quite effective: `printk` debugging. Although a debugger can also be used, it is generally not very useful: simple bugs (uninitialized variables, memory management problems, etc.) can be easily localized by control messages and the kernel-decoded oop message.

For more complex bugs, even a debugger can not help us too much unless the operating system structure is very well understood. When debugging a kernel module, there are a lot of unknowns in the equation: multiple contexts (we have multiple processes and threads running at a time), interruptions, virtual memory, etc.

You can use `printk` to display kernel messages to user space. It is similar to `printf`'s functionality; the only difference is that the transmitted message can be prefixed with a string of `"<n>"`, where `n` indicates the error level (loglevel) and has values between `0` and `7`. Instead of `"<n>"`, the levels can also be coded by symbolic constants:

<div class="highlight-c">

<div class="highlight">

    KERN_EMERG - n = 0
    KERN_ALERT - n = 1
    KERN_CRIT - n = 2
    KERN_ERR - n = 3
    KERN_WARNING - n = 4
    KERN_NOTICE - n = 5
    KERN_INFO - n = 6
    KERN_DEBUG - n = 7

</div>

</div>

The definitions of all log levels are found in `linux/kern_levels.h`. Basically, these log levels are used by the system to route messages sent to various outputs: console, log files in `/var/log` etc.

<div class="admonition note">

Note

To display `printk` messages in user space, the `printk` log level must be of higher priority than console\_loglevel variable. The default console log level can be configured from `/proc/sys/kernel/printk`.

For instance, the command:

<div class="highlight-bash">

<div class="highlight">

    echo 8 > /proc/sys/kernel/printk

</div>

</div>

will enable all the kernel log messages to be displayed in the console. That is, the logging level has to be strictly less than the `console_loglevel` variable. For example, if the `console_loglevel` has a value of `5` (specific to `KERN_NOTICE`), only messages with loglevel stricter than `5` (i.e `KERN_EMERG`, `KERN_ALERT`, `KERN_CRIT`, `KERN_ERR`, `KERN_WARNING`) will be shown.

</div>

Console-redirected messages can be useful for quickly viewing the effect of executing the kernel code, but they are no longer so useful if the kernel encounters an irreparable error and the system freezes. In this case, the logs of the system must be consulted, as they keep the information between system restarts. These are found in `/var/log` and are text files, populated by `syslogd` and `klogd` during the kernel run. `syslogd` and `klogd` take the information from the virtual file system mounted in `/proc`. In principle, with `syslogd` and `klogd` turned on, all messages coming from the kernel will go to `/var/log/kern.log`.

A simpler version for debugging is using the `/var/log/debug` file. It is populated only with the `printk` messages from the kernel with the `KERN_DEBUG` log level.

Given that a production kernel (similar to the one we're probably running with) contains only release code, our module is among the few that send messages prefixed with KERN\_DEBUG . In this way, we can easily navigate through the `/var/log/debug` information by finding the messages corresponding to a debugging session for our module.

Such an example would be the following:

<div class="highlight-bash">

<div class="highlight">

    # Clear the debug file of previous information (or possibly a backup)
    $ echo "New debug session" > /var/log/debug
    # Run the tests
    # If there is no critical error causing a panic kernel, check the output
    # if a critical error occurs and the machine only responds to a restart,
      restart the system and check /var/log/debug.

</div>

</div>

The format of the messages must obviously contain all the information of interest in order to detect the error, but inserting in the code `printk` to provide detailed information can be as time-consuming as writing the code to solve the problem. This is usually a trade-off between the completeness of the debugging messages displayed using `printk` and the time it takes to insert these messages into the text.

A very simple way, less time-consuming for inserting `printk` and providing the possibility to analyze the flow of instructions for tests is the use of the predefined constants `__FILE__`, `__LINE__` and `__func__`:

> 
> 
> <div>
> 
>   - `__FILE__` is replaced by the compiler with the name of the source file it is currently being compiled.
>   - `__LINE__` is replaced by the compiler with the line number on which the current instruction is found in the current source file.
>   - `__func__` /`__FUNCTION__` is replaced by the compiler with the name of the function in which the current instruction is found.
> 
> </div>

<div class="admonition note">

Note

`__FILE__` and `__LINE__` are part of the ANSI C specifications: `__func__` is part of specification C99; `__FUNCTION__` is a GNU `C` extension and is not portable; However, since we write code for the `Linux` kernel, we can use it without any problems.

</div>

The following macro definition can be used in this case:

<div class="highlight-c">

<div class="highlight">

    #define PRINT_DEBUG \
           printk (KERN_DEBUG "[% s]: FUNC:% s: LINE:% d \ n", __FILE__,
                   __FUNCTION__, __LINE__)

</div>

</div>

Then, at each point where we want to see if it is "reached" in execution, insert PRINT\_DEBUG; This is a simple and quick way, and can yield by carefully analyzing the output.

The **dmesg** command is used to view the messages printed with `printk` but not appearing on the console.

To delete all previous messages from a log file, run:

<div class="highlight-bash">

<div class="highlight">

    cat /dev/null > /var/log/debug

</div>

</div>

To delete messages displayed by the **dmesg** command, run:

<div class="highlight-bash">

<div class="highlight">

    dmesg -c

</div>

</div>

</div>

<div id="dynamic-debugging" class="section">

### Dynamic debugging[¶](#dynamic-debugging "Permalink to this headline")

Dynamic [dyndbg](https://www.kernel.org/doc/html/v4.15/admin-guide/dynamic-debug-howto.html) debugging enables dynamic debugging activation/deactivation. Unlike `printk`, it offers more advanced `printk` options for the messages we want to display; it is very useful for complex modules or troubleshooting subsystems. This significantly reduces the amount of messages displayed, leaving only those relevant for the debug context. To enable `dyndbg`, the kernel must be compiled with the `CONFIG_DYNAMIC_DEBUG` option. Once configured, `pr_debug()`, `dev_dbg()` and `print_hex_dump_debug()`, `print_hex_dump_bytes()` can be dynamically enabled per call.

The `/sys/kernel/debug/dynamic_debug/control` file from the debugfs (where `/sys/kernel/debug` is the path to which debugfs was mounted) is used to filter messages or to view existing filters.

<div class="highlight-c">

<div class="highlight">

    mount -t debugfs none /debug

</div>

</div>

[Debugfs](http://opensourceforu.com/2010/10/debugging-linux-kernel-with-debugfs/) is a simple file system, used as a kernel-space interface and user-space interface to configure different debug options. Any debug utility can create and use its own files /folders in debugfs.

For example, to display existing filters in `dyndbg`, you will use:

<div class="highlight-bash">

<div class="highlight">

    cat /debug/dynamic_debug/control

</div>

</div>

And to enable the debug message from line `1603` in the `svcsock.c` file:

<div class="highlight-bash">

<div class="highlight">

    echo 'file svcsock.c line 1603 +p' > /debug/dynamic_debug/control

</div>

</div>

The `/debug/dynamic_debug/control` file is not a regular file. It shows the `dyndbg` settings on the filters. Writing in it with an echo will change these settings (it will not actually make a write). Be aware that the file contains settings for `dyndbg` debugging messages. Do not log in this file.

<div id="dyndbg-options" class="section">

#### Dyndbg Options[¶](#dyndbg-options "Permalink to this headline")

  - `func` - just the debug messages from the functions that have the same name as the one defined in the filter.
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        echo 'func svc_tcp_accept +p' > /debug/dynamic_debug/control
    
    </div>
    
    </div>

  - `file` - the name of the file(s) for which we want to display the debug messages. It can be just the source name, but also the absolute path or kernel-tree path.
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        file svcsock.c
        file kernel/freezer.c
        file /usr/src/packages/BUILD/sgi-enhancednfs-1.4/default/net/sunrpc/svcsock.c
    
    </div>
    
    </div>

  - `module` - module name.
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        module sunrpc
    
    </div>
    
    </div>

  - `format` - only messages whose display format contains the specified string.
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        format "nfsd: SETATTR"
    
    </div>
    
    </div>

  - `line` - the line or lines for which we want to enable debug calls.
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        # Triggers debug messages between lines 1603 and 1605 in the svcsock.c file
        $ echo 'file svcsock.c line 1603-1605 +p' > /sys/kernel/debug/dynamic_debug/control
        # Enables debug messages from the beginning of the file to line 1605
        $ echo 'file svcsock.c line -1605 +p' > /sys/kernel/debug/dynamic_debug/control
    
    </div>
    
    </div>

In addition to the above options, a series of flags can be added, removed, or set with operators `+`, `-` or `=`:

> 
> 
> <div>
> 
>   - `p` activates the pr\_debug() .
>   - `f` includes the name of the function in the printed message.
>   - `l` includes the line number in the printed message.
>   - `m` includes the module name in the printed message.
>   - `t` includes the thread id if it is not called from interrupt context
>   - `_` no flag is set.
> 
> </div>

</div>

</div>

<div id="kdb-kernel-debugger" class="section">

### KDB: Kernel debugger[¶](#kdb-kernel-debugger "Permalink to this headline")

The kernel debugger has proven to be very useful to facilitate the development and debugging process. One of its main advantages is the possibility to perform live debugging. This allows us to monitor, in real time, the accesses to memory or even modify the memory while debugging. The debugger has been integrated in the mainline kernel starting with version 2.6.26-rci. KDB is not a *source debugger*, but for a complete analysis it can be used in parallel with gdb and symbol files -- see [<span class="std std-ref">the GDB debugging section</span>](#gdb-intro)

To use KDB, you have the following options:

> 
> 
> <div>
> 
>   - non-usb keyboard + VGA text console
>   - serial port console
>   - USB EHCI debug port
> 
> </div>

For the lab, we will use a serial interface connected to the host. The following command will activate GDB over the serial port:

<div class="highlight-bash">

<div class="highlight">

    echo hvc0 > /sys/module/kgdboc/parameters/kgdboc

</div>

</div>

KDB is a *stop mode debugger*, which means that, while it is active, all the other processes are stopped. The kernel can be *forced* to enter KDB during execution using the following [SysRq](http://en.wikipedia.org/wiki/Magic_SysRq_key) command

<div class="highlight-bash">

<div class="highlight">

    echo g > /proc/sysrq-trigger

</div>

</div>

or by using the key combination `Ctrl+O g` in a terminal connected to the serial port (for example using **minicom**).

KDB has various commands to control and define the context of the debugged system:

> 
> 
> <div>
> 
>   - lsmod, ps, kill, dmesg, env, bt (backtrace)
>   - dump trace logs
>   - hardware breakpoints
>   - modifying memory
> 
> </div>

For a better description of the available commands you can use the `help` command in the KDB shell. In the next example, you can notice a simple KDB usage example which sets a hardware breakpoint to monitor the changes of the `mVar` variable.

<div class="highlight-bash">

<div class="highlight">

    # trigger KDB
    echo g > /proc/sysrq-trigger
    # or if we are connected to the serial port issue
    Ctrl-O g
    # breakpoint on write access to the mVar variable
    kdb> bph mVar dataw
    # return from KDB
    kdb> go

</div>

</div>

<div class="admonition note">

Note

If you want to learn how to easily browse through the Linux source code and how to debug kernel code, read the [Good to know](#good-to-know) section.

</div>

</div>

</div>

<div id="exercises" class="section">

## Exercises[¶](#exercises "Permalink to this headline")

<div id="remarks" class="section">

### Remarks[¶](#remarks "Permalink to this headline")

<div class="admonition note">

Note

  - Usually, the steps used to develop a kernel module are the following:
      - editing the module source code (on the physical machine);
      - module compilation (on the physical machine);
      - generation of the minimal image for the virtual machine; this image contains the kernel, your module, busybox and eventually test programs;
      - starting the virtual machine using QEMU;
      - running the tests in the virtual machine.
  - When using cscope, use `~/src/linux`. If there is no `cscope.out` file, you can generate it using the command **make ARCH=x86 cscope**.
  - You can find more details about the virtual machine at [<span class="std std-ref">Recommended Setup</span>](../info/vm.html#vm-link).

</div>

<div class="admonition important">

Important

Before solving an exercice, **carefully** read all its bullets.

</div>

<div id="exercises-summary" class="admonition important">

Important

We strongly encourage you to use the setup from [this repository](https://gitlab.cs.pub.ro/so2/so2-labs).

  - To solve exercises, you need to perform these steps:
    
      - prepare skeletons from templates
      - build modules
      - start the VM and test the module in the VM.

The current lab name is kernel\_modules. See the exercises for the task name.

The skeleton code is generated from full source examples located in `tools/labs/templates`. To solve the tasks, start by generating the skeleton code for a complete lab:

<div class="highlight-shell">

<div class="highlight">

    tools/labs $ make clean
    tools/labs $ LABS=<lab name> make skels

</div>

</div>

You can also generate the skeleton for a single task, using

<div class="highlight-shell">

<div class="highlight">

    tools/labs $ LABS=<lab name>/<task name> make skels

</div>

</div>

Once the skeleton drivers are generated, build the source:

<div class="highlight-shell">

<div class="highlight">

    tools/labs $ make build

</div>

</div>

Then, start the VM:

<div class="highlight-shell">

<div class="highlight">

    tools/labs $ make console

</div>

</div>

The modules are placed in /home/root/skels/kernel\_modules/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

</div>

<div id="kernel-module" class="section">

### 1\. Kernel module[¶](#kernel-module "Permalink to this headline")

To work with the kernel modules, we will follow the steps described [<span class="std std-ref">above</span>](#exercises-summary).

  - Generate the skeleton for the task named **1-2-test-mod** then build the module,  
    by running the following command in `tools/labs`.

<div class="highlight-bash">

<div class="highlight">

    $ LABS=kernel_modules make skels
    $ make build

</div>

</div>

These command will build all the modules in the current lab skeleton.

<div class="admonition warning">

Warning

Until after solving exercise 3, you will get a compilation error for `3-error-mod`. To avoid this issue, remove the directory `skels/kernel_modules/3-error-mod/` and remove the corresponding line from `skels/Kbuild`.

</div>

Start the VM using **make console**, and perform the following tasks:

  - load the kernel module.
  - list the kernel modules and check if current module is present
  - unload the kernel module
  - view the messages displayed at loading/unloading the kernel module using **dmesg** command

<div class="admonition note">

Note

Read [Loading/unloading a kernel module](#loading-unloading-a-kernel-module) section. When unloading a kernel module, you can specify only the module name (without extension).

</div>

</div>

<div id="printk" class="section">

### 2\. Printk[¶](#printk "Permalink to this headline")

Watch the virtual machine console. Why were the messages displayed directly to the virtual machine console?

Configure the system such that the messages are not displayed directly on the serial console, and they can only be inspected using `dmesg`.

<div class="admonition hint">

Hint

One option is to set the console log level by writting the desired level to `/proc/sys/kernel/printk`. Use a value smaller than the level used for the prints in the source code of the module.

</div>

Load/unload the module again. The messages should not be printed to the virtual machine console, but they should be visible when running `dmesg`.

</div>

<div id="error" class="section">

### 3\. Error[¶](#error "Permalink to this headline")

Generate the skeleton for the task named **3-error-mod**. Compile the sources and get the corresponding kernel module.

Why have compilation errors occurred? **Hint:** How does this module differ from the previous module?

Modify the module to solve the cause of those errors, then compile and test the module.

</div>

<div id="sub-modules" class="section">

### 4\. Sub-modules[¶](#sub-modules "Permalink to this headline")

Inspect the C source files `mod1.c` and `mod2.c` in `4-multi-mod/`. Module 2 contains only the definition of a function used by module 1.

Change the `Kbuild` file to create the `multi_mod.ko` module from the two C source files.

<div class="admonition hint">

Hint

Read the [Compiling kernel modules](#compiling-kernel-modules) section of the lab.

</div>

Compile, copy, boot the VM, load and unload the kernel module. Make sure messages are properly displayed on the console.

</div>

<div id="kernel-oops-1" class="section">

### 5\. Kernel oops[¶](#kernel-oops-1 "Permalink to this headline")

Enter the directory for the task **5-oops-mod** and inspect the C source file. Notice where the problem will occur. Add the compilation flag `-g` in the Kbuild file.

<div class="admonition hint">

Hint

Read [Compiling kernel modules](#compiling-kernel-modules) section of the lab.

</div>

Compile the corresponding module and load it into the kernel. Identify the memory address at which the oops appeared.

<div class="admonition hint">

Hint

Read [<span id="problematic-1" class="problematic">\`Debugging\`\_</span>](#system-message-1) section of the lab. To identify the address, follow the oops message and extract the value of the instructions pointer (`EIP`) register.

</div>

Determine which instruction has triggered the oops.

<div class="admonition hint">

Hint

Use the `proc/modules` information to get the load address of the kernel module. Use, on the physical machine, objdump and/or addr2line . Objdump needs debugging support for compilation\! Read the lab's [objdump](#objdump) and [addr2line](#addr2line) sections.

</div>

Try to unload the kernel module. Notice that the operation does not work because there are references from the kernel module within the kernel since the oops; Until the release of those references (which is almost impossible in the case of an oops), the module can not be unloaded.

</div>

<div id="module-parameters" class="section">

### 6\. Module parameters[¶](#module-parameters "Permalink to this headline")

Enter the directory for the task **6-cmd-mod** and inspect the C `cmd_mod.c` source file. Compile and copy the associated module and load the kernel module to see the printk message. Then unload the module from the kernel.

Without modifying the sources, load the kernel module so that the message shown is `Early bird gets tired`.

<div class="admonition hint">

Hint

The str variable can be changed by passing a parameter to the module. Find more information [here](http://tldp.org/LDP/lkmpg/2.6/html/x323.html).

</div>

<span id="proc-info" class="target"></span>

</div>

<div id="proc-info-1" class="section">

### 7\. Proc info[¶](#proc-info-1 "Permalink to this headline")

Check the skeleton for the task named **7-list-proc**. Add code to display the Process ID (`PID`) and the executable name for the current process.

Follow the commands marked with `TODO`. The information must be displayed both when loading and unloading the module.

<div class="admonition note">

Note

  - In the Linux kernel, a process is described by the `struct task_struct`. Use [LXR](http://elixir.free-electrons.com/linux/latest/source) or `cscope` to find the definition of `struct task_struct`.
  - To find the structure field that contains the name of the executable, look for the "executable" comment.
  - The pointer to the structure of the current process running at a given time in the kernel is given by the `current` variable (of the type `struct task_struct*`).

</div>

<div class="admonition hint">

Hint

To use `current` you'll need to include the header in which the `struct task_struct` is defined, i.e `linux/sched.h`.

</div>

Compile, copy, boot the VM and load the module. Unload the kernel module.

Repeat the loading/unloading operation. Note that the PIDs of the displayed processes differ. This is because a process is created from the executable `/sbin/insmod` when the module is loaded and when the module is unloaded a process is created from the executable `/sbin/rmmod`.

</div>

</div>

<div id="good-to-know-1" class="section">

<span id="good-to-know"></span>

## Good to know[¶](#good-to-know-1 "Permalink to this headline")

The following sections contain useful information for getitng used to the Linux kernel code and debugging techniques.

</div>

<div id="source-code-navigation" class="section">

## Source code navigation[¶](#source-code-navigation "Permalink to this headline")

<div id="cscope" class="section">

<span id="cscope-intro"></span>

### cscope[¶](#cscope "Permalink to this headline")

[Cscope](http://cscope.sourceforge.net/) is a tool for efficient navigation of C sources. To use it, a cscope database must be generated from the existing sources. In a Linux tree, the command **make ARCH=x86 cscope** is sufficient. Specification of the architecture through the ARCH variable is optional but recommended; otherwise, some architecture dependent functions will appear multiple times in the database.

You can build the cscope database with the command **make ARCH=x86 COMPILED\_SOURCE=1 cscope**. This way, the cscope database will only contain symbols that have already been used in the compile process before, thus resulting in better performance when searching for symbols.

Cscope can also be used as stand-alone, but it is more useful when combined with an editor. To use cscope with **vim**, it is necessary to install both packages and add the following lines to the file `.vimrc` (the machine in the lab already has the settings):

<div class="highlight-vim">

<div class="highlight">

    if has("cscope")
            " Look for a 'cscope.out' file starting from the current directory,
            " going up to the root directory.
            let s:dirs = split(getcwd(), "/")
            while s:dirs != []
                    let s:path = "/" . join(s:dirs, "/")
                    if (filereadable(s:path . "/cscope.out"))
                            execute "cs add " . s:path . "/cscope.out " . s:path . " -v"
                            break
                    endif
                    let s:dirs = s:dirs[:-2]
            endwhile
    
            set csto=0  " Use cscope first, then ctags
            set cst     " Only search cscope
            set csverb  " Make cs verbose
    
            nmap `<C-\>`s :cs find s `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`g :cs find g `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`c :cs find c `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`t :cs find t `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`e :cs find e `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`f :cs find f `<C-R>`=expand("`<cfile>`")`<CR>``<CR>`
            nmap `<C-\>`i :cs find i ^`<C-R>`=expand("`<cfile>`")`<CR>`$`<CR>`
            nmap `<C-\>`d :cs find d `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap <F6> :cnext <CR>
            nmap <F5> :cprev <CR>
    
            " Open a quickfix window for the following queries.
            set cscopequickfix=s-,c-,d-,i-,t-,e-,g-
    endif

</div>

</div>

The script searches for a file called `cscope.out` in the current directory, or in parent directories. If **vim** finds this file, you can use the shortcut `Ctrl +]` or `Ctrl+\ g` (the combination control-\\ followed by g) to jump directly to the definition of the word under the cursor (function, variable, structure, etc.). Similarly, you can use `Ctrl+\ s` to go where the word under the cursor is used.

You can take a cscope-enabled `.vimrc` file (also contains other goodies) from <https://github.com/ddvlad/cfg/blob/master/_vimrc>. The following guidelines are based on this file, but also show basic **vim** commands that have the same effect.

If there are more than one results (usually there are) you can move between them using `F6` and `F5` (`:ccnext` and `:cprev`). You can also open a new panel showing the results using `:copen`. To close the panel, use the `:cclose` command.

To return to the previous location, use `Ctrl+o` (o, not zero). The command can be used multiple times and works even if cscope changed the file you are currently editing.

To go to a symbol definition directly when **vim** starts, use `vim -t <symbol_name>` (for example `vim -t task_struct`). Otherwise, if you started **vim** and want to search for a symbol by name, use `cs find g <symbol_name>` (for example `cs find g task_struct`).

If you found more than one results and opened a panel showing all the matches (using `:copen`) and you want to find a symbol of type structure, it is recommended to search in the results panel (using `/` -- slash) the character `{` (opening brace).

<div class="admonition important">

Important

You can get a summary of all the **cscope** commands using **:cs help**.

For more info, use the **vim** built-in help command: **:h cscope** or **:h copen**.

</div>

If you use **emacs**, install the `xcscope-el` package and add the following lines in `~/.emacs`.

<div class="highlight-vim">

<div class="highlight">

    (require ‘xcscope)
    (cscope-setup)

</div>

</div>

These commands will activate cscope for the C and C++ modes automatically. `C-s s` is the key bindings prefix and `C-s s s` is used to search for a symbol (if you call it when the cursor is over a word, it will use that). For more details, check https://github.com/dkogan/xcscope.el

</div>

<div id="clangd" class="section">

### clangd[¶](#clangd "Permalink to this headline")

[Clangd](https://clangd.llvm.org/) is a language server that provides tools for navigating C and C++ code. [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) facilitates features like go-to-definition, find-references, hover, completion, etc., using semantic whole project analysis.

Clangd requires a compilation database to understand the kernel source code. It can be generated with:

<div class="highlight-bash">

<div class="highlight">

    make defconfig
    make
    scripts/clang-tools/gen_compile_commands.py

</div>

</div>

LSP clients:

  - Vim/Neovim ([coc.nvim](https://github.com/neoclide/coc.nvim), [nvim-lsp](https://github.com/neovim/nvim-lspconfig), [vim-lsc](https://github.com/natebosch/vim-lsc), [vim-lsp](https://github.com/prabirshrestha/vim-lsp))
  - Emacs ([lsp-mode](https://github.com/emacs-lsp/lsp-mode))
  - VSCode ([clangd extension](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd))

</div>

<div id="kscope" class="section">

### Kscope[¶](#kscope "Permalink to this headline")

For a simpler interface, [Kscope](http://sourceforge.net/projects/kscope/) is a cscope frontend which uses QT. It is lightweight, very fast and very easy to use. It allows searching using regular expressions, call graphs, etc. Kscope is no longer mantained.

There is also a [port](https///opendesktop.org/content/show.php/Kscope4?content=156987) of version 1.6 for Qt4 and KDE 4 which keeps the integration of the text editor Kate and is easier to use than the last version on SourceForge.

</div>

<div id="lxr-cross-reference" class="section">

### LXR Cross-Reference[¶](#lxr-cross-reference "Permalink to this headline")

LXR (LXR Cross-Reference) is a tool that allows indexing and referencing the symbols in the source code of a program using a web interface. The web interface shows links to locations in files where a symbol is defined or used. Development website for LXR is <http://sourceforge.net/projects/lxr>. Similar tools are [OpenGrok](http://oracle.github.io/opengrok/) and [Gonzui](http://en.wikipedia.org/wiki/Gonzui).

Although LXR was originally intended for the Linux kernel sources, it is also used in the sources of [Mozilla](http://lxr.mozilla.org/), [Apache HTTP Server](http://apache.wirebrain.de/lxr/) and [FreeBSD](http://lxr.linux.no/freebsd/source).

There are a number of sites that use LXR for cross-referencing the the sources of the Linux kernel, the main site being [the original site of development](http://lxr.linux.no/linux/) which does not work anymore. You can use <https://elixir.bootlin.com/>.

LXR allows searching for an identifier (symbol), after a free text or after a file name. The main feature and, at the same time, the main advantage provided is the ease of finding the declaration of any global identifier. This way, it facilitates quick access to function declarations, variables, macro definitions and the code can be easily navigated. Also, the fact that it can detect what code areas are affected when a variable or function is changed is a real advantage in the development and debugging phase.

</div>

<div id="sourceweb" class="section">

### SourceWeb[¶](#sourceweb "Permalink to this headline")

[SourceWeb](http://rprichard.github.io/sourceweb/) is a source code indexer for C and C++. It uses the [framework](http://clang.llvm.org/docs/IntroductionToTheClangAST.html) provided by the Clang compiler to index the code.

The main difference between cscope and SourceWeb is the fact that SourceWeb is, in a way, a compiler pass. SourceWeb doesn't index all the code, but only the code that was efectively compiled by the compiler. This way, some problems are eliminated, such as ambiguities about which variant of a function defined in multiple places is used. This also means that the indexing takes more time, because the compiled files must pass one more time through the indexer to generate the references.

Usage example:

<div class="highlight-bash">

<div class="highlight">

    make oldconfig
    sw-btrace make -j4
    sw-btrace-to-compile-db
    sw-clang-indexer --index-project
    sourceweb index

</div>

</div>

`sw-btrace` is a script that adds the `libsw-btrace.so` library to `LD_PRELOAD`. This way, the library is loaded by every process started by `make` (basically, the compiler), registers the commands used to start the processes and generates a filed called `btrace.log`. This file is then used by `sw-btrace-to-compile-db` which converts it to a format defined by clang: [JSON Compilation Database](http://clang.llvm.org/docs/JSONCompilationDatabase.html). This JSON Compilation Database resulted from the above steps is then used by the indexer, which makes one more pass through the compiled source files and generates the index used by the GUI.

Word of advice: don't index the sources you are working with, but use a copy, because SourceWeb doesn't have, at this moment, the capability to regenerate the index for a single file and you will have to regenerate the complete index.

</div>

</div>

<div id="kernel-debugging" class="section">

## Kernel Debugging[¶](#kernel-debugging "Permalink to this headline")

Debugging a kernel is a much more difficult process than the debugging of a program, because there is no support from the operating system. This is why this process is usually done using two computers, connected on serial interfaces.

<div id="gdb-linux" class="section">

<span id="gdb-intro"></span>

### gdb (Linux)[¶](#gdb-linux "Permalink to this headline")

A simpler debug method on Linux, but with many disadvantages, is local debugging, using [gdb](http://www.gnu.org/software/gdb/), the uncompressed kernel image (`vmlinux`) and `/proc/kcore` (the real-time kernel image). This method is usually used to inspect the kernel and detect certain inconsistencies while it runs. The method is useful especially if the kernel was compiled using the `-g` option, which keeps debug information. Some well-known debug techniques can't be used by this method, such as breakpoints of data modification.

<div class="admonition note">

Note

Because `/proc` is a virtual filesystem, `/proc/kcore` does not physically exist on the disk. It is generated on-the-fly by the kernel when a program tries to access `proc/kcore`.

It is used for debugging purposes.

From **man proc**, we have:

<div class="last highlight-none">

<div class="highlight">

    /proc/kcore
    This file represents the physical memory of the system and is stored in the ELF core file format.  With this pseudo-file, and
    an unstripped kernel (/usr/src/linux/vmlinux) binary, GDB can be used to examine the current state of any kernel data struc‐
    tures.

</div>

</div>

</div>

The uncompressed kernel image offers information about the data structures and symbols it contains.

<div class="highlight-bash">

<div class="highlight">

    student@eg106$ cd ~/src/linux
    student@eg106$ file vmlinux
    vmlinux: ELF 32-bit LSB executable, Intel 80386, ...
    student@eg106$ nm vmlinux | grep sys_call_table
    c02e535c R sys_call_table
    student@eg106$ cat System.map | grep sys_call_table
    c02e535c R sys_call_table

</div>

</div>

The **nm** utility is used to show the symbols in an object or executable file. In our case, `vmlinux` is an ELF file. Alternately, we can use the file `System.map` to view information about the symbols in kernel.

Then we use **gdb** to inspect the symbols using the uncompressed kernel image. A simple **gdb** session is the following:

<div class="highlight-bash">

<div class="highlight">

    student@eg106$ cd ~/src/linux
    stduent@eg106$ gdb --quiet vmlinux
    Using host libthread_db library "/lib/tls/libthread_db.so.1".
    (gdb) x/x 0xc02e535c
    0xc02e535c `<sys_call_table>`:    0xc011bc58
    (gdb) x/16 0xc02e535c
    0xc02e535c `<sys_call_table>`:    0xc011bc58      0xc011482a      0xc01013d3     0xc014363d
    0xc02e536c `<sys_call_table+16>`: 0xc014369f      0xc0142d4e      0xc0142de5     0xc011548b
    0xc02e537c `<sys_call_table+32>`: 0xc0142d7d      0xc01507a1      0xc015042c     0xc0101431
    0xc02e538c `<sys_call_table+48>`: 0xc014249e      0xc0115c6c      0xc014fee7     0xc0142725
    (gdb) x/x sys_call_table
    0xc011bc58 `<sys_restart_syscall>`:       0xffe000ba
    (gdb) x/x &sys_call_table
    0xc02e535c `<sys_call_table>`:    0xc011bc58
    (gdb) x/16 &sys_call_table
    0xc02e535c `<sys_call_table>`:    0xc011bc58      0xc011482a      0xc01013d3     0xc014363d
    0xc02e536c `<sys_call_table+16>`: 0xc014369f      0xc0142d4e      0xc0142de5     0xc011548b
    0xc02e537c `<sys_call_table+32>`: 0xc0142d7d      0xc01507a1      0xc015042c     0xc0101431
    0xc02e538c `<sys_call_table+48>`: 0xc014249e      0xc0115c6c      0xc014fee7     0xc0142725
    (gdb) x/x sys_fork
    0xc01013d3 `<sys_fork>`:  0x3824548b
    (gdb) disass sys_fork
    Dump of assembler code for function sys_fork:
    0xc01013d3 `<sys_fork+0>`:        mov    0x38(%esp),%edx
    0xc01013d7 `<sys_fork+4>`:        mov    $0x11,%eax
    0xc01013dc `<sys_fork+9>`:        push   $0x0
    0xc01013de `<sys_fork+11>`:       push   $0x0
    0xc01013e0 `<sys_fork+13>`:       push   $0x0
    0xc01013e2 `<sys_fork+15>`:       lea    0x10(%esp),%ecx
    0xc01013e6 `<sys_fork+19>`:       call   0xc0111aab `<do_fork>`
    0xc01013eb `<sys_fork+24>`:       add    $0xc,%esp
    0xc01013ee `<sys_fork+27>`:       ret
    End of assembler dump.

</div>

</div>

It can be noticed that the uncompressed kernel image was used as an argument for **gdb**. The image can be found in the root of the kernel sources after compilation.

A few commands used for debugging using **gdb** are:

  - **x** (examine) - Used to show the contents of the memory area whose address is specified as an argument to the command (this address can be the value of a physical address, a symbol or the address of a symbol). It can take as arguments (preceded by `/`): the format to display the data in (`x` for hexadecimal, `d` for decimal, etc.), how many memory units to display and the size of a memory unit.
  - **disassemble** - Used to disassemble a function.
  - **p** (print) - Used to evaluate and show the value of an expression. The format to show the data in can be specified as an argument (`/x` for hexadecimal, `/d` for decimal, etc.).

The analysis of the kernel image is a method of static analysis. If we want to perform dynamic analysis (analyzing how the kernel runs, not only its static image) we can use `/proc/kcore`; this is a dynamic image (in memory) of the kernel.

<div class="highlight-bash">

<div class="highlight">

    student@eg106$ gdb ~/src/linux/vmlinux /proc/kcore
    Core was generated by `root=/dev/hda3 ro'.
    #0  0x00000000 in ?? ()
    (gdb) p sys_call_table
    $1 = -1072579496
    (gdb) p /x sys_call_table
    $2 = 0xc011bc58
    (gdb) p /x &sys_call_table
    $3 = 0xc02e535c
    (gdb) x/16 &sys_call_table
    0xc02e535c `<sys_call_table>`:    0xc011bc58      0xc011482a      0xc01013d3     0xc014363d
    0xc02e536c `<sys_call_table+16>`: 0xc014369f      0xc0142d4e      0xc0142de5     0xc011548b
    0xc02e537c `<sys_call_table+32>`: 0xc0142d7d      0xc01507a1      0xc015042c     0xc0101431
    0xc02e538c `<sys_call_table+48>`: 0xc014249e      0xc0115c6c      0xc014fee7     0xc0142725

</div>

</div>

Using the dynamic image of the kernel is useful for detecting [rootkits](http://en.wikipedia.org/wiki/Rootkit).

  - [Linux Device Drivers 3rd Edition - Debuggers and Related Tools](http://linuxdriver.co.il/ldd3/linuxdrive3-CHP-4-SECT-6.html)
  - [Detecting Rootkits and Kernel-level Compromises in Linux](http://www.securityfocus.com/infocus/1811)
  - [User-Mode Linux](http://user-mode-linux.sf.net/)

</div>

<div id="getting-a-stack-trace" class="section">

### Getting a stack trace[¶](#getting-a-stack-trace "Permalink to this headline")

Sometimes, you will want information about the trace the execution reaches a certain point. You can determine this information using **cscope** or LXR, but some function are called from many execution paths, which makes this method difficult.

In these situations, it is useful to get a stack trace, which can be simply done using the function `dump_stack()`.

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lec12-virtualization.html "SO2 Lecture 12 - Virtualization") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lab2-kernel-api.html "SO2 Lab 02 - Kernel API")

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
