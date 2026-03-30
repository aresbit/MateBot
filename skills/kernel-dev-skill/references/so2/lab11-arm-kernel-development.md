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
      - [SO2 Lab 11 - Kernel Development on ARM](#)
          - [Lab objectives](#lab-objectives)
          - [System on a Chip](#system-on-a-chip)
          - [Board Support package](#board-support-package)
          - [Toolchain](#toolchain)
              - [Compiling the Linux kernel on ARM](#compiling-the-linux-kernel-on-arm)
          - [Linux kernel image](#linux-kernel-image)
          - [Rootfs](#rootfs)
          - [Device tree](#device-tree)
          - [Qemu](#qemu)
          - [Exercises](#exercises)
              - [0. Intro](#intro)
              - [1. Boot](#boot)
              - [2. CPU information](#cpu-information)
              - [3. I/O memory](#i-o-memory)
              - [4. Hello World](#hello-world)
              - [5. Simple device](#simple-device)
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
  - SO2 Lab 11 - Kernel Development on ARM
  - [View page source](../_sources/so2/lab11-arm-kernel-development.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="so2-lab-11-kernel-development-on-arm" class="section">

# SO2 Lab 11 - Kernel Development on ARM[¶](#so2-lab-11-kernel-development-on-arm "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

  - get a feeling of what System on a Chip (SoC) means
  - get familiar with embedded world using ARM as a supported architecture
  - understand what a Board Support Package means (BSP)
  - compile and boot an ARM kernel with Qemu using i.MX6UL platform as an example
  - get familiar with hardware description using Device Trees

</div>

<div id="system-on-a-chip" class="section">

## System on a Chip[¶](#system-on-a-chip "Permalink to this headline")

A System on a Chip (**SoC**) is an integrated circuit (**IC**) that integrates an entire system onto it. The components that can be usually found on an SoC include a central processing unit (**CPU**), memory, input/output ports, storage devices together with more sophisticated modules like audio digital interfaces, neural processing units (**NPU**) or graphical processing units (**GPU**).

  - SoCs can be used in various applications most common are:
    
      - consumer electronics (TV sets, mobile phones, video game consoles)
      - industrial computers (medical imaging, etc)
      - automotive
      - home appliances

The leading architecture for SoCs is **ARM**. Worth mentioning here is that there are also x86-based SoCs platforms. Another thing we need to keep an eye on is **RISC-V** an open standard instruction set architecture.

A simplified view of an **ARM** platform is shown in the image below:

![../\_images/schematic1.png](../_images/schematic1.png)

We will refer as a reference platform at NXP's [i.MX6UL](imx6ul) platform, but in general all SoC's contain the following building blocks:

> 
> 
> <div>
> 
> > 
> > 
> > <div>
> > 
> >   - one or more CPU cores
> >   - a system bus
> >   - clock and reset module
> >       - PLL
> >       - OSC
> >       - reset controller
> > 
> > </div>
> 
>   - interrupt controller
>   - timers
>   - memory controller
>   - peripheral controllers
>       - [I2C](https://en.wikipedia.org/wiki/I%C2%B2C)
>       - [SPI](https://en.wikipedia.org/wiki/Serial_Peripheral_Interface)
>       - [GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output)
>       - [Ethernet](https://en.wikipedia.org/wiki/Network_interface_controller) (for network)
>       - [uSDHC](https://en.wikipedia.org/wiki/MultiMediaCard) (for storage)
>       - USB
>       - [UART](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter)
>       - [I2S](https://en.wikipedia.org/wiki/I%C2%B2S) (for sound)
>       - eLCDIF (for LCD Panel)
> 
> </div>

Here is the complete block diagram for i.MX6UL platform:

<https://www.nxp.com/assets/images/en/block-diagrams/IMX6UL-BD.jpg>

i.MX6UL Evaluation Kit board looks like this:

<https://www.compulab.com/wp-content/gallery/sbc-imx6ul/compulab_sbc-imx6ul_single-board-computer.jpg>

Other popular SoC boards:

> 
> 
> <div>
> 
>   - [Broadcom Raspberry Pi](https://en.wikipedia.org/wiki/Raspberry_Pi)
>   - [Texas Instruments Beagle board](https://en.wikipedia.org/wiki/BeagleBoard)
>   - [Odroid Xu4](https://wiki.odroid.com/odroid-xu4/odroid-xu4)
>   - [Nvidia Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
> 
> </div>

</div>

<div id="board-support-package" class="section">

## Board Support package[¶](#board-support-package "Permalink to this headline")

A board support package (**BSP**) is the minimal set of software packages that allow to demonstrate the capabilities of a certain hardware platform. This includes:

> 
> 
> <div>
> 
>   - toolchain
>   - bootloader
>   - Linux kernel image, device tree files and drivers
>   - root filesystem
> 
> </div>

Semiconductor manufacturers usually provide a **BSP** together with an evaluation board. BSP is typically bundled using [Yocto](https://www.yoctoproject.org/)

</div>

<div id="toolchain" class="section">

## Toolchain[¶](#toolchain "Permalink to this headline")

Because our development machines are mostly x86-based we need a cross compiler that can produce executable code for ARM platform.

We can build our own cross compiler from scratch using <https://crosstool-ng.github.io/> or we can install one

<div class="highlight-bash">

<div class="highlight">

    $ sudo apt-get install gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf # for arm32
    $ sudo apt-get install gcc-aarch64-linux-gnu g++-aarch64-linux-gnu     # for arm64

</div>

</div>

There are several of toolchain binaries depending on the configuration:

> 
> 
> <div>
> 
>   - With "arm-eabi-gcc" you have the Linux system C library which will make calls into the kernel IOCTLs, e.g. for allocating memory pages to the process.
>   - With "arm-eabi-none-gcc" you are running on platform which doesn't have an operating system at all - so the C library is different to cope with that.
> 
> </div>

<div id="compiling-the-linux-kernel-on-arm" class="section">

### Compiling the Linux kernel on ARM[¶](#compiling-the-linux-kernel-on-arm "Permalink to this headline")

Compile the kernel for 32bit ARM boards:

<div class="highlight-bash">

<div class="highlight">

    # select defconfig based on your platform
    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make imx_v6_v7_defconfig
    # compile the kernel
    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make -j8

</div>

</div>

Compile the kernel for 64bit ARM boards:

<div class="highlight-bash">

<div class="highlight">

    # for 64bit ARM there is a single config for all supported boards
    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make defconfig
    # compile the kernel
    $ ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- make -j8

</div>

</div>

</div>

</div>

<div id="linux-kernel-image" class="section">

## Linux kernel image[¶](#linux-kernel-image "Permalink to this headline")

The kernel image binary is named `vmlinux` and it can be found in the root of the kernel tree. Compressed image used for booting can be found under:

  - `arch/arm/boot/Image`, for arm32
  - `arch/arm64/boot/Image`, for arm64

<div class="highlight-bash">

<div class="highlight">

    $ file vmlinux
      vmlinux: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, not stripped
    
    $ file vmlinux
      vmlinux: ELF 64-bit LSB shared object, ARM aarch64, version 1 (SYSV), statically linked, not stripped

</div>

</div>

</div>

<div id="rootfs" class="section">

## Rootfs[¶](#rootfs "Permalink to this headline")

The root filesystem (`rootfs`) is the filesystem mounted at the top of files hierarchy (`/`). It should contain at least the critical files allowing the system to boot to a shell.

<div class="highlight-bash">

<div class="highlight">

    root@so2$ tree -d -L 2
    ├── bin
    ├── boot
    ├── dev
    ├── etc
    ├── home
    │   └── root
    ├── lib
    │   └── udev
    ├── mnt
    ├── proc
    ├── sbin
    │   └── init
    ├── sys
    ├── usr
    │   ├── bin
    │   ├── include
    │   ├── lib
    └── var

</div>

</div>

As for `x86` we will make use of Yocto rootfs images. In order to download an `ext4` rootfs image for `arm32` one needs to run:

<div class="highlight-bash">

<div class="highlight">

    $ cd tools/labs/
    $ ARCH=arm make core-image-minimal-qemuarm.ext4

</div>

</div>

</div>

<div id="device-tree" class="section">

## Device tree[¶](#device-tree "Permalink to this headline")

Device tree (**DT**) is a tree structure used to describe the hardware devices in a system. Each node in the tree describes a device hence it is called **device node**. DT was introduced to provide a way to discover non-discoverable hardware (e.g a device on an I2C bus). This information was previously stored inside the source code for the Linux kernel. This meant that each time we needed to modify a node for a device the kernel needed to be recompiled. This no longer holds true as device tree and kernel image are separate binaries now.

Device trees are stored inside device tree sources (*.dts*) and compiled into device tree blobs (*.dtb*).

<div class="highlight-bash">

<div class="highlight">

    # compile dtbs
    $ make dtbs
    
    # location for DT sources on arm32
    $ ls arch/arm/boot/dts/
      imx6ul-14x14-evk.dtb imx6ull-14x14-evk.dtb bcm2835-rpi-a-plus.dts
    
    # location for DT source on arm64
    $ ls arch/arm64/boot/dts/<vendor>
      imx8mm-evk.dts imx8mp-evk.dts

</div>

</div>

The following image is a represantation of a simple device tree, describing board type, cpu and memory.

![../\_images/dts\_node1.png](../_images/dts_node1.png)

Notice that a device tree node can be defined using `label: name@address`:

> 
> 
> <div>
> 
>   - `label`, is an identifier used to reference the node from other places
>   - `name`, node identifier
>   - `address`, used to differentiate nodes with the same name.
> 
> </div>

A node might contain several properties arranged in the `name = value` format. The name is a string and the value can be bytes, strings, array of strings.

Here is an example:

<div class="code c highlight-none">

<div class="highlight">

    / {
         node@0 {
              empty-property;
              string-property = "string value";
              string-list-property = "string value 1", "string value 2";
              int-list-property = <value1 value2>;
    
              child-node@0 {
                      child-empty-property;
                      child-string-property = "string value";
                      child-node-reference = <&child-node1>;
              };
    
              child-node1: child-node@1 {
                      child-empty-property;
                      child-string-property = "string value";
              };
       };
    };

</div>

</div>

</div>

<div id="qemu" class="section">

## Qemu[¶](#qemu "Permalink to this headline")

We will use `qemu-system-arm` to boot 32bit ARM platforms. Although, this can be installed from official distro repos, for example:

<div class="code bash highlight-none">

<div class="highlight">

    sudo apt-get install -y qemu-system-arm

</div>

</div>

We strongly recommend using latest version of `qemu-system-arm` build from sources:

<div class="code bash highlight-none">

<div class="highlight">

    $ git clone https://gitlab.com/qemu-project/qemu.git
    $ ./configure --target-list=arm-softmmu --disable-docs
    $ make -j8
    $ ./build/qemu-system-arm

</div>

</div>

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

The current lab name is arm\_kernel\_development. See the exercises for the task name.

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

The modules are placed in /home/root/skels/arm\_kernel\_development/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

<div class="admonition warning">

Warning

The rules for working with the virtual machine for `ARM` are modified as follows

<div class="last highlight-shell">

<div class="highlight">

    # modules build
    tools/labs $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make build
    # modules copy
    tools/labs $ ARCH=arm make copy
    # kernel build
    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make -j8

</div>

</div>

</div>

<div id="intro" class="section">

### 0\. Intro[¶](#intro "Permalink to this headline")

Inspect the following locations in the Linux kernel code and identify platforms and vendors using ARM architecture:

> 
> 
> <div>
> 
>   - 32-bit: `arch/arm/boot/dts`
>   - 64-bit: `arch/arm64/boot/dts`
> 
> </div>

Use `qemu` and look at the supported platforms:

<div class="highlight-bash">

<div class="highlight">

    ../qemu/build/arm-softmmu/qemu-system-arm -M ?

</div>

</div>

<div class="admonition note">

Note

We used our own compiled version of `Qemu` for `arm32`. See [Qemu](#qemu) section for more details.

</div>

</div>

<div id="boot" class="section">

### 1\. Boot[¶](#boot "Permalink to this headline")

Use `qemu` to boot `i.MX6UL` platform. In order to boot, we first need to compile the kernel. Review [Compiling the Linux kernel on ARM](#compiling-the-linux-kernel-on-arm) section.

Successful compilation will result in the following binaries:

> 
> 
> <div>
> 
>   - `arch/arm/boot/Image`, kernel image compiled for ARM
>   - `arch/arm/boot/dts/imx6ul-14x14-evk.dtb`, device tree blob for `i.MX6UL` board
> 
> </div>

Review [Rootfs](#rootfs) section and download `core-image-minimal-qemuarm.ext4` rootfs. Run `qemu` using then following command:

<div class="highlight-bash">

<div class="highlight">

    ../qemu/build/arm-softmmu/qemu-system-arm -M mcimx6ul-evk -cpu cortex-a7 -m 512M \
      -kernel arch/arm/boot/zImage -nographic  -dtb arch/arm/boot/dts/imx6ul-14x14-evk.dtb \
      -append "root=/dev/mmcblk0 rw console=ttymxc0 loglevel=8 earlycon printk" -sd tools/labs/core-image-minimal-qemuarm.ext4

</div>

</div>

<div class="admonition note">

Note

LCDIF and ASRC devices are not well supported with `Qemu`. Remove them from compilation.

</div>

<div class="highlight-bash">

<div class="highlight">

    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make menuconfig
    # set FSL_ASRC=n and DRM_MXSFB=n
    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make -j8

</div>

</div>

Once the kernel is booted check kernel version and cpu info:

<div class="highlight-bash">

<div class="highlight">

    $ cat /proc/cpuinfo
    $ cat /proc/version

</div>

</div>

</div>

<div id="cpu-information" class="section">

### 2\. CPU information[¶](#cpu-information "Permalink to this headline")

Inspect the CPU configuration for `NXP i.MX6UL` board. Start with `arch/arm/boot/dts/imx6ul-14x14-evk.dts`.

> 
> 
> <div>
> 
>   - find `cpu@0` device tree node and look for `operating-points` property.
>   - read the maximum and minimum operating frequency the processor can run
> 
> > 
> > 
> > <div>
> > 
> > <div class="code bash highlight-none">
> > 
> > <div class="highlight">
> > 
> >     $ cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_min_freq
> >     $ cat /sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq
> > 
> > </div>
> > 
> > </div>
> > 
> > </div>
> 
> </div>

</div>

<div id="i-o-memory" class="section">

### 3\. I/O memory[¶](#i-o-memory "Permalink to this headline")

Inspect I/O space configuration for `NXP i.MX6UL` board. Start with `arch/arm/boot/dts/imx6ul-14x14-evk.dts` and identify each device mentioned below.

<div class="code bash highlight-none">

<div class="highlight">

    $ cat /proc/iomem
      00900000-0091ffff : 900000.sram sram@900000
      0209c000-0209ffff : 209c000.gpio gpio@209c000
      021a0000-021a3fff : 21a0000.i2c i2c@21a0000
      80000000-9fffffff : System RAM

</div>

</div>

Identify device tree nodes corresponding to:

> 
> 
> <div>
> 
>   - `System RAM`, look for `memory@80000000` node in `arch/arm/boot/dts/imx6ul-14x14-evk.dtsi`. What's the size of the System RAM?
>   - `GPIO1`, look for `gpio@209c000` node in `arch/arm/boot/dts/imx6ul.dtsi`. What's the size of the I/O space for this device?
>   - `I2C1`, look for `i2c@21a0000` node in `arch/arm/boot/dts/imx6ul.dtsi`. What's the size of the I/O spaces for this device?
> 
> </div>

</div>

<div id="hello-world" class="section">

### 4\. Hello World[¶](#hello-world "Permalink to this headline")

Implement a simple kernel module that prints a message at load/unload time. Compile it and load it on `i.MX6UL` emulated platform.

<div class="highlight-shell">

<div class="highlight">

    # modules build
    tools/labs $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make build
    # modules copy
    tools/labs $ ARCH=arm make copy
    # kernel build
    $ ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- make -j8

</div>

</div>

</div>

<div id="simple-device" class="section">

### 5\. Simple device[¶](#simple-device "Permalink to this headline")

Implement a driver for a simple platform device. Find `TODO 1` and notice how `simple_driver` is declared and register as a platform driver. Follow `TODO 2` and add the `so2,simple-device-v1` and `so2,simple-device-v2` compatible strings in the simple\_device\_ids array.

Create two device tree nodes in `arch/arm/boot/dts/imx6ul.dtsi` under `soc` node with compatible strings `so2,simple-device-v1` and `so2,simple-device-v2` respectively. Then notice the behavior when loading `simple_driver` module.

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](lab10-networking.html "SO2 Lab 10 - Networking") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](lab12-kernel-profiling.html "SO2 Lab 12 - Kernel Profiling")

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
