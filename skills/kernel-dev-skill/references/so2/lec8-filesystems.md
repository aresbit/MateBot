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
      - [SO2 Lecture 08 - Filesystem Management](#)
          - [Lecture objectives:](#lecture-objectives)
          - [Filesystem Abstractions](#filesystem-abstractions)
          - [Filesystem Operations](#filesystem-operations)
              - [Mounting a filesystem](#mounting-a-filesystem)
              - [Opening a file](#opening-a-file)
              - [Querying file attributes](#querying-file-attributes)
              - [Reading data from a file](#reading-data-from-a-file)
              - [Writing data to a file](#writing-data-to-a-file)
              - [Closing a file](#closing-a-file)
              - [Directories](#directories)
              - [Creating a file](#creating-a-file)
              - [Deleting a file](#deleting-a-file)
          - [Linux Virtual File System](#linux-virtual-file-system)
              - [Superblock Operations](#superblock-operations)
              - [Inode Operations](#inode-operations)
              - [The Inode Cache](#the-inode-cache)
              - [The Dentry Cache](#the-dentry-cache)
              - [The Page Cache](#the-page-cache)
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
  - [Operating Systems 2](index.html)
  - SO2 Lecture 08 - Filesystem Management
  - [View page source](../_sources/so2/lec8-filesystems.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lecture-08-filesystem-management" class="section">

# SO2 Lecture 08 - Filesystem Management[¶](#so2-lecture-08-filesystem-management "Permalink to this headline")

[View slides](lec8-filesystems-slides.html)

<span class="admonition-so2-lecture-08-filesystem-management"></span>

<div id="lecture-objectives" class="section">

## Lecture objectives:[¶](#lecture-objectives "Permalink to this headline")

  - Filesystem abstractions
  - Filesystem operations
  - Linux VFS
  - Overview of Linux I/O Management

</div>

<div id="filesystem-abstractions" class="section">

## Filesystem Abstractions[¶](#filesystem-abstractions "Permalink to this headline")

A fileystem is a way to organize files and directories on storage devices such as hard disks, SSDs or flash memory. There are many types of filesystems (e.g. FAT, ext4, btrfs, ntfs) and on one running system we can have multiple instances of the same filesystem type in use.

While filesystems use different data structures to organizing the files, directories, user data and meta (internal) data on storage devices there are a few common abstractions that are used in almost all filesystems:

  - superblock
  - file
  - inode
  - dentry

Some of these abstractions are present both on disk and in memory while some are only present in memory.

The *superblock* abstraction contains information about the filesystem instance such as the block size, the root inode, filesystem size. It is present both on storage and in memory (for caching purposes).

The *file* abstraction contains information about an opened file such as the current file pointer. It only exists in memory.

The *inode* is identifying a file on disk. It exists both on storage and in memory (for caching purposes). An inode identifies a file in a unique way and has various properties such as the file size, access rights, file type, etc.

<div class="admonition note">

Note

The file name is not a property of the file.

</div>

The *dentry* associates a name with an inode. It exists both on storage and in memory (for caching purposes).

The following diagram shows the relationship between the various filesystem abstractions as they used in memory:

![../\_images/ditaa-29f54aaa1a85b819ff29cb7d101a4d646b3b0b06.png](../_images/ditaa-29f54aaa1a85b819ff29cb7d101a4d646b3b0b06.png)

Note that not all of the one to many relationships between the various abstractions are depicted.

Multiple file descriptors can point to the same *file* because we can use the `dup()` system call to duplicate a file descriptor.

Multiple *file* abstractions can point to the same *dentry* if we open the same path multiple times.

Multiple *dentries* can point to the same *inode* when hard links are used.

The following diagram shows the relationship of the filesystem abstraction on storage:

![../\_images/ditaa-bc662dab7bb3d9ba3a37efbf69b82c513dcaadd4.png](../_images/ditaa-bc662dab7bb3d9ba3a37efbf69b82c513dcaadd4.png)

The diagram shows that the *superblock* is typically stored at the beginning of the fileystem and that various blocks are used with different purposes: some to store dentries, some to store inodes and some to store user data blocks. There are also blocks used to manage the available free blocks (e.g. bitmaps for the simple filesystems).

The next diagram show a very simple filesystem where blocks are grouped together by function:

  - the superblock contains information about the block size as well as the IMAP, DMAP, IZONE and DZONE areas.
  - the IMAP area is comprised of multiple blocks which contains a bitmap for inode allocation; it maintains the allocated/free state for all inodes in the IZONE area
  - the DMAP area is comprised of multiple blocks which contains a bitmap for data blocks; it maintains the allocated/free state for all blocks the DZONE area

 

![../\_images/ditaa-8b59fc3f5245ffb5d7089dc80cf2e306c39a62d8.png](../_images/ditaa-8b59fc3f5245ffb5d7089dc80cf2e306c39a62d8.png)

</div>

<div id="filesystem-operations" class="section">

## Filesystem Operations[¶](#filesystem-operations "Permalink to this headline")

The following diagram shows a high level overview of how the file system drivers interact with the rest of the file system "stack". In order to support multiple filesystem types and instances Linux implements a large and complex subsystem that deals with filesystem management. This is called Virtual File System (or sometimes Virtual File Switch) and it is abbreviated with VFS.

![../\_images/ditaa-6d39f541805ae8197b413ec9c79116382abc4dbc.png](../_images/ditaa-6d39f541805ae8197b413ec9c79116382abc4dbc.png)

VFS translates the complex file management related system calls to simpler operations that are implemented by the device drivers. These are some of the operations that a file system must implement:

  - Mount
  - Open a file
  - Querying file attributes
  - Reading data from a file
  - Writing file to a file
  - Creating a file
  - Deleting a file

The next sections will look in-depth at some of these operations.

<div id="mounting-a-filesystem" class="section">

### Mounting a filesystem[¶](#mounting-a-filesystem "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: a storage device (partition)
  - Output: dentry pointing to the root directory
  - Steps: check device, determine filesystem parameters, locate the root inode
  - Example: check magic, determine block size, read the root inode and create dentry

</div>

<div id="opening-a-file" class="section">

### Opening a file[¶](#opening-a-file "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: path
  - Output: file descriptor
  - Steps:
      - Determine the filesystem type
      - For each name in the path: lookup parent dentry, load inode, load data, find dentry
      - Create a new *file* that points to the last *dentry*
      - Find a free entry in the file descriptor table and set it to *file*

</div>

<div id="querying-file-attributes" class="section">

### Querying file attributes[¶](#querying-file-attributes "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: path
  - Output: file attributes
  - Steps:
      - Access file-\>dentry-\>inode
      - Read file attributes from the *inode*

</div>

<div id="reading-data-from-a-file" class="section">

### Reading data from a file[¶](#reading-data-from-a-file "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: file descriptor, offset, length
  - Output: data
  - Steps:
      - Access file-\>dentry-\>inode
      - Determine data blocks
      - Copy data blocks to memory

</div>

<div id="writing-data-to-a-file" class="section">

### Writing data to a file[¶](#writing-data-to-a-file "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: file descriptor, offset, length, data
  - Output:
  - Steps:
      - Allocate one or more data blocks
      - Add the allocated blocks to the inode and update file size
      - Copy data from userspace to internal buffers and write them to storage

</div>

<div id="closing-a-file" class="section">

### Closing a file[¶](#closing-a-file "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: file descriptor
  - Output:
  - Steps:
      - set the file descriptor entry to NULL
      - Decrement file reference counter
      - When the counter reaches 0 free *file*

</div>

<div id="directories" class="section">

### Directories[¶](#directories "Permalink to this headline")

Directories are special files which contain one or more dentries.

</div>

<div id="creating-a-file" class="section">

### Creating a file[¶](#creating-a-file "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: path
  - Output:
  - Steps:
      - Determine the inode directory
      - Read data blocks and find space for a new dentry
      - Write back the modified inode directory data blocks

</div>

<div id="deleting-a-file" class="section">

### Deleting a file[¶](#deleting-a-file "Permalink to this headline")

A summary of a typical implementation is presented below:

  - Input: path
  - Output:
  - Steps:
      - determine the parent inode
      - read parent inode data blocks
      - find and erase the dentry (check for links)
      - when last file is closed: deallocate data and inode blocks

</div>

</div>

<div id="linux-virtual-file-system" class="section">

## Linux Virtual File System[¶](#linux-virtual-file-system "Permalink to this headline")

Although the main purpose for the original introduction of VFS in UNIX kernels was to support multiple filesystem types and instances, a side effect was that it simplified fileystem device driver development since command parts are now implement in the VFS. Almost all of the caching and buffer management is dealt with VFS, leaving just efficient data storage management to the filesystem device driver.

In order to deal with multiple filesystem types, VFS introduced the common filesystem abstractions previously presented. Note that the filesystem driver can also use its own particular fileystem abstractions in memory (e.g. ext4 inode or dentry) and that there might be a different abstraction on storage as well. Thus we may end up with three slightly different filesystem abstractions: one for VFS - always in memory, and two for a particular filesystem - one in memory used by the filesystem driver, and one on storage.

[![../\_images/ditaa-e3a27a84dde42de58bcc5c360e1c4b15062507c2.png](../_images/ditaa-e3a27a84dde42de58bcc5c360e1c4b15062507c2.png)](../_images/ditaa-e3a27a84dde42de58bcc5c360e1c4b15062507c2.png)

<div id="superblock-operations" class="section">

### Superblock Operations[¶](#superblock-operations "Permalink to this headline")

VFS requires that all filesystem implement a set of "superblock operations".

They deal with initializing, updating and freeing the VFS superblock:

> 
> 
> <div>
> 
>   - `fill_super()` - reads the filesystem statistics (e.g. total number of inode, free number of inodes, total number of blocks, free number of blocks)
>   - `write_super()` - updates the superblock information on storage (e.g. updating the number of free inode or data blocks)
>   - `put_super()` - free any data associated with the filsystem instance, called when unmounting a filesystem
> 
> </div>

The next class of operations are dealing with manipulating fileystem inodes. These operations will receive VFS inodes as parameters but the filesystem driver may use its own inode structures internally and, if so, they will convert in between them as necessary.

A summary of the superblock operations are presented below:

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td><ul>
<li>fill_super</li>
<li>put_super</li>
<li>write_super</li>
<li>read_inode</li>
</ul></td>
<td><ul>
<li>write_inode</li>
<li>evict_inode</li>
<li>statfs</li>
<li>remount_fs</li>
</ul></td>
</tr>
</tbody>
</table>

</div>

<div id="inode-operations" class="section">

### Inode Operations[¶](#inode-operations "Permalink to this headline")

The next set of operations that VFS calls when interacting with filesystem device drivers are the "inode operations". Non-intuitively these mostly deal with manipulating dentries - looking up a file name, creating, linking and removing files, dealing with symbolic links, creating and removing directories.

This is the list of the most important inode operations:

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td><ul>
<li>create</li>
<li>lookup</li>
<li>link</li>
<li>unlink</li>
<li>symlink</li>
<li>mkdir</li>
</ul></td>
<td><ul>
<li>rmdir</li>
<li>rename</li>
<li>readlink</li>
<li>follow_link</li>
<li>put_link</li>
<li>...</li>
</ul></td>
</tr>
</tbody>
</table>

</div>

<div id="the-inode-cache" class="section">

### The Inode Cache[¶](#the-inode-cache "Permalink to this headline")

The inode cache is used to avoid reading and writing inodes to and from storage every time we need to read or update them. The cache uses a hash table and inodes are indexed with a hash function which takes as parameters the superblock (of a particular filesystem instance) and the inode number associated with an inode.

inodes are cached until either the filesystem is unmounted, the inode deleted or the system enters a memory pressure state. When this happens the Linux memory management system will (among other things) free inodes from the inode cache based on how often they were accessed.

  - Caches inodes into memory to avoid costly storage operations
  - An inode is cached until low memory conditions are triggered
  - inodes are indexed with a hash table
  - The inode hash function takes the superblock and inode number as inputs

</div>

<div id="the-dentry-cache" class="section">

### The Dentry Cache[¶](#the-dentry-cache "Permalink to this headline")

  - State:
      - Used – *d\_inode* is valid and the *dentry* object is in use
      - Unused – *d\_inode* is valid but the dentry object is not in use
      - Negative – *d\_inode* is not valid; the inode was not yet loaded or the file was erased
  - Dentry cache
      - List of used dentries (dentry-\>d\_state == used)
      - List of the most recent used dentries (sorted by access time)
      - Hash table to avoid searching the tree

</div>

<div id="the-page-cache" class="section">

### The Page Cache[¶](#the-page-cache "Permalink to this headline")

  - Caches file data and not block device data
  - Uses the `struct address_space` to translate file offsets to block offsets
  - Used for both read / write and mmap
  - Uses a radix tree

<div class="admonition-struct-address-space highlight-c">

<div class="highlight">

    /**
     * struct address_space - Contents of a cacheable, mappable object.
     * @host: Owner, either the inode or the block_device.
     * @i_pages: Cached pages.
     * @gfp_mask: Memory allocation flags to use for allocating pages.
     * @i_mmap_writable: Number of VM_SHARED mappings.
     * @nr_thps: Number of THPs in the pagecache (non-shmem only).
     * @i_mmap: Tree of private and shared mappings.
     * @i_mmap_rwsem: Protects @i_mmap and @i_mmap_writable.
     * @nrpages: Number of page entries, protected by the i_pages lock.
     * @nrexceptional: Shadow or DAX entries, protected by the i_pages lock.
     * @writeback_index: Writeback starts here.
     * @a_ops: Methods.
     * @flags: Error bits and flags (AS_*).
     * @wb_err: The most recent error which has occurred.
     * @private_lock: For use by the owner of the address_space.
     * @private_list: For use by the owner of the address_space.
     * @private_data: For use by the owner of the address_space.
     */
    struct address_space {
      struct inode            *host;
      struct xarray           i_pages;
      gfp_t                   gfp_mask;
      atomic_t                i_mmap_writable;
    #ifdef CONFIG_READ_ONLY_THP_FOR_FS
      /* number of thp, only for non-shmem files */
      atomic_t                nr_thps;
    #endif
      struct rb_root_cached   i_mmap;
      struct rw_semaphore     i_mmap_rwsem;
      unsigned long           nrpages;
      unsigned long           nrexceptional;
      pgoff_t                 writeback_index;
      const struct address_space_operations *a_ops;
      unsigned long           flags;
      errseq_t                wb_err;
      spinlock_t              private_lock;
      struct list_head        private_list;
      void                    *private_data;
    } __attribute__((aligned(sizeof(long)))) __randomize_layout;
    
    struct address_space_operations {
      int (*writepage)(struct page *page, struct writeback_control *wbc);
      int (*readpage)(struct file *, struct page *);
    
      /* Write back some dirty pages from this mapping. */
      int (*writepages)(struct address_space *, struct writeback_control *);
    
      /* Set a page dirty.  Return true if this dirtied it */
      int (*set_page_dirty)(struct page *page);
    
      /*
       * Reads in the requested pages. Unlike ->readpage(), this is
       * PURELY used for read-ahead!.
       */
      int (*readpages)(struct file *filp, struct address_space *mapping,
                      struct list_head *pages, unsigned nr_pages);
      void (*readahead)(struct readahead_control *);
    
      int (*write_begin)(struct file *, struct address_space *mapping,
                              loff_t pos, unsigned len, unsigned flags,
                              struct page **pagep, void **fsdata);
      int (*write_end)(struct file *, struct address_space *mapping,
                              loff_t pos, unsigned len, unsigned copied,
                              struct page *page, void *fsdata);
    
      /* Unfortunately this kludge is needed for FIBMAP. Don't use it */
      sector_t (*bmap)(struct address_space *, sector_t);
      void (*invalidatepage) (struct page *, unsigned int, unsigned int);
      int (*releasepage) (struct page *, gfp_t);
      void (*freepage)(struct page *);
      ssize_t (*direct_IO)(struct kiocb *, struct iov_iter *iter);
      /*
       * migrate the contents of a page to the specified target. If
       * migrate_mode is MIGRATE_ASYNC, it must not block.
       */
      int (*migratepage) (struct address_space *,
                      struct page *, struct page *, enum migrate_mode);
      bool (*isolate_page)(struct page *, isolate_mode_t);
      void (*putback_page)(struct page *);
      int (*launder_page) (struct page *);
      int (*is_partially_uptodate) (struct page *, unsigned long,
                                      unsigned long);
      void (*is_dirty_writeback) (struct page *, bool *, bool *);
      int (*error_remove_page)(struct address_space *, struct page *);
    
      /* swapfile support */
      int (*swap_activate)(struct swap_info_struct *sis, struct file *file,
                              sector_t *span);
      void (*swap_deactivate)(struct file *file);
    };

</div>

</div>

<div class="admonition-reading-data highlight-c">

<div class="highlight">

    /**
     * generic_file_read_iter - generic filesystem read routine
     * @iocb: kernel I/O control block
     * @iter: destination for the data read
     *
     * This is the "read_iter()" routine for all filesystems
     * that can use the page cache directly.
     *
     * The IOCB_NOWAIT flag in iocb->ki_flags indicates that -EAGAIN shall
     * be returned when no data can be read without waiting for I/O requests
     * to complete; it doesn't prevent readahead.
     *
     * The IOCB_NOIO flag in iocb->ki_flags indicates that no new I/O
     * requests shall be made for the read or for readahead.  When no data
     * can be read, -EAGAIN shall be returned.  When readahead would be
     * triggered, a partial, possibly empty read shall be returned.
     *
     * Return:
     * * number of bytes copied, even for partial reads
     * * negative error code (or 0 if IOCB_NOIO) if nothing was read
     */
    ssize_t
    generic_file_read_iter(struct kiocb *iocb, struct iov_iter *iter)
    
    /*
     * Generic "read page" function for block devices that have the normal
     * get_block functionality. This is most of the block device filesystems.
     * Reads the page asynchronously --- the unlock_buffer() and
     * set/clear_buffer_uptodate() functions propagate buffer state into the
     * page struct once IO has completed.
     */
    int block_read_full_page(struct page *page, get_block_t *get_block)

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lec7-memory-management.html "SO2 Lecture 07 - Memory Management") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lec9-debugging.html "SO2 Lecture 09 - Kernel debugging")

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
