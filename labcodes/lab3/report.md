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

* PTE contains bit 0 (present) that indicates if the page is in the physical memory. If the entire entry is 0, then the page doesn't yet exist, and should be created. 
Otherwise the page is in swap and should be moved back to memory. PTE also contains bit 6 (accessed) and 7 (dirty). These indicate if the page has been used, or written to. 
They can affect the decision when selecting the swap victim

* During a page fault, the hardware must put the address that triggered the page fault in CR2, save the current context information into the stack, 
find the interrupt entry for page fault exception, and execute the interrupt handler function


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

* The current swap manager can support this if we add a new field that indicates the current position of the clock, and add another field in ```struct Page``` that points to the PTE entry corresponding to this physical page, 
and a flag that indicates if this page is dirty. 
Each time a victim is to be selected, we check the physical page at the current clock position, and if 
  1. access=1, dirty=1, set access=0 and move clock one page forward
  2. access=0, dirty=1, set dirty=0 and set the dirty flag in ```struct Page```, move clock one page forward
  3. access=1, dirty=0, set access=0 and move clock one page forward
  4. access=0, dirty=0, if the dirty flag in ```struct Page``` is 1, write the page back to swap. Set this page as the swap out victim
Additional questions:
  1. The replaced page should have both accessed and dirty bit set to 0
  2. By checking bit 6 and bit 7 of the PTE entry
  3. Swap out whenever a new page is needed, but not physical pages are available. Swap in whenever a page in swap is accessed
