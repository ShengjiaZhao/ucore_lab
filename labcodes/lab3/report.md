# Task 1

This task is accomplished by finding the corresponding page table entry and allocate a page in case it does not yet exist
```
    ptep = get_pte(mm->pgdir, addr, 1);     //(1) try to find a pte, if pte's PT(Page Table) isn't existed, then create a PT.
    if (ptep == NULL) {
		cprintf("Cannot find page table entry");
		goto failed;
    }
    if (*ptep == NULL) {					//(2) if the phy addr isn't exist, then alloc a page & map the phy addr with logical addr
        if (pgdir_alloc_page(mm->pgdir, addr, perm) == NULL) {
            cprintf("Cannot allocate new page\n");
            goto failed;
        }
    }
```


# Task 2
To implement the FIFO algorithm, each new page is inserted at the back of the queue
```
	list_add(head->prev, entry);
```
and when a "victim" needs to be swapped out, the front element of the queue is selected
```
	list_entry_t *victim = head->next;
	list_del(victim);
    *ptr_page = le2page(victim, pra_page_link);
```

The following code is used to perform swapping
```
	struct Page *page = NULL;
	ret = swap_in(mm, addr, &page);
	if (ret != 0) {
		cprintf("swap in failed\n");
		goto failed;
	}
	page_insert(mm->pgdir, page, addr, perm);
	swap_map_swappable(mm, addr, page, 1);
	page->pra_vaddr = addr;
```
