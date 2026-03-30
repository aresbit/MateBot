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
  - [Block Device Drivers](#)
      - [Lab objectives](#lab-objectives)
      - [Overview](#overview)
      - [Register a block I/O device](#register-a-block-i-o-device)
      - [Register a disk](#register-a-disk)
      - [`struct gendisk` structure](#struct-gendisk-structure)
      - [`struct block_device_operations` structure](#struct-block-device-operations-structure)
      - [Request Queues - Multi-Queue Block Layer](#request-queues-multi-queue-block-layer)
          - [Software staging queues](#software-staging-queues)
          - [Hardware dispatch queues](#hardware-dispatch-queues)
          - [Tag sets](#tag-sets)
          - [Create and delete a request queue](#create-and-delete-a-request-queue)
          - [Useful functions for processing request queues](#useful-functions-for-processing-request-queues)
      - [Requests for block devices](#requests-for-block-devices)
          - [Create a request](#create-a-request)
          - [Process a request](#process-a-request)
      - [`struct bio` structure](#struct-bio-structure)
          - [Create a `struct bio` structure](#create-a-struct-bio-structure)
          - [Submit a `struct bio` structure](#submit-a-struct-bio-structure)
          - [Wait for the completion of a `struct bio` structure](#wait-for-the-completion-of-a-struct-bio-structure)
          - [Initialize a `struct bio` structure](#initialize-a-struct-bio-structure)
          - [How to use the content of a `struct bio` structure](#how-to-use-the-content-of-a-struct-bio-structure)
          - [Free a `struct bio` structure](#free-a-struct-bio-structure)
          - [Set up a request queue at `struct bio` level](#set-up-a-request-queue-at-struct-bio-level)
      - [Further reading](#further-reading)
      - [Exercises](#exercises)
          - [0. Intro](#intro)
          - [1. Block device](#block-device)
          - [2. Disk registration](#disk-registration)
          - [3. RAM disk](#ram-disk)
          - [4. Read data from the disk](#read-data-from-the-disk)
          - [5. Write data to the disk](#write-data-to-the-disk)
          - [6. Processing requests from the request queue at `struct bio` level](#processing-requests-from-the-request-queue-at-struct-bio-level)
  - [File system drivers (Part 1)](filesystems_part1.html)
  - [File system drivers (Part 2)](filesystems_part2.html)
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
  - Block Device Drivers
  - [View page source](../_sources/labs/block_device_drivers.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="block-device-drivers" class="section">

# Block Device Drivers[¶](#block-device-drivers "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

> 
> 
> <div>
> 
>   - acquiring knowledge about the behavior of the I/O subsystem on Linux
>   - hands-on activities in structures and functions of block devices
>   - acquiring basic skills for utilizing the API for block devices, by solving exercises
> 
> </div>

</div>

<div id="overview" class="section">

## Overview[¶](#overview "Permalink to this headline")

Block devices are characterized by random access to data organized in fixed-size blocks. Examples of such devices are hard drives, CD-ROM drives, RAM disks, etc. The speed of block devices is generally much higher than the speed of character devices, and their performance is also important. This is why the Linux kernel handles differently these 2 types of devices (it uses a specialized API).

Working with block devices is therefore more complicated than working with character devices. Character devices have a single current position, while block devices must be able to move to any position in the device to provide random access to data. To simplify work with block devices, the Linux kernel provides an entire subsystem called the block I/O (or block layer) subsystem.

From the kernel perspective, the smallest logical unit of addressing is the block. Although the physical device can be addressed at sector level, the kernel performs all disk operations using blocks. Since the smallest unit of physical addressing is the sector, the size of the block must be a multiple of the size of the sector. Additionally, the block size must be a power of 2 and can not exceed the size of a page. The size of the block may vary depending on the file system used, the most common values being 512 bytes, 1 kilobytes and 4 kilobytes.

</div>

<div id="register-a-block-i-o-device" class="section">

## Register a block I/O device[¶](#register-a-block-i-o-device "Permalink to this headline")

To register a block I/O device, function `register_blkdev()` is used. To deregister a block I/O device, function `unregister_blkdev()` is used.

Starting with version 4.9 of the Linux kernel, the call to `register_blkdev()` is optional. The only operations performed by this function are the dynamic allocation of a major (if the major argument is 0 when calling the function) and creating an entry in `/proc/devices`. In future kernel versions it may be removed; however, most drivers still call it.

Usually, the call to the register function is performed in the module initialization function, and the call to the deregister function is performed in the module exit function. A typical scenario is presented below:

<div class="highlight-c">

<div class="highlight">

    #include <linux/fs.h>
    
    #define MY_BLOCK_MAJOR           240
    #define MY_BLKDEV_NAME          "mybdev"
    
    static int my_block_init(void)
    {
        int status;
    
        status = register_blkdev(MY_BLOCK_MAJOR, MY_BLKDEV_NAME);
        if (status < 0) {
                 printk(KERN_ERR "unable to register mybdev block device\n");
                 return -EBUSY;
         }
         //...
    }
    
    static void my_block_exit(void)
    {
         //...
         unregister_blkdev(MY_BLOCK_MAJOR, MY_BLKDEV_NAME);
    }

</div>

</div>

</div>

<div id="register-a-disk" class="section">

## Register a disk[¶](#register-a-disk "Permalink to this headline")

Although the `register_blkdev()` function obtains a major, it does not provide a device (disk) to the system. For creating and using block devices (disks), a specialized interface defined in `linux/genhd.h` is used.

The useful functions defined in `linux/genhd.h` are to register /allocate a disk, add it to the system, and de-register /unmount the disk.

The `alloc_disk()` function is used to allocate a disk, and the `del_gendisk()` function is used to deallocate it. Adding the disk to the system is done using the `add_disk()` function.

The `alloc_disk()` and `add_disk()` functions are typically used in the module initialization function, and the `del_gendisk()` function in the module exit function.

<div class="highlight-c">

<div class="highlight">

    #include <linux/fs.h>
    #include <linux/genhd.h>
    
    #define MY_BLOCK_MINORS       1
    
    static struct my_block_dev {
        struct gendisk *gd;
        //...
    } dev;
    
    static int create_block_device(struct my_block_dev *dev)
    {
        dev->gd = alloc_disk(MY_BLOCK_MINORS);
        //...
        add_disk(dev->gd);
    }
    
    static int my_block_init(void)
    {
        //...
        create_block_device(&dev);
    }
    
    static void delete_block_device(struct my_block_dev *dev)
    {
        if (dev->gd)
            del_gendisk(dev->gd);
        //...
    }
    
    static void my_block_exit(void)
    {
        delete_block_device(&dev);
        //...
    }

</div>

</div>

As with character devices, it is recommended to use `my_block_dev` structure to store important elements describing the block device.

Note that immediately after calling the `add_disk()` function (actually even during the call), the disk is active and its methods can be called at any time. As a result, this function should not be called before the driver is fully initialized and ready to respond to requests for the registered disk.

It can be noticed that the basic structure in working with block devices (disks) is the `struct gendisk` structure.

After a call to `del_gendisk()`, the `struct gendisk` structure may continue to exist (and the device operations may still be called) if there are still users (an open operation was called on the device but the associated release operation has not been called). One solution is to keep the number of users of the device and call the `del_gendisk()` function only when there are no users left of the device.

</div>

<div id="struct-gendisk-structure" class="section">

## `struct gendisk` structure[¶](#struct-gendisk-structure "Permalink to this headline")

The `struct gendisk` structure stores information about a disk. As stated above, such a structure is obtained from the `alloc_disk()` call and its fields must be filled before it is sent to the `add_disk()` function.

The `struct gendisk` structure has the following important fields:

> 
> 
> <div>
> 
>   - `major`, `first_minor`, `minor`, describing the identifiers used by the disk; a disk must have at least one minor; if the disk allows the partitioning operation, a minor must be allocated for each possible partition
>   - `disk_name`, which represents the disk name as it appears in `/proc/partitions` and in sysfs (`/sys/block`)
>   - `fops`, representing operations associated with the disk
>   - `queue`, which represents the queue of requests
>   - `capacity`, which is disk capacity in 512 byte sectors; it is initialized using the `set_capacity()` function
>   - `private_data`, which is a pointer to private data
> 
> </div>

An example of filling a `struct gendisk` structure is presented below:

<div class="highlight-c">

<div class="highlight">

    #include <linux/genhd.h>
    #include <linux/fs.h>
    #include <linux/blkdev.h>
    
    #define NR_SECTORS                   1024
    
    #define KERNEL_SECTOR_SIZE           512
    
    static struct my_block_dev {
        //...
        spinlock_t lock;                /* For mutual exclusion */
        struct request_queue *queue;    /* The device request queue */
        struct gendisk *gd;             /* The gendisk structure */
        //...
    } dev;
    
    static int create_block_device(struct my_block_dev *dev)
    {
        ...
        /* Initialize the gendisk structure */
        dev->gd = alloc_disk(MY_BLOCK_MINORS);
        if (!dev->gd) {
            printk (KERN_NOTICE "alloc_disk failure\n");
            return -ENOMEM;
        }
    
        dev->gd->major = MY_BLOCK_MAJOR;
        dev->gd->first_minor = 0;
        dev->gd->fops = &my_block_ops;
        dev->gd->queue = dev->queue;
        dev->gd->private_data = dev;
        snprintf (dev->gd->disk_name, 32, "myblock");
        set_capacity(dev->gd, NR_SECTORS);
    
        add_disk(dev->gd);
    
        return 0;
    }
    
    static int my_block_init(void)
    {
        int status;
        //...
        status = create_block_device(&dev);
        if (status < 0)
            return status;
        //...
    }
    
    static void delete_block_device(struct my_block_dev *dev)
    {
        if (dev->gd) {
            del_gendisk(dev->gd);
        }
        //...
    }
    
    static void my_block_exit(void)
    {
        delete_block_device(&dev);
        //...
    }

</div>

</div>

As stated before, the kernel considers a disk as a vector of 512 byte sectors. In reality, the devices may have a different size of the sector. To work with these devices, the kernel needs to be informed about the real size of a sector, and for all operations the necessary conversions must be made.

To inform the kernel about the device sector size, a parameter of the request queue must be set just after the request queue is allocated, using the `blk_queue_logical_block_size()` function. All requests generated by the kernel will be multiple of this sector size and will be aligned accordingly. However, communication between the device and the driver will still be performed in sectors of 512 bytes in size, so conversion should be done each time (an example of such conversion is when calling the `set_capacity()` function in the code above).

</div>

<div id="struct-block-device-operations-structure" class="section">

## `struct block_device_operations` structure[¶](#struct-block-device-operations-structure "Permalink to this headline")

Just as for a character device, operations in `struct file_operations` should be completed, so for a block device, the operations in `struct block_device_operations` should be completed. The association of operations is done through the `fops` field in the `struct gendisk` structure.

Some of the fields of the `struct block_device_operations` structure are presented below:

<div class="highlight-c">

<div class="highlight">

    struct block_device_operations {
        int (*open) (struct block_device *, fmode_t);
        int (*release) (struct gendisk *, fmode_t);
        int (*locked_ioctl) (struct block_device *, fmode_t, unsigned,
                             unsigned long);
        int (*ioctl) (struct block_device *, fmode_t, unsigned, unsigned long);
        int (*compat_ioctl) (struct block_device *, fmode_t, unsigned,
                             unsigned long);
        int (*direct_access) (struct block_device *, sector_t,
                              void **, unsigned long *);
        int (*media_changed) (struct gendisk *);
        int (*revalidate_disk) (struct gendisk *);
        int (*getgeo)(struct block_device *, struct hd_geometry *);
        blk_qc_t (*submit_bio) (struct bio *bio);
        struct module *owner;
    }

</div>

</div>

`open()` and `release()` operations are called directly from user space by utilities that may perform the following tasks: partitioning, file system creation, file system verification. In a `mount()` operation, the `open()` function is called directly from the kernel space, the file descriptor being stored by the kernel. A driver for a block device can not differentiate between `open()` calls performed from user space and kernel space.

An example of how to use these two functions is given below:

<div class="highlight-c">

<div class="highlight">

    #include <linux/fs.h>
    #include <linux/genhd.h>
    
    static struct my_block_dev {
        //...
        struct gendisk * gd;
        //...
    } dev;
    
    static int my_block_open(struct block_device *bdev, fmode_t mode)
    {
        //...
    
        return 0;
    }
    
    static int my_block_release(struct gendisk *gd, fmode_t mode)
    {
        //...
    
        return 0;
    }
    
    struct block_device_operations my_block_ops = {
        .owner = THIS_MODULE,
        .open = my_block_open,
        .release = my_block_release
    };
    
    static int create_block_device(struct my_block_dev *dev)
    {
        //....
        dev->gd->fops = &my_block_ops;
        dev->gd->private_data = dev;
        //...
    }

</div>

</div>

Please notice that there are no read or write operations. These operations are performed by the `request()` function associated with the request queue of the disk.

</div>

<div id="request-queues-multi-queue-block-layer" class="section">

## Request Queues - Multi-Queue Block Layer[¶](#request-queues-multi-queue-block-layer "Permalink to this headline")

Drivers for block devices use queues to store the block I/O requests that will be processed. A request queue is represented by the `struct request_queue` structure. The request queue is made up of a double-linked list of requests and their associated control information. The requests are added to the queue by higher-level kernel code (for example, file systems).

The block device driver associates each queue with a handling function, which will be called for each request in the queue (the `struct request` structure).

In earlier version of the Linux kernel, each device driver had associated one or more request queues (`struct request_queue`), where any client could add requests, while also being able to reorder them. The problem with this approach is that it requires a per-queue lock, making it inefficient in distributed systems.

The [Multi-Queue Block Queing Mechanism](https://www.kernel.org/doc/html/latest/block/blk-mq.html) solves this issue by splitting the device driver queue in two parts:

> 
> 
> <div>
> 
> 1.  Software staging queues
> 2.  Hardware dispatch queues
> 
> </div>

<div id="software-staging-queues" class="section">

### Software staging queues[¶](#software-staging-queues "Permalink to this headline")

The staging queues hold requests from the clients before sending them to the block device driver. To prevent the waiting for a per-queue lock, a staging queue is allocated for each CPU or node. A software queue is associated to only one hardware queue.

While in this queue, the requests can be merged or reordered, according to an I/O Scheduler, in order to maximize performance. This means that only the requests coming from the same CPU or node can be optimized.

Staging queues are usually not used by the block device drivers, but only internally by the I/O subsystem to optimize requests before sending them to the device drivers.

</div>

<div id="hardware-dispatch-queues" class="section">

### Hardware dispatch queues[¶](#hardware-dispatch-queues "Permalink to this headline")

The hardware queues (`struct blk_mq_hw_ctx`) are used to send the requests from the staging queues to the block device driver. Once in this queue, the requests can't be merged or reordered.

Depending on the underlying hardware, a block device driver can create multiple hardware queues in order to improve parallelism and maximize performance.

</div>

<div id="tag-sets" class="section">

### Tag sets[¶](#tag-sets "Permalink to this headline")

A block device driver can accept a request before the previous one is completed. As a consequence, the upper layers need a way to know when a request is completed. For this, a "tag" is added to each request upon submission and sent back using a completion notification after the request is completed.

The tags are part of a tag set (`struct blk_mq_tag_set`), which is unique to a device. The tag set structure is allocated and initialized before the request queues and also stores some of the queues properties.

<div class="highlight-c">

<div class="highlight">

    struct blk_mq_tag_set {
      ...
      const struct blk_mq_ops   *ops;
      unsigned int               nr_hw_queues;
      unsigned int               queue_depth;
      unsigned int               cmd_size;
      int                        numa_node;
      void                      *driver_data;
      struct blk_mq_tags       **tags;
      struct list_head           tag_list;
      ...
    };

</div>

</div>

Some of the fields in `struct blk_mq_tag_set` are:

> 
> 
> <div>
> 
>   - `ops` - Queue operations, most notably the request handling function.
>   - `nr_hw_queues` - The number of hardware queues allocated for the device
>   - `queue_depth` - Hardware queues size
>   - `cmd_size` - Number of extra bytes allocated at the end of the device, to be used by the block device driver, if needed.
>   - `numa_node` - In NUMA systems, the index of the node the storage device is connected to.
>   - `driver_data` - Data private to the driver, if needed.
>   - `tags` - Pointer to an array of `nr_hw_queues` tag sets.
>   - `tag_list` - List of request queues using this tag set.
> 
> </div>

</div>

<div id="create-and-delete-a-request-queue" class="section">

### Create and delete a request queue[¶](#create-and-delete-a-request-queue "Permalink to this headline")

Request queues are created using the `blk_mq_init_queue()` function and are deleted using `blk_cleanup_queue()`. The first function creates both the hardware and the software queues and initializes their structures.

Queue properties, including the number of hardware queues, their capacity and request handling function are configured using the `blk_mq_tag_set` structure, as described above.

An example of using these functions is as follows:

<div class="highlight-c">

<div class="highlight">

    #include <linux/fs.h>
    #include <linux/genhd.h>
    #include <linux/blkdev.h>
    
    static struct my_block_dev {
        //...
        struct blk_mq_tag_set tag_set;
        struct request_queue *queue;
        //...
    } dev;
    
    static blk_status_t my_block_request(struct blk_mq_hw_ctx *hctx,
                                         const struct blk_mq_queue_data *bd)
    //...
    
    static struct blk_mq_ops my_queue_ops = {
       .queue_rq = my_block_request,
    };
    
    static int create_block_device(struct my_block_dev *dev)
    {
        /* Initialize tag set. */
        dev->tag_set.ops = &my_queue_ops;
        dev->tag_set.nr_hw_queues = 1;
        dev->tag_set.queue_depth = 128;
        dev->tag_set.numa_node = NUMA_NO_NODE;
        dev->tag_set.cmd_size = 0;
        dev->tag_set.flags = BLK_MQ_F_SHOULD_MERGE;
        err = blk_mq_alloc_tag_set(&dev->tag_set);
        if (err) {
            goto out_err;
        }
    
        /* Allocate queue. */
        dev->queue = blk_mq_init_queue(&dev->tag_set);
        if (IS_ERR(dev->queue)) {
            goto out_blk_init;
        }
    
        blk_queue_logical_block_size(dev->queue, KERNEL_SECTOR_SIZE);
    
         /* Assign private data to queue structure. */
        dev->queue->queuedata = dev;
        //...
    
    out_blk_init:
        blk_mq_free_tag_set(&dev->tag_set);
    out_err:
        return -ENOMEM;
    }
    
    static int my_block_init(void)
    {
        int status;
        //...
        status = create_block_device(&dev);
        if (status < 0)
            return status;
        //...
    }
    
    static void delete_block_device(struct block_dev *dev)
    {
        //...
        blk_cleanup_queue(dev->queue);
        blk_mq_free_tag_set(&dev->tag_set);
    }
    
    static void my_block_exit(void)
    {
        delete_block_device(&dev);
        //...
    }

</div>

</div>

After initializing the tag set structure, the tag lists are allocated using the `blk_mq_alloc_tag_set()` function. The pointer to the function which will process the requests (`my_block_request()`) is filled in the `my_queue_ops` structure and then the pointer to this structure is added to the tag set.

The queue is created using the `blk_mq_init_queue()` function, based on the information added in the tag set.

As part of the request queue initialization, you can configure the `queuedata` field, which is equivalent to the `private_data` field in other structures.

</div>

<div id="useful-functions-for-processing-request-queues" class="section">

### Useful functions for processing request queues[¶](#useful-functions-for-processing-request-queues "Permalink to this headline")

The `queue_rq` function from `struct blk_mq_ops` is used to handle requests for working with the block device. This function is the equivalent of read and write functions encountered on character devices. The function receives the requests for the device as arguments and can use various functions for processing them.

The functions used to process the requests in the handler are described below:

> 
> 
> <div>
> 
>   - `blk_mq_start_request()` - must be called before starting processing a request;
>   - `blk_mq_requeue_request()` - to re-send the request in the queue;
>   - `blk_mq_end_request()` - to end request processing and notify the upper layers.
> 
> </div>

</div>

</div>

<div id="requests-for-block-devices" class="section">

## Requests for block devices[¶](#requests-for-block-devices "Permalink to this headline")

A request for a block device is described by `struct request` structure.

The fields of `struct request` structure include:

> 
> 
> <div>
> 
>   - `cmd_flags`: a series of flags including direction (reading or writing); to find out the direction, the macrodefinition `rq_data_dir` is used, which returns 0 for a read request and 1 for a write request on the device;
>   - `__sector`: the first sector of the transfer request; if the device sector has a different size, the appropriate conversion should be done. To access this field, use the `blk_rq_pos` macro;
>   - `__data_len`: the total number of bytes to be transferred; to access this field the `blk_rq_bytes` macro is used;
>   - generally, data from the current `struct bio` will be transferred; the data size is obtained using the `blk_rq_cur_bytes` macro;
>   - `bio`, a dynamic list of `struct bio` structures that is a set of buffers associated to the request; this field is accessed by macrodefinition `rq_for_each_segment` if there are multiple buffers, or by `bio_data` macrodefinition in case there is only one associated buffer;
> 
> </div>

We will discuss more about the `struct bio` structure and its associated operations in the <span class="xref std std-ref">bio\_structure</span> section.

<div id="create-a-request" class="section">

### Create a request[¶](#create-a-request "Permalink to this headline")

Read /write requests are created by code layers superior to the kernel I/O subsystem. Typically, the subsystem that creates requests for block devices is the file management subsystem. The I/O subsystem acts as an interface between the file management subsystem and the block device driver. The main operations under the responsibility of the I/O subsystem are adding requests to the queue of the specific block device and sorting and merging requests according to performance considerations.

</div>

<div id="process-a-request" class="section">

### Process a request[¶](#process-a-request "Permalink to this headline")

The central part of a block device driver is the request handling function (`queue_rq`). In previous examples, the function that fulfilled this role was `my_block_request()`. As stated in the [Create and delete a request queue](#create-and-delete-a-request-queue) section, this function is associated to the driver when creating the tag set structure.

This function is called when the kernel considers that the driver should process I/O requests. The function must start processing the requests from the queue, but it is not mandatory to finish them, as requests may be finished by other parts of the driver.

The request function runs in an atomic context and must follow the rules for atomic code (it does not need to call functions that can cause sleep, etc.).

Calling the function that processes the requests is asynchronous relative to the actions of any userspace process and no assumptions about the process in which the respective function is running should be made. Also, it should not be assumed that the buffer provided by a request is from kernel space or user space, any operation that accesses the userspace being erroneous.

One of the simplest request handling function is presented below:

<div class="highlight-c">

<div class="highlight">

    static blk_status_t my_block_request(struct blk_mq_hw_ctx *hctx,
                                         const struct blk_mq_queue_data *bd)
    {
        struct request *rq = bd->rq;
        struct my_block_dev *dev = q->queuedata;
    
        blk_mq_start_request(rq);
    
        if (blk_rq_is_passthrough(rq)) {
            printk (KERN_NOTICE "Skip non-fs request\n");
            blk_mq_end_request(rq, BLK_STS_IOERR);
            goto out;
        }
    
        /* do work */
        ...
    
        blk_mq_end_request(rq, BLK_STS_OK);
    
    out:
        return BLK_STS_OK;
    }

</div>

</div>

The `my_block_request()` function performs the following operations:

> 
> 
> <div>
> 
>   - Get a pointer to the request structure from the `bd` argument and start its processing using the `blk_mq_start_request()` function.
>   - A block device can receive calls which do not transfer data blocks (e.g. low level operations on the disk, instructions referring to special ways of accessing the device). Most drivers do not know how to handle these requests and return an error.
>   - To return an error, `blk_mq_end_request()` function is called, `BLK_STS_IOERR` being the second argument.
>   - The request is processed according to the needs of the associated device.
>   - The request ends. In this case, `blk_mq_end_request()` function is called in order to complete the request.
> 
> </div>

</div>

</div>

<div id="struct-bio-structure" class="section">

## `struct bio` structure[¶](#struct-bio-structure "Permalink to this headline")

Each `struct request` structure is an I/O block request, but may come from combining more independent requests from a higher level. The sectors to be transferred for a request can be scattered into the main memory but they always correspond to a set of consecutive sectors on the device. The request is represented as a series of segments, each corresponding to a buffer in memory. The kernel can combine requests that refer to adjacent sectors but will not combine write requests with read requests into a single `struct request` structure.

A `struct request` structure is implemented as a linked list of `struct bio` structures together with information that allows the driver to retain its current position while processing the request.

The `struct bio` structure is a low-level description of a portion of a block I/O request.

<div class="highlight-c">

<div class="highlight">

    struct bio {
        //...
        struct gendisk          *bi_disk;
        unsigned int            bi_opf;         /* bottom bits req flags, top bits REQ_OP. Use accessors. */
        //...
        struct bio_vec          *bi_io_vec;     /* the actual vec list */
        //...
        struct bvec_iter        bi_iter;
        /...
        void                    *bi_private;
        //...
    };

</div>

</div>

In turn, the `struct bio` structure contains a `bi_io_vec` vector of `struct bio_vec` structures. It consists of the individual pages in the physical memory to be transferred, the offset within the page and the size of the buffer. To iterate through a `struct bio` structure, we need to iterate through the vector of `struct bio_vec` and transfer the data from every physical page. To simplify vector iteration, the `struct bvec_iter` structure is used. This structure maintains information about how many buffers and sectors were consumed during the iteration. The request type is encoded in the `bi_opf` field; to determine it, use the `bio_data_dir()` function.

<div id="create-a-struct-bio-structure" class="section">

### Create a `struct bio` structure[¶](#create-a-struct-bio-structure "Permalink to this headline")

Two functions can be used to create a `struct bio` structure:

> 
> 
> <div>
> 
>   - `bio_alloc()`: allocates space for a new structure; the structure must be initialized;
>   - `bio_clone()`: makes a copy of an existing `struct bio` structure; the newly obtained structure is initialized with the values of the cloned structure fields; the buffers are shared with the `struct bio` structure that has been cloned so that access to the buffers has to be done carefully to avoid access to the same memory area from the two clones;
> 
> </div>

Both functions return a new `struct bio` structure.

</div>

<div id="submit-a-struct-bio-structure" class="section">

### Submit a `struct bio` structure[¶](#submit-a-struct-bio-structure "Permalink to this headline")

Usually, a `struct bio` structure is created by the higher levels of the kernel (usually the file system). A structure thus created is then transmitted to the I/O subsystem that gathers more `struct bio` structures into a request.

For submitting a `struct bio` structure to the associated I/O device driver, the `submit_bio()` function is used. The function receives as argument an initialized `struct bio` structure that will be added to a request from the request queue of an I/O device. From that queue, it can be processed by the I/O device driver using a specialized function.

</div>

<div id="wait-for-the-completion-of-a-struct-bio-structure" class="section">

<span id="bio-completion"></span>

### Wait for the completion of a `struct bio` structure[¶](#wait-for-the-completion-of-a-struct-bio-structure "Permalink to this headline")

Submitting a `struct bio` structure to a driver has the effect of adding it to a request from the request queue from where it will be further processed. Thus, when the `submit_bio()` function returns, it is not guaranteed that the processing of the structure has finished. If you want to wait for the processing of the request to be finished, use the `submit_bio_wait()` function.

To be notified when the processing of a `struct bio` structure ends (when we do not use `submit_bio_wait()` function), the `bi_end_io` field of the structure should be used. This field specifies the function that will be called at the end of the `struct bio` structure processing. You can use the `bi_private` field of the structure to pass information to the function.

</div>

<div id="initialize-a-struct-bio-structure" class="section">

### Initialize a `struct bio` structure[¶](#initialize-a-struct-bio-structure "Permalink to this headline")

Once a `struct bio` structure has been allocated and before being transmitted, it must be initialized.

Initializing the structure involves filling in its important fields. As mentioned above, the `bi_end_io` field is used to specify the function called when the processing of the structure is finished. The `bi_private` field is used to store useful data that can be accessed in the function pointed by `bi_end_io`.

The `bi_opf` field specifies the type of operation.

<div class="highlight-c">

<div class="highlight">

    struct bio *bio = bio_alloc(GFP_NOIO, 1);
    //...
    bio->bi_disk = bdev->bd_disk;
    bio->bi_iter.bi_sector = sector;
    bio->bi_opf = REQ_OP_READ;
    bio_add_page(bio, page, size, offset);
    //...

</div>

</div>

In the code snippet above we specified the block device to which we sent the following: `struct bio` structure, startup sector, operation (`REQ_OP_READ` or `REQ_OP_WRITE`) and content. The content of a `struct bio` structure is a buffer described by: a physical page, the offset in the page and the size of the bufer. A page can be assigned using the `alloc_page()` call.

<div class="admonition note">

Note

The `size` field of the `bio_add_page()` call must be a multiple of the device sector size.

</div>

</div>

<div id="how-to-use-the-content-of-a-struct-bio-structure" class="section">

<span id="bio-content"></span>

### How to use the content of a `struct bio` structure[¶](#how-to-use-the-content-of-a-struct-bio-structure "Permalink to this headline")

To use the content of a `struct bio` structure, the structure's support pages must be mapped to the kernel address space from where they can be accessed. For mapping /unmapping, use the `kmap_atomic` and the `kunmap_atomic` macros.

A typical example of use is:

<div class="highlight-c">

<div class="highlight">

    static void my_block_transfer(struct my_block_dev *dev, size_t start,
                                  size_t len, char *buffer, int dir);
    
    
    static int my_xfer_bio(struct my_block_dev *dev, struct bio *bio)
    {
        struct bio_vec bvec;
        struct bvec_iter i;
        int dir = bio_data_dir(bio);
    
        /* Do each segment independently. */
        bio_for_each_segment(bvec, bio, i) {
            sector_t sector = i.bi_sector;
            char *buffer = kmap_atomic(bvec.bv_page);
            unsigned long offset = bvec.bv_offset;
            size_t len = bvec.bv_len;
    
            /* process mapped buffer */
            my_block_transfer(dev, sector, len, buffer + offset, dir);
    
            kunmap_atomic(buffer);
        }
    
        return 0;
    }

</div>

</div>

As it can be seen from the example above, iterating through a `struct bio` requires iterating through all of its segments. A segment (`struct bio_vec`) is defined by the physical address page, the offset in the page and its size.

To simplify the processing of a `struct bio`, use the `bio_for_each_segment` macrodefinition. It will iterate through all segments, and will also update global information stored in an iterator (`struct bvec_iter`) such as the current sector as well as other internal information (segment vector index, number of bytes left to be processed, etc.) .

You can store information in the mapped buffer, or extract information.

In case request queues are used and you needed to process the requests at `struct bio` level, use the `rq_for_each_segment` macrodefinition instead of the `bio_for_each_segment` macrodefinition. This macrodefinition iterates through each segment of each `struct bio` structure of a `struct request` structure and updates a `struct req_iterator` structure. The `struct req_iterator` contains the current `struct bio` structure and the iterator that traverses its segments.

A typical example of use is:

<div class="highlight-c">

<div class="highlight">

    struct bio_vec bvec;
    struct req_iterator iter;
    
    rq_for_each_segment(bvec, req, iter) {
        sector_t sector = iter.iter.bi_sector;
        char *buffer = kmap_atomic(bvec.bv_page);
        unsigned long offset = bvec.bv_offset;
        size_t len = bvec.bv_len;
        int dir = bio_data_dir(iter.bio);
    
        my_block_transfer(dev, sector, len, buffer + offset, dir);
    
        kunmap_atomic(buffer);
    }

</div>

</div>

</div>

<div id="free-a-struct-bio-structure" class="section">

### Free a `struct bio` structure[¶](#free-a-struct-bio-structure "Permalink to this headline")

Once a kernel subsystem uses a `struct bio` structure, it will have to release the reference to it. This is done by calling `bio_put()` function.

</div>

<div id="set-up-a-request-queue-at-struct-bio-level" class="section">

### Set up a request queue at `struct bio` level[¶](#set-up-a-request-queue-at-struct-bio-level "Permalink to this headline")

We have previously seen how we can specify a function to be used to process requests sent to the driver. The function receives as argument the requests and carries out processing at `struct request` level.

If, for flexibility reasons, we need to specify a function that carries out processing at `struct bio` structure level, we no longer use request queues and we will need to fill the `submit_bio` field in the `struct block_device_operations` associated to the driver.

Below is a typical example of initializing a function that carries out processing at `struct bio` structure level:

<div class="highlight-c">

<div class="highlight">

    // the declaration of the function that carries out processing
    // :c:type:`struct bio` structures
    static blk_qc_t my_submit_bio(struct bio *bio);
    
    struct block_device_operations my_block_ops = {
       .owner = THIS_MODULE,
       .submit_bio = my_submit_bio
       ...
    };

</div>

</div>

</div>

</div>

<div id="further-reading" class="section">

## Further reading[¶](#further-reading "Permalink to this headline")

  - [Linux Device Drivers 3rd Edition, Chapter 16. Block Drivers](http://static.lwn.net/images/pdf/LDD3/ch16.pdf)
  - Linux Kernel Development, Second Edition – Chapter 13. The Block I/O Layer
  - [A simple block driver](https://lwn.net/Articles/58719/)
  - [The gendisk interface](https://lwn.net/Articles/25711/)
  - [The bio structure](https://lwn.net/Articles/26404/)
  - [Request queues](https://lwn.net/Articles/27055/)
  - [Documentation/block/request.txt - Struct request documentation](https://elixir.bootlin.com/linux/v4.15/source/Documentation/block/request.txt)
  - [Documentation/block/biodoc.txt - Notes on the Generic Block Layer](https://elixir.bootlin.com/linux/v4.15/source/Documentation/block/biodoc.txt)
  - [drivers/block/brd/c - RAM backed block disk driver](https://elixir.bootlin.com/linux/v4.15/source/drivers/block/brd.c)
  - [I/O Schedulers](https://www.linuxjournal.com/article/6931)

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

The current lab name is block\_device\_drivers. See the exercises for the task name.

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

The modules are placed in /home/root/skels/block\_device\_drivers/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

<div id="intro" class="section">

### 0\. Intro[¶](#intro "Permalink to this headline")

Using [LXR](http://elixir.free-electrons.com/linux/latest/source) find the definitions of the following symbols in the Linux kernel:

> 
> 
> <div>
> 
>   - `struct bio`
>   - `struct bio_vec`
>   - `bio_for_each_segment`
>   - `struct gendisk`
>   - `struct block_device_operations`
>   - `struct request`
> 
> </div>

</div>

<div id="block-device" class="section">

### 1\. Block device[¶](#block-device "Permalink to this headline")

Create a kernel module that allows you to register or deregister a block device. Start from the files in the `1-2-3-6-ram-disk/kernel` directory in the lab skeleton.

Follow the comments marked with **TODO 1** in the laboratory skeleton. Use the existing macrodefinitions (`MY_BLOCK_MAJOR`, `MY_BLKDEV_NAME`). Check the value returned by the register function, and in case of error, return the error code.

Compile the module, copy it to the virtual machine and insert it into the kernel. Verify that your device was successfully created inside the `/proc/devices`. You will see a device with major 240.

Unload the kernel module and check that the device was unregistered.

<div class="admonition hint">

Hint

Review the [Register a block I/O device](#register-a-block-i-o-device) section.

</div>

Change the `MY_BLOCK_MAJOR` value to 7. Compile the module, copy it to the virtual machine, and insert it into the kernel. Notice that the insertion fails because there is already another driver/device registered in the kernel with the major 7.

Restore the 240 value for the `MY_BLOCK_MAJOR` macro.

</div>

<div id="disk-registration" class="section">

### 2\. Disk registration[¶](#disk-registration "Permalink to this headline")

Modify the previous module to add a disk associated with the driver. Analyze the macrodefinitions, `my_block_dev` structure and existing functions from the `ram-disk.c` file.

Follow the comments marked with **TODO 2**. Use the `create_block_device()` and the `delete_block_device()` functions.

<div class="admonition hint">

Hint

Review the [Register a disk](#register-a-disk) and [Process a request](#process-a-request) sections.

</div>

Fill in the `my_block_request()` function to process the request without actually processing your request: display the "request received" message and the following information: start sector, total size, data size from the current `struct bio` structure, direction. To validate a request type, use the `blk_rq_is_passthrough()` (the function returns 0 in the case in which we are interested, i.e. when the request is generated by the file system).

<div class="admonition hint">

Hint

To find the needed info, review the [Requests for block devices](#requests-for-block-devices) section.

</div>

Use the `blk_mq_end_request()` function to finish processing the request.

Insert the module into the kernel and inspect the messages printed by the module. When a device is added, a request is sent to the device. Check the presence of `/dev/myblock` and if it doesn't exist, create the device using the command:

<div class="highlight-shell">

<div class="highlight">

    mknod /dev/myblock b 240 0

</div>

</div>

To generate writing requests, use the command:

<div class="highlight-shell">

<div class="highlight">

    echo "abc"> /dev/myblock

</div>

</div>

Notice that a write request is preceded by a read request. The request is done to read the block from the disk and "update" its content with the data provided by the user, without overwriting the rest. After reading and updating, writing takes place.

</div>

<div id="ram-disk" class="section">

### 3\. RAM disk[¶](#ram-disk "Permalink to this headline")

Modify the previous module to create a RAM disk: requests to the device will result in reads/writes in a memory area.

The memory area `dev->data` is already allocated in the source code of the module using `vmalloc()` and deallocated using `vfree()`.

<div class="admonition note">

Note

Review the [Process a request](#process-a-request) section.

</div>

Follow the comments marked with **TODO 3** to complete the `my_block_transfer()` function to write/read the request information in/from the memory area. The function will be called for each request within the queue processing function: `my_block_request()`. To write/read to/from the memory area, use `memcpy()`. To determine the write/read information, use the fields of the `struct request` structure.

<div class="admonition hint">

Hint

To find out the size of the request data, use the `blk_rq_cur_bytes` macro. Do not use the `blk_rq_bytes` macro.

</div>

<div class="admonition hint">

Hint

To find out the buffer associated to the request, use ``bio_data`(:c:data:`rq->bio``).

</div>

<div class="admonition hint">

Hint

A description of useful macros is in the [Requests for block devices](#requests-for-block-devices) section.

</div>

<div class="admonition hint">

Hint

You can find useful information in the [block device driver example](https://github.com/martinezjavier/ldd3/blob/master/sbull/sbull.c) from [Linux Device Driver](http://lwn.net/Kernel/LDD3/).

</div>

For testing, use the test file `user/ram-disk-test.c`. The test program is compiled automatically at `make build`, copied to the virtual machine at `make copy` and can be run on the QEMU virtual machine using the command:

<div class="highlight-shell">

<div class="highlight">

    ./ram-disk-test

</div>

</div>

There is no need to insert the module into the kernel, it will be inserted by the `ram-disk-test` command.

Some tests may fail because of lack of synchronization between the transmitted data (flush).

</div>

<div id="read-data-from-the-disk" class="section">

### 4\. Read data from the disk[¶](#read-data-from-the-disk "Permalink to this headline")

The purpose of this exercise is to read data from the `PHYSICAL_DISK_NAME` disk (`/dev/vdb`) directly from the kernel.

<div class="admonition attention">

Attention

Before solving the exercise, we need to make sure the disk is added to the virtual machine.

Check the variable `QEMU_OPTS` from `qemu/Makefile`. There should already be two extra disks added using `-drive ...`.

If there are not, generate a file that we will use as the disk image using the command: **dd if=/dev/zero of=qemu/mydisk.img bs=1024 count=1** and add the following option: **-drive file=qemu/mydisk.img,if=virtio,format=raw** to `qemu/Makefile` (in the `QEMU_OPTS` variable, after the root disk).

</div>

Follow the comments marked with **TODO 4** in the directory `4-5-relay/` and implement `open_disk()` and `close_disk()`. Use the `blkdev_get_by_path()` and `blkdev_put()` functions. The device must be opened in read-write mode exclusively (`FMODE_READ` | `FMODE_WRITE` | `FMODE_EXCL`), and as holder you must use the current module (`THIS_MODULE`).

Implement the `send_test_bio()` function. You will have to create a new `struct bio` structure and fill it, submit it and wait for it. Read the first sector of the disk. To wait, call the `submit_bio_wait()` function.

<div class="admonition hint">

Hint

The first sector of the disk is the sector with the index 0. This value must be used to initialize the field `bi_iter.bi_sector` of the `struct bio`.

For the read operation, use the `REQ_OP_READ` macro to initialize the `bi_opf` field of the `struct bio`.

</div>

After finishing the operation, display the first 3 bytes of data read by `struct bio` structure. Use the format `"% 02x"` for `printk()` to display the data and the `kmap_atomic` and `kunmap_atomic` macros respectively.

<div class="admonition hint">

Hint

As an argument for the `kmap_atomic()` function, just use the page which is allocated above in the code, in the `page` variable.

</div>

<div class="admonition hint">

Hint

Review the sections [<span class="std std-ref">How to use the content of a struct bio structure</span>](../so2/lab7-block-device-drivers.html#bio-content) and [<span class="std std-ref">Wait for the completion of a struct bio structure</span>](../so2/lab7-block-device-drivers.html#bio-completion).

</div>

For testing, use the `test-relay-disk` script, which is copied on the virtual machine when running **make copy**. If it is not copied, make sure it is executable:

<div class="highlight-shell">

<div class="highlight">

    chmod +x test-relay-disk

</div>

</div>

There is no need to load the module into the kernel, it will be loaded by **test-relay-disk**.

Use the command below to run the script:

<div class="highlight-shell">

<div class="highlight">

    ./test-relay-disk

</div>

</div>

The script writes "abc" at the beginning of the disk indicated by `PHYSICAL_DISK_NAME`. After running, the module will display 61 62 63 (the corresponding hexadecimal values of letters "a", "b" and "c").

</div>

<div id="write-data-to-the-disk" class="section">

### 5\. Write data to the disk[¶](#write-data-to-the-disk "Permalink to this headline")

Follow the comments marked with **TODO 5** to write a message (`BIO_WRITE_MESSAGE`) on the disk.

The `send_test_bio()` function receives as argument the operation type (read or write). Call in the `relay_init()` function the function for reading and in the `relay_exit()` function the function for writing. We recommend using the `REQ_OP_READ` and the `REQ_OP_WRITE` macros.

Inside the `send_test_bio()` function, if the operation is write, fill in the buffer associated to the `struct bio` structure with the message `BIO_WRITE_MESSAGE`. Use the `kmap_atomic` and the `kunmap_atomic` macros to work with the buffer associated to the `struct bio` structure.

<div class="admonition hint">

Hint

You need to update the type of the operation associated to the `struct bio` structure by setting the `bi_opf` field accordingly.

</div>

For testing, run the `test-relay-disk` script using the command:

<div class="highlight-shell">

<div class="highlight">

    ./test-relay-disk

</div>

</div>

The script will display the `"read from /dev/sdb: 64 65 66"` message at the standard output.

</div>

<div id="processing-requests-from-the-request-queue-at-struct-bio-level" class="section">

### 6\. Processing requests from the request queue at `struct bio` level[¶](#processing-requests-from-the-request-queue-at-struct-bio-level "Permalink to this headline")

In the implementation from Exercise 3, we have only processed a `struct bio_vec` of the current `struct bio` from the request. We want to process all `struct bio_vec` structures from all `struct bio` structures. For this, we will iterate through all `struct bio` requests and through all `struct bio_vec` structures (also called segments) of each `struct bio`.

Add, within the ramdisk implementation (`1-2-3-6-ram-disk/` directory), support for processing the requests from the request queue at `struct bio` level. Follow the comments marked with **TODO 6**.

Set the `USE_BIO_TRANSFER` macro to 1.

Implement the `my_xfer_request()` function. Use the `rq_for_each_segment` macro to iterate through the `bio_vec` structures of each `struct bio` from the request.

<div class="admonition hint">

Hint

Review the indications and the code snippets from the [<span class="std std-ref">How to use the content of a struct bio structure</span>](../so2/lab7-block-device-drivers.html#bio-content) section.

</div>

<div class="admonition hint">

Hint

Use the `struct bio` segment iterator to get the current sector (`iter.iter.bi_sector`).

</div>

<div class="admonition hint">

Hint

Use the request iterator to get the reference to the current `struct bio` (`iter.bio`).

</div>

<div class="admonition hint">

Hint

Use the `bio_data_dir` macro to find the reading or writing direction for a `struct bio`.

</div>

Use the `kmap_atomic` or the `kunmap_atomic` macros to map the pages of each `struct bio` structure and access its associated buffers. For the actual transfer, call the `my_block_transfer()` function implemented in the previous exercise.

For testing, use the `ram-disk-test.c` test file:

<div class="highlight-shell">

<div class="highlight">

    ./ram-disk-test

</div>

</div>

There is no need to insert the module into the kernel, it will be inserted by the **ram-disk-test** executable.

Some tests may crash because of lack of synchronization between the transmitted data (flush).

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](deferred_work.html "Deferred work") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](filesystems_part1.html "File system drivers (Part 1)")

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
