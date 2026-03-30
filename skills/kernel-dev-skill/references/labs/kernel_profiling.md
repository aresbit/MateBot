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
  - [File system drivers (Part 2)](filesystems_part2.html)
  - [Networking](networking.html)
  - [Kernel Development on ARM](arm_kernel_development.html)
  - [Memory mapping](memory_mapping.html)
  - [Linux Device Model](device_model.html)
  - [Kernel Profiling](#)
      - [Lab Objectives](#lab-objectives)
      - [Overview](#overview)
      - [Profiling Tools](#profiling-tools)
          - [perf](#perf)
          - [ps](#ps)
          - [time](#time)
          - [top](#top)
      - [Profiling Methodology](#profiling-methodology)
      - [Exercises](#exercises)
      - [0. Demo: Profiling I/O Problems](#demo-profiling-i-o-problems)
          - [1. Investigating Reduced Responsiveness](#investigating-reduced-responsiveness)
          - [2. Launching New Threads](#launching-new-threads)
          - [3. Tuning `cp`](#tuning-cp)
          - [4. I/O Latency](#i-o-latency)
          - [5. Bad ELF](#bad-elf)

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
  - Kernel Profiling
  - [View page source](../_sources/labs/kernel_profiling.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="kernel-profiling" class="section">

# Kernel Profiling[¶](#kernel-profiling "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab Objectives[¶](#lab-objectives "Permalink to this headline")

> 
> 
> <div>
> 
>   - Familiarize yourself with the basics of Linux kernel profiling
>   - Understanding basic profiling tools
>   - Learning profiling methodologies and good practices
> 
> </div>

</div>

<div id="overview" class="section">

## Overview[¶](#overview "Permalink to this headline")

Up until now we have studied how the different components of the Linux kernel work, and how to write drivers that interface with them in order to provide support for devices or protocols. This has helped us understand how the Linux kernel works, but most people will not get to write kernel drivers.

Nonetheless, the skills learned will help us to write applications that better integrate with the whole operating system. In order to do this, one has to have a good view of both the user space and the kernel space.

This session aims to merge the work we have done up until now in the kernel space with real world use cases where we do not write kernel space code, but we look through the kernel using profiling tools, in order to debug issues that we're having when writing regular, low-level, applications.

Another focus of this session will be learning a general methodology for debugging software issues, and we will approach some tools that give us insight from the kernel on the way our application runs.

</div>

<div id="profiling-tools" class="section">

## Profiling Tools[¶](#profiling-tools "Permalink to this headline")

The main tool that we will focus our attention on is `perf`, which offers support for tracing applications, and also inspecting general aspects of the system. We will also be using debugging tools that most people have used in their day to day life, such as `htop`, `ps`, `lsof` and others.

<div id="perf" class="section">

### perf[¶](#perf "Permalink to this headline")

`perf` is a tool that instruments the CPU using tracepoints, kprobes and uprobes. This tool allows us to take a look at what functions are being called at a given point. This allows us to take a peak at where the kernel is pending the most time, print out call stacks of functions, and in general log what the CPU is running.

`perf` integrates modules such as: \* static tracing \* dynamic tracing \* resource monitoring

The tracing interface that is offered by perf can be used by itself, using the `perf` command together with its subcommands.

<div class="highlight-bash">

<div class="highlight">

    root@qemux86:~# ./skels/kernel_profiling/perf
    
     usage: perf [--version] [--help] [OPTIONS] COMMAND [ARGS]
    
     The most commonly used perf commands are:
       annotate        Read perf.data (created by perf record) and display annotated code
       archive         Create archive with object files with build-ids found in perf.data file
       bench           General framework for benchmark suites
       buildid-cache   Manage build-id cache.
       buildid-list    List the buildids in a perf.data file
       c2c             Shared Data C2C/HITM Analyzer.
       config          Get and set variables in a configuration file.
       data            Data file related processing
       diff            Read perf.data files and display the differential profile
       evlist          List the event names in a perf.data file
       ftrace          simple wrapper for kernel's ftrace functionality
       inject          Filter to augment the events stream with additional information
       kallsyms        Searches running kernel for symbols
       kmem            Tool to trace/measure kernel memory properties
       kvm             Tool to trace/measure kvm guest os
       list            List all symbolic event types
       lock            Analyze lock events
       mem             Profile memory accesses
       record          Run a command and record its profile into perf.data
       report          Read perf.data (created by perf record) and display the profile
       sched           Tool to trace/measure scheduler properties (latencies)
       script          Read perf.data (created by perf record) and display trace output
       stat            Run a command and gather performance counter statistics
       test            Runs sanity tests.
       timechart       Tool to visualize total system behavior during a workload
       top             System profiling tool.
       version         display the version of perf binary
       probe           Define new dynamic tracepoints
    
     See 'perf help COMMAND' for more information on a specific command.

</div>

</div>

In the output above we can see all of perf's subcommands together with a description of their functionality, the most significant of which are:

  - `stat` - displays statistics such as the number of context switches and page faults;
  - `top` - an interactive interface where we can inspect the most frequent function calls and their caller. This interface allows us direct feedback while profiling;
  - `list` - lists the static trace point that we can instrument inside the kernel. These are useful when trying to get an insight from inside the kernel;
  - `probe` - add a dynamic trace point that instruments a function call in order to be recorded by perf;
  - `record` - records function calls and stack traces based on tracing points defined by the user; It can also record specific function calls and their stack traces. The record is saved in a file, named `perf.data` by default;
  - `report` - displays the information saved in a perf recording.

Another way to use perf's interface is through scripts that wrap over perf that offer a higher level way of looking at events or data, without needing to know the intricacies of the command. An example of this is the `iosnoop.sh` script, which displays what I/O transfers are taking place.

</div>

<div id="ps" class="section">

### ps[¶](#ps "Permalink to this headline")

`ps` is the Linux tool that allows us to monitor the processes that are running at a given time on the machine, including the kernel threads. This is a simple and easy to use way of checking at a glance what processes are running on the CPU, and what is their CPU and memory usage.

In order to list all the processes running, we use to `ps aux` command in the following way:

<div class="highlight-c">

<div class="highlight">

    TODO
    root@qemux86:~/skels/kernel_profiling/0-demo# cd
     root@qemux86:~# ps aux
     USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
     root         1  0.0  0.5   2004  1256 ?        Ss   12:06   0:12 init [5]
     root         2  0.0  0.0      0     0 ?        S    12:06   0:00 [kthreadd]
     [...]
     root       350  4.5  4.4  11132 10688 hvc0     T    12:07  17:21 ./io-app
     root      1358  0.0  0.0      0     0 ?        I    14:30   0:00 [kworker/u2:1-e
     root      2293  0.1  1.5   5516  3704 ?        Ss   18:18   0:00 sshd: root@pts/
     root      2295  0.0  1.3   3968  3232 pts/0    Ss+  18:19   0:00 -sh
     root      2307  0.0  0.0      0     0 ?        I    18:19   0:00 [kworker/u2:2-e
     root      2350  0.0  0.7   3032  1792 hvc0     R+   18:26   0:00 ps aux
     root      2392  2.6  0.0      0     0 ?        D    18:31   0:00 test-script

</div>

</div>

One information of note is that the 7th column represents the that of the process, `S` meaning suspended, `D` suspended due to I/O, and `R` meaning running.

</div>

<div id="time" class="section">

### time[¶](#time "Permalink to this headline")

The `time` command allows us to inspect the amount of time spent by a process in I/O, running the application code, or running code in kernel space. This can be useful in order to find out whether an application's issue comes from running too much in kernel space, so it has some overhead when it does system calls, or the issue is in the user code.

<div class="highlight-c">

<div class="highlight">

    root@qemux86:~# time dd if=/dev/urandom of=./test-file bs=1K count=10
    10+0 records in
    10+0 records out
    10240 bytes (10 kB, 10 KiB) copied, 0.00299749 s, 3.4 MB/s
    
    real        0m0.020s
    user        0m0.001s
    sys 0m0.015s

</div>

</div>

In the output above we timed the generation of a file using `dd`. The result of the timing is displayed at the bottom of output. The values outputted by the tool are the following:

  - `real` - the amount of time has passed from the start of the application to its finishing;
  - `user` - time spent running the `dd` code;
  - `sys` - time spent running kernel code on behalf of the process.

We see that the sum of the `user` and `sys` values doesn't add up to the `real` value. This happens either when the application runs on multiple cores, in which case the sum might be higher, or the application sleeps, in which case the sum is lower.

</div>

<div id="top" class="section">

### top[¶](#top "Permalink to this headline")

`top` is an application that is found on most systems which lists in real time the applications that are running on the system. `top` runs interactively, and it auto-refreshes its output, as opposed to `ps`. We use this tool when we want a high level of continuous monitoring.

</div>

</div>

<div id="profiling-methodology" class="section">

## Profiling Methodology[¶](#profiling-methodology "Permalink to this headline")

When doing profiling, our goal is to identify the cause of a problem. Usually this problem is observed by someone when their application doesn't work as expected. When we say that an application did not work as expected, this can mean different things for different people. For example, one person might complain that the application has a slowdown, while another might say that the application runs on the CPU, but it doesn't output anything.

The first step in any problem solving context is to understand the default behaviour of the application we're trying to debug, and to make sure that it is now not running in the expected parameters.

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

The current lab name is kernel\_profiling. See the exercises for the task name.

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

The modules are placed in /home/root/skels/kernel\_profiling/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

<div class="admonition note">

Note

This session will require us to use the `perf` tracing tool. When running natively on our systems, we have to install the `linux-tools-<version>-generic` package using a package manager in order to run it. Because in our visual machine we don't have access to a package manager, we will be downloading the `perf` binary from [this](http://swarm.cs.pub.ro/~sweisz/perf) link. Download the application in the `skels/kernel_profiling` directory, and grant in execution permissions.

</div>

<div class="admonition warning">

Warning

When running `perf`, make sure that you're running the downloaded version, not the version in the `PATH` variable.

</div>

<div class="admonition note">

Note

When going through this session's exercises, we will have to run command in parallel. In order to do this, we will have to connect to the virtual machine using SSH. We recommend using the `core-image-sato-sdk-qemu` image, since it has the tools that we need. To run the virtual machine using the `core-image-sato-sdk-qemu` file system, uncomment line 16 in the `qemu/Makefile` file.

</div>

<div class="admonition note">

Note

If you wish to run the `perf-tools` based scripts that we have included in the repository, such as `iosnoop.sh`, you will have to grant it execution privilleges, in order to be copied to the virtual machine file system.

</div>

<div class="admonition note">

Note

In order to improve the course of SO2, its components and the way it is conducted, your opinions are very useful to us. Please fill the feedback form on [curs.upb.ro platform](https://curs.upb.ro/2022/mod/feedbackadm/view.php?id=15292).

The form is anonymous and is active between May 22 and June 2, 2023. The results will be visible to the SO2 team after all the grades have been marked.

We invite you to evaluate the activity of the SO2 team and specify its strengths and weaknesses and your suggestions for improving the subject. Your feedback is very important to us to increase the quality of the subject in the coming years.

We are particularly interested in:

> 
> 
> <div>
> 
>   - What did you not like and what do you think did not go well?
>   - Why didn't you like it and why do you think it didn't go well?
>   - What should we do to make things better?
> 
> </div>

</div>

</div>

<div id="demo-profiling-i-o-problems" class="section">

## 0\. Demo: Profiling I/O Problems[¶](#demo-profiling-i-o-problems "Permalink to this headline")

When working with I/O, we have to keep in mind that it is one of the slowest systems in the operating system, compared to memory, which is an order of magnitude faster, and scheduling, which deals with what is currently running on the CPU.

Because of this, I/O operations have do be thought out, because you might starve you application by saturating the system with requests. Another issue that you might face is that the I/O's slow speed might affect your application's responsiveness, if it waits for the I/O operations to finish.

Let's take a look at an application and debug its issues.

We are going to run the `io-app` application, from the `0-demo` directory.

In order to inspect what is running on the CPU, and look at the stack of the process, we can use the `perf record` subcommand in the following way:

<div class="highlight-bash">

<div class="highlight">

    root@qemux86:~# ./perf record -a -g
    Couldn't synthesize bpf events.
    ^C[ perf record: Woken up 7 times to write data ]
    [ perf record: Captured and wrote 1.724 MB perf.data (8376 samples) ]

</div>

</div>

perf will record values indefinitely, but we can close it using the `Ctrl+c` hotkey. We used the `-a` option in order to probe all CPUs, and `-g` option, which record the whole call stack.

To visualize the recorded information, we will use the `perf report` command, which will bring up a pager which will display the most frequent function calls that were found on the CPU, and their call stack.

<div class="highlight-bash">

<div class="highlight">

    root@qemux86:~# ./perf report --header -F overhead,comm,parent
    # Total Lost Samples: 0
    #
    # Samples: 8K of event 'cpu-clock:pppH'
    # Event count (approx.): 2094000000
    #
    # Overhead  Command          Parent symbol
    # ........  ...............  .............
    #
        58.63%  io-app           [other]
                |
                 --58.62%--__libc_start_main
                           main
                           __kernel_vsyscall
                           |
                            --58.61%--__irqentry_text_end
                                      do_SYSENTER_32
                                      do_fast_syscall_32
                                      __noinstr_text_start
                                      __ia32_sys_write
                                      ksys_write
                                      vfs_write
                                      |
                                       --58.60%--ext4_file_write_iter
                                                 ext4_buffered_write_iter
    [...]

</div>

</div>

We have used the `--header` in order to print the table header, and `-F overhead,comm,parent`, in order to print the percentage of time where the call stack, the command and the caller.

We can see that the `io-app` command is doing some writes in the file system, and this contributes to much of the load on the system.

Armed with this information, we know that there are many I/O calls being done by the application. In order to look at the size of these requests, we can use the `iosnoop.sh` script in order to see how big these requests are.

<div class="highlight-bash">

<div class="highlight">

    root@qemux86:~/skels/kernel_profiling# ./iosnoop.sh 1
    Tracing block I/O. Ctrl-C to end.
    COMM         PID    TYPE DEV      BLOCK        BYTES     LATms
    io-app       889    WS   254,0    4800512      1310720     2.10
    io-app       889    WS   254,0    4803072      1310720     2.04
    io-app       889    WS   254,0    4805632      1310720     2.03
    io-app       889    WS   254,0    4808192      1310720     2.43
    io-app       889    WS   254,0    4810752      1310720     3.48
    io-app       889    WS   254,0    4813312      1310720     3.46
    io-app       889    WS   254,0    4815872      524288     1.03
    io-app       889    WS   254,0    5029888      1310720     5.82
    io-app       889    WS   254,0    5032448      786432     5.80
    jbd2/vda-43  43     WS   254,0    2702392      8192       0.22
    kworker/0:1H 34     WS   254,0    2702408      4096       0.40
    io-app       889    WS   254,0    4800512      1310720     2.60
    io-app       889    WS   254,0    4803072      1310720     2.58
    [...]

</div>

</div>

From this output we see that the `io-app` is reading in a loop from the fact that the first block `4800512` is repeating, and that it is doing big reads, since it is reading one megabyte fer request. This constant looping adds the load to the system that we're experiencing.

<div id="investigating-reduced-responsiveness" class="section">

### 1\. Investigating Reduced Responsiveness[¶](#investigating-reduced-responsiveness "Permalink to this headline")

The `io.ko` module, located in the `kernel_profiling/1-io` directory, decreases the system's responsiveness when inserted. We see that the command line stutters when typing commands, but when running top, we see that the system's load is not high, and there aren't any processes that are hogging resources.

Find out what the `io.ko` module is doing and why is it leading to the stuttering effect that we experience.

<div class="admonition hint">

Hint

Trace all the functions being called and check where the CPU is spending most of its time. In order to do this, you can run either `perf record` and `perf report` to view the output, or `perf top`.

</div>

</div>

<div id="launching-new-threads" class="section">

### 2\. Launching New Threads[¶](#launching-new-threads "Permalink to this headline")

We want to run the same function in a loop 100 times in parallel. We have implemented two solutions inside the `scheduling` binary file, located in the `kernel_profiling/2-scheduling` directory.

When executing the `scheduling` binary, it prints a message in parallel from 100 running instances. We can tune this execution by running the application either with the first parameter `0` or `1`.

Find out which solution is better, and why.

</div>

<div id="tuning-cp" class="section">

### 3\. Tuning `cp`[¶](#tuning-cp "Permalink to this headline")

Our goal is to write a copy of the `cp` tool integrated in Linux, which has been implemented by the `memory` binary, in the `kernel_profiling/3-memory` directory. It implements two approaches that we can take for the copy operation:

  - reading the contents of the source file in a buffer in memory using the `read()` system call, and writing that buffer to the destination file using the `write()` system call;
  - mapping the source and destination files to memory using the `mmap` system call, and copying the contents of the source file to the destination in memory.

Another tunable parameter that we're going to use is the block size of to copies that we're going to make, either through reads/writes or in memory.

1\) Investigate which of the two copying mechanisms is faster. For this step, you will use the 1024 block size.

2\) Once you have found which copying mechanism is faster, change the block size parameter and see which value gives you the best copies. Why?

</div>

<div id="i-o-latency" class="section">

### 4\. I/O Latency[¶](#i-o-latency "Permalink to this headline")

We have written a module that reads the content of a disk. Insert the `bio.ko` module, located in the `4-bio` module, we see a large spike in the system's load, as can be seen in the `top` command, but we see that the system is still responsive.

Investigate what is causing the increased load to the system. Is it an I/O issue, or is it a scheduling issue?

<div class="admonition hint">

Hint

Try to trace the I/O operations using `perf`, or use the `iosnoop.sh` script in order to inspect what I/O is happening at a certain point.

</div>

</div>

<div id="bad-elf" class="section">

### 5\. Bad ELF[¶](#bad-elf "Permalink to this headline")

<div class="admonition note">

Note

This is a bonus exercise that has been tested on a native Linux system. It may run under the QEMU virtual machine, but the behavior was weird in our testing. We recommend you used a native (or VirtualBox or VMware) Linux system.

</div>

We managed to build (as part of a [Unikraft](https://github.com/unikraft/unikraft) build) an ELF file that is valid when doing static analysis, but that can't be executed. The file is `bad_elf`, located in the `5-bad-elf/` folder.

Running it triggers a *segmentation fault* message. Running it using `strace` show an error with `execve()`.

<div class="code highlight-none">

<div class="highlight">

    ... skels/kernel_profiling/5-bad-elf$ ./bad_elf
    Segmentation fault
    
    ... skels/kernel_profiling/5-bad-elf$ strace ./bad_elf
    execve("./bad_elf", ["./bad_elf"], 0x7ffc3349ba50 /* 70 vars \*/) = -1 EINVAL (Invalid argument)
    --- SIGSEGV {si_signo=SIGSEGV, si_code=SI_KERNEL, si_addr=NULL} ---
    +++ killed by SIGSEGV +++
    Segmentation fault (core dumped)

</div>

</div>

The ELF file itself is valid:

<div class="code highlight-none">

<div class="highlight">

    ... skels/kernel_profiling/5-bad-elf$ readelf -a bad_elf

</div>

</div>

The issue is to be detected in the kernel.

Use either `perf`, or, better yet [ftrace](https://jvns.ca/blog/2017/03/19/getting-started-with-ftrace/) to inspect the kernel function calls done by the program. Identify the function call that sends out the `SIGSEGV` signal. Identify the cause of the issue. Find that cause in the [manual page elf(5)](https://linux.die.net/man/5/elf).

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](device_model.html "Linux Device Model") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](../info/vm.html "Recommended Setup")

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
