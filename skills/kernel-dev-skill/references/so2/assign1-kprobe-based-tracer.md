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
      - [Assignment 1 - Kprobe based tracer](#)
          - [Assignment's Objectives](#assignment-s-objectives)
          - [Statement](#statement)
              - [Implementation details](#implementation-details)
          - [Testing](#testing)
          - [QuickStart](#quickstart)
              - [Tips](#tips)
              - [Penalties](#penalties)
              - [Submitting the assigment](#submitting-the-assigment)
          - [Resources](#resources)
          - [Questions](#questions)
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
  - Assignment 1 - Kprobe based tracer
  - [View page source](../_sources/so2/assign1-kprobe-based-tracer.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="assignment-1-kprobe-based-tracer" class="section">

# Assignment 1 - Kprobe based tracer[¶](#assignment-1-kprobe-based-tracer "Permalink to this headline")

  - Deadline: **Monday, 8 April 2024, 23:59**

<div id="assignment-s-objectives" class="section">

## Assignment's Objectives[¶](#assignment-s-objectives "Permalink to this headline")

  - gaining knowledge related to the instrumentation of functions in the Linux kernel (`kretprobes` mechanism)
  - gaining knowledge regarding the `/proc` file system from the Linux kernel
  - get familiar with data structures specific to the Linux kernel (`hash table` and `list`)

</div>

<div id="statement" class="section">

## Statement[¶](#statement "Permalink to this headline")

Build a kernel operations surveillant.

With this surveillant, we aim to intercept:

  - `kmalloc` and `kfree` calls
  - `schedule` calls
  - `up` and `down_interruptible` calls
  - `mutex_lock` and `mutex_unlock` calls

The surveillant will hold, at the process level, the number of calls for each of the above functions. For the `kmalloc` and `kfree` calls the total quantity of allocated and deallocated memory will be shown.

The surveillant will be implemented as a kernel module with the name `tracer.ko`.

<div id="implementation-details" class="section">

### Implementation details[¶](#implementation-details "Permalink to this headline")

The interception will be done by recording a sample (`kretprobe`) for each of the above functions. The surveillant will retain a list/hashtable with the monitored processes and will account for the above information for these processes.

For the control of the list/hashtable with the monitored processes, a char device called `/dev/tracer` will be used, with major 10 and minor 42. It will expose an `ioctl` interface with two arguments:

  - the first argument is the request to the monitoring subsystem:
    
    > 
    > 
    > <div>
    > 
    >   - `TRACER_ADD_PROCESS`
    >   - `TRACER_REMOVE_PROCESS`
    > 
    > </div>

  - the second argument is the PID of the process for which the monitoring request will be executed

In order to create a char device with major 10 you will need to use the [miscdevice](https://elixir.bootlin.com/linux/latest/source/include/linux/miscdevice.h) interface in the kernel. Definitions of related macros can be found in the [tracer.h header](https://gitlab.cs.pub.ro/so2/1-tracer/-/blob/master/src/tracer.h).

Since the `kmalloc` function is inline for instrumenting the allocated amount of memory, the `__kmalloc` function will be inspected as follows:

  - a `kretprobe` will be used, which will retain the amount of memory allocated and the address of the allocated memory area.
  - the `.entry_handler` and `.handler` fields in the `kretprobe` structure will be used to retain information about the amount of memory allocated and the address from which the allocated memory starts.

<div class="highlight-C">

<div class="highlight">

    static struct kretprobe kmalloc_probe = {
       .entry_handler = kmalloc_probe_entry_handler, /* entry handler */
       .handler = kmalloc_probe_handler, /* return probe handler */
       .maxactive = 32,
    };

</div>

</div>

Since the `kfree` function only receives the address of the memory area to be freed, in order to determine the total amount of memory freed, we will need to determine its size based on the address of the area. This is possible because there is an address-size association made when inspecting the `__kmalloc` function.

For the rest of the instrumentation functions it is enough to use a `kretprobe`.

<div class="highlight-C">

<div class="highlight">

    static struct kretprobe up_probe = {
       .entry_handler = up_probe_handler,
       .maxactive = 32,
    };

</div>

</div>

The virtual machine kernel has the `CONFIG_DEBUG_LOCK_ALLOC` option enabled where the `mutex_lock` symbol is a macro that expands to `mutex_lock_nested`. Thus, in order to obtain information about the `mutex_lock` function you will have to instrument the `mutex_lock_nested` function.

Processes that have been added to the list/hashtable and that end their execution will be removed from the list/hashtable. Also, a process will be removed from the dispatch list/hashtable following the `TRACER_REMOVE_PROCESS` operation.

The information retained by the surveillant will be displayed via the procfs file system, in the `/proc/tracer` file. For each monitored process an entry is created in the `/proc/tracer` file having as first field the process PID. The entry will be read-only, and a read operation on it will display the retained results. An example of displaying the contents of the entry is:

<div class="highlight-console">

<div class="highlight">

    $cat /proc/tracer
    PID   kmalloc kfree kmalloc_mem kfree_mem  sched   up     down  lock   unlock
    42    12      12    2048        2048        124    2      2     9      9
    1099  0       0     0           0           1984   0      0     0      0
    1244  0       0     0           0           1221   100   1023   1023   1002
    1337  123     99    125952      101376      193821 992   81921  7421   6392

</div>

</div>

</div>

</div>

<div id="testing" class="section">

## Testing[¶](#testing "Permalink to this headline")

In order to simplify the assignment evaluation process, but also to reduce the mistakes of the submitted assignments, the assignment evaluation will be done automatically with the help of a [test script](https://github.com/linux-kernel-labs/linux/blob/master/tools/labs/templates/assignments/1-tracer/checker/_checker) called \_checker. The test script assumes that the kernel module is called tracer.ko.

</div>

<div id="quickstart" class="section">

## QuickStart[¶](#quickstart "Permalink to this headline")

It is mandatory to start the implementation of the assignment from the code skeleton found in the [src](https://gitlab.cs.pub.ro/so2/1-tracer/-/tree/master/src) directory. There is only one header in the skeleton called [tracer.h](https://gitlab.cs.pub.ro/so2/1-tracer/-/blob/master/src/tracer.h). You will provide the rest of the implementation. You can add as many \*.c\` sources and additional \*.h\` headers. You should also provide a Kbuild file that will compile the kernel module called tracer.ko. Follow the instructions in the [README.md file](https://gitlab.cs.pub.ro/so2/1-tracer/-/blob/master/README.md) of the [assignment's repo](https://gitlab.cs.pub.ro/so2/1-tracer).

<div id="tips" class="section">

### Tips[¶](#tips "Permalink to this headline")

To increase your chances of getting the highest grade, read and follow the Linux kernel coding style described in the [Coding Style document](https://elixir.bootlin.com/linux/v4.19.19/source/Documentation/process/coding-style.rst).

Also, use the following static analysis tools to verify the code:

  - checkpatch.pl

<div class="highlight-console">

<div class="highlight">

    $ linux/scripts/checkpatch.pl --no-tree --terse -f /path/to/your/tracer.c

</div>

</div>

  - sparse

<div class="highlight-console">

<div class="highlight">

    $ sudo apt-get install sparse
    $ cd linux
    $ make C=2 /path/to/your/tracer.c

</div>

</div>

  - cppcheck

<div class="highlight-console">

<div class="highlight">

    $ sudo apt-get install cppcheck
    $ cppcheck /path/to/your/tracer.c

</div>

</div>

</div>

<div id="penalties" class="section">

### Penalties[¶](#penalties "Permalink to this headline")

Information about assigments penalties can be found on the [General Directions page](https://ocw.cs.pub.ro/courses/so2/teme/general). In addition, the following elements will be taken into account:

  - *-2*: missing of proper disposal of resources (`kretprobes`, entries in `/proc`)
  - *-2*: data synchronization issues for data used by multiple executing instances (e.g. the list/hashtable)

In exceptional cases (the assigment passes the tests but it is not complying with the requirements) and if the assigment does not pass all the tests, the grade may decrease more than mentioned above.

</div>

<div id="submitting-the-assigment" class="section">

### Submitting the assigment[¶](#submitting-the-assigment "Permalink to this headline")

The assignment will be graded automatically using the [vmchecker-next](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Student-Handbook) infrastructure. The submission will be made on moodle on the [course's page](https://curs.upb.ro/2022/course/view.php?id=5121) to the related assignment. You will find the submission details in the [README.md file](https://gitlab.cs.pub.ro/so2/1-tracer/-/blob/master/README.md) of the [repo](https://gitlab.cs.pub.ro/so2/1-tracer).

</div>

</div>

<div id="resources" class="section">

## Resources[¶](#resources "Permalink to this headline")

  - [Documentation/kprobes.txt](https://www.kernel.org/doc/Documentation/kprobes.txt) - description of the `kprobes` subsystem from Linux kernel sources.
  - [samples/kprobes/](https://elixir.bootlin.com/linux/latest/source/samples/kprobes) - some examples of using `kprobes` from Linux kernel sources.

We recommend that you use gitlab to store your homework. Follow the directions in [README](https://gitlab.cs.pub.ro/so2/1-tracer/-/blob/master/README.md).

</div>

<div id="questions" class="section">

## Questions[¶](#questions "Permalink to this headline")

For questions about the topic, you can consult the mailing [list archives](http://cursuri.cs.pub.ro/pipermail/so2/) or you can write a question on the dedicated Teams channel.

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](assign0-kernel-api.html "Assignment 0 - Kernel API") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](assign2-driver-uart.html "Assignment 2 - Driver UART")

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
