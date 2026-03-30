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
  - [Introduction](#)
      - [Lab objectives](#lab-objectives)
      - [Keywords](#keywords)
      - [About this laboratory](#about-this-laboratory)
      - [References](#references)
      - [Source code navigation](#source-code-navigation)
          - [cscope](#cscope)
          - [clangd](#clangd)
          - [Kscope](#kscope)
          - [LXR Cross-Reference](#lxr-cross-reference)
          - [SourceWeb](#sourceweb)
      - [Kernel Debugging](#kernel-debugging)
          - [gdb (Linux)](#gdb-linux)
          - [Getting a stack trace](#getting-a-stack-trace)
      - [Documentation](#documentation)
      - [Exercises](#exercises)
          - [Remarks](#remarks)
          - [Booting the virtual machine](#booting-the-virtual-machine)
          - [Adding and using a virtual disk](#adding-and-using-a-virtual-disk)
          - [GDB and QEMU](#gdb-and-qemu)
          - [4. GDB spelunking](#gdb-spelunking)
          - [5. Cscope spelunking](#cscope-spelunking)
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
  - Introduction
  - [View page source](../_sources/labs/introduction.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="introduction" class="section">

# Introduction[¶](#introduction "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

  - presenting the rules and objectives of the Operating Systems 2 lab
  - introducing the lab documentation
  - introducing the Linux kernel and related resources

</div>

<div id="keywords" class="section">

## Keywords[¶](#keywords "Permalink to this headline")

  - kernel, kernel programming
  - Linux, vanilla, <http://www.kernel.org>
  - cscope, LXR
  - gdb, /proc/kcore, addr2line, dump\_stack

</div>

<div id="about-this-laboratory" class="section">

## About this laboratory[¶](#about-this-laboratory "Permalink to this headline")

The Operating Systems 2 lab is a kernel programming and driver development lab. The objectives of the laboratory are:

  - deepening the notions presented in the course
  - presentation of kernel programming interfaces (kernel API)
  - gaining documenting, development and debugging skills on a freestanding environment
  - acquiring knowledge and skills for drivers development

A laboratory will present a set of concepts, applications and commands specific to a given problem. The lab will start with a presentation (each lab will have a set of slides) (15 minutes) and the remaining time will be allocated to the lab exercises (80 minutes).

For best laboratory performance, we recommend that you read the related slides. To fully understand a laboratory, we recommend going through the lab support. For in-depth study, use the supporting documentation.

</div>

<div id="references" class="section">

## References[¶](#references "Permalink to this headline")

  - Linux
      - [Linux Kernel Development, 3rd Edition](http://www.amazon.com/Linux-Kernel-Development-Robert-Love/dp/0672329468/)
      - [Linux Device Drivers, 3rd Edition](http://free-electrons.com/doc/books/ldd3.pdf)
      - [Essential Linux Device Drivers](http://www.amazon.com/Essential-Device-Drivers-Sreekrishnan-Venkateswaran/dp/0132396556)
  - General
      - [mailing list](http://cursuri.cs.pub.ro/cgi-bin/mailman/listinfo/pso) ([searching the mailing list](http://blog.gmane.org/gmane.education.region.romania.operating-systems-design))

</div>

<div id="source-code-navigation" class="section">

## Source code navigation[¶](#source-code-navigation "Permalink to this headline")

<div id="cscope" class="section">

<span id="cscope-intro"></span>

### cscope[¶](#cscope "Permalink to this headline")

[Cscope](http://cscope.sourceforge.net/) is a tool for efficient navigation of C sources. To use it, a cscope database must be generated from the existing sources. In a Linux tree, the command **make ARCH=x86 cscope** is sufficient. Specification of the architecture through the ARCH variable is optional but recommended; otherwise, some architecture dependent functions will appear multiple times in the database.

You can build the cscope database with the command **make ARCH=x86 COMPILED\_SOURCE=1 cscope**. This way, the cscope database will only contain symbols that have already been used in the compile process before, thus resulting in better performance when searching for symbols.

Cscope can also be used as stand-alone, but it is more useful when combined with an editor. To use cscope with **vim**, it is necessary to install both packages and add the following lines to the file `.vimrc` (the machine in the lab already has the settings):

<div class="highlight-vim">

<div class="highlight">

    if has("cscope")
            " Look for a 'cscope.out' file starting from the current directory,
            " going up to the root directory.
            let s:dirs = split(getcwd(), "/")
            while s:dirs != []
                    let s:path = "/" . join(s:dirs, "/")
                    if (filereadable(s:path . "/cscope.out"))
                            execute "cs add " . s:path . "/cscope.out " . s:path . " -v"
                            break
                    endif
                    let s:dirs = s:dirs[:-2]
            endwhile
    
            set csto=0  " Use cscope first, then ctags
            set cst     " Only search cscope
            set csverb  " Make cs verbose
    
            nmap `<C-\>`s :cs find s `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`g :cs find g `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`c :cs find c `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`t :cs find t `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`e :cs find e `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap `<C-\>`f :cs find f `<C-R>`=expand("`<cfile>`")`<CR>``<CR>`
            nmap `<C-\>`i :cs find i ^`<C-R>`=expand("`<cfile>`")`<CR>`$`<CR>`
            nmap `<C-\>`d :cs find d `<C-R>`=expand("`<cword>`")`<CR>``<CR>`
            nmap <F6> :cnext <CR>
            nmap <F5> :cprev <CR>
    
            " Open a quickfix window for the following queries.
            set cscopequickfix=s-,c-,d-,i-,t-,e-,g-
    endif

</div>

</div>

The script searches for a file called `cscope.out` in the current directory, or in parent directories. If **vim** finds this file, you can use the shortcut `Ctrl +]` or `Ctrl+\ g` (the combination control-\\ followed by g) to jump directly to the definition of the word under the cursor (function, variable, structure, etc.). Similarly, you can use `Ctrl+\ s` to go where the word under the cursor is used.

You can take a cscope-enabled `.vimrc` file (also contains other goodies) from <https://github.com/ddvlad/cfg/blob/master/_vimrc>. The following guidelines are based on this file, but also show basic **vim** commands that have the same effect.

If there are more than one results (usually there are) you can move between them using `F6` and `F5` (`:ccnext` and `:cprev`). You can also open a new panel showing the results using `:copen`. To close the panel, use the `:cclose` command.

To return to the previous location, use `Ctrl+o` (o, not zero). The command can be used multiple times and works even if cscope changed the file you are currently editing.

To go to a symbol definition directly when **vim** starts, use `vim -t <symbol_name>` (for example `vim -t task_struct`). Otherwise, if you started **vim** and want to search for a symbol by name, use `cs find g <symbol_name>` (for example `cs find g task_struct`).

If you found more than one results and opened a panel showing all the matches (using `:copen`) and you want to find a symbol of type structure, it is recommended to search in the results panel (using `/` -- slash) the character `{` (opening brace).

<div class="admonition important">

Important

You can get a summary of all the **cscope** commands using **:cs help**.

For more info, use the **vim** built-in help command: **:h cscope** or **:h copen**.

</div>

If you use **emacs**, install the `xcscope-el` package and add the following lines in `~/.emacs`.

<div class="highlight-vim">

<div class="highlight">

    (require ‘xcscope)
    (cscope-setup)

</div>

</div>

These commands will activate cscope for the C and C++ modes automatically. `C-s s` is the key bindings prefix and `C-s s s` is used to search for a symbol (if you call it when the cursor is over a word, it will use that). For more details, check https://github.com/dkogan/xcscope.el

</div>

<div id="clangd" class="section">

### clangd[¶](#clangd "Permalink to this headline")

[Clangd](https://clangd.llvm.org/) is a language server that provides tools for navigating C and C++ code. [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) facilitates features like go-to-definition, find-references, hover, completion, etc., using semantic whole project analysis.

Clangd requires a compilation database to understand the kernel source code. It can be generated with:

<div class="highlight-bash">

<div class="highlight">

    make defconfig
    make
    scripts/clang-tools/gen_compile_commands.py

</div>

</div>

LSP clients:

  - Vim/Neovim ([coc.nvim](https://github.com/neoclide/coc.nvim), [nvim-lsp](https://github.com/neovim/nvim-lspconfig), [vim-lsc](https://github.com/natebosch/vim-lsc), [vim-lsp](https://github.com/prabirshrestha/vim-lsp))
  - Emacs ([lsp-mode](https://github.com/emacs-lsp/lsp-mode))
  - VSCode ([clangd extension](https://marketplace.visualstudio.com/items?itemName=llvm-vs-code-extensions.vscode-clangd))

</div>

<div id="kscope" class="section">

### Kscope[¶](#kscope "Permalink to this headline")

For a simpler interface, [Kscope](http://sourceforge.net/projects/kscope/) is a cscope frontend which uses QT. It is lightweight, very fast and very easy to use. It allows searching using regular expressions, call graphs, etc. Kscope is no longer mantained.

There is also a [port](https///opendesktop.org/content/show.php/Kscope4?content=156987) of version 1.6 for Qt4 and KDE 4 which keeps the integration of the text editor Kate and is easier to use than the last version on SourceForge.

</div>

<div id="lxr-cross-reference" class="section">

### LXR Cross-Reference[¶](#lxr-cross-reference "Permalink to this headline")

LXR (LXR Cross-Reference) is a tool that allows indexing and referencing the symbols in the source code of a program using a web interface. The web interface shows links to locations in files where a symbol is defined or used. Development website for LXR is <http://sourceforge.net/projects/lxr>. Similar tools are [OpenGrok](http://oracle.github.io/opengrok/) and [Gonzui](http://en.wikipedia.org/wiki/Gonzui).

Although LXR was originally intended for the Linux kernel sources, it is also used in the sources of [Mozilla](http://lxr.mozilla.org/), [Apache HTTP Server](http://apache.wirebrain.de/lxr/) and [FreeBSD](http://lxr.linux.no/freebsd/source).

There are a number of sites that use LXR for cross-referencing the the sources of the Linux kernel, the main site being [the original site of development](http://lxr.linux.no/linux/) which does not work anymore. You can use <https://elixir.bootlin.com/>.

LXR allows searching for an identifier (symbol), after a free text or after a file name. The main feature and, at the same time, the main advantage provided is the ease of finding the declaration of any global identifier. This way, it facilitates quick access to function declarations, variables, macro definitions and the code can be easily navigated. Also, the fact that it can detect what code areas are affected when a variable or function is changed is a real advantage in the development and debugging phase.

</div>

<div id="sourceweb" class="section">

### SourceWeb[¶](#sourceweb "Permalink to this headline")

[SourceWeb](http://rprichard.github.io/sourceweb/) is a source code indexer for C and C++. It uses the [framework](http://clang.llvm.org/docs/IntroductionToTheClangAST.html) provided by the Clang compiler to index the code.

The main difference between cscope and SourceWeb is the fact that SourceWeb is, in a way, a compiler pass. SourceWeb doesn't index all the code, but only the code that was efectively compiled by the compiler. This way, some problems are eliminated, such as ambiguities about which variant of a function defined in multiple places is used. This also means that the indexing takes more time, because the compiled files must pass one more time through the indexer to generate the references.

Usage example:

<div class="highlight-bash">

<div class="highlight">

    make oldconfig
    sw-btrace make -j4
    sw-btrace-to-compile-db
    sw-clang-indexer --index-project
    sourceweb index

</div>

</div>

`sw-btrace` is a script that adds the `libsw-btrace.so` library to `LD_PRELOAD`. This way, the library is loaded by every process started by `make` (basically, the compiler), registers the commands used to start the processes and generates a filed called `btrace.log`. This file is then used by `sw-btrace-to-compile-db` which converts it to a format defined by clang: [JSON Compilation Database](http://clang.llvm.org/docs/JSONCompilationDatabase.html). This JSON Compilation Database resulted from the above steps is then used by the indexer, which makes one more pass through the compiled source files and generates the index used by the GUI.

Word of advice: don't index the sources you are working with, but use a copy, because SourceWeb doesn't have, at this moment, the capability to regenerate the index for a single file and you will have to regenerate the complete index.

</div>

</div>

<div id="kernel-debugging" class="section">

## Kernel Debugging[¶](#kernel-debugging "Permalink to this headline")

Debugging a kernel is a much more difficult process than the debugging of a program, because there is no support from the operating system. This is why this process is usually done using two computers, connected on serial interfaces.

<div id="gdb-linux" class="section">

<span id="gdb-intro"></span>

### gdb (Linux)[¶](#gdb-linux "Permalink to this headline")

A simpler debug method on Linux, but with many disadvantages, is local debugging, using [gdb](http://www.gnu.org/software/gdb/), the uncompressed kernel image (`vmlinux`) and `/proc/kcore` (the real-time kernel image). This method is usually used to inspect the kernel and detect certain inconsistencies while it runs. The method is useful especially if the kernel was compiled using the `-g` option, which keeps debug information. Some well-known debug techniques can't be used by this method, such as breakpoints of data modification.

<div class="admonition note">

Note

Because `/proc` is a virtual filesystem, `/proc/kcore` does not physically exist on the disk. It is generated on-the-fly by the kernel when a program tries to access `proc/kcore`.

It is used for debugging purposes.

From **man proc**, we have:

<div class="last highlight-none">

<div class="highlight">

    /proc/kcore
    This file represents the physical memory of the system and is stored in the ELF core file format.  With this pseudo-file, and
    an unstripped kernel (/usr/src/linux/vmlinux) binary, GDB can be used to examine the current state of any kernel data struc‐
    tures.

</div>

</div>

</div>

The uncompressed kernel image offers information about the data structures and symbols it contains.

<div class="highlight-bash">

<div class="highlight">

    student@eg106$ cd ~/src/linux
    student@eg106$ file vmlinux
    vmlinux: ELF 32-bit LSB executable, Intel 80386, ...
    student@eg106$ nm vmlinux | grep sys_call_table
    c02e535c R sys_call_table
    student@eg106$ cat System.map | grep sys_call_table
    c02e535c R sys_call_table

</div>

</div>

The **nm** utility is used to show the symbols in an object or executable file. In our case, `vmlinux` is an ELF file. Alternately, we can use the file `System.map` to view information about the symbols in kernel.

Then we use **gdb** to inspect the symbols using the uncompressed kernel image. A simple **gdb** session is the following:

<div class="highlight-bash">

<div class="highlight">

    student@eg106$ cd ~/src/linux
    stduent@eg106$ gdb --quiet vmlinux
    Using host libthread_db library "/lib/tls/libthread_db.so.1".
    (gdb) x/x 0xc02e535c
    0xc02e535c `<sys_call_table>`:    0xc011bc58
    (gdb) x/16 0xc02e535c
    0xc02e535c `<sys_call_table>`:    0xc011bc58      0xc011482a      0xc01013d3     0xc014363d
    0xc02e536c `<sys_call_table+16>`: 0xc014369f      0xc0142d4e      0xc0142de5     0xc011548b
    0xc02e537c `<sys_call_table+32>`: 0xc0142d7d      0xc01507a1      0xc015042c     0xc0101431
    0xc02e538c `<sys_call_table+48>`: 0xc014249e      0xc0115c6c      0xc014fee7     0xc0142725
    (gdb) x/x sys_call_table
    0xc011bc58 `<sys_restart_syscall>`:       0xffe000ba
    (gdb) x/x &sys_call_table
    0xc02e535c `<sys_call_table>`:    0xc011bc58
    (gdb) x/16 &sys_call_table
    0xc02e535c `<sys_call_table>`:    0xc011bc58      0xc011482a      0xc01013d3     0xc014363d
    0xc02e536c `<sys_call_table+16>`: 0xc014369f      0xc0142d4e      0xc0142de5     0xc011548b
    0xc02e537c `<sys_call_table+32>`: 0xc0142d7d      0xc01507a1      0xc015042c     0xc0101431
    0xc02e538c `<sys_call_table+48>`: 0xc014249e      0xc0115c6c      0xc014fee7     0xc0142725
    (gdb) x/x sys_fork
    0xc01013d3 `<sys_fork>`:  0x3824548b
    (gdb) disass sys_fork
    Dump of assembler code for function sys_fork:
    0xc01013d3 `<sys_fork+0>`:        mov    0x38(%esp),%edx
    0xc01013d7 `<sys_fork+4>`:        mov    $0x11,%eax
    0xc01013dc `<sys_fork+9>`:        push   $0x0
    0xc01013de `<sys_fork+11>`:       push   $0x0
    0xc01013e0 `<sys_fork+13>`:       push   $0x0
    0xc01013e2 `<sys_fork+15>`:       lea    0x10(%esp),%ecx
    0xc01013e6 `<sys_fork+19>`:       call   0xc0111aab `<do_fork>`
    0xc01013eb `<sys_fork+24>`:       add    $0xc,%esp
    0xc01013ee `<sys_fork+27>`:       ret
    End of assembler dump.

</div>

</div>

It can be noticed that the uncompressed kernel image was used as an argument for **gdb**. The image can be found in the root of the kernel sources after compilation.

A few commands used for debugging using **gdb** are:

  - **x** (examine) - Used to show the contents of the memory area whose address is specified as an argument to the command (this address can be the value of a physical address, a symbol or the address of a symbol). It can take as arguments (preceded by `/`): the format to display the data in (`x` for hexadecimal, `d` for decimal, etc.), how many memory units to display and the size of a memory unit.
  - **disassemble** - Used to disassemble a function.
  - **p** (print) - Used to evaluate and show the value of an expression. The format to show the data in can be specified as an argument (`/x` for hexadecimal, `/d` for decimal, etc.).

The analysis of the kernel image is a method of static analysis. If we want to perform dynamic analysis (analyzing how the kernel runs, not only its static image) we can use `/proc/kcore`; this is a dynamic image (in memory) of the kernel.

<div class="highlight-bash">

<div class="highlight">

    student@eg106$ gdb ~/src/linux/vmlinux /proc/kcore
    Core was generated by `root=/dev/hda3 ro'.
    #0  0x00000000 in ?? ()
    (gdb) p sys_call_table
    $1 = -1072579496
    (gdb) p /x sys_call_table
    $2 = 0xc011bc58
    (gdb) p /x &sys_call_table
    $3 = 0xc02e535c
    (gdb) x/16 &sys_call_table
    0xc02e535c `<sys_call_table>`:    0xc011bc58      0xc011482a      0xc01013d3     0xc014363d
    0xc02e536c `<sys_call_table+16>`: 0xc014369f      0xc0142d4e      0xc0142de5     0xc011548b
    0xc02e537c `<sys_call_table+32>`: 0xc0142d7d      0xc01507a1      0xc015042c     0xc0101431
    0xc02e538c `<sys_call_table+48>`: 0xc014249e      0xc0115c6c      0xc014fee7     0xc0142725

</div>

</div>

Using the dynamic image of the kernel is useful for detecting [rootkits](http://en.wikipedia.org/wiki/Rootkit).

  - [Linux Device Drivers 3rd Edition - Debuggers and Related Tools](http://linuxdriver.co.il/ldd3/linuxdrive3-CHP-4-SECT-6.html)
  - [Detecting Rootkits and Kernel-level Compromises in Linux](http://www.securityfocus.com/infocus/1811)
  - [User-Mode Linux](http://user-mode-linux.sf.net/)

</div>

<div id="getting-a-stack-trace" class="section">

### Getting a stack trace[¶](#getting-a-stack-trace "Permalink to this headline")

Sometimes, you will want information about the trace the execution reaches a certain point. You can determine this information using **cscope** or LXR, but some function are called from many execution paths, which makes this method difficult.

In these situations, it is useful to get a stack trace, which can be simply done using the function `dump_stack()`.

</div>

</div>

<div id="documentation" class="section">

## Documentation[¶](#documentation "Permalink to this headline")

Kernel development is a difficult process, compared to user space programming. The API is different and the complexity of the subsystems in kernel requires additional preparation. The associated documentation is heterogeneous, sometimes requiring the inspection of multiple sources to have a more complete understanding of a certain aspect.

The main advantages of the Linux kernel are the access to sources and the open development system. Because of this, the Internet offers a larger number of documentation for the kernel.

A few links related to the Linux kernel are shown bellow:

  - [KernelNewbies](http://kernelnewbies.org)
  - [KernelNewbies - Kernel Hacking](http://kernelnewbies.org/KernelHacking)
  - [Kernel Analysis - HOWTO](http://www.tldp.org/HOWTO/KernelAnalysis-HOWTO.html)
  - [Linux Kernel Programming](http://web.archive.org/web/20090228191439/http://www.linuxhq.com/lkprogram.html)
  - [Linux kernel - Wikibooks](http://en.wikibooks.org/wiki/Linux_kernel)

The links are not comprehensive. Using [The Internet](http://www.google.com) and [kernel source code](http://lxr.free-electrons.com/) is essential.

</div>

<div id="exercises" class="section">

## Exercises[¶](#exercises "Permalink to this headline")

<div id="remarks" class="section">

### Remarks[¶](#remarks "Permalink to this headline")

<div class="admonition note">

Note

  - Usually, the steps used to develop a kernel module are the following:
      - editing the module source code (on the physical machine);
      - module compilation (on the physical machine);
      - generation of the minimal image for the virtual machine; this image contains the kernel, your module, busybox and eventually test programs;
      - starting the virtual machine using QEMU;
      - running the tests in the virtual machine.
  - When using cscope, use `~/src/linux`. If there is no `cscope.out` file, you can generate it using the command **make ARCH=x86 cscope**.
  - You can find more details about the virtual machine at [<span class="std std-ref">Recommended Setup</span>](../info/vm.html#vm-link).

</div>

<div class="admonition important">

Important

Before solving an exercice, **carefully** read all its bullets.

</div>

</div>

<div id="booting-the-virtual-machine" class="section">

### Booting the virtual machine[¶](#booting-the-virtual-machine "Permalink to this headline")

A summary of the virtual machine infrastructure:

  - `~/src/linux` - Linux kernel sources, needed to compile modules. The directory contains the file `cscope.out`, used for navigation in the source tree.
  - `~/src/linux/tools/labs/qemu`- scripts and auxiliary files used to generate and run the QEMU VM.

To start the VM, run **make boot** in the directory `~/src/linux/tools/labs`:

<div class="highlight-shell">

<div class="highlight">

    student@eg106:~$ cd ~/src/linux/tools/labs
    student@eg106:~/src/linux/tools/labs$ make boot

</div>

</div>

By default, you will not get a prompt or any graphical interface, but you can connect to a console exposed by the virtual machine using **minicom** or **screen**.

<div class="highlight-shell">

<div class="highlight">

    student@eg106:~/src/linux/tools/labs$ minicom -D serial.pts
    
    <press enter>
    
    qemux86 login:
    Poky (Yocto Project Reference Distro) 2.3 qemux86 /dev/hvc0

</div>

</div>

Alternatively, you can start the virtual machine with graphical interface support, using the **QEMU\_DISPLAY=gtk make boot**.

<div class="admonition note">

Note

To access the virtual machine, at the login prompt, enter the username `root`; there is no need to enter a password. The virtual machine will start with the permissions of the root account.

</div>

</div>

<div id="adding-and-using-a-virtual-disk" class="section">

### Adding and using a virtual disk[¶](#adding-and-using-a-virtual-disk "Permalink to this headline")

<div class="admonition note">

Note

If you don't have the file `mydisk.img`, you can download it from the address <http://elf.cs.pub.ro/so2/res/laboratoare/mydisk.img>. The file must be placed in `tools/labs`.

</div>

In the `~/src/linux/tools/labs` directory, you have a new virtual machine disk, in the file `mydisk.img`. We want to add the disk to the virtual machine and use it within the virtual machine.

Edit `qemu/Makefile` and add `-drive file=mydisk.img,if=virtio,format=raw` to the `QEMU_OPTS` variable.

<div class="admonition note">

Note

There are already two disks added to qemu (disk1.img and disk2.img). You will need to add the new one after them. In this case, the new disk can be accessed as `/dev/vdd` (vda is the root partition, vdb is disk1 and vdc is disk2).

</div>

<div class="admonition hint">

Hint

You do not need to manually create the entry for the new disk in `/dev` because the virtual machine uses **devtmpfs**.

</div>

Run `make` in `tools/labs` to boot the virtual machine. Create `/test` directory and try to mount the new disk:

<div class="highlight-bash">

<div class="highlight">

    mkdir /test
    mount /dev/vdd /test

</div>

</div>

The reason why we can not mount the virtual disk is because we do not have support in the kernel for the filesystem with which the `mydisk.img` is formatted. You will need to identify the filesystem for `mydisk.img` and compile kernel support for that filesystem.

Close the virtual machine (close the QEMU window, you do not need to use another command). Use the **file** command on the physical machine to find out with which filesystem the `mydisk.img` file is formatted. You will identify the **btrfs** file system.

You will need to enable **btrfs** support in the kernel and recompile the kernel image.

<div class="admonition warning">

Warning

If you receive an error while executing the **make menuconfig** command, you probably do not have the **libncurses5-dev** package installed. Install it using the command:

<div class="last highlight-none">

<div class="highlight">

    sudo apt-get install libncurses5-dev

</div>

</div>

</div>

<div class="admonition hint">

Hint

Enter the `~/src/linux/` subdirectory. Run **make menuconfig** and go to the *File systems* section. Enable *Btrfs filesystem support*. You will need to use the builtin option (not the module), i.e. **\<\*\>** must appear next to the option (**not** **\<M\>**).

Save the configuration you have made. Use the default configuration file (`config`).

In the kernel source subdirectory (`~/src/linux/`) recompile using the command:

<div class="highlight-none">

<div class="highlight">

    make

</div>

</div>

To wait less, you can use the **-j** option run multiple jobs in parallel. Generally, it is recommended to use **number of CPUs+1**:

<div class="last highlight-none">

<div class="highlight">

    make -j5

</div>

</div>

</div>

After the kernel recompilation finishes, **restart** the QEMU virtual machine: that is, launch the **make** command in the subdirectory. You do not need to copy anything, because the `bzImage` file is a symlink to the kernel image you just recompiled.

Inside the QEMU virtual machine, repeat the **mkdir** and **mount** operations. With support for the **btrfs** filesystem, now **mount** will finish successfully.

<div class="admonition note">

Note

When doing your homework, there is no need to recompile the kernel because you will only use kernel modules. However, it is important to be familiar with configuring and recompiling a kernel.

If you still plan to recompile the kernel, make a backup of the bzImage file (follow the link in \~/src/linux for the full path). This will allow you to return to the initial setup in order to have an environment identical to the one used by vmchecker.

</div>

</div>

<div id="gdb-and-qemu" class="section">

### GDB and QEMU[¶](#gdb-and-qemu "Permalink to this headline")

We can investigate and troubleshoot the QEMU virtual machine in real time.

<div class="admonition note">

Note

You can also use the **GDB Dashboard** plugin for a user-friendly interface. **gdb** must be compiled with Python support.

In order to install it, you can just run:

<div class="last highlight-none">

<div class="highlight">

    wget -P ~ git.io/.gdbinit

</div>

</div>

</div>

To do this, we start the QEMU virtual machine first. Then, we can connect with **gdb** to **a running QEMU virtual machine** using the command

<div class="highlight-none">

<div class="highlight">

    make gdb

</div>

</div>

We used the QEMU command with the **-s** parameter, which means listening to port `1234` from **gdb**. We can do debugging using a **remote target** for **gdb**. The existing `Makefile` takes care of the details.

When you attach a debugger to a process, the process is suspended. You can add breakpoints and inspect the current status of the process.

Attach to the QEMU virtual machine (using the **make gdb** command) and place a breakpoint in the `sys_access` function using the following command in the **gdb** console:

<div class="highlight-none">

<div class="highlight">

    break sys_access

</div>

</div>

At this time, the virtual machine is suspended. To continue executing it (up to the possible call of the `sys_access` function), use the command:

<div class="highlight-none">

<div class="highlight">

    continue

</div>

</div>

in the **gdb** console.

At this time, the virtual machine is active and has a usable console. To make a `sys_access` call, issue a **ls** command. Note that the virtual machine was again suspended by **gdb** and the corresponding `sys_access` callback message appeared within the **gdb** console.

Trace code execution using **step** instruction, **continue** or **next** instruction. You probably do not understand everything that happens, so use commands such as **list** and **backtrace** to trace the execution.

<div class="admonition hint">

Hint

At the **gdb** prompt, you can press **Enter** (without anything else) to rerun the last command.

</div>

</div>

<div id="gdb-spelunking" class="section">

### 4\. GDB spelunking[¶](#gdb-spelunking "Permalink to this headline")

Use **gdb** to display the source code of the function that creates kernel threads (`kernel_thread`).

<div class="admonition note">

Note

You can use GDB for static kernel analysis using, in the kernel source directory, a command such as:

<div class="highlight-none">

<div class="highlight">

    gdb vmlinux

</div>

</div>

Go over the [gdb (Linux)](#gdb-linux) section of the lab.

</div>

Use **gdb** to find the address of the `jiffies` variable in memory and its contents. The `jiffies` variable holds the number of ticks (clock beats) since the system started.

<div class="admonition hint">

Hint

To track the value of the jiffies variable, use dynamic analysis in **gdb** by running the command:

<div class="highlight-none">

<div class="highlight">

    make gdb

</div>

</div>

as in the previous exercise.

Go over the [gdb (Linux)](#gdb-linux) section of the lab.

</div>

<div class="admonition hint">

Hint

The `jiffies` is a 64-bit variable. You can see that its address is the same as the `jiffies_64` variable.

To explore the contents of a 64-bit variable, use in the **gdb** console the command:

<div class="highlight-none">

<div class="highlight">

    x/gx & jiffies

</div>

</div>

If you wanted to display the contents of the 32-bit variable, you would use in the **gdb** console the command:

<div class="last highlight-none">

<div class="highlight">

    x/wx & jiffies

</div>

</div>

</div>

</div>

<div id="cscope-spelunking" class="section">

### 5\. Cscope spelunking[¶](#cscope-spelunking "Permalink to this headline")

Use LXR or cscope in the `~/src/linux/` directory to discover the location of certain structures or functions.

Cscope index files are already generated. Use **vim** and other related commands to scroll through the source code. For example, use the command:

<div class="highlight-none">

<div class="highlight">

    vim

</div>

</div>

for opening the **vim** editor. Afterwards, inside the editor, use commands such as:

**:cs find g task\_struct**.

Find the file in which the following data types are defined:

  - `struct task_struct`
  - `struct semaphore`
  - `struct list_head`
  - `spinlock_t`
  - `struct file_system_type`

<div class="admonition hint">

Hint

For a certain structure, only its name needs to be searched.

For instance, in the case of **struct task\_struct**, search for the **task\_struct** string.

</div>

Usually, you will get more matches. To locate the one you are interested in, do the following:

1.  List all matches by using, in **vim**, **:copen** command.
2.  Look for the right match (where the structure is defined) by looking for an open character (**{**), a single character on the structure definition line. To search for the open braid you use in **vim** the construction **/{**.
3.  On the respective line, press **Enter** to get into the source code where the variable is defined.
4.  Close the secondary window using the command: **:cclose** command.

Find the file in which the following global kernel variables are declared:

  - `sys_call_table`
  - `file_systems`
  - `current`
  - `chrdevs`

<div class="admonition hint">

Hint

To do this, use a **vim** command with the syntax:

**:cs f g \<symbol\>**

where **\<symbol\>** is the name of the symbol being searched.

</div>

Find the file in which the following functions are declared:

  - `copy_from_user`
  - `vmalloc`
  - `schedule_timeout`
  - `add_timer`

<div class="admonition hint">

Hint

To do this, use a **vim** command with the syntax:

**:cs f g \<symbol\>**

where **\<symbol\>** is the name of the symbol being searched.

</div>

Scroll through the following sequence of structures:

  - `struct task_struct`
  - `struct mm_struct`
  - `struct vm_area_struct`
  - `struct vm_operations_struct`

That is, you access a structure and then you find fields with the data type of the next structure, access the respective fields and so on. Note in which files these structures are defined; this will be useful to the following labs.

<div class="admonition hint">

Hint

In order to search for a symbol in **vim** (with **cscope** support) when the cursor is placed on it, use the **Ctrl+\]** keyboard shortcut.

To return to the previous match (the one before search/jump), use the **Ctrl+o** keyboard shortcut.

To move forward with the search (to return to matches before **Ctrl+o**), use the **Ctrl+i** keyboard shortcut.

</div>

Following the above instructions, find and go through the function call sequence:

  - `bio_alloc`
  - `bio_alloc_bioset`
  - `bvec_alloc`
  - `kmem_cache_alloc`
  - `slab_alloc`

<div class="admonition note">

Note

Read [cscope](#cscope) or [LXR Cross-Reference](#lxr-cross-reference) sections of the lab.

</div>

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](infrastructure.html "Infrastructure") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](kernel_modules.html "Kernel modules")

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
