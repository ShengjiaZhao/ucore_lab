# Task 0 
The only difference from lab6 is the need to update timers in ```trap.c```
```
    case IRQ_OFFSET + IRQ_TIMER:
		run_timer_list();
```

# Task 1
## Implementation of kernel semaphore
There are four methods for ```semaphore_t``` in ucore
1. ```sem_init```: sets the initial value of the semaphore
2. ```up```: if the ```wait_queue``` is empty, this increases the semaphore value. Otherwise a process in the semaphore wait queue is selected to be waken up
3. ```down```: if the semaphore is greater than 0, the value is decreased by 1. Otherwise this process is added to the ```wait_queue```, and ```schedule()``` is called to enter waiting state until ```sem_up``` wakes it up
4. ```try_down```: if the semaphore is greater than 0, decrease it by 1 and return 1. Otherwise do nothing and return 0

## Comparison with user semaphore
Users cannot turn off interrupt, but can use test and set (TS) instruction to enter a critical section. The pseudo-code could look like
```
	while(test_and_set(flag))
		schedule();
	// critical section code
	flag = 0;
```
Everything else is similar

# Task 2
## Monitor
The following code unlocks a thread waiting on the condition
```
void cond_signal (condvar_t *cvp) {
   if(cvp->count > 0) {
	   monitor_t *mt = cvp->owner;
	   mt->next_count++;
	   up(&(cvp->sem));
	   down(&(mt->next));
	   mt->next_count--;
   }
}
```	
and the following suspends a process until another process wakes it up
```
void cond_wait (condvar_t *cvp) {
	cvp->count ++;
	monitor_t* mt = cvp->owner;
	if(mt->next_count > 0)
		up(&(mt->next));
	else
		up(&(mt->mutex));
	down(&(cvp->sem));
	cvp->count --;
}
```

## Philosopher's problem
Add the following code to ```phi_take_forks_condvar``` to test for condition to eat, and wait if condition not satisfied
```
	down(&(mtp->mutex));
	state_condvar[i] = HUNGRY;
	phi_test_condvar(i);
	if(state_condvar[i] != EATING)
		cond_wait(&(mtp->cv[i]));
```
and the following code to ```phi_put_forks_condvar``` to stop eating and test on neighbor's condition to eat
```
	down(&(mtp->mutex));
	state_condvar[i] = THINKING;
	phi_test_condvar(LEFT);
	phi_test_condvar(RIGHT);
```

## Comparison with user monitor
This is essentially the same as before, entering critical sections by the TS instruction
