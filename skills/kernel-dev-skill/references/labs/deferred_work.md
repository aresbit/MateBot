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
  - [Deferred work](#)
      - [Lab objectives](#lab-objectives)
      - [Background information](#background-information)
      - [Softirqs](#softirqs)
          - [Tasklets](#tasklets)
          - [Timers](#timers)
          - [Locking](#locking)
      - [Workqueues](#workqueues)
      - [Kernel threads](#kernel-threads)
      - [Further reading](#further-reading)
      - [Exercises](#exercises)
          - [0. Intro](#intro)
          - [1.Timer](#timer)
          - [2. Periodic timer](#periodic-timer)
          - [3. Timer control using ioctl](#timer-control-using-ioctl)
          - [4. Blocking operations](#blocking-operations)
          - [5. Workqueues](#workqueues-1)
          - [6. Kernel thread](#kernel-thread)
          - [7. Buffer shared between timer and process](#buffer-shared-between-timer-and-process)
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
  - Deferred work
  - [View page source](../_sources/labs/deferred_work.rst.txt)

-----

</div>

<div class="document" role="main" itemscope="itemscope" itemtype="http://schema.org/Article">

<div itemprop="articleBody">

<div id="deferred-work" class="section">

# Deferred work[¶](#deferred-work "Permalink to this headline")

<div id="lab-objectives" class="section">

## Lab objectives[¶](#lab-objectives "Permalink to this headline")

  - Understanding deferred work (i.e. code scheduled to be executed at a later time)
  - Implementation of common tasks that uses deferred work
  - Understanding the peculiarities of synchronization for deferred work

Keywords: softirq, tasklet, struct tasklet\_struct, bottom-half handlers, jiffies, HZ, timer, struct timer\_list, spin\_lock\_bh, spin\_unlock\_bh, workqueue, struct work\_struct, kernel thread, events/x

</div>

<div id="background-information" class="section">

## Background information[¶](#background-information "Permalink to this headline")

Deferred work is a class of kernel facilities that allows one to schedule code to be executed at a later timer. This scheduled code can run either in the process context or in interruption context depending on the type of deferred work. Deferred work is used to complement the interrupt handler functionality since interrupts have important requirements and limitations:

  - The execution time of the interrupt handler must be as small as possible
  - In interrupt context we can not use blocking calls

Using deferred work we can perform the minimum required work in the interrupt handler and schedule an asynchronous action from the interrupt handler to run at a later time and execute the rest of the operations.

Deferred work that runs in interrupt context is also known as bottom-half, since its purpose is to execute the rest of the actions from an interrupt handler (top-half).

Timers are another type of deferred work that are used to schedule the execution of future actions after a certain amount of time has passed.

Kernel threads are not themselves deferred work, but can be used to complement the deferred work mechanisms. In general, kernel threads are used as "workers" to process events whose execution contains blocking calls.

There are three typical operations that are used with all types of deferred work:

1.  **Initialization**. Each type is described by a structure whose fields will have to be initialized. The handler to be scheduled is also set at this time.
2.  **Scheduling**. Schedules the execution of the handler as soon as possible (or after expiry of a timeout).
3.  **Masking** or **Canceling**. Disables the execution of the handler. This action can be either synchronous (which guarantees that the handler will not run after the completion of canceling) or asynchronous.

<div class="admonition attention">

Attention

When doing deferred work cleanup, like freeing the structures associated with the deferred work or removing the module and thus the handler code from the kernel, always use the synchronous type of canceling the deferred work.

</div>

The main types of deferred work are kernel threads and softirqs. Work queues are implemented on top of kernel threads and tasklets and timers on top of softirqs. Bottom-half handlers were the first implementation of deferred work in Linux, but in the meantime it was replaced by softirqs. That is why some functions presented contain *bh* in their name.

</div>

<div id="softirqs" class="section">

## Softirqs[¶](#softirqs "Permalink to this headline")

softirqs can not be used by device drivers, they are reserved for various kernel subsystems. Because of this there is a fixed number of softirqs defined at compile time. For the current kernel version we have the following types defined:

<div class="highlight-c">

<div class="highlight">

    enum {
        HI_SOFTIRQ = 0,
        TIMER_SOFTIRQ,
        NET_TX_SOFTIRQ,
        NET_RX_SOFTIRQ,
        BLOCK_SOFTIRQ,
        IRQ_POLL_SOFTIRQ,
        TASKLET_SOFTIRQ,
        SCHED_SOFTIRQ,
        HRTIMER_SOFTIRQ,
        RCU_SOFTIRQ,
        NR_SOFTIRQS
    };

</div>

</div>

Each type has a specific purpose:

  - *HI\_SOFTIRQ* and *TASKLET\_SOFTIRQ* - running tasklets
  - *TIMER\_SOFTIRQ* - running timers
  - *NET\_TX\_SOFIRQ* and *NET\_RX\_SOFTIRQ* - used by the networking subsystem
  - *BLOCK\_SOFTIRQ* - used by the IO subsystem
  - *BLOCK\_IOPOLL\_SOFTIRQ* - used by the IO subsystem to increase performance when the iopoll handler is invoked;
  - *SCHED\_SOFTIRQ* - load balancing
  - *HRTIMER\_SOFTIRQ* - implementation of high precision timers
  - *RCU\_SOFTIRQ* - implementation of RCU type mechanisms [\[1\]](#footnote-1)

|                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [\[1\]](#footnote-reference-1) | RCU is a mechanism by which destructive operations (e.g. deleting an element from a chained list) are done in two steps: (1) removing references to deleted data and (2) freeing the memory of the element. The second setup is done only after we are sure nobody uses the element anymore. The advantage of this mechanism is that reading the data can be done without synchronization. For more information see Documentation/RCU/rcu.txt. |

The highest priority is the *HI\_SOFTIRQ* type softirqs, followed in order by the other softirqs defined. *RCU\_SOFTIRQ* has the lowest priority.

Softirqs are running in interrupt context which means that they can not call blocking functions. If the sofitrq handler requires calls to such functions, work queues can be scheduled to execute these blocking calls.

<div id="tasklets" class="section">

### Tasklets[¶](#tasklets "Permalink to this headline")

A tasklet is a special form of deferred work that runs in interrupt context, just like softirqs. The main difference between sofirqs and tasklets is that tasklets can be allocated dynamically and thus they can be used by device drivers. A tasklet is represented by `struct tasklet` and as many other kernel structures it needs to be initialized before being used. A pre-initialized tasklet can be defined as following:

<div class="highlight-c">

<div class="highlight">

    void handler(unsigned long data);
    
    DECLARE_TASKLET(tasklet, handler, data);
    DECLARE_TASKLET_DISABLED(tasklet, handler, data);

</div>

</div>

If we want to initialize the tasklet manually we can use the following approach:

<div class="highlight-c">

<div class="highlight">

    void handler(unsigned long data);
    
    struct tasklet_struct tasklet;
    
    tasklet_init(&tasklet, handler, data);

</div>

</div>

The *data* parameter will be sent to the handler when it is executed.

Programming tasklets for running is called scheduling. Tasklets are running from softirqs. Tasklets scheduling is done with:

<div class="highlight-c">

<div class="highlight">

    void tasklet_schedule(struct tasklet_struct *tasklet);
    
    void tasklet_hi_schedule(struct tasklet_struct *tasklet);

</div>

</div>

When using *tasklet\_schedule*, a *TASKLET\_SOFTIRQ* softirq is scheduled and all tasklets scheduled are run. For *tasklet\_hi\_schedule*, a *HI\_SOFTIRQ* softirq is scheduled.

If a tasklet was scheduled multiple times and it did not run between schedules, it will run once. Once the tasklet has run, it can be re-scheduled, and will run again at a later timer. Tasklets can be re-scheduled from their handlers.

Tasklets can be masked and the following functions can be used:

<div class="highlight-c">

<div class="highlight">

    void tasklet_enable(struct tasklet_struct * tasklet);
    void tasklet_disable(struct tasklet_struct * tasklet);

</div>

</div>

Remember that since tasklets are running from softirqs, blocking calls can not be used in the handler function.

</div>

<div id="timers" class="section">

### Timers[¶](#timers "Permalink to this headline")

A particular type of deferred work, very often used, are timers. They are defined by `struct timer_list`. They run in interrupt context and are implemented on top of softirqs.

To be used, a timer must first be initialized by calling `timer_setup()`:

<div class="highlight-c">

<div class="highlight">

    #include <linux/sched.h>
    
    void timer_setup(struct timer_list * timer,
                     void (*function)(struct timer_list *),
                     unsigned int flags);

</div>

</div>

The above function initializes the internal fields of the structure and associates *function* as the timer handler. Since timers are planned over softirqs, blocking calls can not be used in the code associated with the treatment function.

Scheduling a timer is done with `mod_timer()`:

<div class="highlight-c">

<div class="highlight">

    int mod_timer(struct timer_list *timer, unsigned long expires);

</div>

</div>

Where *expires* is the time (in the future) to run the handler function. The function can be used to schedule or reschedule a timer.

The time unit is *jiffie*. The absolute value of a jiffie is dependent on the platform and it can be found using the `HZ` macro that defines the number of jiffies for 1 second. To convert between jiffies (*jiffies\_value*) and seconds (*seconds\_value*), the following formulas are used:

<div class="highlight-c">

<div class="highlight">

    jiffies_value = seconds_value * HZ ;
    seconds_value = jiffies_value / HZ ;

</div>

</div>

The kernel maintains a counter that contains the number of jiffies since the last boot, which can be accessed via the `jiffies` global variable or macro. We can use it to calculate a time in the future for timers:

<div class="highlight-c">

<div class="highlight">

    #include <linux/jiffies.h>
    
    unsigned long current_jiffies, next_jiffies;
    unsigned long seconds = 1;
    
    current_jiffies = jiffies;
    next_jiffies = jiffies + seconds * HZ;

</div>

</div>

To stop a timer, use `del_timer()` and `del_timer_sync()`:

<div class="highlight-c">

<div class="highlight">

    int del_timer(struct timer_list *timer);
    int del_timer_sync(struct timer_list *timer);

</div>

</div>

These functions can be called for both a scheduled timer and an unplanned timer. `del_timer_sync()` is used to eliminate the races that can occur on multiprocessor systems, since at the end of the call it is guaranteed that the timer processing function does not run on any processor.

A frequent mistake in using timers is that we forget to turn off timers. For example, before removing a module, we must stop the timers because if a timer expires after the module is removed, the handler function will no longer be loaded into the kernel and a kernel oops will be generated.

The usual sequence used to initialize and schedule a one-second timeout is:

<div class="highlight-c">

<div class="highlight">

    #include <linux/sched.h>
    
    void timer_function(struct timer_list *);
    
    struct timer_list timer ;
    unsigned long seconds = 1;
    
    timer_setup(&timer, timer_function, 0);
    mod_timer(&timer, jiffies + seconds * HZ);

</div>

</div>

And to stop it:

<div class="highlight-c">

<div class="highlight">

    del_timer_sync(&timer);

</div>

</div>

</div>

<div id="locking" class="section">

### Locking[¶](#locking "Permalink to this headline")

For synchronization between code running in process context (A) and code running in softirq context (B) we need to use special locking primitives. We must use spinlock operations augmented with deactivation of bottom-half handlers on the current processor in (A), and in (B) only basic spinlock operations. Using spinlocks makes sure that we don't have races between multiple CPUs while deactivating the softirqs makes sure that we don't deadlock in the softirq is scheduled on the same CPU where we already acquired a spinlock.

We can use the `local_bh_disable()` and `local_bh_enable()` to disable and enable softirqs handlers (and since they run on top of softirqs also timers and tasklets):

<div class="highlight-c">

<div class="highlight">

    void local_bh_disable(void);
    void local_bh_enable(void);

</div>

</div>

Nested calls are allowed, the actual reactivation of the softirqs is done only when all local\_bh\_disable() calls have been complemented by local\_bh\_enable() calls:

<div class="highlight-c">

<div class="highlight">

    /* We assume that softirqs are enabled */
    local_bh_disable();  /* Softirqs are now disabled */
    local_bh_disable();  /* Softirqs remain disabled */
    
    local_bh_enable();  /* Softirqs remain disabled */
    local_bh_enable();  /* Softirqs are now enabled */

</div>

</div>

<div class="admonition attention">

Attention

These above calls will disable the softirqs only on the local processor and they are usually not safe to use, they must be complemented with spinlocks.

</div>

Most of the time device drivers will use special versions of spinlocks calls for synchronization like `spin_lock_bh()` and `spin_unlock_bh()`:

<div class="highlight-c">

<div class="highlight">

    void spin_lock_bh(spinlock_t *lock);
    void spin_unlock_bh(spinlock_t *lock);

</div>

</div>

</div>

</div>

<div id="workqueues" class="section">

## Workqueues[¶](#workqueues "Permalink to this headline")

Workqueues are used to schedule actions to run in process context. The base unit with which they work is called work. There are two types of work:

  - `struct work_struct` - it schedules a task to run at a later time
  - `struct delayed_work` - it schedules a task to run after at least a given time interval

A delayed work uses a timer to run after the specified time interval. The calls with this type of work are similar to those for `struct work_struct`, but has **\_delayed** in the functions names.

Before using them a work item must be initialized. There are two types of macros that can be used, one that declares and initializes the work item at the same time and one that only initializes the work item (and the declaration must be done separately):

<div class="highlight-c">

<div class="highlight">

    #include <linux/workqueue.h>
    
    DECLARE_WORK(name , void (*function)(struct work_struct *));
    DECLARE_DELAYED_WORK(name, void(*function)(struct work_struct *));
    
    INIT_WORK(struct work_struct *work, void(*function)(struct work_struct *));
    INIT_DELAYED_WORK(struct delayed_work *work, void(*function)(struct work_struct *));

</div>

</div>

`DECLARE_WORK()` and `DECLARE_DELAYED_WORK()` declare and initialize a work item, and `INIT_WORK()` and `INIT_DELAYED_WORK()` initialize an already declared work item.

The following sequence declares and initiates a work item:

<div class="highlight-c">

<div class="highlight">

    #include <linux/workqueue.h>
    
    void my_work_handler(struct work_struct *work);
    
    DECLARE_WORK(my_work, my_work_handler);

</div>

</div>

Or, if we want to initialize the work item separately:

<div class="highlight-c">

<div class="highlight">

    void my_work_handler(struct work_struct * work);
    
    struct work_struct my_work;
    
    INIT_WORK(&my_work, my_work_handler);

</div>

</div>

Once declared and initialized, we can schedule the task using `schedule_work()` and `schedule_delayed_work()`:

<div class="highlight-c">

<div class="highlight">

    schedule_work(struct work_struct *work);
    
    schedule_delayed_work(struct delayed_work *work, unsigned long delay);

</div>

</div>

`schedule_delayed_work()` can be used to plan a work item for execution with a given delay. The delay time unit is jiffies.

Work items can not be masked but they can be canceled by calling `cancel_delayed_work_sync()` or `cancel_work_sync()`:

<div class="highlight-c">

<div class="highlight">

    int cancel_work_sync(struct delayed_work *work);
    int cancel_delayed_work_sync(struct delayed_work *work);

</div>

</div>

The call only stops the subsequent execution of the work item. If the work item is already running at the time of the call, it will continue to run. In any case, when these calls return, it is guaranteed that the task will no longer run.

<div class="admonition attention">

Attention

While there are versions of these functions that are not synchronous (.e.g. `cancel_work()`) do not use them when you are performing cleanup work otherwise race condition could occur.

</div>

We can wait for a workqueue to complete running all of its work items by calling `flush_scheduled_work()`:

<div class="highlight-c">

<div class="highlight">

    void flush_scheduled_work(void);

</div>

</div>

This function is blocking and, therefore, can not be used in interrupt context. The function will wait for all work items to be completed. For delayed work items, `cancel_delayed_work` must be called before `flush_scheduled_work()`.

Finally, the following functions can be used to schedule work items on a particular processor (`schedule_delayed_work_on()`), or on all processors (`schedule_on_each_cpu()`):

<div class="highlight-c">

<div class="highlight">

    int schedule_delayed_work_on(int cpu, struct delayed_work *work, unsigned long delay);
    int schedule_on_each_cpu(void(*function)(struct work_struct *));

</div>

</div>

A usual sequence to initialize and schedule a work item is the following:

<div class="highlight-c">

<div class="highlight">

    void my_work_handler(struct work_struct *work);
    
    struct work_struct my_work;
    
    INIT_WORK(&my_work, my_work_handler);
    
    schedule_work(&my_work);

</div>

</div>

And for waiting for termination of a work item:

<div class="highlight-c">

<div class="highlight">

    flush_scheduled_work();

</div>

</div>

As you can see, the *my\_work\_handler* function receives the task as the parameter. To be able to access the module's private data, you can use `container_of()`:

<div class="highlight-c">

<div class="highlight">

    struct my_device_data {
        struct work_struct my_work;
        // ...
    };
    
    void my_work_handler(struct work_struct *work)
    {
       struct my_device_data * my_data;
    
       my_data = container_of(work, struct my_device_data,  my_work);
       // ...
    }

</div>

</div>

Scheduling work items with the functions above will run the handler in the context of a kernel thread called *events/x*, where x is the processor number. The kernel will initialize a kernel thread (or a pool of workers) for each processor present in the system:

<div class="highlight-shell">

<div class="highlight">

    $ ps -e
    PID TTY TIME CMD
    1?  00:00:00 init
    2 ?  00:00:00 ksoftirqd / 0
    3 ?  00:00:00 events / 0 <--- kernel thread that runs work items
    4 ?  00:00:00 khelper
    5 ?  00:00:00 kthread
    7?  00:00:00 kblockd / 0
    8?  00:00:00 kacpid

</div>

</div>

The above functions use a predefined workqueue (called events), and they run in the context of the *events/x* thread, as noted above. Although this is sufficient in most cases, it is a shared resource and large delays in work items handlers can cause delays for other queue users. For this reason there are functions for creating additional queues.

A workqueue is represented by `struct workqueue_struct`. A new workqueue can be created with these functions:

<div class="highlight-c">

<div class="highlight">

    struct workqueue_struct *create_workqueue(const char *name);
    struct workqueue_struct *create_singlethread_workqueue(const char *name);

</div>

</div>

`create_workqueue()` uses one thread for each processor in the system, and `create_singlethread_workqueue()` uses a single thread.

To add a task in the new queue, use `queue_work()` or `queue_delayed_work()`:

<div class="highlight-c">

<div class="highlight">

    int queue_work(struct workqueue_struct * queue, struct work_struct *work);
    
    int queue_delayed_work(struct workqueue_struct *queue,
                           struct delayed_work * work , unsigned long delay);

</div>

</div>

`queue_delayed_work()` can be used to plan a work for execution with a given delay. The time unit for the delay is jiffies.

To wait for all work items to finish call `flush_workqueue()`:

<div class="highlight-c">

<div class="highlight">

    void flush_workqueue(struct worksqueue_struct * queue);

</div>

</div>

And to destroy the workqueue call `destroy_workqueue()`

<div class="highlight-c">

<div class="highlight">

    void destroy_workqueue(struct workqueue_struct *queue);

</div>

</div>

The next sequence declares and initializes an additional workqueue, declares and initializes a work item and adds it to the queue:

<div class="highlight-c">

<div class="highlight">

    void my_work_handler(struct work_struct *work);
    
    struct work_struct my_work;
    struct workqueue_struct * my_workqueue;
    
    my_workqueue = create_singlethread_workqueue("my_workqueue");
    INIT_WORK(&my_work, my_work_handler);
    
    queue_work(my_workqueue, &my_work);

</div>

</div>

And the next code sample shows how to remove the workqueue:

<div class="highlight-c">

<div class="highlight">

    flush_workqueue(my_workqueue);
    destroy_workqueue(my_workqueue);

</div>

</div>

The work items planned with these functions will run in the context of a new kernel thread called *my\_workqueue*, the name passed to `create_singlethread_workqueue()`.

</div>

<div id="kernel-threads" class="section">

## Kernel threads[¶](#kernel-threads "Permalink to this headline")

Kernel threads have emerged from the need to run kernel code in process context. Kernel threads are the basis of the workqueue mechanism. Essentially, a kernel thread is a thread that only runs in kernel mode and has no user address space or other user attributes.

To create a kernel thread, use `kthread_create()`:

<div class="highlight-c">

<div class="highlight">

    #include <linux/kthread.h>
    
    struct task_struct *kthread_create(int (*threadfn)(void *data),
                                          void *data, const char namefmt[], ...);

</div>

</div>

  - *threadfn* is a function that will be run by the kernel thread
  - *data* is a parameter to be sent to the function
  - *namefmt* represents the kernel thread name, as it is displayed in ps/top ; Can contain sequences %d , %s etc. Which will be replaced according to the standard printf syntax.

For example, the following call:

<div class="highlight-c">

<div class="highlight">

    kthread_create (f, NULL, "%skthread%d", "my", 0);

</div>

</div>

Will create a kernel thread with the name mykthread0.

The kernel thread created with this function will be stopped (in the *TASK\_INTERRUPTIBLE* state). To start the kernel thread, call the `wake_up_process()`:

<div class="highlight-c">

<div class="highlight">

    #include <linux/sched.h>
    
    int wake_up_process(struct task_struct *p);

</div>

</div>

Alternatively, you can use `kthread_run()` to create and run a kernel thread:

<div class="highlight-c">

<div class="highlight">

    struct task_struct * kthread_run(int (*threadfn)(void *data)
                                     void *data, const char namefmt[], ...);

</div>

</div>

Even if the programming restrictions for the function running within the kernel thread are more relaxed and scheduling is closer to scheduling in userspace, there are, however, some limitations to be taken into account. We will list below the actions that can or can not be made from a kernel thread:

  - can't access the user address space (even with copy\_from\_user, copy\_to\_user) because a kernel thread does not have a user address space
  - can't implement busy wait code that runs for a long time; if the kernel is compiled without the preemptive option, that code will run without being preempted by other kernel threads or user processes thus hogging the system
  - can call blocking operations
  - can use spinlocks, but if the hold time of the lock is significant, it is recommended to use mutexes

The termination of a kernel thread is done voluntarily, within the function running in the kernel thread, by calling `do_exit()`:

<div class="highlight-c">

<div class="highlight">

    fastcall NORET_TYPE void do_exit(long code);

</div>

</div>

Most of the implementations of kernel threads handlers use the same model and it is recommended to start using the same model to avoid common mistakes:

<div class="highlight-c">

<div class="highlight">

    #include <linux/kthread.h>
    
    DECLARE_WAIT_QUEUE_HEAD(wq);
    
    // list events to be processed by kernel thread
    struct list_head events_list;
    struct spin_lock events_lock;
    
    
    // structure describing the event to be processed
    struct event {
        struct list_head lh;
        bool stop;
        //...
    };
    
    struct event* get_next_event(void)
    {
        struct event *e;
    
        spin_lock(&events_lock);
        e = list_first_entry(&events_list, struct event*, lh);
        if (e)
            list_del(&e->lh);
        spin_unlock(&events_lock);
    
        return e
    }
    
    int my_thread_f(void *data)
    {
        struct event *e;
    
        while (true) {
            wait_event(wq, (e = get_next_event));
    
            /* Event processing */
    
            if (e->stop)
                break;
        }
    
        do_exit(0);
    }
    
    /* start and start kthread */
    kthread_run(my_thread_f, NULL, "%skthread%d", "my", 0);

</div>

</div>

With the template above, the kernel thread requests can be issued with:

<div class="highlight-c">

<div class="highlight">

    void send_event(struct event *ev)
    {
        spin_lock(&events_lock);
        list_add(&ev->lh, &events_list);
        spin_unlock(&events_lock);
        wake_up(&wq);
    }

</div>

</div>

</div>

<div id="further-reading" class="section">

## Further reading[¶](#further-reading "Permalink to this headline")

  - [Linux Device Drivers, 3rd ed., Ch. 7: Time, Delays, and Deferred Work](http://lwn.net/images/pdf/LDD3/ch07.pdf)
  - [Scheduling Tasks](http://tldp.org/LDP/lkmpg/2.6/html/x1211.html)
  - [Driver porting: the workqueue interface](http://lwn.net/Articles/23634/)
  - [Workqueues get a rework](http://lwn.net/Articles/211279/)
  - [Kernel threads made easy](http://lwn.net/Articles/65178/)
  - [Unreliable Guide to Locking](http://www.kernel.org/pub/linux/kernel/people/rusty/kernel-locking/index.html)

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

The current lab name is deferred\_work. See the exercises for the task name.

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

The modules are placed in /home/root/skels/deferred\_work/\<task\_name\>.

You DO NOT need to STOP the VM when rebuilding modules\! The local skels directory is shared with the VM.

Review the [Exercises](#exercises) section for more detailed information.

</div>

<div class="admonition warning">

Warning

Before starting the exercises or generating the skeletons, please run **git pull** inside the Linux repo, to make sure you have the latest version of the exercises.

If you have local changes, the pull command will fail. Check for local changes using `git status`. If you want to keep them, run `git stash` before `pull` and `git stash pop` after. To discard the changes, run `git reset --hard master`.

If you already generated the skeleton before `git pull` you will need to generate it again.

</div>

<div id="intro" class="section">

### 0\. Intro[¶](#intro "Permalink to this headline")

Using [LXR](http://elixir.free-electrons.com/linux/latest/source), find the definitions of the following symbols:

  - `jiffies`
  - `struct timer_list`
  - `spin_lock_bh function()`

</div>

<div id="timer" class="section">

### 1.Timer[¶](#timer "Permalink to this headline")

We're looking at creating a simple kernel module that displays a message at *TIMER\_TIMEOUT* seconds after the module's kernel load.

Generate the skeleton for the task named **1-2-timer** and follow the sections marked with **TODO 1** to complete the task.

<div class="admonition hint">

Hint

Use pr\_info(...). Messages will be displayed on the console and can also be viewed using dmesg. When scheduling the timer we need to use the absolute time of the system (in the future) in number of ticks. The current time of the system in the number of ticks is given by `jiffies`. Thus, the absolute time we need to pass to the timer is `jiffies + TIMER_TIMEOUT * HZ`.

For more information review the [Timers](#timers) section.

</div>

</div>

<div id="periodic-timer" class="section">

### 2\. Periodic timer[¶](#periodic-timer "Permalink to this headline")

Modify the previous module to display the message in once every TIMER\_TIMEOUT seconds. Follow the section marked with **TODO 2** in the skeleton.

</div>

<div id="timer-control-using-ioctl" class="section">

### 3\. Timer control using ioctl[¶](#timer-control-using-ioctl "Permalink to this headline")

We plan to display information about the current process after N seconds of receiving a ioctl call from user space. N is transmitted as ioctl parameter.

Generate the skeleton for the task named **3-4-5-deferred** and follow the sections marked with **TODO 1** in the skeleton driver.

You will need to implement the following ioctl operations.

  - MY\_IOCTL\_TIMER\_SET to schedule a timer to run after a number of seconds which is received as an argument to ioctl. The timer does not run periodically. \* This command receives directly a value, not a pointer.
  - MY\_IOCTL\_TIMER\_CANCEL to deactivate the timer.

<div class="admonition note">

Note

Review [<span class="std std-ref">ioctl</span>](../so2/lab3-device-drivers.html#ioctl) for a way to access the ioctl argument.

</div>

<div class="admonition note">

Note

Review the [Timers](#timers) section for information on enabling / disabling a timer. In the timer handler, display the current process identifier (PID) and the process executable image name.

</div>

<div class="admonition hint">

Hint

You can find the current process identifier using the *pid* and *comm* fields of the current process. For details, review <span class="xref std std-ref">proc-info</span>.

</div>

<div class="admonition hint">

Hint

To use the device driver from userspace you must create the device character file */dev/deferred* using the mknod utility. Alternatively, you can run the *3-4-5-deferred/kernel/makenode* script that performs this operation.

</div>

Enable and disable the timer by calling user-space ioctl operations. Use the *3-4-5-deferred/user/test* program to test planning and canceling of the timer. The program receives the ioctl type operation and its parameters (if any) on the command line.

<div class="admonition hint">

Hint

Run the test executable without arguments to observe the command line options it accepts.

To enable the timer after 3 seconds use:

<div class="highlight-c">

<div class="highlight">

    ./test s 3

</div>

</div>

To disable the timer use:

<div class="last highlight-c">

<div class="highlight">

    ./test c

</div>

</div>

</div>

Note that every time the current process the timer runs from is *swapper/0* with PID 0. This process is the idle process. It is running when there is nothing else to run on. Because the virtual machine is very light and does not do much it is natural to see this process most of the time.

</div>

<div id="blocking-operations" class="section">

### 4\. Blocking operations[¶](#blocking-operations "Permalink to this headline")

Next we want to see what happens when we perform blocking operations in a timer routine. For this we try to call in the timer-handling routines a function called alloc\_io() that simulates a blocking operation.

Modify the module so that when you receive *MY\_IOCTL\_TIMER\_ALLOC* command the timer handler will call `alloc_io()`. Follow the sections marked with **TODO 2** in the skeleton.

Use the same timer. To differentiate functionality in the timer handler, use a flag in the device structure. Use the *TIMER\_TYPE\_ALLOC* and *TIMER\_TYPE\_SET* macros defined in the code skeleton. For initialization, use TIMER\_TYPE\_NONE.

Run the test program to verify the functionality of task 3. Run the test program again to call `alloc_io()`.

<div class="admonition note">

Note

The driver causes an error because a blocking function is called in the atomic context (the timer handler runs interrupt context).

</div>

</div>

<div id="workqueues-1" class="section">

### 5\. Workqueues[¶](#workqueues-1 "Permalink to this headline")

We will modify the module to prevent the error observed in the previous task.

To do so, lets call `alloc_io()` using workqueues. Schedule a work item from the timer handler In the work handler (running in process context) call the `alloc_io()`. Follow the sections marked with **TODO 3** in the skeleton and review the [Workqueues](#workqueues) section if needed.

<div class="admonition hint">

Hint

Add a new field with the type `struct work_struct` in your device structure. Initialize this field. Schedule the work from the timer handler using `schedule_work()`. Schedule the timer handler aften N seconds from the ioctl.

</div>

</div>

<div id="kernel-thread" class="section">

### 6\. Kernel thread[¶](#kernel-thread "Permalink to this headline")

Implement a simple module that creates a kernel thread that shows the current process identifier.

Generate the skeleton for the task named **6-kthread** and follow the TODOs from the skeleton.

<div class="admonition note">

Note

There are two options for creating and running a thread:

  - `kthread_run()` to create and run the thread
  - `kthread_create()` to create a suspended thread and then start it running with `wake_up_process()`.

Review the [Kernel Threads](#kernel-threads) section if needed.

</div>

<div class="admonition attention">

Attention

Synchronize the thread termination with module unloading:

  - The thread should finish when the module is unloaded
  - Wait for the kernel thread to exit before continuing with unloading

</div>

<div class="admonition hint">

Hint

For synchronization use two wait queues and two flags.

Review <span class="xref std std-ref">waiting-queues</span> on how to use waiting queue.

Use atomic variables for flags. Review [<span class="std std-ref">Atomic variables</span>](../so2/lab2-kernel-api.html#atomic-variables).

</div>

</div>

<div id="buffer-shared-between-timer-and-process" class="section">

### 7\. Buffer shared between timer and process[¶](#buffer-shared-between-timer-and-process "Permalink to this headline")

The purpose of this task is to exercise the synchronization between a deferrable action (a timer) and process context. Set up a periodic timer that monitors a list of processes. If one of the processes terminate a message is printed. Processes can be dynamically added to the list. Use the *3-4-5-deferred/kernel/* skeleton as a base and follow the **TODO 4** markings to complete the task.

When the *MY\_IOCTL\_TIMER\_MON* command is received check that the given process exists and if so add to the monitored list of processes and then arm the timer after setting its type.

<div class="admonition hint">

Hint

Use `get_proc()` which checks the pid, finds the associated `struct task_struct` and allocates a `struct mon_proc` item you can add to your list. Note that the function also increases the reference counter of the task, so that its memory won't be free when the task terminates.

</div>

<div class="admonition attention">

Attention

Use a spinlock to protect the access to the list. Note that since we share data with the timer handler we need to disable bottom-half handlers in addition to taking the lock. Review the [Locking](#locking) section.

</div>

<div class="admonition hint">

Hint

Collect the information every second from a timer. Use the existing timer and add new behaviour for it via the TIMER\_TYPE\_ACCT. To set the flag, use the *t* argument of the test program.

</div>

In the timer handler iterate over the list of monitored processes and check if they have terminated. If so, print the process name and pid then remove the process from the list, decrement the task usage counter so that it's memory can be free and finally free the `struct mon_proc` structure.

<div class="admonition hint">

Hint

Use the *state* field of `struct task_struct()`. A task has terminated if its state is *TASK\_DEAD*.

</div>

<div class="admonition hint">

Hint

Use `put_task_struct()` to decrement the task usage counter.

</div>

<div class="admonition attention">

Attention

Make sure you protect the list access with a spinlock. The simple variant will suffice.

</div>

<div class="admonition attention">

Attention

Make sure to use the safe iteration over the list since we may need to remove an item from the list.

</div>

Rearm the timer after checking the list.

</div>

</div>

</div>

</div>

</div>

<div class="rst-footer-buttons" role="navigation" aria-label="Footer">

[<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous](interrupts.html "I/O access and Interrupts") [Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span>](block_device_drivers.html "Block Device Drivers")

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
