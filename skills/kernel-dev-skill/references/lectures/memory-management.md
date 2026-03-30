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
  - [Memory Management](#)
      - [Lecture objectives:](#lecture-objectives)
      - [Physical Memory Management](#physical-memory-management)
          - [Memory zones](#memory-zones)
          - [Non-Uniform Memory Access](#non-uniform-memory-access)
          - [Page allocation](#page-allocation)
          - [Small allocations](#small-allocations)
      - [Virtual memory management](#virtual-memory-management)
      - [Fault page handling](#fault-page-handling)
  - [Filesystem Management](fs.html)
  - [Debugging](debugging.html)
  - [Network Management](networking.html)
  - [Architecture Layer](arch.html)
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
  - Memory Management
  - [View page source](../_sources/lectures/memory-management.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="memory-management" class="section">

# Memory Management[¶](#memory-management "Permalink to this headline")

[View slides](memory-management-slides.html)

<div id="lecture-objectives" class="section">

## Lecture objectives:[¶](#lecture-objectives "Permalink to this headline")

  - Physical Memory Management
      - Page allocations
      - Small allocations
  - Virtual Memory Management
  - Page Fault Handling Overview

</div>

<div id="physical-memory-management" class="section">

## Physical Memory Management[¶](#physical-memory-management "Permalink to this headline")

  - Algorithms and data structure that keep track of physical memory pages
  - Independent of virtual memory management
  - Both virtual and physical memory management is required for complete memory management
  - Physical pages are being tracked using a special data structure: `struct page`
  - All physical pages have an entry reserved in the `mem_map` vector
  - The physical page status may include: a counter for how many times is a page used, position in swap or file, buffers for this page, position int the page cache, etc.

<div id="memory-zones" class="section">

### Memory zones[¶](#memory-zones "Permalink to this headline")

  - DMA zone
  - DMA32 zone
  - Normal zone (LowMem)
  - HighMem Zone
  - Movable Zone

</div>

<div id="non-uniform-memory-access" class="section">

### Non-Uniform Memory Access[¶](#non-uniform-memory-access "Permalink to this headline")

  - Physical memory is split in between multiple nodes, one for each CPU
  - There is single physical address space accessible from every node
  - Access to the local memory is faster
  - Each node maintains is own memory zones (.e. DMA, NORMAL, HIGHMEM, etc.)

</div>

<div id="page-allocation" class="section">

### Page allocation[¶](#page-allocation "Permalink to this headline")

<div class="admonition-page-allocation highlight-c">

<div class="highlight">

    /* Allocates 2^order contiguous pages and returns a pointer to the
     * descriptor for the first page
     */
    struct page *alloc_pages(gfp_mask, order);
    
    /* allocates a single page */
    struct page *alloc_page(gfp_mask);
    
    
    /* helper functions that return the kernel virtual address */
    void *__get_free_pages(gfp_mask, order);
    void *__get_free_page(gfp_mask);
    void *__get_zero_page(gfp_mask);
    void *__get_dma_pages(gfp_mask, order);

</div>

</div>

  - Typical memory allocation algorithms have linear complexity
  - Why not use paging?
      - Sometime we do need contiguous memory allocations (for DMA)
      - Allocation would require page table changes and TLB flushes
      - Not able to use extended pages
      - Some architecture directly (in hardware) linearly maps a part of the address space (e.g. MIPS)

<!-- end list -->

  - Free blocks are distributed in multiple lists
  - Each list contains blocks of the same size
  - The block size is a power of two

<!-- end list -->

  - If there is a free block in the N-size list, pick the first
  - If not, look for a free block in the 2N-size list
  - Split the 2N-size block in two N-size blocks and add them to the N-size list
  - Now that we have the N-size list populated, pick the first free block from that list

<!-- end list -->

  - If the "buddy" is free coalesce into a 2N-size block
  - Try until no more free buddy block is found and place the resulting block in the respective list

<!-- end list -->

  - 11 lists for blocks of 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024 pages
  - Each memory zone has its own buddy allocator
  - Each zone has a vector of descriptors for free blocks, one entry for each size
  - The descriptor contains the number of free blocks and the head of the list
  - Blocks are linked in the list using the lru field of `struct page`
  - Free pages have the PG\_buddy flag set
  - The page descriptor keeps a copy of the block size in the private field to easily check if the "buddy" is free

</div>

<div id="small-allocations" class="section">

### Small allocations[¶](#small-allocations "Permalink to this headline")

  - Buddy is used to allocate pages
  - Many of the kernel subsystems need to allocate buffers smaller than a page
  - Typical solution: variable size buffer allocation
      - Leads to external fragmentation
  - Alternative solution: fixed size buffer allocation
      - Leads to internal fragmentation
  - Compromise: fixed size block allocation with multiple sizes, geometrically distributed
      - e.g.: 32, 64, ..., 131056

<!-- end list -->

  - Buffers = objects
  - Uses buddy to allocate a pool of pages for object allocations
  - Each object (optionally) has a constructor and destructor
  - Deallocated objects are cached - avoids subsequent calls for constructors and buddy allocation / deallocation

<!-- end list -->

  - The kernel will typically allocate and deallocate multiple types the same data structures over time (e.g. `struct task_struct`) effectively using fixed size allocations. Using the SLAB reduces the frequency of the more heavy allocation/deallocation operations.
  - For variable size buffers (which occurs less frequently) a geometric distribution of caches with fixed-size can be used
  - Reduces the memory allocation foot-print since we are searching a much smaller memory area, compared to buddy which can span over a larger area
  - Employs cache optimization techniques (slab coloring)

![../\_images/slab-overview.png](../_images/slab-overview.png)

  - A name to identify the cache for stats
  - object constructor and destructor functions
  - size of the objects
  - Flags
  - Size of the slab in power of 2 pages
  - GFP masks
  - One or mores slabs, grouped by state: full, partially full, empty

<!-- end list -->

  - Number of objects
  - Memory region where the objects are stored
  - Pointer to the first free object
  - Descriptor are stored either in
      - the SLAB itself (if the object size is lower the 512 or if internal fragmentation leaves enough space for the SLAB descriptor)
      - in generic caches internally used by the SLAB allocator

![../\_images/slab-detailed-arch.png](../_images/slab-detailed-arch.png)

  - Generic caches are used internally by the slab allocator
      - allocating memory for cache and slab descriptors
  - They are also used to implement `kmalloc()` by implementing 20 caches with object sizes geometrically distributed between 32bytes and 4MB
  - Specific cache are created on demand by kernel subsystems

![../\_images/slab-object-descriptors.png](../_images/slab-object-descriptors.png)

  - Only used for free objects
  - An integer that points to the next free object
  - The last free object uses a terminator value
  - Internal descriptors - stored in the slab
  - External descriptors - stored in generic caches

![../\_images/slab-coloring.png](../_images/slab-coloring.png)

</div>

</div>

<div id="virtual-memory-management" class="section">

## Virtual memory management[¶](#virtual-memory-management "Permalink to this headline")

  - Used in both kernel and user space
  - Using virtual memory requires:
      - reserving (allocating) a segment in the *virtual* address space (be it kernel or user)
      - allocating one or more physical pages for the buffer
      - allocating one or more physical pages for page tables and internal structures
      - mapping the virtual memory segment to the physical allocated pages

 

![../\_images/ditaa-0eda95a3f39dfac448fd07589656b123d3548328.png](../_images/ditaa-0eda95a3f39dfac448fd07589656b123d3548328.png)

  - Page table is used either by:
      - The CPU's MMU
      - The kernel to handle TLB exception (some RISC processors)
  - The address space descriptor is used by the kernel to maintain high level information such as file and file offset (for mmap with files), read-only segment, copy-on-write segment, etc.

<!-- end list -->

  - Search a free area in the address space descriptor
  - Allocate memory for a new area descriptor
  - Insert the new area descriptor in the address space descriptor
  - Allocate physical memory for one or more page tables
  - Setup the page tables for the newly allocated area in the virtual address space
  - Allocating (on demand) physical pages and map them in the virtual address space by updating the page tables

<!-- end list -->

  - Removing the area descriptor
  - Freeing the area descriptor memory
  - Updating the page tables to remove the area from the virtual address space
  - Flushing the TLB for the freed virtual memory area
  - Freeing physical memory of the page tables associated with the freed area
  - Freeing physical memory of the freed virtual memory area

<!-- end list -->

  - Kernel
      - vmalloc
          - area descriptor: `struct vm_struct`
          - address space descriptor: simple linked list of `struct vm_struct`
  - Userspace
      - area descriptor: `struct vm_area_struct`
      - address space descriptor: `struct mm_struct`, red-black tree

</div>

<div id="fault-page-handling" class="section">

## Fault page handling[¶](#fault-page-handling "Permalink to this headline")

![../\_images/page-fault-handling.png](../_images/page-fault-handling.png)

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](address-space.html "Address Space") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](fs.html "Filesystem Management")

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
