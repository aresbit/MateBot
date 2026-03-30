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
      - [Assignment 1 - Kprobe based tracer](assign1-kprobe-based-tracer.html)
      - [Assignment 2 - Driver UART](#)
          - [Assignment's Objectives](#assignment-s-objectives)
          - [Statement](#statement)
              - [Buffers Scheme](#buffers-scheme)
          - [Implementation Details](#implementation-details)
          - [Testing](#testing)
          - [QuickStart](#quickstart)
              - [Tips](#tips)
              - [Penalties](#penalties)
              - [Submitting the assigment](#submitting-the-assigment)
          - [Resources](#resources)
          - [Questions](#questions)
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
  - Assignment 2 - Driver UART
  - [View page source](../_sources/so2/assign2-driver-uart.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="assignment-2-driver-uart" class="section">

# Assignment 2 - Driver UART[¶](#assignment-2-driver-uart "Permalink to this headline")

  - Deadline: **Monday, 22 April 2024, 23:59**
  - The assigment is individual

<div id="assignment-s-objectives" class="section">

## Assignment's Objectives[¶](#assignment-s-objectives "Permalink to this headline")

  - consolidating the knowledge of device drivers
  - read hardware documentation and track the desired functionality in the documentation
  - work with interrupts; use of non-blocking functions in interrupt context
  - use of buffers; synchronization
  - kernel modules with parameters

</div>

<div id="statement" class="section">

## Statement[¶](#statement "Permalink to this headline")

Write a kernel module that implements a driver for the serial port (UART16550). The device driver must support the two standard serial ports in a PC, COM1 and COM2 (0x3f8 and 0x2f8, in fact the entire range of 8 addresses 0x3f8-0x3ff and 0x2f8-0x2ff specific to the two ports). In addition to the standard routines (open, read, write, close), the driver must also have support for changing communication parameters using an ioctl operation (UART16550\_IOCTL\_SET\_LINE).

The driver must use interrupts for both reception and transmission to reduce latency and CPU usage time. Read and write calls must also be blocking. **Assignments that do not meet these requirements will not be considered.** It is recommended that you use a buffer for the read routine and another buffer for the write routine for each serial port in the driver.

A blocking read call means that the read routine called from the user-space will be blocked until **at least** one byte is read (the read buffer in the kernel is empty and no data can be read). A blocking write call means that the write routine called from the user-space will be blocked until **at least** one byte is written (the write buffer in the kernel is full and no data can be written).

<div id="buffers-scheme" class="section">

### Buffers Scheme[¶](#buffers-scheme "Permalink to this headline")

![../\_images/buffers-scheme.png](../_images/buffers-scheme.png)

Data transfer between the various buffers is a [Producer-Consumer](https://en.wikipedia.org/wiki/Producer%E2%80%93consumer_problem) problem. Example:

  - The process is the producer and the device is the consumer if it is written from the process to the device; the process will block until there is at least one free space in the consumer's buffer
  - The process is the consumer and the device is the producer if it is read from a process from the device; the process will block until there is at least one element in the producer's buffer.

</div>

</div>

<div id="implementation-details" class="section">

## Implementation Details[¶](#implementation-details "Permalink to this headline")

  - the driver will be implemented as a kernel module named **uart16550.ko**
  - the driver will be accessed as a character device driver, with different functions depending on the parameters transmitted to the load module:
      - the major parameter will specify the major with which the device must be registered
      - the option parameter will specify how it works:
          - OPTION\_BOTH: will also register COM1 and COM2, with the major given by the major parameter and the minors 0 (for COM1) and 1 (for COM2);
          - OPTION\_COM1: will only register COM1, with the major major and minor 0;
          - OPTION\_COM2: will only register COM2, with the major major and minor 1;
      - to learn how to pass parameters in Linux, see [tldp](https://tldp.org/LDP/lkmpg/2.6/html/x323.html)
      - the default values are major=42 and option=OPTION\_BOTH.
  - the interrupt number associated with COM1 is 4 (IRQ\_COM1) and the interrupt number associated with COM2 is 3 (IRQ\_COM2)
  - [the header](https://gitlab.cs.pub.ro/so2/2-uart/-/blob/master/src/uart16550.h) with the definitions needed for special operations;
  - a starting point in implementing read / write routines is the [example](https://ocw.cs.pub.ro/courses/so2/laboratoare/lab04?&#sincronizare_-_cozi_de_asteptare) of uppercase / lowercase character device driver; the only difference is that you have to use two buffers, one for read and one for write;
  - you can use [kfifo](https://lwn.net/Articles/347619/) for buffers;
  - you do not have to use deferred functions to read / write data from / to ports (you can do everything from interrupt context);
  - you will need to synchronize the read / write routines with the interrupt handling routine for the routines to be blocking; it is recommended to use [synchronization with waiting queues](https://ocw.cs.pub.ro/courses/so2/laboratoare/lab04?&#sincronizare_-_cozi_de_asteptare)
  - In order for the assigment to work, the default serial driver must be disabled:
      - cat /proc/ioports | grep serial will detect the presence of the default driver on the regions where COM1 and COM2 are defined
      - in order to deactivate it, the kernel must be recompiled, either by setting the serial driver as the module, or by deactivating it completely (this modification is already made on the virtual machine)
          - Device Drivers -\> Character devices -\> Serial driver -\> 8250/16550 and compatible serial support.

</div>

<div id="testing" class="section">

## Testing[¶](#testing "Permalink to this headline")

In order to simplify the assignment evaluation process, but also to reduce the mistakes of the submitted assignments, the assignment evaluation will be done automatically with the help of a [test script](https://gitlab.cs.pub.ro/so2/2-uart/-/blob/master/checker/2-uart-checker/_checker) called \_checker. The test script assumes that the kernel module is called uart16550.ko.

</div>

<div id="quickstart" class="section">

## QuickStart[¶](#quickstart "Permalink to this headline")

It is mandatory to start the implementation of the assignment from the code skeleton found in the [src](https://gitlab.cs.pub.ro/so2/2-uart/-/tree/master/src) directory. There is only one header in the skeleton called [uart16550.h](https://gitlab.cs.pub.ro/so2/2-uart/-/blob/master/src/uart16550.h). You will provide the rest of the implementation. You can add as many \*.c\` sources and additional \*.h\` headers. You should also provide a Kbuild file that will compile the kernel module called uart16550.ko. Follow the instructions in the [README.md file](https://gitlab.cs.pub.ro/so2/2-uart/-/blob/master/README.md) of the [assignment's repo](https://gitlab.cs.pub.ro/so2/2-uart).

<div id="tips" class="section">

### Tips[¶](#tips "Permalink to this headline")

To increase your chances of getting the highest grade, read and follow the Linux kernel coding style described in the [Coding Style document](https://elixir.bootlin.com/linux/v4.19.19/source/Documentation/process/coding-style.rst).

Also, use the following static analysis tools to verify the code:

  - checkpatch.pl

<div class="highlight-console">

<div class="highlight">

    $ linux/scripts/checkpatch.pl --no-tree --terse -f /path/to/your/list.c

</div>

</div>

  - sparse

<div class="highlight-console">

<div class="highlight">

    $ sudo apt-get install sparse
    $ cd linux
    $ make C=2 /path/to/your/list.c

</div>

</div>

  - cppcheck

<div class="highlight-console">

<div class="highlight">

    $ sudo apt-get install cppcheck
    $ cppcheck /path/to/your/list.c

</div>

</div>

</div>

<div id="penalties" class="section">

### Penalties[¶](#penalties "Permalink to this headline")

Information about assigments penalties can be found on the [General Directions page](https://ocw.cs.pub.ro/courses/so2/teme/general).

In exceptional cases (the assigment passes the tests by not complying with the requirements) and if the assigment does not pass all the tests, the grade will may decrease more than mentioned above.

</div>

<div id="submitting-the-assigment" class="section">

### Submitting the assigment[¶](#submitting-the-assigment "Permalink to this headline")

The assignment will be graded automatically using the [vmchecker-next](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Student-Handbook) infrastructure. The submission will be made on moodle on the [course's page](https://curs.upb.ro/2022/course/view.php?id=5121) to the related assignment. You will find the submission details in the [README.md file](https://gitlab.cs.pub.ro/so2/2-uart/-/blob/master/README.md) of the [repo](https://gitlab.cs.pub.ro/so2/2-uart).

</div>

</div>

<div id="resources" class="section">

## Resources[¶](#resources "Permalink to this headline")

  - serial port documentation can be found on [tldp](https://tldp.org/HOWTO/Serial-HOWTO-19.html)
  - [table with registers](http://www.byterunner.com/16550.html)
  - [datasheet 16550](https://pdf1.alldatasheet.com/datasheet-pdf/view/9301/NSC/PC16550D.html)
  - [alternative documentation](https://en.wikibooks.org/wiki/Serial_Programming/8250_UART_Programming)

We recommend that you use gitlab to store your homework. Follow the directions in [README](https://gitlab.cs.pub.ro/so2/2-uart/-/blob/master/README.md).

</div>

<div id="questions" class="section">

## Questions[¶](#questions "Permalink to this headline")

For questions about the topic, you can consult the mailing [list archives](http://cursuri.cs.pub.ro/pipermail/so2/) or you can write a question on the dedicated Teams channel.

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](assign1-kprobe-based-tracer.html "Assignment 1 - Kprobe based tracer") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](assign3-software-raid.html "Assignment 3 - Software RAID")

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
