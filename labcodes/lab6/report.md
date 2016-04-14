# Task 0
Additional initialization is required in ```alloc_proc``` of ```proc.c```
```
    proc->rq = NULL;
    list_init(&(proc->run_link));
    proc->time_slice = 0;
    proc->lab6_run_pool.left = NULL;
	proc->lab6_run_pool.right = NULL;
	proc->lab6_run_pool.parent = NULL;
    proc->lab6_stride = 0;
    proc->lab6_priority = 0;
```

Furthermore in ```trap.c``` during timer interrupt, the ```sched_class_proc_tick``` function should be called. 
```
	extern void sched_class_proc_tick(struct proc_struct *);
	sched_class_proc_tick(current);
```
This means that the corresponding function in ```sched.c``` should be set to global
```
	/* static */ void
	sched_class_proc_tick(struct proc_struct *proc)
```


# Task 1
1. In sched_class
	1. ```init``` initializes the run queue struct
	2. ```enqueue``` inserts a process into the queue so that this process could be scheduled to run
	3. ```dequeue``` removes a process from the queue
	4. ```pick_next``` returns the next process in the queue that the scheduler thinks should run
	5. ```proc_tick``` is called during each timer interrupt event. The scheduler decreases the remaining time of the running process and sets ```need_resched``` to 1 if its time expires. 
2. To implement multi-level feedback queue, the scheduler should contain pointers to multiple queues (lists). Each ```proc_struct``` should also contain an additional member, its priority.
When ```enqueue``` is called, the process is inserted into the queue with the same priority as in ```proc_struct```. The schedulers selects a queue during each scheduling event. The number of times on average 
it selects each queue should be exponentially smaller as we move to lower priority queues. When a process relinquishes the CPU volentarily, its priority increases. 
If ```proc_tick``` forces the process to relinquish the CPU, it priority decreases. This change in priority is accomlished by resetting the value of priority member variable in ```proc_struct```

# Task 2
For initialization add the following code to ```stride_init```
```
	list_init(&(rq->run_list));
	rq->max_time_slice = MAX_TIME_SLICE;
	rq->lab6_run_pool = NULL;
	rq->proc_num = 0;	
```
To enqueue or dequeue a new element insert the following code to ```stride_enqueue``` and ```stride_dequeue```
```
	rq->lab6_run_pool = skew_heap_insert(rq->lab6_run_pool, &(proc->lab6_run_pool), proc_stride_comp_f);
	if (proc->time_slice <= 0 || proc->time_slice > rq->max_time_slice)
		proc->time_slice = rq->max_time_slice;
	proc->rq = rq;
	rq->proc_num++;
```
```
	rq->lab6_run_pool = skew_heap_remove(rq->lab6_run_pool, &(proc->lab6_run_pool), proc_stride_comp_f);
	rq->proc_num--;
```
To pick the next process to run, use the following code in ```stride_pick_next```
```
	if (rq->lab6_run_pool == NULL)
		return NULL;
    struct proc_struct *next_proc = le2proc(rq->lab6_run_pool, lab6_run_pool);
	next_proc->lab6_stride += next_proc->lab6_priority == 0 ? BIG_STRIDE : BIG_STRIDE / next_proc->lab6_priority;	
	return next_proc;
```
And finally in ```stride_proc_tick```	
```
	if(proc->time_slice == 0)
		proc->need_resched = 1;
	else
		proc->time_slice--;
```
