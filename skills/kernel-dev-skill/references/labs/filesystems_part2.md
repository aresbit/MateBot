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

  - [Infrastructure](infrastructure.html)
  - [Introduction](introduction.html)
  - [Kernel modules](kernel_modules.html)
  - [Kernel API](kernel_api.html)
  - [Character device drivers](device_drivers.html)
  - [I/O access and Interrupts](interrupts.html)
  - [Deferred work](deferred_work.html)
  - [Block Device Drivers](block_device_drivers.html)
  - [File system drivers (Part 1)](filesystems_part1.html)
  - [File system drivers (Part 2)](#)
      - [Lab objectives](#lab-objectives)
      - [Inode](#inode)
          - [The inode structure](#the-inode-structure)
          - [Inode operations](#inode-operations)
              - [Getting an inode](#getting-an-inode)
              - [Superoperations](#superoperations)
              - [inode\_operations](#inode-operations-1)
      - [The file structure](#the-file-structure)
      - [Regular files inodes](#regular-files-inodes)
          - [Regular files inode operations](#regular-files-inode-operations)
          - [Address space operations](#address-space-operations)
      - [Dentry structure](#dentry-structure)
          - [Dentry operations](#dentry-operations)
      - [Directory inodes operations](#directory-inodes-operations)
          - [Creating an inode](#creating-an-inode)
          - [Creating a directory](#creating-a-directory)
          - [Creating a link](#creating-a-link)
          - [Creating a symbolic link](#creating-a-symbolic-link)
          - [Deleting a link](#deleting-a-link)
          - [Deleting a directory](#deleting-a-directory)
          - [Searching for an inode in a directory](#searching-for-an-inode-in-a-directory)
          - [Iterating through entries in a directory](#iterating-through-entries-in-a-directory)
      - [Bitmap operations](#bitmap-operations)
      - [Further reading](#further-reading)
      - [Exercises](#exercises)
          - [myfs](#myfs)
              - [1. Directory operations](#directory-operations)
              - [2. File operations](#file-operations)
          - [minfs](#minfs)
              - [1. Iterate operation](#iterate-operation)
              - [2. Lookup operation](#lookup-operation)
              - [3. Create operation](#create-operation)
  - [Networking](networking.html)
  - [Kernel Development on ARM](arm_kernel_development.html)
  - [Memory mapping](memory_mapping.html)
  - [Linux Device Model](device_model.html)
  - [Kernel Profiling](kernel_profiling.html)

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
  - File system drivers (Part 2)
  - [View page source](../_sources/labs/filesystems_part2.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="file-system-drivers-part-2" class="section">

# File system drivers (Part 2)[¶](#file-system-drivers-part-2 "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

> 
> 
> <div>
> 
>   - Improving the knowledge about inode, file and dentry.
>   - Acquiring knowledge about adding support for working with regular files and directories in VFS (*Virtual File System*).
>   - Acquiring knowledge about the internal implementation of a file system.
> 
> </div>

</div>

<div id="inode" class="section">

## Inode[¶](#inode "Permalink to this headline")

The inode is an essential component of a UNIX file system and, at the same time, an important component of VFS. An inode is a metadata (it has information about information). An inode uniquely identifies a file on disk and holds information about it (uid, gid, access rights, access times, pointers to data blocks, etc.). An important aspect is that an inode does not have information about the file name (it is retained by the associated `struct dentry` structure).

The inode refers to a file on the disk. To refer an open file (associated with a file descriptor within a process), the `struct file` structure is used. An inode can have any number of (zero or more) `file` structures associated (multiple processes can open the same file, or a process can open the same file several times).

Inode exists both as a VFS entity (in memory) and as a disk entity (for UNIX, HFS, NTFS, etc.). The inode in VFS is represented by the structure `struct inode`. Like the other structures in VFS, `struct inode` is a generic structure that covers the options for all supported file types, even those that do not have an associated disk entity (such as FAT).

<div id="the-inode-structure" class="section">

### The inode structure[¶](#the-inode-structure "Permalink to this headline")

The inode structure is the same for all file systems. In general, file systems also have private information. These are referenced through the `i_private` field of the structure. Conventionally, the structure that keeps that particular information is called `<fsname>_inode_info`, where `fsname` represents the file system name. For example, minix and ext4 filesystems store particular information in structures `struct minix_inode_info`, or `struct ext4_inode_info`.

Some of the important fields of `struct inode` are:

> 
> 
> <div>
> 
>   - `i_sb` : The superblock structure of the file system the inode belongs to.
>   - `i_rdev`: the device on which this file system is mounted
>   - `i_ino` : the number of the inode (uniquely identifies the inode within the file system)
>   - `i_blkbits`: number of bits used for the block size == log<sub>2</sub>(block size)
>   - `i_mode`, `i_uid`, `i_gid`: access rights, uid, gid
>   - `i_size`: file/directory/etc. size in bytes
>   - `i_mtime`, `i_atime`, `i_ctime`: change, access, and creation time
>   - `i_nlink`: the number of names entries (dentries) that use this inode; for file systems without links (either hard or symbolic) this is always set to 1
>   - `i_blocks`: the number of blocks used by the file (all blocks, not just data); this is only used by the quota subsystem
>   - `i_op`, `i_fop`: pointers to operations structures: `struct inode_operations` and `struct file_operations`; `i_mapping->a_ops` contains a pointer to `struct address_space_operations`.
>   - `i_count`: the inode counter indicating how many kernel components use it.
> 
> </div>

Some functions that can be used to work with inodes:

> 
> 
> <div>
> 
>   - `new_inode()`: creates a new inode, sets the `i_nlink` field to 1 and initializes `i_blkbits`, `i_sb` and `i_dev`;
> 
>   - `insert_inode_hash()`: adds the inode to the hash table of inodes; an interesting effect of this call is that the inode will be written to the disk if it is marked as dirty;
>     
>     <div class="admonition warning">
>     
>     Warning
>     
>     An inode created with `new_inode()` is not in the hash table, and unless you have serious reasons not to, you must enter it in the hash table;
>     
>     </div>
> 
>   - `mark_inode_dirty()`: marks the inode as dirty; at a later moment, it will be written on the disc;
> 
>   - `iget_locked()`: loads the inode with the given number from the disk, if it is not already loaded;
> 
>   - `unlock_new_inode()`: used in conjunction with `iget_locked()`, releases the lock on the inode;
> 
>   - `iput()`: tells the kernel that the work on the inode is finished; if no one else uses it, it will be destroyed (after being written on the disk if it is maked as dirty);
> 
>   - `make_bad_inode()`: tells the kernel that the inode can not be used; It is generally used from the function that reads the inode when the inode could not be read from the disk, being invalid.
> 
> </div>

</div>

<div id="inode-operations" class="section">

### Inode operations[¶](#inode-operations "Permalink to this headline")

<div id="getting-an-inode" class="section">

#### Getting an inode[¶](#getting-an-inode "Permalink to this headline")

One of the main inode operations is obtaining an inode (the `struct inode` in VFS). Until version `2.6.24` of the Linux kernel, the developer defined a `read_inode` function. Starting with version `2.6.25`, the developer must define a `<fsname>_iget` where `<fsname>` is the name of the file system. This function is responsible with finding the VFS inode if it exists or creating a new one and filling it with the information from the disk.

Generally, this function will call `iget_locked()` to get the inode structure from VFS. If the inode is newly created then it will need to read the inode from the disk (using `sb_bread()`) and fill in the useful information.

An example of such a function is `minix_iget()`:

<div class="highlight-c">

<div class="highlight">

    static struct inode *V1_minix_iget(struct inode *inode)
    {
          struct buffer_head * bh;
          struct minix_inode * raw_inode;
          struct minix_inode_info *minix_inode = minix_i(inode);
          int i;
    
          raw_inode = minix_V1_raw_inode(inode->i_sb, inode->i_ino, &bh);
          if (!raw_inode) {
                  iget_failed(inode);
                  return ERR_PTR(-EIO);
          ...
    }
    
    struct inode *minix_iget(struct super_block *sb, unsigned long ino)
    {
          struct inode *inode;
    
          inode = iget_locked(sb, ino);
          if (!inode)
                  return ERR_PTR(-ENOMEM);
          if (!(inode->i_state & I_NEW))
                  return inode;
    
          if (INODE_VERSION(inode) == MINIX_V1)
                  return V1_minix_iget(inode);
        ...
    }

</div>

</div>

The minix\_iget function gets the VFS inode using `iget_locked()`. If the inode is already existing (not new == the `I_NEW` flag is not set) the function returns. Otherwise, the function calls the `V1_minix_iget()` function that will read the inode from the disk using `minix_V1_raw_inode()` and then complete the VFS inode with the read information.

</div>

<div id="superoperations" class="section">

#### Superoperations[¶](#superoperations "Permalink to this headline")

Many of the superoperations (components of the `struct super_operations` structure used by the superblock) are used when working with inodes. These operations are described next:

> 
> 
> <div>
> 
>   - `alloc_inode`: allocates an inode. Usually, this funcion allocates a `struct <fsname>_inode_info` structure and performs basic VFS inode initialization (using `inode_init_once()`); minix uses for allocation the `kmem_cache_alloc()` function that interacts with the SLAB subsystem. For each allocation, the cache construction is called, which in the case of minix is the `init_once()` function. Alternatively, `kmalloc()` can be used, in which case the `inode_init_once()` function should be called. The `alloc_inode()` function will be called by the `new_inode()` and `iget_locked()` functions.
>   - `write_inode` : saves/updates the inode received as a parameter on disk; to update the inode, though inefficient, for beginners it is recommended to use the following sequence of operations:
>       - load the inode from the disk using the `sb_bread()` function;
>       - modify the buffer according to the saved inode;
>       - mark the buffer as dirty using `mark_buffer_dirty()`; the kernel will then handle its writing on the disk;
>       - an example is the `minix_write_inode()` function in the `minix` file system
>   - `evict_inode`: removes any information about the inode with the number received in the `i_ino` field from the disk and memory (both the inode on the disk and the associated data blocks). This involves performing the following operations:
>       - delete the inode from the disk;
>       - updates disk bitmaps (if any);
>       - delete the inode from the page cache by calling `truncate_inode_pages()`;
>       - delete the inode from memory by calling `clear_inode()` ;
>       - an example is the `minix_evict_inode()` function from the minix file system.
>   - `destroy_inode` releases the memory occupied by inode
> 
> </div>

</div>

<div id="inode-operations-1" class="section">

#### inode\_operations[¶](#inode-operations-1 "Permalink to this headline")

The inode operations are described by the `struct inode_operations` structure.

Inodes are of several types: file, directory, special file (pipe, fifo), block device, character device, link etc. For this reason, the operations that an inode needs to implement are different for each type of inode. Below are detailed operations for a [<span class="std std-ref">file type inode</span>](../so2/lab9-filesystems-part2.html#fileinodes) and a [<span class="std std-ref">directory inode</span>](../so2/lab9-filesystems-part2.html#directoryinodes).

The operations of an inode are initialized and accessed using the `i_op` field of the structure `struct inode`.

</div>

</div>

</div>

<div id="the-file-structure" class="section">

## The file structure[¶](#the-file-structure "Permalink to this headline")

The `file` structure corresponds to a file open by a process and exists only in memory, being associated with an inode. It is the closest VFS entity to user-space; the structure fields contain familiar information of a user-space file (access mode, file position, etc.) and the operations with it are performed by known system calls (`read`, `write` , etc.).

The file operations are described by the `struct file_operations` structure.

The file operations for a file system are initialized using the `i_fop` field of the `struct inode` structure. When opening a file, the VFS initializes the `f_op` field of the `struct file` structure with address of `inode->i_fop`, such that subsequent system calls use the value stored in the `file->f_op`.

</div>

<div id="regular-files-inodes" class="section">

<span id="fileinodes"></span>

## Regular files inodes[¶](#regular-files-inodes "Permalink to this headline")

To work with the inode, the `i_op` and `i_fop` fields of the inode structure must be filled in. The type of the inode determines the operations that it needs to implement.

<div id="regular-files-inode-operations" class="section">

<span id="fileoperations"></span>

### Regular files inode operations[¶](#regular-files-inode-operations "Permalink to this headline")

In the `minix` file system, the `minix_file_inode_operations` structure is defined for the operations on an inode and for the file operations the `minix_file_operations` structure is defined:

<div class="highlight-c">

<div class="highlight">

    const struct file_operations minix_file_operations = {
             .llseek         = generic_file_llseek,
             .read_iter      = generic_file_read_iter,
             //...
             .write_iter     = generic_file_write_iter,
             //...
             .mmap           = generic_file_mmap,
             //...
    };
    
    const struct inode_operations minix_file_inode_operations = {
            .setattr        = minix_setattr,
            .getattr        = minix_getattr,
    };
    
            //...
            if (S_ISREG(inode->i_mode)) {
                    inode->i_op = &minix_file_inode_operations;
                    inode->i_fop = &minix_file_operations;
            }
            //...

</div>

</div>

The functions `generic_file_llseek()` , `generic_file_mmap()` , `generic_file_read_iter()` and `generic_file_write_iter()` are implemented in the kernel.

For simple file systems, only the truncation operation (`truncate` system call) must be implemented. Although initially there was a dedicated operation, starting with 3.14 the operation was embedded in `setattr`: if the paste size is different from the current size of the inode, then a truncate operation must be performed. An example of implementing this verification is in the `minix_setattr()` function:

<div class="highlight-c">

<div class="highlight">

    static int minix_setattr(struct dentry *dentry, struct iattr *attr)
    {
            struct inode *inode = d_inode(dentry);
            int error;
    
            error = setattr_prepare(dentry, attr);
            if (error)
                    return error;
    
            if ((attr->ia_valid & ATTR_SIZE) &&
                attr->ia_size != i_size_read(inode)) {
                    error = inode_newsize_ok(inode, attr->ia_size);
                    if (error)
                            return error;
    
                    truncate_setsize(inode, attr->ia_size);
                    minix_truncate(inode);
            }
    
            setattr_copy(inode, attr);
            mark_inode_dirty(inode);
            return 0;
    }

</div>

</div>

The truncate operation involves:

> 
> 
> <div>
> 
>   - freeing blocks of data on the disk that are now extra (if the new dimension is smaller than the old one) or allocating new blocks (for cases where the new dimension is larger)
>   - updating disk bit maps (if used);
>   - updating the inode;
>   - filling with zero the space that was left unused from the last block using the `block_truncate_page()` function.
> 
> </div>

An example of the implementation of the cropping operation is the `minix_truncate()` function in the `minix` file system.

</div>

<div id="address-space-operations" class="section">

<span id="addressspaceoperations"></span>

### Address space operations[¶](#address-space-operations "Permalink to this headline")

There is a close link between the address space of a process and files: the execution of the programs is done almost exclusively by mapping the file into the process address space. Because this approach works very well and is quite general, it can also be used for regular system calls such as `read` and `write`.

The structure that describes the address space is `struct address_space`, and the operations with it are described by the structure `struct address_space_operations`. To initialize the address space operations, fill `inode->i_mapping->a_ops` of the file type inode.

An example is the `minix_aops` structure in the minix file system:

<div class="highlight-c">

<div class="highlight">

    static const struct address_space_operations minix_aops = {
           .readpage = minix_readpage,
           .writepage = minix_writepage,
           .write_begin = minix_write_begin,
           .write_end = generic_write_end,
           .bmap = minix_bmap
    };
    
    //...
    if (S_ISREG(inode->i_mode)) {
          inode->i_mapping->a_ops = &minix_aops;
    }
    //...

</div>

</div>

The `generic_write_end()` function is already implemented. Most of the specific functions are very easy to implement, as follows:

<div class="highlight-c">

<div class="highlight">

    static int minix_writepage(struct page *page, struct writeback_control *wbc)
    {
             return block_write_full_page(page, minix_get_block, wbc);
    }
    
    static int minix_readpage(struct file *file, struct page *page)
    {
             return block_read_full_page(page, minix_get_block);
    }
    
    static void minix_write_failed(struct address_space *mapping, loff_t to)
    {
            struct inode *inode = mapping->host;
    
            if (to > inode->i_size) {
                    truncate_pagecache(inode, inode->i_size);
                    minix_truncate(inode);
            }
    }
    
    static int minix_write_begin(struct file *file, struct address_space *mapping,
                            loff_t pos, unsigned len, unsigned flags,
                            struct page **pagep, void **fsdata)
    {
            int ret;
    
            ret = block_write_begin(mapping, pos, len, flags, pagep,
                                    minix_get_block);
            if (unlikely(ret))
                    minix_write_failed(mapping, pos + len);
    
            return ret;
    }
    
    static sector_t minix_bmap(struct address_space *mapping, sector_t block)
    {
             return generic_block_bmap(mapping, block, minix_get_block);
    }

</div>

</div>

All that needs to be done is to implement `minix_get_block`, which has to translate a block of a file into a block on the device. If the flag `create` received as a parameter is set, a new block must be allocated. In case a new block is created, the bit map must be updated accordingly. To notify the kernel not to read the block from the disk, `bh` must be marked with `set_buffer_new()`. The buffer must be associated with the block through `map_bh()`.

</div>

</div>

<div id="dentry-structure" class="section">

## Dentry structure[¶](#dentry-structure "Permalink to this headline")

Directories operations use the `struct dentry` structure. Its main task is to make links between inodes and filenames. The important fields of this structure are presented below:

<div class="highlight-c">

<div class="highlight">

    struct dentry {
            //...
            struct inode             *d_inode;     /* associated inode */
            //...
            struct dentry            *d_parent;    /* dentry object of parent */
            struct qstr              d_name;       /* dentry name */
            //...
    
            struct dentry_operations *d_op;        /* dentry operations table */
            struct super_block       *d_sb;        /* superblock of file */
            void                     *d_fsdata;    /* filesystem-specific data */
            //...
    };

</div>

</div>

Fields meaning:

> 
> 
> <div>
> 
>   - `d_inode`: the inode referenced by this dentry;
>   - `d_parent`: the dentry associated with the parent directory;
>   - `d_name`: a `struct qstr` structure that contains the fields `name` and `len` (the name and the length of the name).
>   - `d_op`: operations with dentries, represented by the `struct dentry_operations` structure. The kernel implements default operations so there is no need to (re)implement them. Some file systems can do optimizations based on the specific structure of the dentries.
>   - `d_fsdata`: field reserved for the file system that implements dentry operations;
> 
> </div>

<div id="dentry-operations" class="section">

### Dentry operations[¶](#dentry-operations "Permalink to this headline")

The most commonly operations applied to dentries are:

> 
> 
> <div>
> 
>   - `d_make_root`: allocates the root dentry. It is generally used in the function that is called to read the superblock (`fill_super`), which must initialize the root directory. So the root inode is obtained from the superblock and is used as an argument to this function, to fill the `s_root` field from the `struct super_block` structure.
>   - `d_add`: associates a dentry with an inode; the dentry received as a parameter in the calls discussed above signifies the entry (name, length) that needs to be created. This function will be used when creating/loading a new inode that does not have a dentry associated with it and has not yet been introduced to the hash table of inodes (at `lookup`);
>   - `d_instantiate`: The lighter version of the previous call, in which the dentry was previously added in the hash table.
> 
> </div>

<div class="admonition warning">

Warning

`d_instantiate` must be used to implement create calls (`mkdir`, `mknod`, `rename`, `symlink`) and NOT `d_add`.

</div>

</div>

</div>

<div id="directory-inodes-operations" class="section">

<span id="directoryinodes"></span>

## Directory inodes operations[¶](#directory-inodes-operations "Permalink to this headline")

The operations for directory type inodes have a higher complexity level than the ones for files. The developer must define operations for inodes and operations for files. In `minix`, these operations are defined in `minix_dir_inode_operations` and `minix_dir_operations`:

<div class="highlight-c">

<div class="highlight">

    struct inode_operations minix_dir_inode_operations = {
          .create = minix_create,
          .lookup = minix_lookup,
          .link = minix_link,
          .unlink = minix_unlink,
          .symlink = minix_symlink,
          .mkdir = minix_mkdir,
          .rmdir = minix_rmdir,
          .mknod = minix_mknod,
          //...
    };
    
    struct file_operations minix_dir_operations = {
          .llseek = generic_file_llseek,
          .read = generic_read_dir,
          .iterate = minix_readdir,
          //...
    };
    
            //...
          if (S_ISDIR(inode->i_mode)) {
                  inode->i_op = &minix_dir_inode_operations;
                  inode->i_fop = &minix_dir_operations;
                  inode->i_mapping->a_ops = &minix_aops;
          }
           //...

</div>

</div>

The only function already implemented is `generic_read_dir()`.

The functions that implement the operations on directory inodes are the ones described below.

<div id="creating-an-inode" class="section">

### Creating an inode[¶](#creating-an-inode "Permalink to this headline")

The inode creation function is indicated by the field `create` in the `inode_operations` structure. In the minix case, the function is `minix_create()`. This function is called by the `open` and `creat` system calls. Such a function performs the following operations:

> 
> 
> <div>
> 
> 1.  Introduces a new entry into the physical structure on the disk; the update of the bit maps on the disk must not be forgotten.
> 2.  Configures access rights to those received as a parameter.
> 3.  Marks the inode as dirty with the `mark_inode_dirty()` function.
> 4.  Instantiates the directory entry (`dentry`) with the `d_instantiate` function.
> 
> </div>

</div>

<div id="creating-a-directory" class="section">

### Creating a directory[¶](#creating-a-directory "Permalink to this headline")

The directory creation function is indicated by the `mkdir` field in the `inode_operations` structure. In the minix case, the function is `minix_mkdir()`. This function is called by the `mkdir` system call. Such a function performs the following operations:

> 
> 
> <div>
> 
> 1.  Calls `minix_create()`.
> 2.  Allocates a data block for the directory.
> 3.  Creates the `"."` and `".."` entries.
> 
> </div>

</div>

<div id="creating-a-link" class="section">

### Creating a link[¶](#creating-a-link "Permalink to this headline")

The link creation function (hard link) is indicated by the `link` field in the `inode_operations` structure. In the minix case, the function is `minix_link()`. This function is called by the `link` system call. Such a function performs the following operations:

> 
> 
> <div>
> 
>   - Binds the new dentry to the inode.
>   - Increments the `i_nlink` field of the inode.
>   - Marks the inode as dirty using the `mark_inode_dirty()` function.
> 
> </div>

</div>

<div id="creating-a-symbolic-link" class="section">

### Creating a symbolic link[¶](#creating-a-symbolic-link "Permalink to this headline")

The symbolic link creation function is indicated by the `symlink` field in the `inode_operations` structure. In the minix case, the function is `minix_symlink()`. The operations to be performed are similar to `minix_link` with the differences being given by the fact that a symbolic link is created.

</div>

<div id="deleting-a-link" class="section">

### Deleting a link[¶](#deleting-a-link "Permalink to this headline")

The link delete function (hard link) is indicated by the `unlink` field in the `inode_operations` structure. In the minix case, the function is `minix_unlink()`. This function is called by the `unlink` system call. Such a function performs the following operations:

> 
> 
> <div>
> 
> 1.  Deletes the directory entry given as a parameter from the physical disk structure.
> 2.  Decrements the `i_nlink` counter of the inode to which the entry points (otherwise the inode will never be deleted).
> 
> </div>

</div>

<div id="deleting-a-directory" class="section">

### Deleting a directory[¶](#deleting-a-directory "Permalink to this headline")

The directory delete function is indicated by the `rmdir` field in the `inode_operations` structure. In the minix case, the function is `minix_rmdir()`. This function is called by the `rmdir` system call. Such a function performs the following operations:

> 
> 
> <div>
> 
> 1.  Performs the operations done by `minix_unlink`.
> 2.  Ensures that the directory is empty; otherwise, returns `ENOTEMPTY`.
> 3.  Also deletes the data blocks.
> 
> </div>

</div>

<div id="searching-for-an-inode-in-a-directory" class="section">

### Searching for an inode in a directory[¶](#searching-for-an-inode-in-a-directory "Permalink to this headline")

The function that searches for an entry in a directory and extracts the inode is indicated by the `lookup` field in the `inode_operations` structure. In the minix case, the function is `minix_lookup`. This function is called indirectly when information about the inode associated with an entry in a directory is needed. Such a function performs the following operations:

> 
> 
> <div>
> 
> 1.  Searches in the directory indicated by `dir` the entry having the name `dentry->d_name.name`.
> 2.  If the entry is found, it will return `NULL` and associate the inode with the name using the `d_add()` function.
> 3.  Otherwise, returns `ERR_PTR`.
> 
> </div>

</div>

<div id="iterating-through-entries-in-a-directory" class="section">

### Iterating through entries in a directory[¶](#iterating-through-entries-in-a-directory "Permalink to this headline")

The function which iterates through the entries in a directory (lists the directory contents) is indicated by the field `iterate` in the `struct file_operations` structure. In the minix case, the function is `minix_readdir`. This function is called by the `readdir` system call.

The function returns either all entries in the directory or just a part when the buffer allocated for it is not available. A call of this function can return:

> 
> 
> <div>
> 
>   - a number equal to the existing number of entries if there is enough space in the corresponding user space buffer;
>   - a number smaller than the actual number of entries, as much as there was space in the corresponding user space buffer;
>   - `0`, where there are no more entries to read.
> 
> </div>

The function will be called consecutively until all available entries are read. The function is called at least twice.

> 
> 
> <div>
> 
>   - It is only called twice if:
>       - the first call reads all entries and returns their number;
>       - the second call returns 0, having no other entries to read.
>   - It is called more than twice if the first call does not return the total number of entries.
> 
> </div>

The function performs the following operations:

> 
> 
> <div>
> 
> 1.  Iterates over the entries (the dentries) from the current directory.
> 2.  For each dentry found, increments `ctx->pos`.
> 3.  For each valid dentry (an inode other than `0`, for example), calls the `dir_emit()` function.
> 4.  If the `dir_emit()` function returns a value other than zero, it means that the buffer in the user space is full and the function returns.
> 
> </div>

The arguments of the `dir_emit` function are:

> 
> 
> <div>
> 
>   - `ctx` is the directory iteration context, passed as an argument to the `iterate` function;
>   - `name` is the name of the entry (a string of characters);
>   - `name_len` is the length of the entry name;
>   - `ino` is the inode number associated with the entry;
>   - `type` identifies the entry type: `DT_REG` (file), `DT_DIR` (directory), `DT_UNKNOWN` etc. `DT_UNKNOWN` can be used when the entry type is unknown.
> 
> </div>

</div>

</div>

<div id="bitmap-operations" class="section">

<span id="bitmapoperations"></span>

## Bitmap operations[¶](#bitmap-operations "Permalink to this headline")

When working with the file systems, management information (what block is free or busy, what inode is free or busy) is stored using bitmaps. For this we often need to use bit operations. Such operations are:

> 
> 
> <div>
> 
>   - searching the first 0 bit: representing a free block or inode
>   - marking a bit as 1: marking a busy block or inode
> 
> </div>

The bitmap operations are found in headers from `include/asm-generic/bitops`, especially in `find.h` and `atomic.h`. Usual functions, with names indicating their role, are:

> 
> 
> <div>
> 
>   - `find_first_zero_bit()`
>   - `find_first_bit()`
>   - `set_bit()`
>   - `clear_bit()`
>   - `test_and_set_bit()`
>   - `test_and_clear_bit()`
> 
> </div>

These functions usually receive the address of the bitmap, possibly its size (in bytes) and, if necessary, the index of the bit that needs to be activated (set) or deactivated (clear).

Some usage examples are listed below:

<div class="highlight-c">

<div class="highlight">

    unsigned int map;
    unsigned char array_map[NUM_BYTES];
    size_t idx;
    int changed;
    
    /* Find first zero bit in 32 bit integer. */
    idx = find_first_zero_bit(&map, 32);
    printk (KERN_ALERT "The %zu-th bit is the first zero bit.\n", idx);
    
    /* Find first one bit in NUM_BYTES bytes array. */
    idx = find_first_bit(array_map, NUM_BYTES * 8);
    printk (KERN_ALERT "The %zu-th bit is the first one bit.\n", idx);
    
    /*
     * Clear the idx-th bit in integer.
     * It is assumed idx is less the number of bits in integer.
     */
    clear_bit(idx, &map);
    
    /*
     * Test and set the idx-th bit in array.
     * It is assumed idx is less the number of bits in array.
     */
    changed = __test_and_set_bit(idx, &sbi->imap);
    if (changed)
          printk(KERN_ALERT "%zu-th bit changed\n", idx);

</div>

</div>

</div>

<div id="further-reading" class="section">

## Further reading[¶](#further-reading "Permalink to this headline")

1.  Robert Love -- Linux Kernel Development, Second Edition -- Chapter 12. The Virtual Filesystem
2.  Understanding the Linux Kernel, 3rd edition - Chapter 12. The Virtual Filesystem
3.  [Linux Virtual File System (presentation)](http://www.coda.cs.cmu.edu/doc/talks/linuxvfs/)
4.  [Understanding Unix/Linux Filesystem](http://www.cyberciti.biz/tips/understanding-unixlinux-file-system-part-i.html)
5.  [Creating Linux virtual filesystems](http://lwn.net/Articles/57369/)
6.  [The Linux Documentation Project - VFS](http://www.tldp.org/LDP/tlk/fs/filesystem.html)
7.  [The "Virtual File System" in Linux](http://www.linux.it/~rubini/docs/vfs/vfs.html)
8.  [A Linux Filesystem Tutorial](http://inglorion.net/documents/tutorials/tutorfs/)
9.  [The Linux Virtual File System](http://www.win.tue.nl/~aeb/linux/lk/lk-8.html)
10. [Documentation/filesystems/vfs.txt](http://lxr.free-electrons.com/source/Documentation/filesystems/vfs.txt)
11. [File systems sources](http://lxr.free-electrons.com/source/fs/)

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

The current lab name is filesystems. See the exercises for the task name.

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

The modules are placed in /home/root/skels/filesystems/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

<div class="admonition important">

Important

In this lab, we will continue the implementation of the file systems started in the previous one. For this, we will generate the laboratory skeleton using the following command:

<div class="highlight-console">

<div class="highlight">

    TODO=5 LABS=filesystems make skels

</div>

</div>

After this, we will start the implementation from `TODO 5`.

</div>

<div id="myfs" class="section">

### myfs[¶](#myfs "Permalink to this headline")

For the exercises below, we will use the `myfs` file system whose implementation we started with the previous lab. We stopped after mounting the file system and now we will continue with the operations for regular files and directories. At the end of these exercises, we will be able to create, modify and delete regular directories and files.

We will mostly use the `inode` and `dentry` VFS structures. The `inode` structure defines a file (of any type: regular, directory, link), while the `dentry` structure defines a name, which is an entry in a directory.

For this we will access the `myfs` directory in the lab skeleton. The previously generated skeleton contains the solution for the previous lab; we will start from this. As in the previous lab, we will use the `ramfs` file system as a starting point.

<div id="directory-operations" class="section">

#### 1\. Directory operations[¶](#directory-operations "Permalink to this headline")

To begin with, we will implement the operations for working with directories. The operations of creating a file or deleting a file are also directory operations; these operations result in adding or deleting a directory entry (*dentry*).

At the end of this exercise we will be able to create and delete entries in the file system. We will not be able to read and write to regular files; we will do so in the next exercise.

Follow directions marked with `TODO 5` which will guide you through the steps you need to take.

You will need to specify the following directory operations:

> 
> 
> <div>
> 
>   - create a file (`create` function)
>   - search (`lookup` function)
>   - link (`link` function)
>   - create directory (`mkdir` function)
>   - deletion (`rmdir` and `unlink` functions)
>   - create node (`mknod`)
>   - rename (`rename` function)
> 
> </div>

For this, define the `myfs_dir_inode_operations` structure in the code, where marked with `TODO 5`. To begin, just define the structure `myfs_dir_inode_operations`; you will define the structures `myfs_file_operations`, `myfs_file_inode_operations` , and `myfs_aops` in the next exercise.

<div class="admonition tip">

Tip

Read the section [<span class="std std-ref">Directory inodes operations</span>](../so2/lab9-filesystems-part2.html#directoryinodes)

As a model, you are following the `ramfs_dir_inode_operations` structure.

</div>

Implement the `mkdir`, `mknod` and `create` operations inside `myfs_mkdir`, `myfs_mknod` and `myfs_create`. These operations will allow you to create directories and files in the file system.

<div class="admonition tip">

Tip

We recommend making the code modular using a `mknod` function, which you can also use for the next exercise. For inode reading and allocation, use `myfs_get_inode`, which is already implemented.

As a model, follow the next functions implemented in the `ramfs` file system:

> 
> 
> <div>
> 
>   - `ramfs_mknod()`
>   - `ramfs_mkdir()`
>   - `ramfs_create()`
> 
> </div>

</div>

For the other functions, use generic calls (`simple_*`) already defined in VFS.

In the `myfs_get_inode` function, initialize the operations fields of the directory inodes:

> 
> 
> <div>
> 
>   - `i_op` must be initialized to the address of the structure `myfs_dir_inode_operations`;
>   - `i_fop` must be initialized to the address of the structure `simple_dir_operations`, defined in VFS.
> 
> </div>

<div class="admonition note">

Note

`i_op` is a pointer to a structure of type `struct inode_operations` containing operations that have to do with the inode, which are, for a directory, creating a new entry, listing entries, deleting entries, etc.

`i_fop` is a pointer to a structure of type `struct file_operations` containing operations that have to do with the `file` structure associated with the inode, such as `read`, `write`, and `lseek`.

</div>

<div id="testing" class="section">

##### Testing[¶](#testing "Permalink to this headline")

Once the module is done, we can test the creation of files and directories. To do this, we compile the kernel module (using `make build`) and copy the resulting file (`myfs.ko`) and the test scripts (`test-myfs-{1,2}.sh`) in the virtual machine directory (using `make copy`).

<div class="admonition note">

Note

The test scripts are copied to the virtual machine using `make copy` only if they are executable:

<div class="last highlight-console">

<div class="highlight">

    student@workstation:~/linux/tools/labs$ chmod +x skels/filesystems/myfs/test-myfs-*.sh

</div>

</div>

</div>

After starting the virtual machine, insert the module, create the mount point and mount the file system:

<div class="highlight-console">

<div class="highlight">

    # insmod myfs.ko
    # mkdir -p /mnt/myfs
    # mount -t myfs none /mnt/myfs

</div>

</div>

Now we can create file hierarchies and subdirectories in the mounted directory (`/mnt/myfs`). We use commands like the ones below:

<div class="highlight-console">

<div class="highlight">

    # touch /mnt/myfs/peanuts.txt
    # mkdir -p /mnt/myfs/mountain/forest
    # touch /mnt/myfs/mountain/forest/tree.txt
    # rm /mnt/myfs/mountain/forest/tree.txt
    # rmdir /mnt/myfs/mountain/forest

</div>

</div>

At this time we can not read or write files. When running commands such as the following ones we will get errors.

<div class="highlight-console">

<div class="highlight">

    # echo "chocolate" > /mnt/myfs/peanuts.txt
    # cat /mnt/myfs/peanuts.txt

</div>

</div>

This happens because we have not implemented the operations for working with files; we will do so further.

To unload the kernel module, use the command

<div class="highlight-console">

<div class="highlight">

    umount /mnt/myfs
    rmmod myfs

</div>

</div>

To test the functionality provided by the kernel module, we can use the dedicated script `test-myfs-1.sh`. If the implementation is correct, no error messages will be displayed.

</div>

</div>

<div id="file-operations" class="section">

#### 2\. File operations[¶](#file-operations "Permalink to this headline")

We want to implement the operations for working with files, which are used for accessing a file's content: read, write, truncate, etc. For this you will specify the operations described in the structures `struct inode_operations`, `struct file_operations` and `struct address_space_operations`.

Follow the locations marked with `TODO` 6 which will guide you through the steps you need to take.

Start by defining `myfs_file_inode_operations` and `myfs_file_operations`.

<div class="admonition tip">

Tip

Read the section [<span class="std std-ref">Regular files inode operations</span>](../so2/lab9-filesystems-part2.html#fileoperations).

Use the generic function provided by VFS.

An example of implementation is the `ramfs` file system. Follow the implementation of `ramfs_file_inode_operations` and `ramfs_file_operations`.

</div>

Inside the function `myfs_get_inode`, initialize the operations fields for the regular file inodes:

> 
> 
> <div>
> 
>   - `i_op` must be initialized to `myfs_file_inode_operations`;
>   - `i_fop` msust be initialized to `myfs_file_operations`.
> 
> </div>

Continue with defining the structure `myfs_aops`.

<div class="admonition tip">

Tip

Read the section [<span class="std std-ref">Address space operations</span>](../so2/lab9-filesystems-part2.html#addressspaceoperations).

Use the generic functions provided by VFS.

An implementation example is the `ramfs` file system: the `ramfs_aops` structure.

You do not need to define the function of type `set_page_dirty`.

</div>

Initialize the `i_mapping->a_ops` field of the inode structure to `myfs_aops`.

<div id="testing-1" class="section">

##### Testing[¶](#testing-1 "Permalink to this headline")

For testing, we use the steps described in the previous exercise. In addition to those steps, we will now be able to read, write and modify a file using commands like the ones below:

<div class="highlight-console">

<div class="highlight">

    # echo "chocolate" > /mnt/myfs/peanuts.txt
    # cat /mnt/myfs/peanuts.txt

</div>

</div>

To test the functionality provided by the module, we can use the dedicated script:

<div class="highlight-console">

<div class="highlight">

    # ./test-myfs-2.sh

</div>

</div>

If the implementation is correct, no error messages will be displayed when running the above script.

</div>

</div>

</div>

<div id="minfs" class="section">

### minfs[¶](#minfs "Permalink to this headline")

For the exercises below, we will use the minfs file system whose development started in the previous lab. This is a file system with disk support. We stopped after mounting the file system and now we will continue with the operations on regular files and directories. At the end of these exercises we will be able to create and delete entries in the file system.

We will mainly use the `inode` and `dentry` VFS structures. The inode structure defines a file (of any type: regular, directory, link), while the dentry structure defines a name, which is a directory entry.

For this we will access the `minfs/kernel` directory from the laboratory skeleton. The generated skeleton contains the solution from the previous lab; we will start from this. As in the previous lab, we will use the `minix` file system as a starting point.

We will use the formatting tool `mkfs.minfs` in the `minfs/user` directory which is automatically compiled when running `make build` and copied to the virtual machine at `make copy`.

The formatting tool prepares a virtual machine disk using a command like

<div class="highlight-console">

<div class="highlight">

    # ./mkfs.minfs /dev/vdb

</div>

</div>

After formatting, the disk has a structure like the one in the diagram below:

![../\_images/minfs\_arch.png](../_images/minfs_arch.png)

As shown in the diagram, `minfs` is a minimalist file system. `minfs` contains a maximum of 32 inodes, each inode having a single data block (the file size is limited to block size). The super block contains a 32-bit map (`imap`), each bit indicating the use of an inode.

<div class="admonition note">

Note

Before you start working, go through the `minfs/kernel/minfs.h` header file. This file contains the structures and macros that will be used in these exercises. These structures and macros define the file system as described in the diagram above.

</div>

<div id="iterate-operation" class="section">

#### 1\. Iterate operation[¶](#iterate-operation "Permalink to this headline")

At first we want to be able to list the contents of the root directory. For this we must be able to read the entries in the root directory, which means implementing the `iterate` operation. The `iterate` operation is a field within the `minfs_dir_operations` structure (of type `file_operations`) and is implemented by the function `minfs_readdir`. We need to implement this function.

Follow directions marked with `TODO 5` which will guide you through the steps you need to take.

<div class="admonition tip">

Tip

Read the section [<span class="std std-ref">Directory inodes operations</span>](../so2/lab9-filesystems-part2.html#directoryinodes)

As a starting point, follow the `minix_readdir()` function. The function is rather complicated, but it gives you an insight into the steps you have to do.

Follow, in `minfs.c` and `minfs.h`, the definitions of structures `struct minfs_inode_info`, `struct minfs_inode` and `struct minfs_dir_entry`. You will use them in the `minfs_readdir` implementation.

</div>

Obtain the inode and the structure `struct minfs_inode_info` associated with the directory. The structure `struct minfs_inode_info` is useful to find out the directory's data block. From this structure you get the `data_block` field, representing the data block index on the disk.

<div class="admonition tip">

Tip

To get the structure `struct minfs_inode_info` structure, use `list_entry()` or `container_of()`.

</div>

Use `sb_bread()` to read the directory data block.

<div class="admonition tip">

Tip

The data block of the directory is indicated by the `data_block` field of the structure `struct minfs_inode_info` corresponding to the directory.

The data in the block is referenced by the `b_data` field of the `buffer_head` structure (the usual code will be `bh->b_data`). This block (being the data block of a directory) contains an array of at most `MINFS_NUM_ENTRIES` entries of type `struct minfs_dir_entry` (directory entries specific to `minfs`). Use casting to `struct minfs_dir_entry *` to work with the data in the block.

</div>

Iterate over all the entries in the data block and fill the user space buffer inside the `for` loop.

<div class="admonition tip">

Tip

For each index, get the corresponding entry of the `struct minfs_dir_entry` by using pointer arithmetics on the `bh->b_data` field. Ignore dentries that have an `ino` field equal to 0. Such a dentry is a free slot in the director's dentry list.

For each valid entry, there is an existing call `dir_emit()` with the appropriate parameters. This is the call that sends the dentries to the caller (and then to user space).

Check the call examples in `qnx6_readdir()` and `minix_readdir()`.

</div>

<div id="testing-2" class="section">

##### Testing[¶](#testing-2 "Permalink to this headline")

Once the module is done, we can test the listing of the root directory contents. To do this, we compile the kernel module (`make build`) and copy the result to the virtual machine together with the test scripts (`minfs/user/test-minfs-{0,1}.sh`) and the formatting utility (`minfs/user/mkfs.minfs`) using `make copy`, then start the machine.

<div class="admonition note">

Note

The test scripts are copied to the virtual machine only if they are executable:

<div class="last highlight-console">

<div class="highlight">

    student@eg106:~/src/linux/tools/labs$ chmod +x skels/filesystems/minfs/user/test-minfs*.sh

</div>

</div>

</div>

After we start the virtual machine, we format the `/dev/vdb` disk, create the mount point and mount the file system:

<div class="highlight-console">

<div class="highlight">

    # ./mkfs.minfs /dev/vdb
    # mkdir -p /mnt/minfs
    # mount -t minfs /dev/vdb /mnt/minfs

</div>

</div>

Now we can list the contents of the root directory:

<div class="highlight-console">

<div class="highlight">

    # ls -l /mnt/minfs

</div>

</div>

We notice that there is already a file (`a.txt`); it is created by the formatting utility.

We also notice that we are not allowed to display information for a file using the `ls` command. This is because we have not implemented the `lookup` function. We will implement it in the next exercise.

To test the functionality provided by the module, we can use the dedicated script:

<div class="highlight-console">

<div class="highlight">

    # ./test-minfs-0.sh
    # ./test-minfs-1.sh

</div>

</div>

</div>

</div>

<div id="lookup-operation" class="section">

#### 2\. Lookup operation[¶](#lookup-operation "Permalink to this headline")

To properly list the contents of a directory, we need to implement the search functionality, ie the `lookup` operation. The `lookup` operation is a field within the `minfs_dir_inode_operations` structure (of type `inode_operations`) and is implemented by the `minfs_lookup` function. This function (`minfs_lookup`) needs to be implemented. We will actually implement the `minfs_find_entry` function called by `minfs_lookup` .

Follow directions marked with `TODO 6` which will tell you the steps you need to take.

<div class="admonition tip">

Tip

Read the section [<span class="std std-ref">Directory inodes operations</span>](../so2/lab9-filesystems-part2.html#directoryinodes)

As a starting point, read the functions `qnx6_find_entry()` and `minix_find_entry()`.

</div>

In the `minfs_find_entry` function, iterate over the directory where the dentry is: `dentry->d_parent->d_inode`. Iterating means going through the entries in the directory's data block (of type `struct minfs_dir_entry`) and locate, if it exists, the requested entry.

<div class="admonition tip">

Tip

From the structure of type `struct minfs_inode_info` corresponding to the directory, find out the data block index and read it (`sb_read`). You will access the block contents using `bh->b_data`. The directory data block contains an array of at most `MINFS_NUM_ENTRIES` entries of type `struct minfs_dir_entry`. Use pointer arithmetics to get entries of type `struct minfs_dir_entry` from the data block (`bh->b_data`).

Check the presence of the name (stored in the local variable `name`) in the directory (if there is an entry in the data block whose name is a string equal to the given name). Use `strcmp()` to verify.

Ignore dentries that have an `ino` field equal to `0`. Those dentries are free slots in the directory dentry list.

Store in the `final_de` variable the dentry found. If you do not find any dentry, then the `final_de` variable will have the value `NULL`, the value with which it was initialized.

</div>

Comment the `simple_lookup` call in the `minfs_lookup` function to invoke the implementation of `minfs_readdir`.

<div id="testing-3" class="section">

##### Testing[¶](#testing-3 "Permalink to this headline")

For testing, we use the steps described in the previous exercise. The long file listing (`ls -l`) of the contents of a directory (root directory) will display permissions and other file-specific information:

<div class="highlight-console">

<div class="highlight">

    # ls -l /mnt/minfs

</div>

</div>

To test the functionality provided by the module, we can use the dedicated scripts:

<div class="highlight-console">

<div class="highlight">

    # ./test-minfs-0.sh
    # ./test-minfs-1.sh

</div>

</div>

If the implementation is correct, no error messages will be displayed when running the scripts above.

<div class="admonition note">

Note

After mounting the file system using the command

<div class="highlight-console">

<div class="highlight">

    # mount -t minfs /dev/vdb /mnt/minfs

</div>

</div>

we try to create a file using the command

<div class="highlight-console">

<div class="highlight">

    # touch /mnt/minfs/peanuts.txt

</div>

</div>

We notice that we get an error because we did not implement the directory operations that allow us to create a file. We will do this for the next exercise.

</div>

</div>

</div>

<div id="create-operation" class="section">

#### 3\. Create operation[¶](#create-operation "Permalink to this headline")

In order to allow the creation of a file in a directory, we must implement the `create` operation. The `create` operation is a field in the `minfs_dir_inode_operations` structure (of type `inode_operations`) and is implemented by the `minfs_create` function. We need to implement this function. In fact, we will implement the `minfs_new_inode` (which creates and initializes an inode) and `minfs_add_link` which adds a link (or name or *dentry*) for the created inode.

Follow directions marked with `TODO 7` which will guide you through the steps you need to take.

<div class="admonition tip">

Tip

Read the section [<span class="std std-ref">Directory inodes operations</span>](../so2/lab9-filesystems-part2.html#directoryinodes)

Inspect the code in the `minfs_create` and the skeleton of functions `minfs_new_inode` and `minfs_add_link`.

</div>

Implement the function `minfs_new_inode`. Inside this function you will create (using `new_inode()`) and initialize an inode. The initialization is done using the data from disk.

<div class="admonition tip">

Tip

Use the `minix_new_inode()` function as a model. Find the first free inode in imap (`sbi->imap`). Use bitwise operations (`find_first_zero_bit` and `set_bit`). Read the [<span class="std std-ref">Bitmap operations</span>](../so2/lab9-filesystems-part2.html#bitmapoperations) section.

The buffer for the superblock (`sbi->sbh`) must be marked as dirty .

You must initialize the usual fields as it is done for the `myfs` file system. Initialize the `i_mode` field to `0` in the call to `inode_init_owner`. It will be initialized in the caller later.

</div>

Implement the `minfs_add_link` function. The function adds a new dentry (`struct minfs_dir_entry`) to the parent directory data block (`dentry->d_parent->d_inode`).

<div class="admonition tip">

Tip

Use the function `minix_add_link` function as a model.

</div>

In `minfs_add_link` we want to find the first free place for the dentry. For this, you will iterate over the directory data block and you will find the first free entry. A free dentry has the `ino` field equal to `0`.

<div class="admonition tip">

Tip

In order to work with the directory, get the inode of type `struct minfs_inode_info` corresponding to the parent directory (the **dir** inode). Do not use the variable `inode` to get `struct minfs_inode_info`; that inode belongs to the file, not to the parent directory inside which you want to add the link/dentry. To get the `struct minfs_inode_info` structure, use `container_of()`.

The structure `struct minfs_inode_info` is useful for finding the directory data block (the one indicated by the `dentry->d_parent->d_inode`, which is the `dir` variable). From this structure, get the `data_block` field, representing index of the data block on the disk. This block contains the entries in the directory. Use `sb_bread()` to read the block and then `bh->b_data` to refer to the data. The block contains at most `MINFS_NUM_ENTRIES` entries of type `struct minfs_dir_entry`.

If all entries are occupied, return `-ENOSPC`.

Iterate over the entries in the data block using the variable `de` and extract the first free entry (for which the `ino` field is `0`).

When you have found a free place, fill in the corresponding entry:

> 
> 
> <div>
> 
>   - the `inode->i_ino` field in `de->ino`
>   - the `dentry->d_name.name` field in `de->name`
> 
> </div>

Then mark the buffer dirty.

</div>

<div id="testing-4" class="section">

##### Testing[¶](#testing-4 "Permalink to this headline")

For testing, we use the steps described in the previous exercise. Now we can create files within the file system:

<div class="highlight-console">

<div class="highlight">

    # touch /mnt/minfs/peanuts.txt

</div>

</div>

To test the functionality provided by the module, we can use the dedicated script:

<div class="highlight-console">

<div class="highlight">

    # ./test-minfs-2.sh

</div>

</div>

If the deployment is valid, no error messages will be displayed following the above script run.

<div class="admonition note">

Note

The current implementation of the `minfs` file system is not definitive. To be complete, the implementations needs function to delete files, create and delete directories, rename entries, and modify the contents of a file.

</div>

</div>

</div>

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](filesystems_part1.html "File system drivers (Part 1)") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](networking.html "Networking")

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
