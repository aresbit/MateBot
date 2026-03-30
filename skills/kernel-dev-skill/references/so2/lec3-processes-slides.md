<div id="slide_container" class="section slides layout-regular">

# SO2 Lecture 03 - Processes

## Processes and threads

  - Process and threads
  - Context switching
  - Blocking and waking up
  - Process context

## What is a process?

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="odd">
<td><ul>
<li>An address space</li>
<li>One or more threads</li>
<li>Opened files</li>
<li>Sockets</li>
<li>Semaphores</li>
</ul></td>
<td><ul>
<li>Shared memory regions</li>
<li>Timers</li>
<li>Signal handlers</li>
<li>Many other resources and status information</li>
</ul></td>
</tr>
</tbody>
</table>

All this information is grouped in the Process Control Group (PCB). In Linux this is `struct task_struct`.

## Overview of process resources

<div class="highlight-none">

<div class="highlight">

``` 
                +-------------------------------------------------------------------+
                | dr-x------    2 tavi tavi 0  2021 03 14 12:34 .                   |
                | dr-xr-xr-x    6 tavi tavi 0  2021 03 14 12:34 ..                  |
                | lrwx------    1 tavi tavi 64 2021 03 14 12:34 0 -> /dev/pts/4     |
           +--->| lrwx------    1 tavi tavi 64 2021 03 14 12:34 1 -> /dev/pts/4     |
           |    | lrwx------    1 tavi tavi 64 2021 03 14 12:34 2 -> /dev/pts/4     |
           |    | lr-x------    1 tavi tavi 64 2021 03 14 12:34 3 -> /proc/18312/fd |
           |    +-------------------------------------------------------------------+
           |                 +----------------------------------------------------------------+
           |                 | 08048000-0804c000 r-xp 00000000 08:02 16875609 /bin/cat        |
$ ls -1 /proc/self/          | 0804c000-0804d000 rw-p 00003000 08:02 16875609 /bin/cat        |
cmdline    |                 | 0804d000-0806e000 rw-p 0804d000 00:00 0 [heap]                 |
cwd        |                 | ...                                                            |
environ    |    +----------->| b7f46000-b7f49000 rw-p b7f46000 00:00 0                        |
exe        |    |            | b7f59000-b7f5b000 rw-p b7f59000 00:00 0                        |
fd --------+    |            | b7f5b000-b7f77000 r-xp 00000000 08:02 11601524 /lib/ld-2.7.so  |
fdinfo          |            | b7f77000-b7f79000 rw-p 0001b000 08:02 11601524 /lib/ld-2.7.so  |
maps -----------+            | bfa05000-bfa1a000 rw-p bffeb000 00:00 0 [stack]                |
mem                          | ffffe000-fffff000 r-xp 00000000 00:00 0 [vdso]                 |
root                         +----------------------------------------------------------------+
stat                 +----------------------------+
statm                |  Name: cat                 |
status ------+       |  State: R (running)        |
task         |       |  Tgid: 18205               |
wchan        +------>|  Pid: 18205                |
                     |  PPid: 18133               |
                     |  Uid: 1000 1000 1000 1000  |
                     |  Gid: 1000 1000 1000 1000  |
                     +----------------------------+
```

</div>

</div>

## struct task\_struct

<div class="highlight-c">

<div class="highlight">

    $ pahole -C task_struct vmlinux
    
    struct task_struct {
        struct thread_info thread_info;                  /*     0     8 */
        volatile long int          state;                /*     8     4 */
        void *                     stack;                /*    12     4 */
    
        ...
    
        /* --- cacheline 45 boundary (2880 bytes) --- */
        struct thread_struct thread __attribute__((__aligned__(64))); /*  2880  4288 */
    
        /* size: 7168, cachelines: 112, members: 155 */
        /* sum members: 7148, holes: 2, sum holes: 12 */
        /* sum bitfield members: 7 bits, bit holes: 2, sum bit holes: 57 bits */
        /* paddings: 1, sum paddings: 2 */
        /* forced alignments: 6, forced holes: 2, sum forced holes: 12 */
    } __attribute__((__aligned__(64)));

</div>

</div>

## Inspecting task\_struct

 

## Quiz: Inspect opened files

Use the debugger to inspect the process named syslogd.

  - What command should we use to list the opened file descriptors?
  - How many file descriptors are opened?
  - What command should we use the determine the file name for opened file descriptor 3?
  - What is the filename for file descriptor 3?

## Threads

  - Each thread has its own stack and together with the register values it determines the thread execution state
  - A thread runs in the context of a process and all threads in the same process share the resources
  - The kernel schedules threads not processes and user-level threads (e.g. fibers, coroutines, etc.) are not visible at the kernel level

## Classic implementation (Windows)

 

![../\_images/ditaa-4b5c1874d3924d9716f26d4893a3e4f313bf1c43.png](../_images/ditaa-4b5c1874d3924d9716f26d4893a3e4f313bf1c43.png)

## Linux implementation

 

![../\_images/ditaa-fd771038e88b95def30ae9bd4df0b7bd6b7b3503.png](../_images/ditaa-fd771038e88b95def30ae9bd4df0b7bd6b7b3503.png)

## The clone system call

  - CLONE\_FILES - shares the file descriptor table with the parent
  - CLONE\_VM - shares the address space with the parent
  - CLONE\_FS - shares the filesystem information (root directory, current directory) with the parent
  - CLONE\_NEWNS - does not share the mount namespace with the parent
  - CLONE\_NEWIPC - does not share the IPC namespace (System V IPC objects, POSIX message queues) with the parent
  - CLONE\_NEWNET - does not share the networking namespaces (network interfaces, routing table) with the parent

## Namespaces and "containers"

  - Containers = a form of lightweight virtual machines
  - Container based technologies: LXC, docker
  - Containers are built of top of kernel namespaces
  - Kernel namespaces allows isolation of otherwise globally visible resources
  - `struct nsproxy` has multiple namespaces each of which can be selectively shared between groups of processes
  - At boot initial namespaces are created (e.g. `init_net`) that are by default shared between new processes (e.g. list of available network interfaces)
  - New namespace can be created a runtime and new processes can point to these new namespaces

## Accessing the current process

Accessing the current process is a frequent operation:

  - opening a file needs access to `struct task_struct`'s file field
  - mapping a new file needs access to `struct task_struct`'s mm field
  - Over 90% of the system calls needs to access the current process structure so it needs to be fast
  - The `current` macro is available to access to current process's `struct task_struct`

## Accessing the current process on x86

 

![../\_images/ditaa-019489e686a2f60f1594e37458cfcb10320eae0f.png](../_images/ditaa-019489e686a2f60f1594e37458cfcb10320eae0f.png)

## Previous implementation for current (x86)

<div class="highlight-c">

<div class="highlight">

    /* how to get the current stack pointer from C */
    register unsigned long current_stack_pointer asm("esp") __attribute_used__;
    
    /* how to get the thread information struct from C */
    static inline struct thread_info *current_thread_info(void)
    {
       return (struct thread_info *)(current_stack_pointer & ~(THREAD_SIZE – 1));
    }
    
    #define current current_thread_info()->task

</div>

</div>

## Quiz: previous implementation for current (x86)

What is the size of `struct thread_info`?

Which of the following are potential valid sizes for `struct thread_info`: 4095, 4096, 4097?

## Overview the context switching processes

![../\_images/ditaa-f6b228332baf165f498d8a1bb0bc0bdb91ae50c5.png](../_images/ditaa-f6b228332baf165f498d8a1bb0bc0bdb91ae50c5.png)

## context\_switch

<div class="highlight-c">

<div class="highlight">

    static __always_inline struct rq *
    context_switch(struct rq *rq, struct task_struct *prev,
             struct task_struct *next, struct rq_flags *rf)
    {
        prepare_task_switch(rq, prev, next);
    
        /*
         * For paravirt, this is coupled with an exit in switch_to to
         * combine the page table reload and the switch backend into
         * one hypercall.
         */
        arch_start_context_switch(prev);
    
        /*
         * kernel -> kernel   lazy + transfer active
         *   user -> kernel   lazy + mmgrab() active
         *
         * kernel ->   user   switch + mmdrop() active
         *   user ->   user   switch
         */
        if (!next->mm) {                                // to kernel
            enter_lazy_tlb(prev->active_mm, next);
    
            next->active_mm = prev->active_mm;
            if (prev->mm)                           // from user
                mmgrab(prev->active_mm);
            else
                prev->active_mm = NULL;
        } else {                                        // to user
            membarrier_switch_mm(rq, prev->active_mm, next->mm);
            /*
             * sys_membarrier() requires an smp_mb() between setting
             * rq->curr / membarrier_switch_mm() and returning to userspace.
             *
             * The below provides this either through switch_mm(), or in
             * case 'prev->active_mm == next->mm' through
             * finish_task_switch()'s mmdrop().
             */
            switch_mm_irqs_off(prev->active_mm, next->mm, next);
    
            if (!prev->mm) {                        // from kernel
                /* will mmdrop() in finish_task_switch(). */
                rq->prev_mm = prev->active_mm;
                prev->active_mm = NULL;
            }
        }
    
        rq->clock_update_flags &= ~(RQCF_ACT_SKIP|RQCF_REQ_SKIP);
    
        prepare_lock_switch(rq, next, rf);
    
        /* Here we just switch the register state and the stack. */
        switch_to(prev, next, prev);
        barrier();
    
        return finish_task_switch(prev);
      }

</div>

</div>

## switch\_to

<div class="highlight-c">

<div class="highlight">

    #define switch_to(prev, next, last)               \
    do {                                              \
        ((last) = __switch_to_asm((prev), (next)));   \
    } while (0)
    
    
    /*
     * %eax: prev task
     * %edx: next task
     */
    .pushsection .text, "ax"
    SYM_CODE_START(__switch_to_asm)
        /*
         * Save callee-saved registers
         * This must match the order in struct inactive_task_frame
         */
        pushl   %ebp
        pushl   %ebx
        pushl   %edi
        pushl   %esi
        /*
         * Flags are saved to prevent AC leakage. This could go
         * away if objtool would have 32bit support to verify
         * the STAC/CLAC correctness.
         */
        pushfl
    
        /* switch stack */
        movl    %esp, TASK_threadsp(%eax)
        movl    TASK_threadsp(%edx), %esp
    
      #ifdef CONFIG_STACKPROTECTOR
        movl    TASK_stack_canary(%edx), %ebx
        movl    %ebx, PER_CPU_VAR(stack_canary)+stack_canary_offset
      #endif
    
      #ifdef CONFIG_RETPOLINE
        /*
         * When switching from a shallower to a deeper call stack
         * the RSB may either underflow or use entries populated
         * with userspace addresses. On CPUs where those concerns
         * exist, overwrite the RSB with entries which capture
         * speculative execution to prevent attack.
         */
        FILL_RETURN_BUFFER %ebx, RSB_CLEAR_LOOPS, X86_FEATURE_RSB_CTXSW
        #endif
    
        /* Restore flags or the incoming task to restore AC state. */
        popfl
        /* restore callee-saved registers */
        popl    %esi
        popl    %edi
        popl    %ebx
        popl    %ebp
    
        jmp     __switch_to
      SYM_CODE_END(__switch_to_asm)
      .popsection

</div>

</div>

## Inspecting task\_struct

 

## Quiz: context switch

We are executing a context switch. Select all of the statements that are true.

  - the ESP register is saved in the task structure
  - the EIP register is saved in the task structure
  - general registers are saved in the task structure
  - the ESP register is saved on the stack
  - the EIP register is saved on the stack
  - general registers are saved on the stack

## Task states

![../\_images/ditaa-0b8cde2be9bbd195ac9dcaeac978a8bbe0d3b805.png](../_images/ditaa-0b8cde2be9bbd195ac9dcaeac978a8bbe0d3b805.png)

## Blocking the current thread

  - Set the current thread state to TASK\_UINTERRUPTIBLE or TASK\_INTERRUPTIBLE
  - Add the task to a waiting queue
  - Call the scheduler which will pick up a new task from the READY queue
  - Do the context switch to the new task

## wait\_event

<div class="highlight-c">

<div class="highlight">

    /**
     * wait_event - sleep until a condition gets true
     * @wq_head: the waitqueue to wait on
     * @condition: a C expression for the event to wait for
     *
     * The process is put to sleep (TASK_UNINTERRUPTIBLE) until the
     * @condition evaluates to true. The @condition is checked each time
     * the waitqueue @wq_head is woken up.
     *
     * wake_up() has to be called after changing any variable that could
     * change the result of the wait condition.
     */
    #define wait_event(wq_head, condition)            \
    do {                                              \
      might_sleep();                                  \
      if (condition)                                  \
              break;                                  \
      __wait_event(wq_head, condition);               \
    } while (0)
    
    #define __wait_event(wq_head, condition)                                  \
        (void)___wait_event(wq_head, condition, TASK_UNINTERRUPTIBLE, 0, 0,   \
                            schedule())
    
    /*
     * The below macro ___wait_event() has an explicit shadow of the __ret
     * variable when used from the wait_event_*() macros.
     *
     * This is so that both can use the ___wait_cond_timeout() construct
     * to wrap the condition.
     *
     * The type inconsistency of the wait_event_*() __ret variable is also
     * on purpose; we use long where we can return timeout values and int
     * otherwise.
     */
    #define ___wait_event(wq_head, condition, state, exclusive, ret, cmd)    \
    ({                                                                       \
        __label__ __out;                                                     \
        struct wait_queue_entry __wq_entry;                                  \
        long __ret = ret;       /* explicit shadow */                        \
                                                                             \
        init_wait_entry(&__wq_entry, exclusive ? WQ_FLAG_EXCLUSIVE : 0);     \
        for (;;) {                                                           \
            long __int = prepare_to_wait_event(&wq_head, &__wq_entry, state);\
                                                                             \
            if (condition)                                                   \
                break;                                                       \
                                                                             \
            if (___wait_is_interruptible(state) && __int) {                  \
                __ret = __int;                                               \
                goto __out;                                                  \
            }                                                                \
                                                                             \
            cmd;                                                             \
        }                                                                    \
        finish_wait(&wq_head, &__wq_entry);                                  \
       __out:  __ret;                                                        \
     })
    
     void init_wait_entry(struct wait_queue_entry *wq_entry, int flags)
     {
        wq_entry->flags = flags;
        wq_entry->private = current;
        wq_entry->func = autoremove_wake_function;
        INIT_LIST_HEAD(&wq_entry->entry);
     }
    
     long prepare_to_wait_event(struct wait_queue_head *wq_head, struct wait_queue_entry *wq_entry, int state)
     {
         unsigned long flags;
         long ret = 0;
    
         spin_lock_irqsave(&wq_head->lock, flags);
         if (signal_pending_state(state, current)) {
             /*
              * Exclusive waiter must not fail if it was selected by wakeup,
              * it should "consume" the condition we were waiting for.
              *
              * The caller will recheck the condition and return success if
              * we were already woken up, we can not miss the event because
              * wakeup locks/unlocks the same wq_head->lock.
              *
              * But we need to ensure that set-condition + wakeup after that
              * can't see us, it should wake up another exclusive waiter if
              * we fail.
              */
             list_del_init(&wq_entry->entry);
             ret = -ERESTARTSYS;
         } else {
             if (list_empty(&wq_entry->entry)) {
                 if (wq_entry->flags & WQ_FLAG_EXCLUSIVE)
                     __add_wait_queue_entry_tail(wq_head, wq_entry);
                 else
                     __add_wait_queue(wq_head, wq_entry);
             }
             set_current_state(state);
         }
         spin_unlock_irqrestore(&wq_head->lock, flags);
    
         return ret;
     }
    
     static inline void __add_wait_queue(struct wait_queue_head *wq_head, struct wait_queue_entry *wq_entry)
     {
         list_add(&wq_entry->entry, &wq_head->head);
     }
    
     static inline void __add_wait_queue_entry_tail(struct wait_queue_head *wq_head, struct wait_queue_entry *wq_entry)
     {
         list_add_tail(&wq_entry->entry, &wq_head->head);
     }
    
     /**
      * finish_wait - clean up after waiting in a queue
      * @wq_head: waitqueue waited on
      * @wq_entry: wait descriptor
      *
      * Sets current thread back to running state and removes
      * the wait descriptor from the given waitqueue if still
      * queued.
      */
     void finish_wait(struct wait_queue_head *wq_head, struct wait_queue_entry *wq_entry)
     {
         unsigned long flags;
    
         __set_current_state(TASK_RUNNING);
         /*
          * We can check for list emptiness outside the lock
          * IFF:
          *  - we use the "careful" check that verifies both
          *    the next and prev pointers, so that there cannot
          *    be any half-pending updates in progress on other
          *    CPU's that we haven't seen yet (and that might
          *    still change the stack area.
          * and
          *  - all other users take the lock (ie we can only
          *    have _one_ other CPU that looks at or modifies
          *    the list).
          */
         if (!list_empty_careful(&wq_entry->entry)) {
             spin_lock_irqsave(&wq_head->lock, flags);
             list_del_init(&wq_entry->entry);
             spin_unlock_irqrestore(&wq_head->lock, flags);
         }
     }

</div>

</div>

## Waking up a task

  - Select a task from the waiting queue
  - Set the task state to TASK\_READY
  - Insert the task into the scheduler's READY queue
  - On SMP system this is a complex operation: each processor has its own queue, queues need to be balanced, CPUs needs to be signaled

## wake\_up

<div class="highlight-c">

<div class="highlight">

    #define wake_up(x)                        __wake_up(x, TASK_NORMAL, 1, NULL)
    
    /**
     * __wake_up - wake up threads blocked on a waitqueue.
     * @wq_head: the waitqueue
     * @mode: which threads
     * @nr_exclusive: how many wake-one or wake-many threads to wake up
     * @key: is directly passed to the wakeup function
     *
     * If this function wakes up a task, it executes a full memory barrier before
     * accessing the task state.
     */
    void __wake_up(struct wait_queue_head *wq_head, unsigned int mode,
                   int nr_exclusive, void *key)
    {
        __wake_up_common_lock(wq_head, mode, nr_exclusive, 0, key);
    }
    
    static void __wake_up_common_lock(struct wait_queue_head *wq_head, unsigned int mode,
                      int nr_exclusive, int wake_flags, void *key)
    {
      unsigned long flags;
      wait_queue_entry_t bookmark;
    
      bookmark.flags = 0;
      bookmark.private = NULL;
      bookmark.func = NULL;
      INIT_LIST_HEAD(&bookmark.entry);
    
      do {
              spin_lock_irqsave(&wq_head->lock, flags);
              nr_exclusive = __wake_up_common(wq_head, mode, nr_exclusive,
                                              wake_flags, key, &bookmark);
              spin_unlock_irqrestore(&wq_head->lock, flags);
      } while (bookmark.flags & WQ_FLAG_BOOKMARK);
    }
    
    /*
     * The core wakeup function. Non-exclusive wakeups (nr_exclusive == 0) just
     * wake everything up. If it's an exclusive wakeup (nr_exclusive == small +ve
     * number) then we wake all the non-exclusive tasks and one exclusive task.
     *
     * There are circumstances in which we can try to wake a task which has already
     * started to run but is not in state TASK_RUNNING. try_to_wake_up() returns
     * zero in this (rare) case, and we handle it by continuing to scan the queue.
     */
    static int __wake_up_common(struct wait_queue_head *wq_head, unsigned int mode,
                                int nr_exclusive, int wake_flags, void *key,
                      wait_queue_entry_t *bookmark)
    {
        wait_queue_entry_t *curr, *next;
        int cnt = 0;
    
        lockdep_assert_held(&wq_head->lock);
    
        if (bookmark && (bookmark->flags & WQ_FLAG_BOOKMARK)) {
              curr = list_next_entry(bookmark, entry);
    
              list_del(&bookmark->entry);
              bookmark->flags = 0;
        } else
              curr = list_first_entry(&wq_head->head, wait_queue_entry_t, entry);
    
        if (&curr->entry == &wq_head->head)
              return nr_exclusive;
    
        list_for_each_entry_safe_from(curr, next, &wq_head->head, entry) {
              unsigned flags = curr->flags;
              int ret;
    
              if (flags & WQ_FLAG_BOOKMARK)
                      continue;
    
              ret = curr->func(curr, mode, wake_flags, key);
              if (ret < 0)
                      break;
              if (ret && (flags & WQ_FLAG_EXCLUSIVE) && !--nr_exclusive)
                      break;
    
              if (bookmark && (++cnt > WAITQUEUE_WALK_BREAK_CNT) &&
                              (&next->entry != &wq_head->head)) {
                      bookmark->flags = WQ_FLAG_BOOKMARK;
                      list_add_tail(&bookmark->entry, &next->entry);
                      break;
              }
        }
    
        return nr_exclusive;
    }
    
    int autoremove_wake_function(struct wait_queue_entry *wq_entry, unsigned mode, int sync, void *key)
    {
        int ret = default_wake_function(wq_entry, mode, sync, key);
    
        if (ret)
            list_del_init_careful(&wq_entry->entry);
    
        return ret;
    }
    
    int default_wake_function(wait_queue_entry_t *curr, unsigned mode, int wake_flags,
                        void *key)
    {
        WARN_ON_ONCE(IS_ENABLED(CONFIG_SCHED_DEBUG) && wake_flags & ~WF_SYNC);
        return try_to_wake_up(curr->private, mode, wake_flags);
    }
    
    /**
     * try_to_wake_up - wake up a thread
     * @p: the thread to be awakened
     * @state: the mask of task states that can be woken
     * @wake_flags: wake modifier flags (WF_*)
     *
     * Conceptually does:
     *
     *   If (@state & @p->state) @p->state = TASK_RUNNING.
     *
     * If the task was not queued/runnable, also place it back on a runqueue.
     *
     * This function is atomic against schedule() which would dequeue the task.
     *
     * It issues a full memory barrier before accessing @p->state, see the comment
     * with set_current_state().
     *
     * Uses p->pi_lock to serialize against concurrent wake-ups.
     *
     * Relies on p->pi_lock stabilizing:
     *  - p->sched_class
     *  - p->cpus_ptr
     *  - p->sched_task_group
     * in order to do migration, see its use of select_task_rq()/set_task_cpu().
     *
     * Tries really hard to only take one task_rq(p)->lock for performance.
     * Takes rq->lock in:
     *  - ttwu_runnable()    -- old rq, unavoidable, see comment there;
     *  - ttwu_queue()       -- new rq, for enqueue of the task;
     *  - psi_ttwu_dequeue() -- much sadness :-( accounting will kill us.
     *
     * As a consequence we race really badly with just about everything. See the
     * many memory barriers and their comments for details.
     *
     * Return: %true if @p->state changes (an actual wakeup was done),
     *           %false otherwise.
     */
     static int
     try_to_wake_up(struct task_struct *p, unsigned int state, int wake_flags)
     {
         ...

</div>

</div>

## Non preemptive kernel

  - At every tick the kernel checks to see if the current process has its time slice consumed
  - If that happens a flag is set in interrupt context
  - Before returning to userspace the kernel checks this flag and calls `schedule()` if needed
  - In this case tasks are not preempted while running in kernel mode (e.g. system call) so there are no synchronization issues

## Preemptive kernel

  - Tasks can be preempted even when running in kernel mode
  - It requires new synchronization primitives to be used in critical sections: `preempt_disable` and `preempt_enable`
  - Spinlocks also disable preemption
  - When a thread needs to be preempted a flag is set and action is taken (e.g. scheduler is called) when preemption is reactivated

## Process context

The kernel is executing in process context when it is running a system call.

In process context there is a well defined context and we can access the current process data with `current`

In process context we can sleep (wait on a condition).

In process context we can access the user-space (unless we are running in a kernel thread context).

## Kernel threads

Sometimes the kernel core or device drivers need to perform blocking operations and thus they need to run in process context.

Kernel threads are used exactly for this and are a special class of tasks that don't "userspace" resources (e.g. no address space or opened files).

## Inspecting kernel threads

 

## Quiz: Kernel gdb scripts

What is the following change of the lx-ps script trying to accomplish?

<div class="highlight-diff">

<div class="highlight">

    diff --git a/scripts/gdb/linux/tasks.py b/scripts/gdb/linux/tasks.py
    index 17ec19e9b5bf..7e43c163832f 100644
    --- a/scripts/gdb/linux/tasks.py
    +++ b/scripts/gdb/linux/tasks.py
    @@ -75,10 +75,13 @@ class LxPs(gdb.Command):
         def invoke(self, arg, from_tty):
             gdb.write("{:>10} {:>12} {:>7}\n".format("TASK", "PID", "COMM"))
             for task in task_lists():
    -            gdb.write("{} {:^5} {}\n".format(
    +            check = task["mm"].format_string() == "0x0"
    +            gdb.write("{} {:^5} {}{}{}\n".format(
                     task.format_string().split()[0],
                     task["pid"].format_string(),
    -                task["comm"].string()))
    +                "[" if check else "",
    +                task["comm"].string(),
    +                "]" if check else ""))
    
    
     LxPs()

</div>

</div>

</div>

<div id="slide_notes" class="section">

</div>
