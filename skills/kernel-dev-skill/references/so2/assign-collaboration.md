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
      - [Collaboration](#)
          - [1. Use Github / Gitlab](#use-github-gitlab)
          - [2. Start with a skeleton for the assignment](#start-with-a-skeleton-for-the-assignment)
          - [3. Add a commit for each individual change](#add-a-commit-for-each-individual-change)
          - [4. Split the work inside the team](#split-the-work-inside-the-team)
          - [5. Do reviews](#do-reviews)
          - [6. Merge the work](#merge-the-work)
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
  - Collaboration
  - [View page source](../_sources/so2/assign-collaboration.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="collaboration" class="section">

# Collaboration[¶](#collaboration "Permalink to this headline")

Collaboration is essential in open source world and we encourage you to pick a team partner to work on selected assignments.

Here is a simple guide to get you started:

<div id="use-github-gitlab" class="section">

## 1\. Use Github / Gitlab[¶](#use-github-gitlab "Permalink to this headline")

Best way to share your work inside the team is to use a version control system (VCS) in order to track each change. Mind that you must make your repo private and only allow read/write access rights to team members.

</div>

<div id="start-with-a-skeleton-for-the-assignment" class="section">

## 2\. Start with a skeleton for the assignment[¶](#start-with-a-skeleton-for-the-assignment "Permalink to this headline")

Add init/exit functions, driver operations and global structures that you driver might need.

<div class="highlight-c">

<div class="highlight">

    // SPDX-License-Identifier: GPL-2.0
    /*
     * uart16550.c - UART16550 driver
     *
     * Author: John Doe <john.doe@mail.com>
     * Author: Ionut Popescu <ionut.popescu@mail.com>
     */
    struct uart16550_dev {
       struct cdev cdev;
       /*TODO */
    };
    
    static struct uart16550_dev devs[MAX_NUMBER_DEVICES];
    
    static int uart16550_open(struct inode *inode, struct file *file)
    {
        /*TODO */
        return 0;
    }
    
    static int uart16550_release(struct inode *inode, struct file *file)
    {
       /*TODO */
       return 0;
    }
    
    static ssize_t uart16550_read(struct file *file,  char __user *user_buffer,
                                  size_t size, loff_t *offset)
    {
          /*TODO */
    }
    
    static ssize_t uart16550_write(struct file *file,
                                   const char __user *user_buffer,
                                   size_t size, loff_t *offset)
    {
         /*TODO */
    }
    
    static long
    uart16550_ioctl(struct file *file, unsigned int cmd, unsigned long arg)
    {
          /*TODO */
          return 0;
    }
    
    static const struct file_operations uart16550_fops = {
           .owner          = THIS_MODULE,
           .open           = uart16550_open,
           .release        = uart16550_release,
           .read           = uart16550_read,
           .write          = uart16550_write,
           .unlocked_ioctl = uart16550_ioctl
    };
    
    static int __init uart16550_init(void)
    {
      /* TODO: */
    }
    
    static void __exit uart16550_exit(void)
    {
       /* TODO: */
    }
    
    module_init(uart16550_init);
    module_exit(uart16550_exit);
    
    MODULE_DESCRIPTION("UART16550 Driver");
    MODULE_AUTHOR("John Doe <john.doe@mail.com");
    MODULE_AUTHOR("Ionut Popescu <ionut.popescu@mail.com");

</div>

</div>

</div>

<div id="add-a-commit-for-each-individual-change" class="section">

## 3\. Add a commit for each individual change[¶](#add-a-commit-for-each-individual-change "Permalink to this headline")

First commit must always be the skeleton file. And the rest of the code should be on top of skeleton file. Please write a good commit mesage. Explain briefly what the commit does and *why* it is necessary.

Follow the seven rules of writing a good commit message: <https://cbea.ms/git-commit/#seven-rules>

<div class="highlight-console">

<div class="highlight">

    Commit 3c92a02cc52700d2cd7c50a20297eef8553c207a (HEAD -> tema2)
    Author: John Doe <john.doe@mail.com>
    Date:   Mon Apr 4 11:54:39 2022 +0300
    
      uart16550: Add initial skeleton for ssignment #2
    
      This adds simple skeleton file for uart16550 assignment. Notice
      module init/exit callbacks and file_operations dummy implementation
      for open/release/read/write/ioctl.
    
      Signed-off-by: John Doe <john.doe@mail.com>

</div>

</div>

</div>

<div id="split-the-work-inside-the-team" class="section">

## 4\. Split the work inside the team[¶](#split-the-work-inside-the-team "Permalink to this headline")

Add TODOs with each team member tasks. Try to split the work evenly.

Before starting to code, make a plan. On top of your skeleton file, add TODOs with each member tasks. Agree on global structures and the overall driver design. Then start coding.

</div>

<div id="do-reviews" class="section">

## 5\. Do reviews[¶](#do-reviews "Permalink to this headline")

Create Pull Requests with your commits and go through review rounds with your team members. You can follow How to create a PR [video](https://www.youtube.com/watch?v=YvoHJJWvn98).

</div>

<div id="merge-the-work" class="section">

## 6\. Merge the work[¶](#merge-the-work "Permalink to this headline")

The final work is the result of merging all the pull requests. Following the commit messages one should clearly understand the progress of the code and how the work was managed inside the team.

<div class="highlight-console">

<div class="highlight">

    f5118b873294 uart16550: Add uart16550_interrupt implementation
    2115503fc3e3 uart16550: Add uart16550_ioctl implementation
    b31a257fd8b8 uart16550: Add uart16550_write implementation
    ac1af6d88a25 uart16550: Add uart16550_read implementation
    9f680e8136bf uart16550: Add uart16550_open/release implementation
    3c92a02cc527 uart16550: Add skeleton for SO2 assignment #2

</div>

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lab12-kernel-profiling.html "SO2 Lab 12 - Kernel Profiling") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](assign0-kernel-api.html "Assignment 0 - Kernel API")

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
