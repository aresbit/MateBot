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

  - [Operating Systems 2](#)
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
  - Operating Systems 2
  - [View page source](../_sources/so2/index.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="operating-systems-2" class="section">

# Operating Systems 2[¶](#operating-systems-2 "Permalink to this headline")

<div class="toctree-wrapper compound">

<span class="caption-text">Good To Know</span>

  - [SO2 - General Rules and Grading](grading.html)

</div>

<div class="toctree-wrapper compound">

<span class="caption-text">Lectures</span>

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

</div>

<div class="toctree-wrapper compound">

<span class="caption-text">Labs</span>

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

</div>

<div class="toctree-wrapper compound">

<span class="caption-text">Assignments</span>

  - [Collaboration](assign-collaboration.html)
  - [Assignment 0 - Kernel API](assign0-kernel-api.html)
  - [Assignment 1 - Kprobe based tracer](assign1-kprobe-based-tracer.html)
  - [Assignment 2 - Driver UART](assign2-driver-uart.html)
  - [Assignment 3 - Software RAID](assign3-software-raid.html)
  - [Assignment 4 - SO2 Transport Protocol](assign4-transport-protocol.html)
  - [Assignment 7 - SO2 Virtual Machine Manager with KVM](assign7-kvm-vmm.html)

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](../index.html "Linux Kernel Teaching") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](grading.html "SO2 - General Rules and Grading")

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
