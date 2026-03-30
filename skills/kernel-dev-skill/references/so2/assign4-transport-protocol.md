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
      - [Assignment 4 - SO2 Transport Protocol](#)
          - [Assignment's Objectives](#assignment-s-objectives)
          - [Statement](#statement)
          - [Implementation Details](#implementation-details)
              - [Sample Protocol Implementations](#sample-protocol-implementations)
          - [Testing](#testing)
              - [tcpdump](#tcpdump)
          - [QuickStart](#quickstart)
              - [Tips](#tips)
              - [Penalties](#penalties)
              - [Submitting the assigment](#submitting-the-assigment)
          - [Resources](#resources)
          - [Questions](#questions)
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
  - Assignment 4 - SO2 Transport Protocol
  - [View page source](../_sources/so2/assign4-transport-protocol.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="assignment-4-so2-transport-protocol" class="section">

# Assignment 4 - SO2 Transport Protocol[¶](#assignment-4-so2-transport-protocol "Permalink to this headline")

  - Deadline: **Monday, 29 May 2023, 23:00**
  - This assignment can be made in teams (max 2). Only one of them must submit the assignment, and the names of the student should be listed in a README file.

Implement a simple datagram transport protocol - STP (*SO2 Transport Protocol*).

<div id="assignment-s-objectives" class="section">

## Assignment's Objectives[¶](#assignment-s-objectives "Permalink to this headline")

  - gaining knowledge about the operation of the networking subsystem in the Linux kernel
  - obtaining skills to work with the basic structures of the networking subsystem in Linux
  - deepening the notions related to communication and networking protocols by implementing a protocol in an existing protocol stack

</div>

<div id="statement" class="section">

## Statement[¶](#statement "Permalink to this headline")

Implement, in the Linux kernel, a protocol called STP (*SO2 Transport Protocol*), at network and transport level, that works using datagrams (it is not connection-oriented and does not use flow-control elements).

The STP protocol acts as a Transport layer protocol (port-based multiplexing) but operates at level 3 (Network) of [the OSI stack](http://en.wikipedia.org/wiki/OSI_model), above the Data Link level.

The STP header is defined by the `struct stp_header` structure:

<div class="highlight-c">

<div class="highlight">

    struct stp_header {
            __be16 dst;
            __be16 src;
            __be16 len;
            __u8 flags;
            __u8 csum;
    };

</div>

</div>

where:

> 
> 
> <div>
> 
>   - `len` is the length of the packet in bytes (including the header);
>   - `dst` and `src` are the destination and source ports, respectively;
>   - `flags` contains various flags, currently unused (marked *reserved*);
>   - `csum` is the checksum of the entire package including the header; the checksum is calculated by exclusive OR (XOR) between all bytes.
> 
> </div>

Sockets using this protocol will use the `AF_STP` family.

The protocol must work directly over Ethernet. The ports used are between `1` and `65535`. Port `0` is not used.

The definition of STP-related structures and macros can be found in the [assignment support header](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/src/stp.h).

</div>

<div id="implementation-details" class="section">

## Implementation Details[¶](#implementation-details "Permalink to this headline")

The kernel module will be named **af\_stp.ko**.

You have to define a structure of type [net\_proto\_family](http://elixir.free-electrons.com/linux/v5.10/source/include/linux/net.h#L211), which provides the operation to create STP sockets. Newly created sockets are not associated with any port or interface and cannot receive / send packets. You must initialize the [socket ops field](http://elixir.free-electrons.com/linux/v5.10/source/include/linux/net.h#L125) with the list of operations specific to the STP family. This field refers to a structure [proto\_ops](http://elixir.free-electrons.com/linux/v5.10/source/include/linux/net.h#L139) which must include the following functions:

  - `release`: releases an STP socket
  - `bind`: associates a socket with a port (possibly also an interface) on which packets will be received / sent:
      - there may be bind sockets only on one port (not on an interface)
      - sockets associated with only one port will be able to receive packets sent to that port on all interfaces (analogous to UDP sockets associated with only one port); these sockets cannot send packets because the interface from which they can be sent via the standard sockets API cannot be specified
      - two sockets cannot be binded to the same port-interface combination:
          - if there is a socket already binded with a port and an interface then a second socket cannot be binded to the same port and the same interface or without a specified interface
          - if there is a socket already binded to a port but without a specified interface then a second socket cannot be binded to the same port (with or without a specified interface)
      - we recommend using a hash table for bind instead of other data structures (list, array); in the kernel there is a hash table implementation in the [hashtable.h header](http://elixir.free-electrons.com/linux/v4.9.11/source/include/linux/hashtable.h)
  - `connect`: associates a socket with a remote port and hardware address (MAC address) to which packets will be sent / received:
      - this should allow `send` / `recv` operations on the socket instead of `sendmsg` / `recvmsg` or `sendto` / `recvfrom`
      - once connected to a host, sockets will only accept packets from that host
      - once connected, the sockets can no longer be disconnected
  - `sendmsg`, `recvmsg`: send or receive a datagram on an STP socket:
      - for the *receive* part, metainformation about the host that sent the packet can be stored in the [cb field in sk\_buff](http://elixir.free-electrons.com/linux/v5.10/source/include/linux/skbuff.h#L742)
  - `poll`: the default function `datagram_poll` will have to be used
  - for the rest of the operations the predefined stubs in the kernel will have to be used (`sock_no_*`)

<div class="highlight-c">

<div class="highlight">

    static const struct proto_ops stp_ops = {
            .family = PF_STP,
            .owner = THIS_MODULE,
            .release = stp_release,
            .bind = stp_bind,
            .connect = stp_connect,
            .socketpair = sock_no_socketpair,
            .accept = sock_no_accept,
            .getname = sock_no_getname,
            .poll = datagram_poll,
            .ioctl = sock_no_ioctl,
            .listen = sock_no_listen,
            .shutdown = sock_no_shutdown,
            .setsockopt = sock_no_setsockopt,
            .getsockopt = sock_no_getsockopt,
            .sendmsg = stp_sendmsg,
            .recvmsg = stp_recvmsg,
            .mmap = sock_no_mmap,
            .sendpage = sock_no_sendpage,
    };

</div>

</div>

Socket operations use a type of address called `sockaddr_stp`, a type defined in the [assignment support header](https://github.com/linux-kernel-labs/linux/blob/master/tools/labs/templates/assignments/4-stp/stp.h). For the *bind* operation, only the port and the index of the interface on which the socket is bind will be considered. For the *receive* operation, only the `addr` and `port` fields in the structure will be filled in with the MAC address of the host that sent the packet and with the port from which it was sent. Also, when sending a packet, the destination host will be obtained from the `addr` and `port` fields of this structure.

You need to register a structure [packet\_type](http://elixir.free-electrons.com/linux/v5.10/source/include/linux/netdevice.h#L2501), using the call [dev\_add\_pack](http://elixir.free-electrons.com/linux/v5.10/source/net/core/dev.c#L521) to be able to receive STP packets from the network layer.

The protocol will need to provide an interface through the *procfs* file system for statistics on sent / received packets. The file must be named `/proc/net/stp_stats`, specified by the `STP_PROC_FULL_FILENAME` macro in [assignment support header](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/src/stp.h). The format must be of simple table type with `2` rows: on the first row the header of the table, and on the second row the statistics corresponding to the columns. The columns of the table must be in order:

<div class="code highlight-none">

<div class="highlight">

    RxPkts HdrErr CsumErr NoSock NoBuffs TxPkts

</div>

</div>

where:

  - `RxPkts` - the number of packets received
  - `HdrErr` - the number of packets received with header errors (packets too short or with source or destination 0 ports)
  - `CsumErr` - the number of packets received with checksum errors
  - `NoSock` - the number of received packets for which no destination socket was found
  - `NoBuffs` - the number of received packets that could not be received because the socket queue was full
  - `TxPkts` - the number of packets sent

To create or delete the entry specified by `STP_PROC_FULL_FILENAME` we recommend using the functions [proc\_create](http://elixir.free-electrons.com/linux/v5.10/source/include/linux/proc_fs.h#L108) and [proc\_remove](http://elixir.free-electrons.com/linux/v5.10/source/fs/proc/generic.c#L772).

<div id="sample-protocol-implementations" class="section">

### Sample Protocol Implementations[¶](#sample-protocol-implementations "Permalink to this headline")

For examples of protocol implementation, we recommend the implementation of [PF\_PACKET](http://elixir.free-electrons.com/linux/v5.10/source/net/packet/af_packet.c) sockets and the various functions in [UDP implementation](http://elixir.free-electrons.com/linux/v5.10/source/net/ipv4/udp.c) or [IP implementation](http://elixir.free-electrons.com/linux/v5.10/source/net/ipv4/af_inet.c).

</div>

</div>

<div id="testing" class="section">

## Testing[¶](#testing "Permalink to this headline")

In order to simplify the assignment evaluation process, but also to reduce the mistakes of the submitted assignments, the assignment evaluation will be done automatically with the help of a [test script](https://gitlab.cs.pub.ro/so2/3-raid/-/blob/master/checker/4-stp-checker/_checker) called \_checker. The test script assumes that the kernel module is called af\_stp.ko.

<div id="tcpdump" class="section">

### tcpdump[¶](#tcpdump "Permalink to this headline")

You can use the `tcpdump` utility to troubleshoot sent packets. The tests use the loopback interface; to track sent packets you can use a command line of the form:

<div class="code console highlight-none">

<div class="highlight">

    tcpdump -i lo -XX

</div>

</div>

You can use a static version of [tcpdump](http://elf.cs.pub.ro/so2/res/teme/tcpdump). To add to the `PATH` environment variable in the virtual machine, copy this file to `/linux/tools/labs/rootfs/bin`. Create the directory if it does not exist. Remember to give the `tcpdump` file execution permissions:

<div class="code console highlight-none">

<div class="highlight">

    # Connect to the docker using ./local.sh docker interactive
    cd /linux/tools/labs/rootfs/bin
    wget http://elf.cs.pub.ro/so2/res/teme/tcpdump
    chmod +x tcpdump

</div>

</div>

</div>

</div>

<div id="quickstart" class="section">

## QuickStart[¶](#quickstart "Permalink to this headline")

It is mandatory to start the implementation of the assignment from the code skeleton found in the [src](https://gitlab.cs.pub.ro/so2/4-stp/-/tree/master/src) directory. There is only one header in the skeleton called [stp.h](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/src/stp.h). You will provide the rest of the implementation. You can add as many \*.c\` sources and additional \*.h\` headers. You should also provide a Kbuild file that will compile the kernel module called af\_stp.ko. Follow the instructions in the [README.md file](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/README.md) of the [assignment's repo](https://gitlab.cs.pub.ro/so2/4-stp).

<div id="tips" class="section">

### Tips[¶](#tips "Permalink to this headline")

To increase your chances of getting the highest grade, read and follow the Linux kernel coding style described in the [Coding Style document](https://elixir.bootlin.com/linux/v5.10/source/Documentation/process/coding-style.rst).

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

</div>

<div id="submitting-the-assigment" class="section">

### Submitting the assigment[¶](#submitting-the-assigment "Permalink to this headline")

The assignment will be graded automatically using the [vmchecker-next](https://github.com/systems-cs-pub-ro/vmchecker-next/wiki/Student-Handbook) infrastructure. The submission will be made on moodle on the [course's page](https://curs.upb.ro/2022/course/view.php?id=5121) to the related assignment. You will find the submission details in the [README.md file](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/README.md) of the [repo](https://gitlab.cs.pub.ro/so2/4-stp).

</div>

</div>

<div id="resources" class="section">

## Resources[¶](#resources "Permalink to this headline")

  - [Lecture 10 - Networking](https://linux-kernel-labs.github.io/refs/heads/master/so2/lec10-networking.html)
  - [Lab 10 - Networking](https://linux-kernel-labs.github.io/refs/heads/master/so2/lab10-networking.html)
  - Linux kernel sources
      - [Implementing PF\_PACKET sockets](http://elixir.free-electrons.com/linux/v5.10/source/net/packet/af_packet.c)
      - [Implementation of the UDP protocol](http://elixir.free-electrons.com/linux/v5.10/source/net/ipv4/udp.c)
      - [Implementation of the IP protocol](http://elixir.free-electrons.com/linux/v5.10/source/net/ipv4/af_inet.c)
  - Understanding Linux Network Internals
      - chapters 8-13
  - [assignment support header](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/src/stp.h)

We recommend that you use gitlab to store your homework. Follow the directions in [README](https://gitlab.cs.pub.ro/so2/4-stp/-/blob/master/README.md).

</div>

<div id="questions" class="section">

## Questions[¶](#questions "Permalink to this headline")

For questions about the topic, you can consult the mailing [list archives](http://cursuri.cs.pub.ro/pipermail/so2/) or you can write a question on the dedicated Teams channel.

Before you ask a question, make sure that:

> 
> 
> <div>
> 
>   - you have read the statement of the assigment well
>   - the question is not already presented on the [FAQ page](https://ocw.cs.pub.ro/courses/so2/teme/tema2/faq)
>   - the answer cannot be found in the [mailing list archives](http://cursuri.cs.pub.ro/pipermail/so2/)
> 
> </div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](assign3-software-raid.html "Assignment 3 - Software RAID") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](assign7-kvm-vmm.html "Assignment 7 - SO2 Virtual Machine Manager with KVM")

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
