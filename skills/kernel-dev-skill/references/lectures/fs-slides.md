<div id="slide_container" class="section slides layout-regular">

## Filesystem Management

  - Filesystem abstractions
  - Filesystem operations
  - Linux VFS
  - Overview of Linux I/O Management

## Filesystem Abstractions

  - superblock
  - file
  - inode
  - dentry

## Filesystem Abstractions - in memory

![../\_images/ditaa-29f54aaa1a85b819ff29cb7d101a4d646b3b0b06.png](../_images/ditaa-29f54aaa1a85b819ff29cb7d101a4d646b3b0b06.png)

## Filesystem Abstractions - on storage

![../\_images/ditaa-bc662dab7bb3d9ba3a37efbf69b82c513dcaadd4.png](../_images/ditaa-bc662dab7bb3d9ba3a37efbf69b82c513dcaadd4.png)

## Simple filesystem example

 

![../\_images/ditaa-8b59fc3f5245ffb5d7089dc80cf2e306c39a62d8.png](../_images/ditaa-8b59fc3f5245ffb5d7089dc80cf2e306c39a62d8.png)

## Overview

![../\_images/ditaa-6d39f541805ae8197b413ec9c79116382abc4dbc.png](../_images/ditaa-6d39f541805ae8197b413ec9c79116382abc4dbc.png)

## Filesystem Operations

  - Mount
  - Open a file
  - Querying file attributes
  - Reading data from a file
  - Writing file to a file
  - Creating a file
  - Deleting a file

## Mounting a filesystem

  - Input: a storage device (partition)
  - Output: dentry pointing to the root directory
  - Steps: check device, determine filesystem parameters, locate the root inode
  - Example: check magic, determine block size, read the root inode and create dentry

## Opening a file

  - Input: path
  - Output: file descriptor
  - Steps:
      - Determine the filesystem type
      - For each name in the path: lookup parent dentry, load inode, load data, find dentry
      - Create a new *file* that points to the last *dentry*
      - Find a free entry in the file descriptor table and set it to *file*

## Querying file attributes

  - Input: path
  - Output: file attributes
  - Steps:
      - Access file-\>dentry-\>inode
      - Read file attributes from the *inode*

## Reading data from a file

  - Input: file descriptor, offset, length
  - Output: data
  - Steps:
      - Access file-\>dentry-\>inode
      - Determine data blocks
      - Copy data blocks to memory

## Writing data to a file

  - Input: file descriptor, offset, length, data
  - Output:
  - Steps:
      - Allocate one or more data blocks
      - Add the allocated blocks to the inode and update file size
      - Copy data from userspace to internal buffers and write them to storage

## Closing a file

  - Input: file descriptor
  - Output:
  - Steps:
      - set the file descriptor entry to NULL
      - Decrement file reference counter
      - When the counter reaches 0 free *file*

## Directories

Directories are special files which contain one or more dentries.

## Creating a file

  - Input: path
  - Output:
  - Steps:
      - Determine the inode directory
      - Read data blocks and find space for a new dentry
      - Write back the modified inode directory data blocks

## Deleting a file

  - Input: path
  - Output:
  - Steps:
      - determine the parent inode
      - read parent inode data blocks
      - find and erase the dentry (check for links)
      - when last file is closed: deallocate data and inode blocks

## Virtual File System

[![../\_images/ditaa-e3a27a84dde42de58bcc5c360e1c4b15062507c2.png](../_images/ditaa-e3a27a84dde42de58bcc5c360e1c4b15062507c2.png)](../_images/ditaa-e3a27a84dde42de58bcc5c360e1c4b15062507c2.png)

## Superblock Operations

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

## Inode Operations

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

## The Inode Cache

  - Caches inodes into memory to avoid costly storage operations
  - An inode is cached until low memory conditions are triggered
  - inodes are indexed with a hash table
  - The inode hash function takes the superblock and inode number as inputs

## The Dentry Cache

  - State:
      - Used – *d\_inode* is valid and the *dentry* object is in use
      - Unused – *d\_inode* is valid but the dentry object is not in use
      - Negative – *d\_inode* is not valid; the inode was not yet loaded or the file was erased
  - Dentry cache
      - List of used dentries (dentry-\>d\_state == used)
      - List of the most recent used dentries (sorted by access time)
      - Hash table to avoid searching the tree

## The Page Cache

  - Caches file data and not block device data
  - Uses the `struct address_space` to translate file offsets to block offsets
  - Used for both read / write and mmap
  - Uses a radix tree

## struct address\_space

<div class="highlight-c">

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

## Reading data

<div class="highlight-c">

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

<div id="slide_notes" class="section">

</div>
