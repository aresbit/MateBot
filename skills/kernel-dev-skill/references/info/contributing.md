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

  - [Recommended Setup](vm.html)
  - [Virtual Machine Setup](vm.html#virtual-machine-setup)
  - [Customizing the Virtual Machine Setup](extra-vm.html)
  - [Contributing to linux-kernel-labs](#)
      - [Repository structure](#repository-structure)
      - [Building the documentation](#building-the-documentation)
      - [Creating a contribution](#creating-a-contribution)
          - [Forking the repository](#forking-the-repository)
          - [Creating a pull request](#creating-a-pull-request)
          - [Making changes to a Pull Request](#making-changes-to-a-pull-request)

</div>

</div>

<div class="section wy-nav-content-wrap" data-toggle="wy-nav-shift">

** [The Linux Kernel](../index.html)

<div class="wy-nav-content">

<div class="rst-content">

<div role="navigation" aria-label="Page navigation">

  - [](../index.html)
  - Contributing to linux-kernel-labs
  - [View page source](../_sources/info/contributing.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="contributing-to-linux-kernel-labs" class="section">

# Contributing to linux-kernel-labs[¶](#contributing-to-linux-kernel-labs "Permalink to this headline")

`linux-kernel-labs` is an open platform. You can help it get better by contributing to the documentation, exercises or the infrastructure. All contributions are welcome, no matter if they are just fixes for typos or new sections in the documentation.

All information required for making a contribution can be found in the [linux-kernel-labs Linux repo](https://github.com/linux-kernel-labs/linux). In order to change anything, you need to create a Pull Request (`PR`) from your own fork to this repository. The PR will be reviewed by the members of the team and will be merged once any potential issue is fixed.

<div id="repository-structure" class="section">

## Repository structure[¶](#repository-structure "Permalink to this headline")

The [linux-kernel-labs repo](https://github.com/linux-kernel-labs/linux) is a fork of the Linux kernel repo, with the following additions:

> 
> 
> <div>
> 
>   - `/tools/labs`: contains the labs and the [<span class="std std-ref">virtual machine (VM) infrastructure</span>](vm.html#vm-link)
>       - `tools/labs/templates`: contains the skeletons sources
>       - `tools/labs/qemu`: contains the qemu VM configuration
>   - `/Documentation/teaching`: contains the sources used to generate this documentation
> 
> </div>

</div>

<div id="building-the-documentation" class="section">

## Building the documentation[¶](#building-the-documentation "Permalink to this headline")

To build the documentation, navigate to `tools/labs` and run the following command:

<div class="highlight-bash">

<div class="highlight">

    make docs

</div>

</div>

<div class="admonition note">

Note

The command should install all the required packages. In some cases, installing the packages or building the documentation might fail, because of broken dependencies versions.

Instead of struggling to fix the dependencies, the simplest way to build the documentation is using a [Docker](https://www.docker.com/). First, install `docker` and `docker-compose` on your host, and then run:

<div class="highlight-bash">

<div class="highlight">

    make docker-docs

</div>

</div>

The first run might take some time, but subsequent builds will be faster.

</div>

</div>

<div id="creating-a-contribution" class="section">

## Creating a contribution[¶](#creating-a-contribution "Permalink to this headline")

<div id="forking-the-repository" class="section">

### Forking the repository[¶](#forking-the-repository "Permalink to this headline")

1.  If you haven't done it already, clone the [linux-kernel-labs repo](https://github.com/linux-kernel-labs/linux) repository locally:
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        $ mkdir -p ~/src
        $ git clone git@github.com:linux-kernel-labs/linux.git ~/src/linux
    
    </div>
    
    </div>

2.  Go to <https://github.com/linux-kernel-labs/linux>, make sure you are logged in and click `Fork` in the top right of the page.

3.  Add the forked repo as a new remote to the local repo:
    
    <div class="highlight-bash">
    
    <div class="highlight">
    
        $ git remote add my_fork git@github.com:<your_username>/linux.git
    
    </div>
    
    </div>

Now, you can push to your fork by using `my_fork` instead of `origin` (e.g. `git push my_fork master`).

</div>

<div id="creating-a-pull-request" class="section">

### Creating a pull request[¶](#creating-a-pull-request "Permalink to this headline")

<div class="admonition warning">

Warning

Pull requests must be created from their own branches, which are started from `master`.

</div>

1.  Go to the master branch and make sure you have no local changes:

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git checkout master
>     student@eg106:~/src/linux$ git status
>     On branch master
>     Your branch is up-to-date with 'origin/master'.
>     nothing to commit, working directory clean
> 
> </div>
> 
> </div>
> 
> </div>

2.  Make sure the local master branch is up-to-date with linux-kernel-labs:

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git pull origin master
> 
> </div>
> 
> </div>
> 
> <div class="admonition note">
> 
> Note
> 
> You can also push the latest master to your forked repo:
> 
> <div class="last highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git push my_fork master
> 
> </div>
> 
> </div>
> 
> </div>
> 
> </div>

3.  Create a new branch for your change:

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git checkout -b <your_branch_name>
> 
> </div>
> 
> </div>
> 
> </div>

4.  Make some changes and commit them. In this example, we are going to change `Documentation/teaching/index.rst`:

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ vim Documentation/teaching/index.rst
>     student@eg106:~/src/linux$ git add Documentation/teaching/index.rst
>     student@eg106:~/src/linux$ git commit -m "<commit message>"
> 
> </div>
> 
> </div>
> 
> <div class="admonition warning">
> 
> Warning
> 
> The commit message must include a relevant description of your change and the location of the changed component.
> 
> Examples:
> 
> > 
> > 
> > <div>
> > 
> >   - `documentation: index: Fix typo in the first section`
> >   - `labs: block_devices: Change printk log level`
> > 
> > </div>
> 
> </div>
> 
> </div>

5.  Push the local branch to your forked repository:

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git push my_fork <your_branch_name>
> 
> </div>
> 
> </div>
> 
> </div>

6.  Open the Pull Request

> 
> 
> <div>
> 
>   - Go to <https://github.com> and open your forked repository page
>   - Click `New pull request`.
>   - Make sure base repository (left side) is `linux-kernel-labs/linux` and the base is master.
>   - Make sure the head repository (right side) is your forked repo and the compare branch is your pushed branch.
>   - Click `Create pull request`.
> 
> </div>

</div>

<div id="making-changes-to-a-pull-request" class="section">

### Making changes to a Pull Request[¶](#making-changes-to-a-pull-request "Permalink to this headline")

After receiving feedback for your changes, you might need to update the Pull Request. Your goal is to do a new push on the same branch. For this, follow the next steps:

1.  Make sure your branch is still up to date with the `linux-kernel-labs` repo `master` branch.

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git fetch origin master
>     student@eg106:~/src/linux$ git rebase FETCH_HEAD
> 
> </div>
> 
> </div>
> 
> <div class="admonition note">
> 
> Note
> 
> If you are getting conflicts, it means that someone else modified the same files/lines as you and already merged the changes since you opened the Pull Request.
> 
> In this case, you will need to fix the conflicts by editing the conflicting files manually (run `git status` to see these files). After fixing the conflicts, add them using `git add` and then run `git rebase --continue`.
> 
> </div>
> 
> </div>

2.  Apply the changes to your local files
3.  Commit the changes. We want all the changes to be in the same commit, so we will amend the changes to the initial commit.

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git add Documentation/teaching/index.rst
>     student@eg106:~/src/linux$ git commit --amend
> 
> </div>
> 
> </div>
> 
> </div>

4.  Force-push the updated commit:

> 
> 
> <div>
> 
> <div class="highlight-bash">
> 
> <div class="highlight">
> 
>     student@eg106:~/src/linux$ git push my_fork <your_branch_name> -f
> 
> </div>
> 
> </div>
> 
> After this step, the Pull Request is updated. It is now up to the linux-kernel-labs team to review the pull request and integrate your contributions in the main project.
> 
> </div>

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](extra-vm.html "Customizing the Virtual Machine Setup")

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
