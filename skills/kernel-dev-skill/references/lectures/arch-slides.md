<div id="slide_container" class="section slides layout-regular">

## Introduction

  - Overview of the arch layer
  - Overview of the boot process

## Overview of the arch layer

[![../\_images/ditaa-ae895f3a8e26b92bf6c6ecbbd71e2c88912d5607.png](../_images/ditaa-ae895f3a8e26b92bf6c6ecbbd71e2c88912d5607.png)](../_images/ditaa-ae895f3a8e26b92bf6c6ecbbd71e2c88912d5607.png)

## Bootstrap

  - The first kernel code that runs
  - Typically runs with the MMU disabled
  - Move / Relocate kernel code

## Bootstrap

  - The first kernel code that runs
  - Typically runs with the MMU disabled
  - Copy bootloader arguments and determine kernel run location
  - Move / relocate kernel code to final location
  - Initial MMU setup - map the kernel

## Memory Setup

  - Determine available memory and setup the boot memory allocator
  - Manages memory regions before the page allocator is setup
  - Bootmem - used a bitmap to track free blocks
  - Memblock - deprecates bootmem and adds support for memory ranges
      - Supports both physical and virtual addresses
      - support NUMA architectures

## MMU management

  - Implements the generic page table manipulation APIs: types, accessors, flags
  - Implement TLB management APIs: flush, invalidate

## Thread Management

  - Defines the thread type (struct thread\_info) and implements functions for allocating threads (if needed)
  - Implement `copy_thread()` and `switch_context()`

## Timer Management

  - Setup the timer tick and provide a time source
  - Mostly transitioned to platform drivers
      - clock\_event\_device - for scheduling timers
      - clocksource - for reading the time

## IRQs and exception management

  - Define interrupt and exception handlers / entry points
  - Setup priorities
  - Platform drivers for interrupt controllers

## System calls

  - Define system call entry point(s)
  - Implement user-space access primitives (e.g. copy\_to\_user)

## Platform Drivers

  - Platform and architecture specific drivers
  - Bindings to platform device enumeration methods (e.g. device tree or ACPI)

## Machine specific code

  - Some architectures use a "machine" / "platform" abstraction
  - Typical for architecture used in embedded systems with a lot of variety (e.g. ARM, powerPC)

## Boot flow inspection

</div>

<div id="slide_notes" class="section">

</div>
