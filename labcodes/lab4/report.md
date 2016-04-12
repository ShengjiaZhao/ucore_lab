# Task 1
The following properties of proc_struct needs to be initialized
```
        proc->state = PROC_UNINIT;
        proc->pid = -1;
        proc->runs = 0;
        proc->kstack = 0;
        proc->need_resched = 0;
        proc->parent = NULL;
        proc->mm = NULL;
        memset(&(proc->context), 0, sizeof(struct context));
        proc->tf = NULL;
        proc->cr3 = boot_cr3;
        proc->flags = 0;
        memset(proc->name, 0, PROC_NAME_LEN);
```
* "context" stores the registers (general, eip, esp) of current thread, which can be used to save and restore excution context
* "trapframe" stores the information for the thread's first execution

# Task 2
```
    proc = alloc_proc()
	if (proc == NULL) {
        goto fork_out;
    }
    proc->parent = current;

    if (setup_kstack(proc) != 0) {
        goto bad_fork_cleanup_proc;
    }
	
    if (copy_mm(clone_flags, proc) != 0) {
        goto bad_fork_cleanup_kstack;
    }
	
    copy_thread(proc, stack, tf);

    bool intr_flag;
    local_intr_save(intr_flag);
	proc->pid = get_pid();
	hash_proc(proc);
	list_add(&proc_list, &(proc->list_link));
	nr_process ++;
    local_intr_restore(intr_flag);

    wakeup_proc(proc);

    ret = proc->pid;
```
* Yes, in function ```get_pid```, ucore finds a pid different from all existing processes

# Task 3
```proc_run``` first enters a critical section, then changes the stack and PDTR to the corresponding values for the new process in
```
            load_esp0(next->kstack + KSTACKSIZE);
            lcr3(next->cr3);
```
Next by ```switch_to``` the context (registers) of the original process is saved, and those of the new process is loaded. 
* Two kernel threads are created, idleproc and initproc
* These two statements turn off and restore interrupt mask, so that the statements within can execute uninterrupted
