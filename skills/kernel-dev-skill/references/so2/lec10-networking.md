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
      - [SO2 Lecture 10 - Networking](#)
          - [Lecture objectives:](#lecture-objectives)
          - [Network Management Overview](#network-management-overview)
          - [Sockets Implementation Overview](#sockets-implementation-overview)
          - [Sockets Families and Protocols](#sockets-families-and-protocols)
              - [Example: UDP send](#example-udp-send)
          - [Network processing phases](#network-processing-phases)
          - [Packet Routing](#packet-routing)
              - [Routing Table(s)](#routing-table-s)
              - [Routing Policy Database](#routing-policy-database)
              - [Routing table processing](#routing-table-processing)
              - [Forwarding Information Database](#forwarding-information-database)
          - [Netfilter](#netfilter)
          - [Network packets / skbs (struct sk\_buff)](#network-packets-skbs-struct-sk-buff)
          - [Network Device](#network-device)
          - [Hardware and Software Acceleration Techniques](#hardware-and-software-acceleration-techniques)
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
  - SO2 Lecture 10 - Networking
  - [View page source](../_sources/so2/lec10-networking.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lecture-10-networking" class="section">

# SO2 Lecture 10 - Networking[¶](#so2-lecture-10-networking "Permalink to this headline")

[View slides](lec10-networking-slides.html)

<span class="admonition-so2-lecture-10-networking"></span>

<div id="lecture-objectives" class="section">

## Lecture objectives:[¶](#lecture-objectives "Permalink to this headline")

  - Socket implementation
  - Routing implementation
  - Network Device Interface
  - Hardware and Software Acceleration Techniques

</div>

<div id="network-management-overview" class="section">

## Network Management Overview[¶](#network-management-overview "Permalink to this headline")

[![../\_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png](../_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png)](../_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png)

</div>

<div id="sockets-implementation-overview" class="section">

## Sockets Implementation Overview[¶](#sockets-implementation-overview "Permalink to this headline")

[![../\_images/ditaa-79e3734c36891f6c04d684aa5caa39f76915dbaf.png](../_images/ditaa-79e3734c36891f6c04d684aa5caa39f76915dbaf.png)](../_images/ditaa-79e3734c36891f6c04d684aa5caa39f76915dbaf.png)

</div>

<div id="sockets-families-and-protocols" class="section">

## Sockets Families and Protocols[¶](#sockets-families-and-protocols "Permalink to this headline")

[![../\_images/ditaa-bf1244d1a5c3d99bd8d40148d81cb3e5748c0b94.png](../_images/ditaa-bf1244d1a5c3d99bd8d40148d81cb3e5748c0b94.png)](../_images/ditaa-bf1244d1a5c3d99bd8d40148d81cb3e5748c0b94.png)

<div id="example-udp-send" class="section">

### Example: UDP send[¶](#example-udp-send "Permalink to this headline")

<div class="admonition-example-udp-send highlight-c">

<div class="highlight">

    char c;
    struct sockaddr_in addr;
    int s;
    
    s = socket(AF_INET, SOCK_DGRAM, 0);
    connect(s, (struct sockaddr*)&addr, sizeof(addr));
    write(s, &c, 1);
    close(s);

</div>

</div>

![../\_images/ditaa-ee04e3e544de75375b914f7645c79d5ae46fe6f3.png](../_images/ditaa-ee04e3e544de75375b914f7645c79d5ae46fe6f3.png)

</div>

</div>

<div id="network-processing-phases" class="section">

## Network processing phases[¶](#network-processing-phases "Permalink to this headline")

  - Interrupt handler - device driver fetches data from the RX ring, creates a network packet and queues it to the network stack for processing
  - NET\_SOFTIRQ - packet goes through the stack layer and it is processed: decapsulate Ethernet frame, check IP packet and route it, if local packet decapsulate protocol packet (e.g. TCP) and queues it to a socket
  - Process context - application fetches data from the socket queue or pushes data to the socket queue

</div>

<div id="packet-routing" class="section">

## Packet Routing[¶](#packet-routing "Permalink to this headline")

![../\_images/ditaa-528948c80a3fd78b89fb6f7bd69503a58b93a4ae.png](../_images/ditaa-528948c80a3fd78b89fb6f7bd69503a58b93a4ae.png)

<div id="routing-table-s" class="section">

### Routing Table(s)[¶](#routing-table-s "Permalink to this headline")

<div class="admonition-routing-table highlight-shell">

<div class="highlight">

    tavi@desktop-tavi:~/src/linux$ ip route list table main
    default via 172.30.240.1 dev eth0
    172.30.240.0/20 dev eth0 proto kernel scope link src 172.30.249.241
    
    tavi@desktop-tavi:~/src/linux$ ip route list table local
    broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
    local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
    local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1
    broadcast 127.255.255.255 dev lo proto kernel scope link src 127.0.0.1
    broadcast 172.30.240.0 dev eth0 proto kernel scope link src 172.30.249.241
    local 172.30.249.241 dev eth0 proto kernel scope host src 172.30.249.241
    broadcast 172.30.255.255 dev eth0 proto kernel scope link src 172.30.249.241
    
    tavi@desktop-tavi:~/src/linux$ ip rule list
    0:      from all lookup local
    32766:  from all lookup main
    32767:  from all lookup default

</div>

</div>

</div>

<div id="routing-policy-database" class="section">

### Routing Policy Database[¶](#routing-policy-database "Permalink to this headline")

  - "Regular" routing only uses the destination address
  - To increase flexibility a "Routing Policy Database" is used that allows different routing based on other fields such as the source address, protocol type, transport ports, etc.
  - This is encoded as a list of rules that are evaluated based on their priority (priority 0 is the highest)
  - Each rule has a selector (how to match the packet) and an action (what action to take if the packet matches)
  - Selectors: source address, destination address, type of service (TOS), input interface, output interface, etc.
  - Action: lookup / unicast - use given routing table, blackhole - drop packet, unreachable - send ICMP unreachable message and drop packet, etc.

</div>

<div id="routing-table-processing" class="section">

### Routing table processing[¶](#routing-table-processing "Permalink to this headline")

  - Special table for local addreses -\> route packets to sockets based on family, type, ports
  - Check every routing entry for starting with the most specific routes (e.g. 192.168.0.0/24 is checked before 192.168.0.0/16)
  - A route matches if the packet destination addreess logical ORed with the subnet mask equals the subnet address
  - Once a route matches the following information is retrieved: interface, link layer next-hop address, network next host address

</div>

<div id="forwarding-information-database" class="section">

### Forwarding Information Database[¶](#forwarding-information-database "Permalink to this headline")

 

![../\_images/fidb-overview1.png](../_images/fidb-overview1.png) ![../\_images/fidb-details1.png](../_images/fidb-details1.png)

 

![../\_images/routing-cache1.png](../_images/routing-cache1.png)

 

![../\_images/fib-trie1.png](../_images/fib-trie1.png)

 

![../\_images/fib-trie-compressed1.png](../_images/fib-trie-compressed1.png)

</div>

</div>

<div id="netfilter" class="section">

## Netfilter[¶](#netfilter "Permalink to this headline")

  - Framework that implements packet filtering and NAT
  - It uses hooks inserted in key places in the packet flow:
      - NF\_IP\_PRE\_ROUTING
      - NF\_IP\_LOCAL\_IN
      - NF\_IP\_FORWARD
      - NF\_IP\_LOCAL\_OUT
      - NF\_IP\_POST\_ROUTING
      - NF\_IP\_NUMHOOKS

</div>

<div id="network-packets-skbs-struct-sk-buff" class="section">

## Network packets / skbs (struct sk\_buff)[¶](#network-packets-skbs-struct-sk-buff "Permalink to this headline")

![../\_images/skb1.png](../_images/skb1.png)

<div class="admonition-struct-sk-buff highlight-c">

<div class="highlight">

    struct sk_buff {
        struct sk_buff *next;
        struct sk_buff *prev;
    
        struct sock *sk;
        ktime_t tstamp;
        struct net_device *dev;
        char cb[48];
    
        unsigned int len,
        data_len;
        __u16 mac_len,
        hdr_len;
    
        void (*destructor)(struct sk_buff *skb);
    
        sk_buff_data_t transport_header;
        sk_buff_data_t network_header;
        sk_buff_data_t mac_header;
        sk_buff_data_t tail;
        sk_buff_data_t end;
    
        unsigned char *head,
        *data;
        unsigned int truesize;
        atomic_t users;

</div>

</div>

<div class="admonition-skb-apis highlight-c">

<div class="highlight">

    /* reserve head room */
    void skb_reserve(struct sk_buff *skb, int len);
    
    /* add data to the end */
    unsigned char *skb_put(struct sk_buff *skb, unsigned int len);
    
    /* add data to the top */
    unsigned char *skb_push(struct sk_buff *skb, unsigned int len);
    
    /* discard data at the top */
    unsigned char *skb_pull(struct sk_buff *skb, unsigned int len);
    
    /* discard data at the end */
    unsigned char *skb_trim(struct sk_buff *skb, unsigned int len);
    
    unsigned char *skb_transport_header(const struct sk_buff *skb);
    
    void skb_reset_transport_header(struct sk_buff *skb);
    
    void skb_set_transport_header(struct sk_buff *skb, const int offset);
    
    unsigned char *skb_network_header(const struct sk_buff *skb);
    
    void skb_reset_network_header(struct sk_buff *skb);
    
    void skb_set_network_header(struct sk_buff *skb, const int offset);
    
    unsigned char *skb_mac_header(const struct sk_buff *skb);
    
    int skb_mac_header_was_set(const struct sk_buff *skb);
    
    void skb_reset_mac_header(struct sk_buff *skb);
    
    void skb_set_mac_header(struct sk_buff *skb, const int offset);

</div>

</div>

 

[![../\_images/ditaa-91073cb05a3f537eb54ab10745c307531e6795a0.png](../_images/ditaa-91073cb05a3f537eb54ab10745c307531e6795a0.png)](../_images/ditaa-91073cb05a3f537eb54ab10745c307531e6795a0.png)

</div>

<div id="network-device" class="section">

## Network Device[¶](#network-device "Permalink to this headline")

![../\_images/net-dev-hw1.png](../_images/net-dev-hw1.png)

  - Scatter-Gather
  - Checksum offloading: Ethernet, IP, UDP, TCP
  - Adaptive interrupt handling (coalescence, adaptive)

</div>

<div id="hardware-and-software-acceleration-techniques" class="section">

## Hardware and Software Acceleration Techniques[¶](#hardware-and-software-acceleration-techniques "Permalink to this headline")

  - Full offload - Implement TCP/IP stack in hardware
  - Issues:
      - Scaling number of connections
      - Security
      - Conformance

<!-- end list -->

  - Performance is proportional with the number of packets to be processed
  - Example: if an end-point can process 60K pps
      - 1538 MSS -\> 738Mbps
      - 2038 MSS -\> 978Mbps
      - 9038 MSS -\> 4.3Gbps
      - 20738 MSS -\> 9.9Gbps

<!-- end list -->

  - The networking stack processes large packets
  - TX path: the hardware splits large packets in smaller packets (TCP Segmentation Offload)
  - RX path: the hardware aggregates small packets into larger packets (Large Receive Offload - LRO)

![../\_images/tso1.png](../_images/tso1.png) ![../\_images/lro1.png](../_images/lro1.png)

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lec9-debugging.html "SO2 Lecture 09 - Kernel debugging") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lec11-arch.html "SO2 Lecture 11 - Architecture Layer")

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
