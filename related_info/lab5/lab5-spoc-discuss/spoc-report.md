* Add the following code in ```proc.c``` to start up a new user process
```
int spoc_fun(void *arg) {
	cprintf("SPOC: Running kernel thread and using syscall to execute as user process");
	extern unsigned char _binary_obj___user_exit_out_start[], _binary_obj___user_exit_out_size[]; 
	kernel_execve("spoc", _binary_obj___user_exit_out_start,
				  (size_t)_binary_obj___user_exit_out_size);  
	cprintf("SPOC: Should never get here\n");
	cpu_idle();
}
```
and in ```proc_init```
```
	pid = kernel_thread(spoc_fun, NULL, 0);
	if (pid <= 0) {
		panic("create new thread failed\n");
	}
	set_proc_name(find_proc(pid), "spoc");
```
