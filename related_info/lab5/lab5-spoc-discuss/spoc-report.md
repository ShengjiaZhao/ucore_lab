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

* The result of printing is (Items starting with SPOC are prints related to process state

SPOC: Creating new kernel thread
ide 0:      10000(sectors), 'QEMU HARDDISK'.
ide 1:     262144(sectors), 'QEMU HARDDISK'.
SWAP: manager = fifo swap manager
BEGIN check_swap: count 31829, total 31829
setup Page Table for vaddr 0X1000, so alloc a page
setup Page Table vaddr 0~4MB OVER!
set up init env for check_swap begin!
page fault at 0x00001000: K/W [no page found].
page fault at 0x00002000: K/W [no page found].
page fault at 0x00003000: K/W [no page found].
page fault at 0x00004000: K/W [no page found].
set up init env for check_swap over!
write Virt Page c in fifo_check_swap
write Virt Page a in fifo_check_swap
write Virt Page d in fifo_check_swap
write Virt Page b in fifo_check_swap
write Virt Page e in fifo_check_swap
page fault at 0x00005000: K/W [no page found].
swap_out: i 0, store page in vaddr 0x1000 to disk swap entry 2
write Virt Page b in fifo_check_swap
write Virt Page a in fifo_check_swap
page fault at 0x00001000: K/W [no page found].
do pgfault: ptep c03a9004, pte 200
swap_out: i 0, store page in vaddr 0x2000 to disk swap entry 3
swap_in: load disk swap entry 2 with swap_page in vadr 0x1000
write Virt Page b in fifo_check_swap
page fault at 0x00002000: K/W [no page found].
do pgfault: ptep c03a9008, pte 300
swap_out: i 0, store page in vaddr 0x3000 to disk swap entry 4
swap_in: load disk swap entry 3 with swap_page in vadr 0x2000
write Virt Page c in fifo_check_swap
page fault at 0x00003000: K/W [no page found].
do pgfault: ptep c03a900c, pte 400
swap_out: i 0, store page in vaddr 0x4000 to disk swap entry 5
swap_in: load disk swap entry 4 with swap_page in vadr 0x3000
write Virt Page d in fifo_check_swap
page fault at 0x00004000: K/W [no page found].
do pgfault: ptep c03a9010, pte 500
swap_out: i 0, store page in vaddr 0x5000 to disk swap entry 6
swap_in: load disk swap entry 5 with swap_page in vadr 0x4000
count is 5, total is 5
check_swap() succeeded!
++ setup timer interrupts
SPOC: process is scheduled to run
SPOC: Running kernel thread and using syscall to execute as user process
I am the parent. Forking the child...
I am parent, fork a child pid 3
I am the parent, waiting now..
SPOC: process is giving up CPU
kernel_execve: pid = 4, name = "exit".
I am the parent. Forking the child...
I am parent, fork a child pid 5
I am the parent, waiting now..
I am the child.
I am the child.
SPOC: process is scheduled to run
waitpid 3 ok.
exit pass.
SPOC: process is exiting
SPOC: process is giving up CPU


