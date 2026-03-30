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
  - [Memory Management](memory-management.html)
  - [Filesystem Management](fs.html)
  - [Debugging](debugging.html)
  - [Network Management](#)
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
  - Network Management
  - [View page source](../_sources/lectures/networking.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="network-management" class="section">

# Network Management[¶](#network-management "Permalink to this headline")

[View slides](networking-slides.html)

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

 

![../\_images/fidb-overview.png](../_images/fidb-overview.png) ![../\_images/fidb-details.png](../_images/fidb-details.png)

 

![../\_images/routing-cache.png](../_images/routing-cache.png)

 

![../\_images/fib-trie.png](../_images/fib-trie.png)

 

![../\_images/fib-trie-compressed.png](../_images/fib-trie-compressed.png)

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

![../\_images/skb.png](../_images/skb.png)

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

![../\_images/net-dev-hw.png](../_images/net-dev-hw.png)

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

![../\_images/tso.png](../_images/tso.png) ![../\_images/lro.png](../_images/lro.png)

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](debugging.html "Debugging") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](arch.html "Architecture Layer")

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
