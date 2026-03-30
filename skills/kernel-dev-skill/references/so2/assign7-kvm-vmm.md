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
      - [Assignment 7 - SO2 Virtual Machine Manager with KVM](#)
          - [I. Virtual Machine Manager](#i-virtual-machine-manager)
              - [1. Initialize the VMM](#initialize-the-vmm)
          - [Running the VM](#running-the-vm)
              - [Setup real mode](#setup-real-mode)
              - [Setup long mode](#setup-long-mode)
              - [Running](#running)
              - [Guest code](#guest-code)
              - [Controller queues](#controller-queues)
              - [Device structures](#device-structures)
          - [Using the skeleton](#using-the-skeleton)
          - [Debugging](#debugging)
          - [Tasks](#tasks)
              - [Submitting the assigment](#submitting-the-assigment)
              - [Tips](#tips)
              - [Penalties](#penalties)
              - [TLDR](#tldr)

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
  - Assignment 7 - SO2 Virtual Machine Manager with KVM
  - [View page source](../_sources/so2/assign7-kvm-vmm.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="assignment-7-so2-virtual-machine-manager-with-kvm" class="section">

# Assignment 7 - SO2 Virtual Machine Manager with KVM[¶](#assignment-7-so2-virtual-machine-manager-with-kvm "Permalink to this headline")

  - Deadline: **Tuesday, 29 May 2023, 23:00**
  - This assignment can be made in teams (max 2). Only one of them must submit the assignment, and the names of the student should be listed in a README file.

In this assignment we will work on a simple Virtual Machine Manager (VMM). We will be using the KVM API from the Linux kernel.

The assignment has two components: the VM code and the VMM code. We will be using a very simple protocol to enable the communication between the two components. The protocol is called SIMVIRTIO.

<div id="i-virtual-machine-manager" class="section">

## I. Virtual Machine Manager[¶](#i-virtual-machine-manager "Permalink to this headline")

In general, to build a VMM from scratch we will have to implement three main functionalities: initialize the VMM, initialize the virtual CPU and run the guest code. We will split the implementation of the VMM in these three phases.

<div id="initialize-the-vmm" class="section">

### 1\. Initialize the VMM[¶](#initialize-the-vmm "Permalink to this headline")

A VM will be represented in general by three elements, a file descriptor used to interact with the KVM API, a file descriptor per VM used to configure it (e.g. set its memory) and a pointer to the VM's memory. We provide you with the following structure to start from when working with a VM.

<div class="highlight-c">

<div class="highlight">

    typedef struct vm {
            int sys_fd;
            int fd;
            char *mem;
    } virtual_machine;

</div>

</div>

The first step in initializing the KVM VM is to interract with the \[KVM\_API\](<https://www.kernel.org/doc/html/latest/virt/kvm/api.html>\]. The KVM API is exposed via `/dev/kvm`. We will be using ioctl calls to call the API.

The snippet below shows how one can call `KVM_GET_API_VERSION` to get the KVM API Version

<div class="highlight-c">

<div class="highlight">

    int kvm_fd = open("/dev/kvm", O_RDWR);
    if (kvm_fd < 0) {
        perror("open /dev/kvm");
        exit(1);
    }
    
    int api_ver = ioctl(kvm_fd, KVM_GET_API_VERSION, 0);
    if (api_ver < 0) {
        perror("KVM_GET_API_VERSION");
        exit(1);
    }

</div>

</div>

Let us now go briefly through how a VMM initializes a VM. This is only the bare bones, a VMM may do lots of other things during VM initialization.

1.  We first use KVM\_GET\_API\_VERSION to check that we are running the expected version of KVM, `KVM_API_VERSION`.
2.  We now create the VM using `KVM_CREATE_VM`. Note that calling `KVM_CREATE_VM` returns a file descriptor. We will be using this file descriptor for the next phases of the setup.
3.  (Optional) On Intel based CPUs we will have to call `KVM_SET_TSS_ADDR` with address `0xfffbd000`
4.  Next, we allocate the memory for the VM, we will be using `mmap` for this with `PROT_WRITE`, `MAP_PRIVATE`, `MAP_ANONYMOUS` and `MAP_NORESERVE`. We recommend allocating 0x100000 bytes for the VM.
5.  We flag the memory as `MADV_MERGEABLE` using `madvise`
6.  Finally, we use `KVM_SET_USER_MEMORY_REGION` to assign the memory to the VM.

**Make sure you understand what file descriptor to use and when, we use the KVM fd when calling KVM\_CREATE\_VM, but when interacting with the vm such as calling KVM\_SET\_USER\_MEMORY\_REGION we use the VMs file descriptor**

TLDR: API used for VM initialization:

  - KVM\_GET\_API\_VERSION
  - KVM\_CREATE\_VM
  - KVM\_SET\_TSS\_ADDR
  - KVM\_SET\_USER\_MEMORY\_REGION.

<div id="initialize-a-virtual-cpu" class="section">

#### 2\. Initialize a virtual CPU[¶](#initialize-a-virtual-cpu "Permalink to this headline")

We need a Virtual CPU (VCPU) to store registers.

<div class="highlight-c">

<div class="highlight">

    typedef struct vcpu {
            int fd;
            struct kvm_run *kvm_run;
    } virtual_cpu;

</div>

</div>

To create a virtual CPU we will do the following: 1. Call `KVM_CREATE_VCPU` to create the virtual CPU. This call returns a file descriptor. 2. Use `KVM_GET_VCPU_MMAP_SIZE` to get the size of the shared memory 3. Allocated the necessary VCPU mem size with `mmap`. We will be passing the VCPU file descriptor to the `mmap` call. We can store the result in `kvm_run`.

TLDR: API used for VM

  - KVM\_CREATE\_VCPU
  - KVM\_GET\_VCPU\_MMAP\_SIZE

**We recommend using 2MB pages to simplify the translation process**

</div>

</div>

</div>

<div id="running-the-vm" class="section">

## Running the VM[¶](#running-the-vm "Permalink to this headline")

<div id="setup-real-mode" class="section">

### Setup real mode[¶](#setup-real-mode "Permalink to this headline")

At first, the CPU will start in Protected mode. To do run any meaningful code, we will switch the CPU to \[Real mode\](<https://wiki.osdev.org/Real_Mode>). To do this we will need to configure several CPU registers.

1.  First, we will use `KVM_GET_SREGS` to get the registers. We use `struct kvm_regs` for this task.
2.  We will need to set `cs.selector` and `cs.base` to 0. We will use `KVM_SET_SREGS` to set the registers.
3.  Next we will clear all `FLAGS` bits via the `rflags` register, this means setting `rflags` to 2 since bit 1 must always be to 1. We alo set the `RIP` register to 0.

</div>

<div id="setup-long-mode" class="section">

### Setup long mode[¶](#setup-long-mode "Permalink to this headline")

Read mode is all right for very simple guests, such as the one found in the folder guest\_16\_bits. But, most programs nowdays need 64 bits addresses, and such we will need to switch to long mode. The following article from OSDev presents all the necessary information about \[Setting Up Long Mode\](<https://wiki.osdev.org/Setting_Up_Long_Mode>).

In `vcpu.h`, you may found helpful macros such as CR0\_PE, CR0\_MP, CR0\_ET, etc.

Since we will running a more complex program, we will also create a small stack for our program `regs.rsp = 1 << 20;`. Don't forget to set the RIP and RFLAGS registers.

</div>

<div id="running" class="section">

### Running[¶](#running "Permalink to this headline")

After we setup our VCPU in real or long mode we can finally start running code on the VM.

1.  We copy to the vm memory the guest code, memcpy(vm-\>mem, guest\_code, guest\_code\_size) The guest code will be available in two variables which will be discussed below.
2.  In a infinite loop we run the following:

> 
> 
> <div>
> 
>   - We call `KVM_RUN` on the VCPU file descriptor to run the VPCU
>   - Through the shared memory of the VCPU we check the `exit_reason` parameter to see if the guest has made any requests:
>   - We will handle the following VMEXITs: KVM\_EXIT\_MMIO, KVM\_EXIT\_IO and `KVM_EXIT_HLT`. `KVM_EXIT_MMIO` is triggered when the VM writes to a MMIO address. `KVM_EXIT_IO` is called when the VM calls `inb` or `outb`. `KVM_EXIT_HLT` is called when the user does a `hlt` instruction.
> 
> </div>

</div>

<div id="guest-code" class="section">

### Guest code[¶](#guest-code "Permalink to this headline")

The VM that is running is also called guest. We will be using the guest to test our implementation.

1.  To test the implementation before implementing SIMVIRTIO. The guest will write at address 400 and the RAX register the value 42.
2.  To test a more complicated implementation,we will extend the previous program to also write "Hello, world\!n" on port 0xE9 using the outb instruction.
3.  To test the implementation of SIMVIRTIO, we will

How do we get the guest code? The guest code is available at the following static pointers guest16, guest16\_end-guest16. The linker script is populating them.

\#\# SIMVIRTIO: From the communication between the guest and the VMM we will implement a very simple protocol called `SIMVIRTIO`. It's a simplified version of the real protocol used in the real world called virtio.

Configuration space:

| u32           | u16             | u8              | u8                | u8                 | u8             | u8             |
| ------------- | --------------- | --------------- | ----------------- | ------------------ | -------------- | -------------- |
| magic value R | max queue len R | device status R | driver status R/W | queue selector R/W | Q0(TX) CTL R/W | Q1(RX) CTL R/w |

</div>

<div id="controller-queues" class="section">

### Controller queues[¶](#controller-queues "Permalink to this headline")

We provide you with the following structures and methods for the `SIMVIRTIO` implementation.

<div class="highlight-c">

<div class="highlight">

    typedef uint8_t q_elem_t;
    typedef struct queue_control {
        // Ptr to current available head/producer index in 'buffer'.
        unsigned head;
        // Ptr to last index in 'buffer' used by consumer.
        unsigned tail;
    } queue_control_t;
    typedef struct simqueue {
        // MMIO queue control.
        volatile queue_control_t *q_ctrl;
        // Size of the queue buffer/data.
        unsigned maxlen;
        // Queue data buffer.
        q_elem_t *buffer;
    } simqueue_t;
    int circ_bbuf_push(simqueue_t *q, q_elem_t data)
    {
    }
    int circ_bbuf_pop(simqueue_t *q, q_elem_t *data)
    {
    }

</div>

</div>

</div>

<div id="device-structures" class="section">

### Device structures[¶](#device-structures "Permalink to this headline")

<div class="highlight-c">

<div class="highlight">

    #define MAGIC_VALUE 0x74726976
    #define DEVICE_RESET 0x0
    #define DEVICE_CONFIG 0x2
    #define DEVICE_READY 0x4
    #define DRIVER_ACK 0x0
    #define DRIVER 0x2
    #define DRIVER_OK 0x4
    #define DRIVER_RESET 0x8000
    typedef struct device {
        uint32_t magic;
        uint8_t device_status;
        uint8_t driver_status;
        uint8_t max_queue_len;
    } device_t;
    typedef struct device_table {
        uint16_t count;
        uint64_t device_addresses[10];
     } device_table_t;

</div>

</div>

We will be implementing the following handles: \* MMIO (read/write) VMEXIT \* PIO (read/write) VMEXIT

</div>

</div>

<div id="using-the-skeleton" class="section">

## Using the skeleton[¶](#using-the-skeleton "Permalink to this headline")

</div>

<div id="debugging" class="section">

## Debugging[¶](#debugging "Permalink to this headline")

</div>

<div id="tasks" class="section">

## Tasks[¶](#tasks "Permalink to this headline")

1.  30p Implement a simple VMM that runs the code from guest\_16\_bits. We will be running the VCPU in read mode for this task
2.  20p Extend the previous implementation to run the VCPU in real mode. We will be running the guest\_32\_bits example
3.  30p Implement the SIMVIRTIO protocol.
4.  10p Implement pooling as opposed to VMEXIT. We will use the macro USE\_POOLING to switch this option on and off.
5.  10p Add profiling code. Measure the number of VMEXITs triggered by the VMM.

<div id="submitting-the-assigment" class="section">

### Submitting the assigment[¶](#submitting-the-assigment "Permalink to this headline")

The assignment archive will be submitted on **Moodle**, according to the rules on the [rules page](https://ocw.cs.pub.ro/courses/so2/reguli-notare#reguli_de_trimitere_a_temelor).

</div>

<div id="tips" class="section">

### Tips[¶](#tips "Permalink to this headline")

To increase your chances of getting the highest grade, read and follow the Linux kernel coding style described in the [Coding Style document](https://elixir.bootlin.com/linux/v4.19.19/source/Documentation/process/coding-style.rst).

Also, use the following static analysis tools to verify the code:

  - checkpatch.pl
    
    <div class="highlight-console">
    
    <div class="highlight">
    
        $ linux/scripts/checkpatch.pl --no-tree --terse -f /path/to/your/file.c
    
    </div>
    
    </div>

  - sparse
    
    <div class="highlight-console">
    
    <div class="highlight">
    
        $ sudo apt-get install sparse
        $ cd linux
        $ make C=2 /path/to/your/file.c
    
    </div>
    
    </div>

  - cppcheck
    
    <div class="highlight-console">
    
    <div class="highlight">
    
        $ sudo apt-get install cppcheck
        $ cppcheck /path/to/your/file.c
    
    </div>
    
    </div>

</div>

<div id="penalties" class="section">

### Penalties[¶](#penalties "Permalink to this headline")

Information about assigments penalties can be found on the [General Directions page](https://ocw.cs.pub.ro/courses/so2/teme/general).

In exceptional cases (the assigment passes the tests by not complying with the requirements) and if the assigment does not pass all the tests, the grade will may decrease more than mentioned above.

\#\# References We recommend you the following readings before starting to work on the homework: \* \[KVM host in a few lines of code\](<https://zserge.com/posts/kvm/>)

</div>

<div id="tldr" class="section">

### TLDR[¶](#tldr "Permalink to this headline")

1.  The VMM creates and initializes a virtual machine and a virtual CPU
2.  We switch to real mode and check run the simple guest code from guest\_16\_bits
3.  We switch to long mode and run the more complex guest from guest\_32\_bits
4.  We implement the SIMVIRTIO protocol. We will describe how it behaves in the following subtasks.
5.  The guest writes in the TX queue (queue 0) the ascii code for R which will result in a VMEXIT

6\. the VMM will handle the VMEXIT caused by the previous write in the queue. When the guests receiver the R letter it will initiate the reser procedure of the device and set the device status to DEVICE\_RESET 7. After the reset handling, the guest must set the status of the device to DRIVER\_ACK. After this, the guest will write to the TX queue the letter C 8. In the VMM we will initialize the config process when letter C is received.It will set the device status to DEVICE\_CONFIG and add a new entry in the device\_table 9. After the configuration process is finished, the guest will set the driver status to DRIVER\_OK 10. Nex, the VMM will set the device status to DEVICE\_READY 11. The guest will write in the TX queue "Ana are mere" and will execute a halt 12. The VMM will print to the STDOUT the message received and execute the halt request 13. Finally, the VMM will verify that at address 0x400 and in register RAX is stored the value 42

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](assign4-transport-protocol.html "Assignment 4 - SO2 Transport Protocol") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](../lectures/intro.html "Introduction")

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
