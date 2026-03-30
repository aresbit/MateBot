<div id="slide_container" class="section slides layout-regular">

# SO2 Lecture 06 - Address Space

## Address Space

  - x86 MMU
      - Segmentation
      - Paging
      - TLB
  - Linux Address Space
      - User
      - Kernel
      - High memory

## x86 MMU

 

![../\_images/ditaa-f3703e3f627a948c59f6f960518d5f68eb7becec.png](../_images/ditaa-f3703e3f627a948c59f6f960518d5f68eb7becec.png)

## Selectors

 

![../\_images/ditaa-d6845a04f0ec792beec598d2a9f4c5b92c65529e.png](../_images/ditaa-d6845a04f0ec792beec598d2a9f4c5b92c65529e.png)

  - Selectors: CS, DS, SS, ES, FS, GS
  - Index: indexes the segment descriptor table
  - TI: selects either the GDT or LDT
  - RPL: for CS only indicates the running (current) priviledge level
  - GDTR and LDTR registers points to the base of GDP and LDT

## Segment descriptor

 

![../\_images/ditaa-5cd4a8fa1ad97cff4bb1f64da13ce9ebfcfc4562.png](../_images/ditaa-5cd4a8fa1ad97cff4bb1f64da13ce9ebfcfc4562.png)

  - Base: linear address for the start of the segment
  - Limit: size of the segment
  - G: granularity bit: if set the size is in bytes otherwise in 4K pages
  - B/D: data/code
  - Type: code segment, data/stack, TSS, LDT, GDT
  - Protection: the minimum priviledge level required to access the segment (RPL is checked against DPL)

## Segmentation in Linux

<div class="highlight-c">

<div class="highlight">

    /*
     * The layout of the per-CPU GDT under Linux:
     *
     *   0 - null                                                             <=== cacheline #1
     *   1 - reserved
     *   2 - reserved
     *   3 - reserved
     *
     *   4 - unused                                                           <=== cacheline #2
     *   5 - unused
     *
     *  ------- start of TLS (Thread-Local Storage) segments:
     *
     *   6 - TLS segment #1                   [ glibc's TLS segment ]
     *   7 - TLS segment #2                   [ Wine's %fs Win32 segment ]
     *   8 - TLS segment #3                                                   <=== cacheline #3
     *   9 - reserved
     *  10 - reserved
     *  11 - reserved
     *
     *  ------- start of kernel segments:
     *
     *  12 - kernel code segment                                              <=== cacheline #4
     *  13 - kernel data segment
     *  14 - default user CS
     *  15 - default user DS
     *  16 - TSS                                                              <=== cacheline #5
     *  17 - LDT
     *  18 - PNPBIOS support (16->32 gate)
     *  19 - PNPBIOS support
     *  20 - PNPBIOS support                                                  <=== cacheline #6
     *  21 - PNPBIOS support
     *  22 - PNPBIOS support
     *  23 - APM BIOS support
     *  24 - APM BIOS support                                                 <=== cacheline #7
     *  25 - APM BIOS support
     *
     *  26 - ESPFIX small SS
     *  27 - per-cpu                  [ offset to per-cpu data area ]
     *  28 - stack_canary-20          [ for stack protector ]                 <=== cacheline #8
     *  29 - unused
     *  30 - unused
     *  31 - TSS for double fault handler
     */
    
     DEFINE_PER_CPU_PAGE_ALIGNED(struct gdt_page, gdt_page) = { .gdt = {
     #ifdef CONFIG_X86_64
             /*
              * We need valid kernel segments for data and code in long mode too
              * IRET will check the segment types  kkeil 2000/10/28
              * Also sysret mandates a special GDT layout
              *
              * TLS descriptors are currently at a different place compared to i386.
              * Hopefully nobody expects them at a fixed place (Wine?)
              */
             [GDT_ENTRY_KERNEL32_CS]         = GDT_ENTRY_INIT(0xc09b, 0, 0xfffff),
             [GDT_ENTRY_KERNEL_CS]           = GDT_ENTRY_INIT(0xa09b, 0, 0xfffff),
             [GDT_ENTRY_KERNEL_DS]           = GDT_ENTRY_INIT(0xc093, 0, 0xfffff),
             [GDT_ENTRY_DEFAULT_USER32_CS]   = GDT_ENTRY_INIT(0xc0fb, 0, 0xfffff),
             [GDT_ENTRY_DEFAULT_USER_DS]     = GDT_ENTRY_INIT(0xc0f3, 0, 0xfffff),
             [GDT_ENTRY_DEFAULT_USER_CS]     = GDT_ENTRY_INIT(0xa0fb, 0, 0xfffff),
     #else
             [GDT_ENTRY_KERNEL_CS]           = GDT_ENTRY_INIT(0xc09a, 0, 0xfffff),
             [GDT_ENTRY_KERNEL_DS]           = GDT_ENTRY_INIT(0xc092, 0, 0xfffff),
             [GDT_ENTRY_DEFAULT_USER_CS]     = GDT_ENTRY_INIT(0xc0fa, 0, 0xfffff),
             [GDT_ENTRY_DEFAULT_USER_DS]     = GDT_ENTRY_INIT(0xc0f2, 0, 0xfffff),
             /*
              * Segments used for calling PnP BIOS have byte granularity.
              * They code segments and data segments have fixed 64k limits,
              * the transfer segment sizes are set at run time.
              */
             /* 32-bit code */
             [GDT_ENTRY_PNPBIOS_CS32]        = GDT_ENTRY_INIT(0x409a, 0, 0xffff),
             /* 16-bit code */
             [GDT_ENTRY_PNPBIOS_CS16]        = GDT_ENTRY_INIT(0x009a, 0, 0xffff),
             /* 16-bit data */
             [GDT_ENTRY_PNPBIOS_DS]          = GDT_ENTRY_INIT(0x0092, 0, 0xffff),
             /* 16-bit data */
             [GDT_ENTRY_PNPBIOS_TS1]         = GDT_ENTRY_INIT(0x0092, 0, 0),
             /* 16-bit data */
             [GDT_ENTRY_PNPBIOS_TS2]         = GDT_ENTRY_INIT(0x0092, 0, 0),
             /*
              * The APM segments have byte granularity and their bases
              * are set at run time.  All have 64k limits.
              */
             /* 32-bit code */
             [GDT_ENTRY_APMBIOS_BASE]        = GDT_ENTRY_INIT(0x409a, 0, 0xffff),
             /* 16-bit code */
             [GDT_ENTRY_APMBIOS_BASE+1]      = GDT_ENTRY_INIT(0x009a, 0, 0xffff),
             /* data */
             [GDT_ENTRY_APMBIOS_BASE+2]      = GDT_ENTRY_INIT(0x4092, 0, 0xffff),
    
             [GDT_ENTRY_ESPFIX_SS]           = GDT_ENTRY_INIT(0xc092, 0, 0xfffff),
             [GDT_ENTRY_PERCPU]              = GDT_ENTRY_INIT(0xc092, 0, 0xfffff),
             GDT_STACK_CANARY_INIT
     #endif
     } };
     EXPORT_PER_CPU_SYMBOL_GPL(gdt_page);

</div>

</div>

## Inspecting selectors and segments

 

## Regular paging

 

![../\_images/ditaa-def299abebe530d760a6c8f16c791bbb016f9238.png](../_images/ditaa-def299abebe530d760a6c8f16c791bbb016f9238.png)

## Extended paging

![../\_images/ditaa-709c2e7a68bfcdcfe9c1938d6ef2a0c9b5627931.png](../_images/ditaa-709c2e7a68bfcdcfe9c1938d6ef2a0c9b5627931.png)

## Page tables

  - Both page directory and page table have 1024 entries
  - Each entry has 4 bytes
  - The special CR3 register point to the base of the page directory
  - Page directory entries points to the base of the page table
  - All tables are stored in memory
  - All table addresses are physical addresses

## Page table entry fields

  - Present/Absent
  - PFN (Page Frame Number): the most 20 significant bits of the physical address
  - Accessed - not updated by hardware (can be used by OS for housekeeping)
  - Dirty - not updated by hardware (can be used by OS for housekeeping)
  - Access rights: Read/Write
  - Privilege: User/Supervisor
  - Page size - only for page directory; if set extended paging is used
  - PCD (page cache disable), PWT (page write through)

## Linux paging

![../\_images/ditaa-5e4d73e3fcb24db9d1f8c16daddf98694c063fe6.png](../_images/ditaa-5e4d73e3fcb24db9d1f8c16daddf98694c063fe6.png)

## Linux APIs for page table handling

<div class="highlight-c">

<div class="highlight">

    struct * page;
    pgd_t pgd;
    pmd_t pmd;
    pud_t pud;
    pte_t pte;
    void *laddr, *paddr;
    
    pgd = pgd_offset(mm, vaddr);
    pud = pud_offet(pgd, vaddr);
    pmd = pmd_offset(pud, vaddr);
    pte = pte_offset(pmd, vaddr);
    page = pte_page(pte);
    laddr = page_address(page);
    paddr = virt_to_phys(laddr);

</div>

</div>

## What about platforms with less then 4 levels of pagination?

<div class="highlight-c">

<div class="highlight">

    static inline pud_t * pud_offset(pgd_t * pgd,unsigned long address)
    {
        return (pud_t *)pgd;
    }
    
    static inline pmd_t * pmd_offset(pud_t * pud,unsigned long address)
    {
        return (pmd_t *)pud;
    }

</div>

</div>

## Translation Look-aside Buffer

  - Caches paging information (PFN, rights, privilege)
  - Content Addressable Memory / Associative Memory
      - Very small (64-128)
      - Very fast (single cycle due to parallel search implementation)
  - CPUs usually have two TLBs: i-TLB (code) and d-TLB (data)
  - TLB miss penalty: up hundreds of cycles

## TLB invalidation

Single address invalidation:

<div class="highlight-asm">

<div class="highlight">

    mov $addr, %eax
    invlpg %(eax)

</div>

</div>

Full invalidation:

<div class="highlight-asm">

<div class="highlight">

    mov %cr3, %eax
    mov %eax, %cr3

</div>

</div>

## Address space options for 32bit systems

 

![../\_images/ditaa-d5d1129b0298a2ea5f116c9d4b246eb1b888db6b.png](../_images/ditaa-d5d1129b0298a2ea5f116c9d4b246eb1b888db6b.png)

## Advantages and disadvantages

  - Disadvantages for dedicated kernel space:
      - Fully invalidating the TLB for every system call
  - Disadvantages for shared address space
      - Less address space for both kernel and user processes

## Linux address space for 32bit systems

 

![../\_images/ditaa-3985c420def8f30934a72ea8c738a00ed629c298.png](../_images/ditaa-3985c420def8f30934a72ea8c738a00ed629c298.png)

## Virtual to physical address translations for I/O transfers

  - Use the virtual address of a kernel buffer in order to copy to data from from user space
  - Walk the page tables to transform the kernel buffer virtual address to a physical address
  - Use the physical address of the kernel buffer to start a DMA transfer

## Linear mappings

  - Virtual to physical address space translation is reduced to one operation (instead of walking the page tables)
  - Less memory is used to create the page tables
  - Less TLB entries are used for the kernel memory

## Highmem

 

![../\_images/ditaa-bb8455a43088bf800eece11869f6ff857574605d.png](../_images/ditaa-bb8455a43088bf800eece11869f6ff857574605d.png)

## Multi-page permanent mappings

<div class="highlight-c">

<div class="highlight">

    void* vmalloc(unsigned long size);
    void vfree(void * addr);
    
    void *ioremap(unsigned long offset, unsigned size);
    void iounmap(void * addr);

</div>

</div>

## Fixed-mapped linear addresses

  - Reserved virtual addresses (constants)
  - Mapped to physical addresses during boot

<div class="highlight-c">

<div class="highlight">

    set_fixmap(idx, phys_addr)
    set_fixmap_nocache(idx, phys_addr)

</div>

</div>

## Fixed-mapped linear addresses

<div class="highlight-c">

<div class="highlight">

    /*
     * Here we define all the compile-time 'special' virtual
     * addresses. The point is to have a constant address at
     * compile time, but to set the physical address only
     * in the boot process.
     * for x86_32: We allocate these special addresses
     * from the end of virtual memory (0xfffff000) backwards.
     * Also this lets us do fail-safe vmalloc(), we
     * can guarantee that these special addresses and
     * vmalloc()-ed addresses never overlap.
     *
     * These 'compile-time allocated' memory buffers are
     * fixed-size 4k pages (or larger if used with an increment
     * higher than 1). Use set_fixmap(idx,phys) to associate
     * physical memory with fixmap indices.
     *
     * TLB entries of such buffers will not be flushed across
     * task switches.
     */
    
    enum fixed_addresses {
    #ifdef CONFIG_X86_32
        FIX_HOLE,
    #else
    #ifdef CONFIG_X86_VSYSCALL_EMULATION
        VSYSCALL_PAGE = (FIXADDR_TOP - VSYSCALL_ADDR) >> PAGE_SHIFT,
    #endif
    #endif
        FIX_DBGP_BASE,
        FIX_EARLYCON_MEM_BASE,
    #ifdef CONFIG_PROVIDE_OHCI1394_DMA_INIT
        FIX_OHCI1394_BASE,
    #endif
    #ifdef CONFIG_X86_LOCAL_APIC
        FIX_APIC_BASE,        /* local (CPU) APIC) -- required for SMP or not */
    #endif
    #ifdef CONFIG_X86_IO_APIC
        FIX_IO_APIC_BASE_0,
        FIX_IO_APIC_BASE_END = FIX_IO_APIC_BASE_0 + MAX_IO_APICS - 1,
    #endif
    #ifdef CONFIG_X86_32
        FIX_KMAP_BEGIN,       /* reserved pte's for temporary kernel mappings */
        FIX_KMAP_END = FIX_KMAP_BEGIN+(KM_TYPE_NR*NR_CPUS)-1,
    #ifdef CONFIG_PCI_MMCONFIG
        FIX_PCIE_MCFG,
    #endif

</div>

</div>

## Conversion between virtual address fixed address indexes

<div class="highlight-c">

<div class="highlight">

    #define __fix_to_virt(x)  (FIXADDR_TOP - ((x) << PAGE_SHIFT))
    #define __virt_to_fix(x)  ((FIXADDR_TOP - ((x)&PAGE_MASK)) >> PAGE_SHIFT)
    
    #ifndef __ASSEMBLY__
    /*
     * 'index to address' translation. If anyone tries to use the idx
     * directly without translation, we catch the bug with a NULL-deference
     * kernel oops. Illegal ranges of incoming indices are caught too.
     */
     static __always_inline unsigned long fix_to_virt(const unsigned int idx)
     {
         BUILD_BUG_ON(idx >= __end_of_fixed_addresses);
         return __fix_to_virt(idx);
     }
    
     static inline unsigned long virt_to_fix(const unsigned long vaddr)
     {
         BUG_ON(vaddr >= FIXADDR_TOP || vaddr < FIXADDR_START);
         return __virt_to_fix(vaddr);
     }
    
    
     inline long fix_to_virt(const unsigned int idx)
     {
         if (idx >= __end_of_fixed_addresses)
             __this_fixmap_does_not_exist();
         return (0xffffe000UL - (idx << PAGE_SHIFT));
     }

</div>

</div>

## Temporary mappings

  - `kmap_atomic()`, `kunmap_atomic()`
  - No context switch is permitted in atomic kmap section
  - Can be used in interrupt context
  - No locking required
  - Only invalidates on TLB entry

## Temporary mappings implementation

<div class="highlight-c">

<div class="highlight">

    #define kmap_atomic(page) kmap_atomic_prot(page, kmap_prot)
    
    void *kmap_atomic_high_prot(struct page *page, pgprot_t prot)
    {
      unsigned long vaddr;
      int idx, type;
    
      type = kmap_atomic_idx_push();
      idx = type + KM_TYPE_NR*smp_processor_id();
      vaddr = __fix_to_virt(FIX_KMAP_BEGIN + idx);
      BUG_ON(!pte_none(*(kmap_pte-idx)));
      set_pte(kmap_pte-idx, mk_pte(page, prot));
      arch_flush_lazy_mmu_mode();
    
      return (void *)vaddr;
    }
    EXPORT_SYMBOL(kmap_atomic_high_prot);
    
    static inline int kmap_atomic_idx_push(void)
    {
      int idx = __this_cpu_inc_return(__kmap_atomic_idx) - 1;
    
    #ifdef CONFIG_DEBUG_HIGHMEM
      WARN_ON_ONCE(in_irq() && !irqs_disabled());
      BUG_ON(idx >= KM_TYPE_NR);
    #endif
      return idx;
    }

</div>

</div>

## Implementation of temporary mappings

  - Use the fixed-mapped linear addresses
  - Every CPU has KM\_TYPE\_NR reserved entries to be used for temporary mappings
  - Stack like selection: every user picks the current entry and increments the "stack" counter

## Permanent mappings

  - `kmap()`, `kunmap()`
  - Context switches are allowed
  - Only available in process context
  - One page table is reserved for permanent mappings
  - Page counter
      - 0 - page is not mapped, free and ready to use
      - 1 - page is not mapped, may be present in TLB needs flushing before using
      - N - page is mapped N-1 times

</div>

<div id="slide_notes" class="section">

</div>
