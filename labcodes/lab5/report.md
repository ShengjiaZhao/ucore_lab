# Task 1
```
	tf->tf_cs = USER_CS;
	tf->tf_ds = tf->tf_es = tf->tf_ss = USER_DS;
	tf->tf_esp = USTACKTOP;
	tf->tf_eip = elf->e_entry;
	tf->tf_eflags = FL_IF;
```

* The thread first calls ```KERNEL_EXECVE```, which calls the ```SYS_exec``` system call. 
This call runs ```do_execve``` do execute a new program. ```do_execve``` first clears previous memory space (unless it's a kernel thread), 
then calls ```load_icode``` to load code of the new program and allocate the new memory space. 
Finally it sets the trapframe to simulate a interrupt started before executing the first line of the user program,
so that an ```iret``` can restore this state to start execution of user program

# Task 2
First add the following additional initialization to ```alloc_proc```
```
		proc->wait_state = 0;
        proc->cptr = NULL;
		proc->optr = NULL;
		proc->yptr = NULL;
```
and add the following to ```do_fork```
```
		proc = alloc_proc()
```
In ```pmm.c```, copying a page is accomplished by
```
		void * src = page2kva(page);
        void * dst = page2kva(npage);
        memcpy(dst, src, PGSIZE);
        ret = page_insert(to, npage, start, perm);
```

* To achieve copy on write a copied page should be set to be readonly. In the mean time, each page (such as in the ```pages``` array) should contain a pointer to a linked list.
In the page is shared between multiple processes, this linked list points to the ```proc_struct``` of all the sharing processes. When a read-only page fault is triggered, by chechking 
```vma_struct``` we know if this page is truly readonly. If not, the page should point to a linked list with the current process as one of its nodes. We remove this process from the linked list,
and copy the content to a new page. If the linked list only contains one element, we remove this linked list and set this page to the access permission of the only process using it. 

# Task 3
1. ```sys_fork``` calls ```do_fork```, and ```do_fork``` allocates a new ```proc_struct``` and fills in correct values to its members. It sets the ```trapframe``` of the new process so that an ```iret``` can correctly start its execution. Furthermore,
it set ups a new kernel stack, copies the ```mm_struct``` and physical memory pages used by the forking process. Finally it sets the new process in ```RUNNABLE``` state
2. ```sys_exec``` calls ```do_execve```, and ```do_execve``` first frees the original virtual memory space and all related data structures unless the process/thread is a kernel thread. Next it calls ```load_icode``` to load in the new program and sets up the new virtual 
memory space
3. ```sys_wait``` calls ```do_wait```, and ```do_wait``` finds the child process, if the process is not in zombie state, the parent process sleeps to wait for this. If the child process is in zombie state, the parent process will remove it from ```proc_list```,
free up kernel stack and PCB
4. ```sys_exit``` calls ```do_exit```, and ```do_exit``` first frees the virtual memory space of the process, then wakes up its parent to finish up the cleaning process. Finally it calls ```schedule``` to relinquish the CPU
so that its parent process may run and finish the clean up


