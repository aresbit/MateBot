<div id="slide_container" class="section slides layout-regular">

## Network Management

  - Socket implementation
  - Routing implementation
  - Network Device Interface
  - Hardware and Software Acceleration Techniques

## Network Management Overview

[![../\_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png](../_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png)](../_images/ditaa-a2ded49c8b739635d6742479583443fb10ad120a.png)

## Sockets Implementation Overview

[![../\_images/ditaa-79e3734c36891f6c04d684aa5caa39f76915dbaf.png](../_images/ditaa-79e3734c36891f6c04d684aa5caa39f76915dbaf.png)](../_images/ditaa-79e3734c36891f6c04d684aa5caa39f76915dbaf.png)

## Sockets Families and Protocols

[![../\_images/ditaa-bf1244d1a5c3d99bd8d40148d81cb3e5748c0b94.png](../_images/ditaa-bf1244d1a5c3d99bd8d40148d81cb3e5748c0b94.png)](../_images/ditaa-bf1244d1a5c3d99bd8d40148d81cb3e5748c0b94.png)

## Example: UDP send

<div class="highlight-c">

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

## Example: UDP send

![../\_images/ditaa-ee04e3e544de75375b914f7645c79d5ae46fe6f3.png](../_images/ditaa-ee04e3e544de75375b914f7645c79d5ae46fe6f3.png)

## Network processing phases

  - Interrupt handler - device driver fetches data from the RX ring, creates a network packet and queues it to the network stack for processing
  - NET\_SOFTIRQ - packet goes through the stack layer and it is processed: decapsulate Ethernet frame, check IP packet and route it, if local packet decapsulate protocol packet (e.g. TCP) and queues it to a socket
  - Process context - application fetches data from the socket queue or pushes data to the socket queue

## Packet Routing

![../\_images/ditaa-528948c80a3fd78b89fb6f7bd69503a58b93a4ae.png](../_images/ditaa-528948c80a3fd78b89fb6f7bd69503a58b93a4ae.png)

## Routing Table

<div class="highlight-shell">

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

## Routing Policy Database

  - "Regular" routing only uses the destination address
  - To increase flexibility a "Routing Policy Database" is used that allows different routing based on other fields such as the source address, protocol type, transport ports, etc.
  - This is encoded as a list of rules that are evaluated based on their priority (priority 0 is the highest)
  - Each rule has a selector (how to match the packet) and an action (what action to take if the packet matches)
  - Selectors: source address, destination address, type of service (TOS), input interface, output interface, etc.
  - Action: lookup / unicast - use given routing table, blackhole - drop packet, unreachable - send ICMP unreachable message and drop packet, etc.

## Routing table processing

  - Special table for local addreses -\> route packets to sockets based on family, type, ports
  - Check every routing entry for starting with the most specific routes (e.g. 192.168.0.0/24 is checked before 192.168.0.0/16)
  - A route matches if the packet destination addreess logical ORed with the subnet mask equals the subnet address
  - Once a route matches the following information is retrieved: interface, link layer next-hop address, network next host address

## Forward Information Database (removed in 3.6)

 

![../\_images/fidb-overview.png](../_images/fidb-overview.png)

## Forward Information Database (removed in 3.6)

![../\_images/fidb-details.png](../_images/fidb-details.png)

## Routing Cache (removed in 3.6)

 

![../\_images/routing-cache.png](../_images/routing-cache.png)

## FIB TRIE

 

![../\_images/fib-trie.png](../_images/fib-trie.png)

## Compressed Trie

 

![../\_images/fib-trie-compressed.png](../_images/fib-trie-compressed.png)

## Netfilter

  - Framework that implements packet filtering and NAT
  - It uses hooks inserted in key places in the packet flow:
      - NF\_IP\_PRE\_ROUTING
      - NF\_IP\_LOCAL\_IN
      - NF\_IP\_FORWARD
      - NF\_IP\_LOCAL\_OUT
      - NF\_IP\_POST\_ROUTING
      - NF\_IP\_NUMHOOKS

## Network packets (skbs)

![../\_images/skb.png](../_images/skb.png)

## struct sk\_buff

<div class="highlight-c">

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

## skb APIs

<div class="highlight-c">

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

## skb data management

 

[![../\_images/ditaa-91073cb05a3f537eb54ab10745c307531e6795a0.png](../_images/ditaa-91073cb05a3f537eb54ab10745c307531e6795a0.png)](../_images/ditaa-91073cb05a3f537eb54ab10745c307531e6795a0.png)

## Network Device Interface

![../\_images/net-dev-hw.png](../_images/net-dev-hw.png)

## Advanced features

  - Scatter-Gather
  - Checksum offloading: Ethernet, IP, UDP, TCP
  - Adaptive interrupt handling (coalescence, adaptive)

## TCP offload

  - Full offload - Implement TCP/IP stack in hardware
  - Issues:
      - Scaling number of connections
      - Security
      - Conformance

## Performance observation

  - Performance is proportional with the number of packets to be processed
  - Example: if an end-point can process 60K pps
      - 1538 MSS -\> 738Mbps
      - 2038 MSS -\> 978Mbps
      - 9038 MSS -\> 4.3Gbps
      - 20738 MSS -\> 9.9Gbps

## Stateless offload

  - The networking stack processes large packets
  - TX path: the hardware splits large packets in smaller packets (TCP Segmentation Offload)
  - RX path: the hardware aggregates small packets into larger packets (Large Receive Offload - LRO)

## TCP Segmentation Offload

![../\_images/tso.png](../_images/tso.png)

## Large Receive Offload

![../\_images/lro.png](../_images/lro.png)

</div>

<div id="slide_notes" class="section">

</div>
