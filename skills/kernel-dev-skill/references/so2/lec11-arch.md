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
      - [SO2 Lecture 11 - Architecture Layer](#)
          - [Lecture objectives:](#lecture-objectives)
          - [Overview of the arch layer](#overview-of-the-arch-layer)
              - [Boot strap](#boot-strap)
              - [Boot strap](#boot-strap-1)
              - [Memory setup](#memory-setup)
              - [MMU management](#mmu-management)
              - [Thread Management](#thread-management)
              - [Time Management](#time-management)
              - [IRQs and exception management](#irqs-and-exception-management)
              - [System calls](#system-calls)
              - [Platform Drivers](#platform-drivers)
              - [Machine specific code](#machine-specific-code)
          - [Overview of the boot process](#overview-of-the-boot-process)
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
  - SO2 Lecture 11 - Architecture Layer
  - [View page source](../_sources/so2/lec11-arch.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lecture-11-architecture-layer" class="section">

# SO2 Lecture 11 - Architecture Layer[¶](#so2-lecture-11-architecture-layer "Permalink to this headline")

[View slides](lec11-arch-slides.html)

<span class="admonition-so2-lecture-11-architecture-layer"></span>

<div id="lecture-objectives" class="section">

## Lecture objectives:[¶](#lecture-objectives "Permalink to this headline")

  - Overview of the arch layer
  - Overview of the boot process

</div>

<div id="overview-of-the-arch-layer" class="section">

## Overview of the arch layer[¶](#overview-of-the-arch-layer "Permalink to this headline")

[![../\_images/ditaa-ae895f3a8e26b92bf6c6ecbbd71e2c88912d5607.png](../_images/ditaa-ae895f3a8e26b92bf6c6ecbbd71e2c88912d5607.png)](../_images/ditaa-ae895f3a8e26b92bf6c6ecbbd71e2c88912d5607.png)

<div id="boot-strap" class="section">

### Boot strap[¶](#boot-strap "Permalink to this headline")

  - The first kernel code that runs
  - Typically runs with the MMU disabled
  - Move / Relocate kernel code

</div>

<div id="boot-strap-1" class="section">

### Boot strap[¶](#boot-strap-1 "Permalink to this headline")

  - The first kernel code that runs
  - Typically runs with the MMU disabled
  - Copy bootloader arguments and determine kernel run location
  - Move / relocate kernel code to final location
  - Initial MMU setup - map the kernel

</div>

<div id="memory-setup" class="section">

### Memory setup[¶](#memory-setup "Permalink to this headline")

  - Determine available memory and setup the boot memory allocator
  - Manages memory regions before the page allocator is setup
  - Bootmem - used a bitmap to track free blocks
  - Memblock - deprecates bootmem and adds support for memory ranges
      - Supports both physical and virtual addresses
      - support NUMA architectures

</div>

<div id="mmu-management" class="section">

### MMU management[¶](#mmu-management "Permalink to this headline")

  - Implements the generic page table manipulation APIs: types, accessors, flags
  - Implement TLB management APIs: flush, invalidate

</div>

<div id="thread-management" class="section">

### Thread Management[¶](#thread-management "Permalink to this headline")

  - Defines the thread type (struct thread\_info) and implements functions for allocating threads (if needed)
  - Implement `copy_thread()` and `switch_context()`

</div>

<div id="time-management" class="section">

### Time Management[¶](#time-management "Permalink to this headline")

  - Setup the timer tick and provide a time source
  - Mostly transitioned to platform drivers
      - clock\_event\_device - for scheduling timers
      - clocksource - for reading the time

</div>

<div id="irqs-and-exception-management" class="section">

### IRQs and exception management[¶](#irqs-and-exception-management "Permalink to this headline")

  - Define interrupt and exception handlers / entry points
  - Setup priorities
  - Platform drivers for interrupt controllers

</div>

<div id="system-calls" class="section">

### System calls[¶](#system-calls "Permalink to this headline")

  - Define system call entry point(s)
  - Implement user-space access primitives (e.g. copy\_to\_user)

</div>

<div id="platform-drivers" class="section">

### Platform Drivers[¶](#platform-drivers "Permalink to this headline")

  - Platform and architecture specific drivers
  - Bindings to platform device enumeration methods (e.g. device tree or ACPI)

</div>

<div id="machine-specific-code" class="section">

### Machine specific code[¶](#machine-specific-code "Permalink to this headline")

  - Some architectures use a "machine" / "platform" abstraction
  - Typical for architecture used in embedded systems with a lot of variety (e.g. ARM, powerPC)

</div>

</div>

<div id="overview-of-the-boot-process" class="section">

## Overview of the boot process[¶](#overview-of-the-boot-process "Permalink to this headline")

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lec10-networking.html "SO2 Lecture 10 - Networking") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lec12-virtualization.html "SO2 Lecture 12 - Virtualization")

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
