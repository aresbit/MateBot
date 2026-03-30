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
      - [Assignment 0 - Kernel API](#)
          - [Assignment's Objectives](#assignment-s-objectives)
          - [Statement](#statement)
          - [Testing](#testing)
          - [QuickStart](#quickstart)
              - [Tips](#tips)
              - [Penalties](#penalties)
              - [Submitting the assigment](#submitting-the-assigment)
          - [Resources](#resources)
          - [Questions](#questions)
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
  - Assignment 0 - Kernel API
  - [View page source](../_sources/so2/assign0-kernel-api.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="assignment-0-kernel-api" class="section">

# Assignment 0 - Kernel API[¶](#assignment-0-kernel-api "Permalink to this headline")

  - Deadline: **Monday, 25 March 2024, 23:59**

<div id="assignment-s-objectives" class="section">

## Assignment's Objectives[¶](#assignment-s-objectives "Permalink to this headline")

  - getting familiar with the qemu setup
  - loading/unloading kernel modules
  - getting familiar with the list API implemented in the kernel
  - have fun :)

</div>

<div id="statement" class="section">

## Statement[¶](#statement "Permalink to this headline")

Write a kernel module called list (the resulting file must be called list.ko) which stores data (strings) in an internal list.

It is mandatory to use [the list API](https://github.com/torvalds/linux/blob/master/include/linux/list.h) implemented in the kernel. For details you can take a look at [the laboratory 2](https://linux-kernel-labs.github.io/refs/heads/master/so2/lab2-kernel-api.html).

The module exports a directory named **list** to procfs. The directory contains two files:

  - **management**: with write-only access; is the interface for transmitting commands to the kernel module
  - **preview**: with read-only access; is the interface through which the internal contents of the kernel list can be viewed.

[The code skeleton](https://github.com/linux-kernel-labs/linux/blob/master/tools/labs/templates/assignments/0-list/list.c) implements the two procfs files. You will need to create a list and implement support for adding and reading data. Follow the TODOs in the code for details.

To interact with the kernel list, you must write commands (using the echo command) in the /proc/list/management file:

  - addf name: adds the name element to the top of the list
  - adde name: adds the name element to the end of the list
  - delf name: deletes the first appearance of the name item from the list
  - dela name: deletes all occurrences of the name element in the list

Viewing the contents of the list is done by viewing the contents of the /proc/list/preview file (use the\` cat\` command). The format contains one element on each line.

</div>

<div id="testing" class="section">

## Testing[¶](#testing "Permalink to this headline")

In order to simplify the assignment evaluation process, but also to reduce the mistakes of the submitted assignments, the assignment evaluation will be done automatically with the help of a [test script](https://github.com/linux-kernel-labs/linux/blob/master/tools/labs/templates/assignments/0-list/checker/_checker) called \_checker. The test script assumes that the kernel module is called list.ko.

</div>

<div id="quickstart" class="section">

## QuickStart[¶](#quickstart "Permalink to this headline")

It is mandatory to start the implementation of the assignment from the code skeleton found in the [list.c](https://gitlab.cs.pub.ro/so2/0-list/-/blob/master/src/list.c) file. You should follow the instructions in the [README.md file](https://gitlab.cs.pub.ro/so2/0-list/-/blob/master/README.md) of the [assignment's repo](https://gitlab.cs.pub.ro/so2/0-list).

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

The assignment will be graded automatically using the [vmchecker-next](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Student-Handbook) infrastructure. The submission will be made on moodle on the [course's page](https://curs.upb.ro/2022/course/view.php?id=5121) to the related assignment. You will find the submission details in the [README.md file](https://gitlab.cs.pub.ro/so2/0-list/-/blob/master/README.md) of the [repo](https://gitlab.cs.pub.ro/so2/0-list/-/blob/master).

</div>

</div>

<div id="resources" class="section">

## Resources[¶](#resources "Permalink to this headline")

We recommend that you use gitlab to store your homework. Follow the directions in [README.md file](https://gitlab.cs.pub.ro/so2/0-list/-/blob/master/README.md).

</div>

<div id="questions" class="section">

## Questions[¶](#questions "Permalink to this headline")

For questions about the topic, you can consult the mailing [list archives](http://cursuri.cs.pub.ro/pipermail/so2/) or you can write a question on the dedicated Teams channel.

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](assign-collaboration.html "Collaboration") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](assign1-kprobe-based-tracer.html "Assignment 1 - Kprobe based tracer")

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
