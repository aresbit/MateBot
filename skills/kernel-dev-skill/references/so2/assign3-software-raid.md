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
      - [Assignment 2 - Driver UART](assign2-driver-uart.html)
      - [Assignment 3 - Software RAID](#)
          - [Assignment's Objectives](#assignment-s-objectives)
          - [Statement](#statement)
              - [Important to know](#important-to-know)
          - [Implementation Details](#implementation-details)
          - [Testing](#testing)
          - [QuickStart](#quickstart)
              - [Tips](#tips)
              - [Penalties](#penalties)
              - [Submitting the assigment](#submitting-the-assigment)
          - [Resources](#resources)
          - [Questions](#questions)
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
  - Assignment 3 - Software RAID
  - [View page source](../_sources/so2/assign3-software-raid.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="assignment-3-software-raid" class="section">

# Assignment 3 - Software RAID[¶](#assignment-3-software-raid "Permalink to this headline")

  - Deadline: **Thursday, 16 May 2024, 23:59**

Implementing a software RAID module that uses a logical block device that will read and write data from two physical devices, ensuring the consistency and synchronization of data from the two physical devices. The type of RAID implemented will be similar to a RAID 1.

<div id="assignment-s-objectives" class="section">

## Assignment's Objectives[¶](#assignment-s-objectives "Permalink to this headline")

  - in-depth understanding of how the I/O subsystem works.
  - acquire advanced skills working with bio structures.
  - work with the block / disk devices in the Linux kernel.
  - acquire skills to navigate and understand the code and API dedicated to the I/O subsystem in Linux.

</div>

<div id="statement" class="section">

## Statement[¶](#statement "Permalink to this headline")

Write a kernel module that implements the RAID software functionality. [Software RAID](https://en.wikipedia.org/wiki/RAID#Software-based_RAID) provides an abstraction between the logical device and the physical devices. The implementation will use [RAID scheme 1](https://en.wikipedia.org/wiki/RAID#Standard_levels).

The virtual machine has two hard disks that will represent the physical devices: /dev/vdb and /dev/vdc. The operating system will provide a logical device (block type) that will interface the access from the user space. Writing requests to the logical device will result in two writes, one for each hard disk. Hard disks are not partitioned. It will be considered that each hard disk has a single partition that covers the entire disk.

Each partition will store a sector along with an associated checksum (CRC32) to ensure error recovery. At each reading, the related information from both partitions is read. If a sector of the first partition has corrupt data (CRC value is wrong) then the sector on the second partition will be read; at the same time the sector of the first partition will be corrected. Similar in the case of a reading of a corrupt sector on the second partition. If a sector has incorrect CRC values on both partitions, an appropriate error code will be returned.

<div id="important-to-know" class="section">

### Important to know[¶](#important-to-know "Permalink to this headline")

To ensure error recovery, a CRC code is associated with each sector. CRC codes are stored by LOGICAL\_DISK\_SIZE byte of the partition (macro defined in the assignment [header](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/src/ssr.h)). The disk structure will have the following layout:

<div class="highlight-console">

<div class="highlight">

    +-----------+-----------+-----------+     +---+---+---+
    |  sector1  |  sector2  |  sector3  |.....|C1 |C2 |C3 |
    +-----------+-----------+-----------+     +---+---+---+

</div>

</div>

where `C1`, `C2`, `C3` are the values CRC sectors `sector1`, `sector2`, `sector3`. The CRC area is found immediately after the `LOGICAL_DISK_SIZE` bytes of the partition.

As a seed for CRC use 0(zero).

</div>

</div>

<div id="implementation-details" class="section">

## Implementation Details[¶](#implementation-details "Permalink to this headline")

  - the kernel module will be named `ssr.ko`
  - the logical device will be accessed as a block device with the major `SSR_MAJOR` and minor `SSR_FIRST_MINOR` under the name `/dev/ssr` (via the macro `LOGICAL_DISK_NAME`)
  - the virtual device (`LOGICAL_DISK_NAME` - `/dev/ssr`) will have the capacity of `LOGICAL_DISK_SECTORS` (use `set_capacity` with the `struct gendisk` structure)
  - the two disks are represented by the devices `/dev/vdb`, respectively `/dev/vdc`, defined by means of macros `PHYSICAL_DISK1_NAME`, respectively `PHYSICAL_DISK2_NAME`
  - to work with the `struct block _device` structure associated with a physical device, you can use the `blkdev_get_by_path` and `blkdev_put` functions
  - for the handling of requests from the user space, we recommend not to use a `request_queue`, but to do processing at `struct bio` level using the `submit_bio` field of `struct block_device_operations`
  - since data sectors are separated from CRC sectors you will have to build separate `bio` structures for data and CRC values
  - to allocate a `struct bio` for physical disks you can use `bio_alloc()`; to add data pages to bio use `alloc_page()` and `bio_add_page()`
  - to free up the space allocated for a `struct bio` you need to release the pages allocated to the bio (using the `__free_page()` macro ) and call `bio_put()`
  - when generating a `struct bio` structure, consider that its size must be multiple of the disk sector size (`KERNEL_SECTOR_SIZE`)
  - to send a request to a block device and wait for it to end, you can use the `submit_bio_wait()` function
  - use `bio_endio()` to signal the completion of processing a `bio` structure
  - for the CRC32 calculation you can use the `crc32()` macro provided by the kernel
  - useful macro definitions can be found in the assignment support [header](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/src/ssr.h)
  - a single request processing function for block devices can be active at one time in a call stack (more details [here](https://elixir.bootlin.com/linux/v5.10/source/block/blk-core.c#L1048)). You will need to submit requests for physical devices in a kernel thread; we recommend using `workqueues`.
  - For a quick run, use a single bio to batch send the read/write request for CRC values for adjacent sectors. For example, if you need to send requests for CRCs in sectors 0, 1, ..., 7, use a single bio, not 8 bios.
  - our recommendations are not mandatory (any solution that meets the requirements of the assignment is accepted)

</div>

<div id="testing" class="section">

## Testing[¶](#testing "Permalink to this headline")

In order to simplify the assignment evaluation process, but also to reduce the mistakes of the submitted assignments, the assignment evaluation will be done automatically with the help of a [test script](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/checker/3-raid-checker/_checker) called \_checker. The test script assumes that the kernel module is called ssr.ko.

If, as a result of the testing process, the sectors on both disks contain invalid data, resulting in read errors that make the module impossible to use, you will need to redo the two disks in the virtual machine using the commands:

<div class="highlight-console">

<div class="highlight">

    $ dd if=/dev/zero of=/dev/vdb bs=1M
    $ dd if=/dev/zero of=/dev/vdc bs=1M

</div>

</div>

You can also get the same result using the following command to start the virtual machine:

<div class="highlight-console">

<div class="highlight">

    $ rm disk{1,2}.img; make console # or rm disk{1,2}.img; make boot

</div>

</div>

</div>

<div id="quickstart" class="section">

## QuickStart[¶](#quickstart "Permalink to this headline")

It is mandatory to start the implementation of the assignment from the code skeleton found in the [src](https://gitlab.cs.pub.ro/so2/3-raid/-/tree/master/src) directory. There is only one header in the skeleton called [ssr.h](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/src/ssr.h). You will provide the rest of the implementation. You can add as many \*.c\` sources and additional \*.h\` headers. You should also provide a Kbuild file that will compile the kernel module called ssr.ko. Follow the instructions in the [README.md file](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/README.md) of the [assignment's repo](https://gitlab.cs.pub.ro/so2/3-raid).

<div id="tips" class="section">

### Tips[¶](#tips "Permalink to this headline")

To increase your chances of getting the highest grade, read and follow the Linux kernel coding style described in the [Coding Style document](https://elixir.bootlin.com/linux/v4.19.19/source/Documentation/process/coding-style.rst).

Also, use the following static analysis tools to verify the code:

  - checkpatch.pl

<div class="highlight-console">

<div class="highlight">

    $ linux/scripts/checkpatch.pl --no-tree --terse -f /path/to/your/file.c

</div>

</div>

  - sparse

<div class="highlight-console">

<div class="highlight">

    $ sudo apt-get install sparse
    $ cd linux
    $ make C=2 /path/to/your/file.c

</div>

</div>

  - cppcheck

<div class="highlight-console">

<div class="highlight">

    $ sudo apt-get install cppcheck
    $ cppcheck /path/to/your/file.c

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

The assignment will be graded automatically using the [vmchecker-next](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Student-Handbook) infrastructure. The submission will be made on moodle on the [course's page](https://curs.upb.ro/2022/course/view.php?id=5121) to the related assignment. You will find the submission details in the [README.md file](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/README.md) of the [repo](https://gitlab.cs.pub.ro/so2/3-raid).

</div>

</div>

<div id="resources" class="section">

## Resources[¶](#resources "Permalink to this headline")

  - implementation of the [RAID](https://elixir.bootlin.com/linux/v5.10/source/drivers/md) software in the Linux kernel

We recommend that you use gitlab to store your homework. Follow the directions in [README](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/README.md).

</div>

<div id="questions" class="section">

## Questions[¶](#questions "Permalink to this headline")

For questions about the topic, you can consult the mailing [list archives](http://cursuri.cs.pub.ro/pipermail/so2/) or you can write a question on the dedicated Teams channel.

Before you ask a question, make sure that:

> 
> 
> <div>
> 
>   - you have read the statement of the assigment well
>   - the question is not already presented on the [FAQ page](https://ocw.cs.pub.ro/courses/so2/teme/tema2/faq)
>   - the answer cannot be found in the [mailing list archives](http://cursuri.cs.pub.ro/pipermail/so2/)
> 
> </div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](assign2-driver-uart.html "Assignment 2 - Driver UART") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](assign4-transport-protocol.html "Assignment 4 - SO2 Transport Protocol")

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
