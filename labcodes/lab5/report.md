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

* To achieve copy on write
