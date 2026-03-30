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
      - [SO2 Lab 06 - Memory Mapping](#)
          - [Lab objectives](#lab-objectives)
          - [Overview](#overview)
          - [Structures used for memory mapping](#structures-used-for-memory-mapping)
              - [`struct page`](#struct-page)
              - [`struct vm_area_struct`](#struct-vm-area-struct)
              - [`struct mm_struct`](#struct-mm-struct)
          - [Device driver memory mapping](#device-driver-memory-mapping)
          - [Further reading](#further-reading)
          - [Exercises](#exercises)
              - [1. Mapping contiguous physical memory to userspace](#mapping-contiguous-physical-memory-to-userspace)
              - [2. Mapping non-contiguous physical memory to userspace](#mapping-non-contiguous-physical-memory-to-userspace)
              - [3. Read / write operations in mapped memory](#read-write-operations-in-mapped-memory)
              - [4. Display memory mapped in procfs](#display-memory-mapped-in-procfs)
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
  - SO2 Lab 06 - Memory Mapping
  - [View page source](../_sources/so2/lab6-memory-mapping.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lab-06-memory-mapping" class="section">

# SO2 Lab 06 - Memory Mapping[¶](#so2-lab-06-memory-mapping "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

  - Understand address space mapping mechanisms
  - Learn about the most important structures related to memory management

Keywords:

  - address space
  - `mmap()`
  - `struct page`
  - `struct vm_area_struct`
  - `struct vm_struct`
  - `remap_pfn_range`
  - `SetPageReserved()`
  - `ClearPageReserved()`

</div>

<div id="overview" class="section">

## Overview[¶](#overview "Permalink to this headline")

In the Linux kernel it is possible to map a kernel address space to a user address space. This eliminates the overhead of copying user space information into the kernel space and vice versa. This can be done through a device driver and the user space device interface (`/dev`).

This feature can be used by implementing the `mmap()` operation in the device driver's `struct file_operations` and using the `mmap()` system call in user space.

The basic unit for virtual memory management is a page, which size is usually 4K, but it can be up to 64K on some platforms. Whenever we work with virtual memory we work with two types of addresses: virtual address and physical address. All CPU access (including from kernel space) uses virtual addresses that are translated by the MMU into physical addresses with the help of page tables.

A physical page of memory is identified by the Page Frame Number (PFN). The PFN can be easily computed from the physical address by dividing it with the size of the page (or by shifting the physical address with PAGE\_SHIFT bits to the right).

[![../\_images/paging1.png](../_images/paging1.png)](../_images/paging1.png)

For efficiency reasons, the virtual address space is divided into user space and kernel space. For the same reason, the kernel space contains a memory mapped zone, called **lowmem**, which is contiguously mapped in physical memory, starting from the lowest possible physical address (usually 0). The virtual address where lowmem is mapped is defined by `PAGE_OFFSET`.

On a 32bit system, not all available memory can be mapped in lowmem and because of that there is a separate zone in kernel space called **highmem** which can be used to arbitrarily map physical memory.

Memory allocated by `kmalloc()` resides in lowmem and it is physically contiguous. Memory allocated by `vmalloc()` is not contiguous and does not reside in lowmem (it has a dedicated zone in highmem).

[![../\_images/kernel-virtmem-map1.png](../_images/kernel-virtmem-map1.png)](../_images/kernel-virtmem-map1.png)

</div>

<div id="structures-used-for-memory-mapping" class="section">

## Structures used for memory mapping[¶](#structures-used-for-memory-mapping "Permalink to this headline")

Before discussing about the memory mapping mechanism over a device, we will present some of the basic structures used by the Linux memory management subsystem. Some of the basic structures are: `struct page`, `struct vm_area_struct`, `struct mm_struct`.

<div id="struct-page" class="section">

### `struct page`[¶](#struct-page "Permalink to this headline")

`struct page` is used to embed information about all physical pages in the system. The kernel has a `struct page` structure for all pages in the system.

There are many functions that interact with this structure:

  - `virt_to_page()` returns the page associated with a virtual address
  - `pfn_to_page()` returns the page associated with a page frame number
  - `page_to_pfn()` return the page frame number associated with a `struct page`
  - `page_address()` returns the virtual address of a `struct page`; this functions can be called only for pages from lowmem
  - `kmap()` creates a mapping in kernel for an arbitrary physical page (can be from highmem) and returns a virtual address that can be used to directly reference the page

</div>

<div id="struct-vm-area-struct" class="section">

### `struct vm_area_struct`[¶](#struct-vm-area-struct "Permalink to this headline")

`struct vm_area_struct` holds information about a contiguous virtual memory area. The memory areas of a process can be viewed by inspecting the *maps* attribute of the process via procfs:

<div class="highlight-shell">

<div class="highlight">

    root@qemux86:~# cat /proc/1/maps
    #address          perms offset  device inode     pathname
    08048000-08050000 r-xp 00000000 fe:00 761        /sbin/init.sysvinit
    08050000-08051000 r--p 00007000 fe:00 761        /sbin/init.sysvinit
    08051000-08052000 rw-p 00008000 fe:00 761        /sbin/init.sysvinit
    092e1000-09302000 rw-p 00000000 00:00 0          [heap]
    4480c000-4482e000 r-xp 00000000 fe:00 576        /lib/ld-2.25.so
    4482e000-4482f000 r--p 00021000 fe:00 576        /lib/ld-2.25.so
    4482f000-44830000 rw-p 00022000 fe:00 576        /lib/ld-2.25.so
    44832000-449a9000 r-xp 00000000 fe:00 581        /lib/libc-2.25.so
    449a9000-449ab000 r--p 00176000 fe:00 581        /lib/libc-2.25.so
    449ab000-449ac000 rw-p 00178000 fe:00 581        /lib/libc-2.25.so
    449ac000-449af000 rw-p 00000000 00:00 0
    b7761000-b7763000 rw-p 00000000 00:00 0
    b7763000-b7766000 r--p 00000000 00:00 0          [vvar]
    b7766000-b7767000 r-xp 00000000 00:00 0          [vdso]
    bfa15000-bfa36000 rw-p 00000000 00:00 0          [stack]

</div>

</div>

A memory area is characterized by a start address, a stop address, length, permissions.

A `struct vm_area_struct` is created at each `mmap()` call issued from user space. A driver that supports the `mmap()` operation must complete and initialize the associated `struct vm_area_struct`. The most important fields of this structure are:

  - `vm_start`, `vm_end` - the beginning and the end of the memory area, respectively (these fields also appear in `/proc/<pid>/maps`);
  - `vm_file` - the pointer to the associated file structure (if any);
  - `vm_pgoff` - the offset of the area within the file;
  - `vm_flags` - a set of flags;
  - `vm_ops` - a set of working functions for this area
  - `vm_next`, `vm_prev` - the areas of the same process are chained by a list structure

</div>

<div id="struct-mm-struct" class="section">

### `struct mm_struct`[¶](#struct-mm-struct "Permalink to this headline")

`struct mm_struct` encompasses all memory areas associated with a process. The `mm` field of `struct task_struct` is a pointer to the `struct mm_struct` of the current process.

</div>

</div>

<div id="device-driver-memory-mapping" class="section">

## Device driver memory mapping[¶](#device-driver-memory-mapping "Permalink to this headline")

Memory mapping is one of the most interesting features of a Unix system. From a driver's point of view, the memory-mapping facility allows direct memory access to a user space device.

To assign a `mmap()` operation to a driver, the `mmap` field of the device driver's `struct file_operations` must be implemented. If that is the case, the user space process can then use the `mmap()` system call on a file descriptor associated with the device.

The mmap system call takes the following parameters:

<div class="highlight-c">

<div class="highlight">

    void *mmap(caddr_t addr, size_t len, int prot,
               int flags, int fd, off_t offset);

</div>

</div>

To map memory between a device and user space, the user process must open the device and issue the `mmap()` system call with the resulting file descriptor.

The device driver `mmap()` operation has the following signature:

<div class="highlight-c">

<div class="highlight">

    int (*mmap)(struct file *filp, struct vm_area_struct *vma);

</div>

</div>

The *filp* field is a pointer to a `struct file` created when the device is opened from user space. The *vma* field is used to indicate the virtual address space where the memory should be mapped by the device. A driver should allocate memory (using `kmalloc()`, `vmalloc()`, `alloc_pages()`) and then map it to the user address space as indicated by the *vma* parameter using helper functions such as `remap_pfn_range()`.

`remap_pfn_range()` will map a contiguous physical address space into the virtual space represented by `vm_area_struct`:

<div class="highlight-c">

<div class="highlight">

    int remap_pfn_range (structure vm_area_struct *vma, unsigned long addr,
                         unsigned long pfn, unsigned long size, pgprot_t prot);

</div>

</div>

`remap_pfn_range()` expects the following parameters:

  - *vma* - the virtual memory space in which mapping is made;
  - *addr* - the virtual address space from where remapping begins; page tables for the virtual address space between addr and addr + size will be formed as needed
  - *pfn* - the page frame number to which the virtual address should be mapped
  - *size* - the size (in bytes) of the memory to be mapped
  - *prot* - protection flags for this mapping

Here is an example of using this function that contiguously maps the physical memory starting at page frame number *pfn* (memory that was previously allocated) to the *vma-\>vm\_start* virtual address:

<div class="highlight-c">

<div class="highlight">

    struct vm_area_struct *vma;
    unsigned long len = vma->vm_end - vma->vm_start;
    int ret ;
    
    ret = remap_pfn_range(vma, vma->vm_start, pfn, len, vma->vm_page_prot);
    if (ret < 0) {
        pr_err("could not map the address area\n");
        return -EIO;
    }

</div>

</div>

To obtain the page frame number of the physical memory we must consider how the memory allocation was performed. For each `kmalloc()`, `vmalloc()`, `alloc_pages()`, we must used a different approach. For `kmalloc()` we can use something like:

<div class="highlight-c">

<div class="highlight">

    static char *kmalloc_area;
    
    unsigned long pfn = virt_to_phys((void *)kmalloc_area)>>PAGE_SHIFT;

</div>

</div>

while for `vmalloc()`:

<div class="highlight-c">

<div class="highlight">

    static char *vmalloc_area;
    
    unsigned long pfn = vmalloc_to_pfn(vmalloc_area);

</div>

</div>

and finally for `alloc_pages()`:

<div class="highlight-c">

<div class="highlight">

    struct page *page;
    
    unsigned long pfn = page_to_pfn(page);

</div>

</div>

<div class="admonition attention">

Attention

Note that memory allocated with `vmalloc()` is not physically contiguous so if we want to map a range allocated with `vmalloc()`, we have to map each page individually and compute the physical address for each page.

</div>

Since the pages are mapped to user space, they might be swapped out. To avoid this we must set the PG\_reserved bit on the page. Enabling is done using `SetPageReserved()` while reseting it (which must be done before freeing the memory) is done with `ClearPageReserved()`:

<div class="highlight-c">

<div class="highlight">

    void alloc_mmap_pages(int npages)
    {
        int i;
        char *mem = kmalloc(PAGE_SIZE * npages);
    
        if (!mem)
            return mem;
    
        for(i = 0; i < npages * PAGE_SIZE; i += PAGE_SIZE)
            SetPageReserved(virt_to_page(((unsigned long)mem) + i));
    
        return mem;
    }
    
    void free_mmap_pages(void *mem, int npages)
    {
        int i;
    
        for(i = 0; i < npages * PAGE_SIZE; i += PAGE_SIZE)
            ClearPageReserved(virt_to_page(((unsigned long)mem) + i));
    
        kfree(mem);
    }

</div>

</div>

</div>

<div id="further-reading" class="section">

## Further reading[¶](#further-reading "Permalink to this headline")

  - [Linux Device Drivers 3rd Edition - Chapter 15. Memory Mapping and DMA](http://lwn.net/images/pdf/LDD3/ch15.pdf)
  - [Linux Device Driver mmap Skeleton](http://www.xml.com/ldd/chapter/book/ch13.html)
  - [Driver porting: supporting mmap ()](http://lwn.net/Articles/28746/)
  - [Device Drivers Concluded](http://www.linuxjournal.com/article/1287)
  - [mmap](http://en.wikipedia.org/wiki/Mmap)

</div>

<div id="exercises" class="section">

## Exercises[¶](#exercises "Permalink to this headline")

<div class="admonition important">

Important

We strongly encourage you to use the setup from [this repository](https://gitlab.cs.pub.ro/so2/so2-labs).

  - To solve exercises, you need to perform these steps:
    
      - prepare skeletons from templates
      - build modules
      - start the VM and test the module in the VM.

The current lab name is memory\_mapping. See the exercises for the task name.

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

The modules are placed in /home/root/skels/memory\_mapping/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

<div id="mapping-contiguous-physical-memory-to-userspace" class="section">

### 1\. Mapping contiguous physical memory to userspace[¶](#mapping-contiguous-physical-memory-to-userspace "Permalink to this headline")

Implement a device driver that maps contiguous physical memory (e.g. obtained via `kmalloc()`) to userspace.

Review the [Device driver memory mapping](#device-driver-memory-mapping) section, generate the skeleton for the task named **kmmap** and fill in the areas marked with **TODO 1**.

Start with allocating a NPAGES+2 memory area page using `kmalloc()` in the module init function and find the first address in the area that is aligned to a page boundary.

<div class="admonition hint">

Hint

The size of a page is *PAGE\_SIZE*.

Store the allocated area in *kmalloc\_ptr* and the page aligned address in *kmalloc\_area*:

Use `PAGE_ALIGN()` to determine *kmalloc\_area*.

</div>

Enable the PG\_reserved bit of each page with `SetPageReserved()`. Clear the bit with `ClearPageReserved()` before freeing the memory.

<div class="admonition hint">

Hint

Use `virt_to_page()` to translate virtual pages into physical pages, as required by `SetPageReserved()` and `ClearPageReserved()`.

</div>

For verification purpose (using the test below), fill in the first 4 bytes of each page with the following values: 0xaa, 0xbb, 0xcc, 0xdd.

Implement the `mmap()` driver function.

<div class="admonition hint">

Hint

For mapping, use `remap_pfn_range()`. The third argument for `remap_pfn_range()` is a page frame number (PFN).

To convert from virtual kernel address to physical address, use `virt_to_phys()`.

To convert a physical address to its PFN, shift the address with PAGE\_SHIFT bits to the right.

</div>

For testing, load the kernel module and run:

<div class="highlight-shell">

<div class="highlight">

    root@qemux86:~# skels/memory_mapping/test/mmap-test 1

</div>

</div>

If everything goes well, the test will show "matched" messages.

</div>

<div id="mapping-non-contiguous-physical-memory-to-userspace" class="section">

### 2\. Mapping non-contiguous physical memory to userspace[¶](#mapping-non-contiguous-physical-memory-to-userspace "Permalink to this headline")

Implement a device driver that maps non-contiguous physical memory (e.g. obtained via `vmalloc()`) to userspace.

Review the [Device driver memory mapping](#device-driver-memory-mapping) section, generate the skeleton for the task named **vmmap** and fill in the areas marked with **TODO 1**.

Allocate a memory area of NPAGES with `vmalloc()`.

<div class="admonition hint">

Hint

The size of a page is *PAGE\_SIZE*. Store the allocated area in *vmalloc\_area*. Memory allocated by `vmalloc()` is paged aligned.

</div>

Enable the PG\_reserved bit of each page with `SetPageReserved()`. Clear the bit with `ClearPageReserved()` before freeing the memory.

<div class="admonition hint">

Hint

Use `vmalloc_to_page()` to translate virtual pages into physical pages used by the functions `SetPageReserved()` and `ClearPageReserved()`.

</div>

For verification purpose (using the test below), fill in the first 4 bytes of each page with the following values: 0xaa, 0xbb, 0xcc, 0xdd.

Implement the mmap driver function.

<div class="admonition hint">

Hint

To convert from virtual vmalloc address to physical address, use `vmalloc_to_pfn()` which returns a PFN directly.

</div>

<div class="admonition attention">

Attention

vmalloc pages are not physically contiguous so it is needed to use `remap_pfn_range()` for each page.

Loop through all virtual pages and for each: \* determine the physical address \* map it with `remap_pfn_range()`

Make sure that you determine the physical address each time and that you use a range of one page for mapping.

</div>

For testing, load the kernel module and run:

<div class="highlight-shell">

<div class="highlight">

    root@qemux86:~# skels/memory_mapping/test/mmap-test 1

</div>

</div>

If everything goes well, the test will show "matched" messages.

</div>

<div id="read-write-operations-in-mapped-memory" class="section">

### 3\. Read / write operations in mapped memory[¶](#read-write-operations-in-mapped-memory "Permalink to this headline")

Modify one of the previous modules to allow read / write operations on your device. This is a didactic exercise to see that the same space can also be used with the `mmap()` call and with `read()` and `write()` calls.

Fill in areas marked with **TODO 2**.

<div class="admonition note">

Note

The offset parameter sent to the read / write operation can be ignored as all reads / writes from the test program will be done with 0 offsets.

</div>

For testing, load the kernel module and run:

<div class="highlight-shell">

<div class="highlight">

    root@qemux86:~# skels/memory_mapping/test/mmap-test 2

</div>

</div>

</div>

<div id="display-memory-mapped-in-procfs" class="section">

### 4\. Display memory mapped in procfs[¶](#display-memory-mapped-in-procfs "Permalink to this headline")

Using one of the previous modules, create a procfs file in which you display the total memory mapped by the calling process.

Fill in the areas marked with **TODO 3**.

Create a new entry in procfs (`PROC_ENTRY_NAME`, defined in `mmap-test.h`) that will show the total memory mapped by the process that called the `read()` on that file.

<div class="admonition hint">

Hint

Use `proc_create()`. For the mode parameter, use 0, and for the parent parameter use NULL. Use `my_proc_file_ops()` for operations.

</div>

In the module exit function, delete the `PROC_ENTRY_NAME` entry using `remove_proc_entry()`.

<div class="admonition note">

Note

A (complex) use and description of the `struct seq_file` interface can be found here in this [example](http://tldp.org/LDP/lkmpg/2.6/html/x861.html) .

For this exercise, just a simple use of the interface described [here](http://lwn.net/Articles/22355/) is sufficient. Check the "extra-simple" API described there.

</div>

In the `my_seq_show()` function you will need to:

  - Obtain the `struct mm_struct` structure of the current process using the `get_task_mm()` function.
    
    <div class="admonition hint">
    
    Hint
    
    The current process is available via the *current* variable of type `struct task_struct*`.
    
    </div>

  - Iterate through the entire `struct vm_area_struct` list associated with the process.
    
    <div class="admonition hint">
    
    Hint
    
    Use the variable `vma_iterator` and start from `mm->mmap`. Use the `vm_next` field of the `struct vm_area_struct` to navigate through the list of memory areas. Stop when you reach `NULL`.
    
    </div>

  - Use *vm\_start* and *vm\_end* for each area to compute the total size.

  - Use `pr_info("%lx %lxn, ...)()` to print *vm\_start* and *vm\_end* for each area.

  - To release `struct mm_struct`, decrement the reference counter of the structure using `mmput()`.

  - Use `seq_printf()` to write to the file. Show only the total count, no other messages. Do not even show newline (n).

In `my_seq_open()` register the display function (`my_seq_show()`) using `single_open()`.

<div class="admonition note">

Note

`single_open()` can use `NULL` as its third argument.

</div>

For testing, load the kernel module and run:

<div class="highlight-shell">

<div class="highlight">

    root@qemux86:~# skels/memory_mapping/test/mmap-test 3

</div>

</div>

<div class="admonition note">

Note

The test waits for a while (it has an internal sleep instruction). As long as the test waits, use the **pmap** command in another console to see the mappings of the test and compare those to the test results.

</div>

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lab5-deferred-work.html "SO2 Lab 05 - Deferred work") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lab7-block-device-drivers.html "SO2 Lab 07 - Block Device Drivers")

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
