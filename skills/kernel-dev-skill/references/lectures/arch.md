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

  - [Operating Systems 2](../so2/index.html)

<span class="caption-text">Lectures</span>

  - [Introduction](intro.html)
  - [System Calls](syscalls.html)
  - [Processes](processes.html)
  - [Interrupts](interrupts.html)
  - [Symmetric Multi-Processing](smp.html)
  - [Address Space](address-space.html)
  - [Memory Management](memory-management.html)
  - [Filesystem Management](fs.html)
  - [Debugging](debugging.html)
  - [Network Management](networking.html)
  - [Architecture Layer](#)
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
  - [Virtualization](virt.html)

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
  - Architecture Layer
  - [View page source](../_sources/lectures/arch.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="architecture-layer" class="section">

# Architecture Layer[¶](#architecture-layer "Permalink to this headline")

[View slides](arch-slides.html)

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

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](networking.html "Network Management") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](virt.html "Virtualization")

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
