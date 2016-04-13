# Task 1
The change to default_pmm.c is very simple, 
all that needs to be done is to insert the freed block in the right order sorted by address, 
and this is accomplished by the following snippet of code
```
    list_entry_t *le = list_next(&free_list);
	list_entry_t *insert_loc = &free_list;
    while (le != &free_list) {
        p = le2page(le, page_link);
        le = list_next(le);
        if (base + base->property == p) {
            base->property += p->property;
            ClearPageProperty(p);
            list_del(&(p->page_link));
        }
        else if (p + p->property == base) {
            p->property += base->property;
            ClearPageProperty(base);
            base = p;
            list_del(&(p->page_link));
        } 
		else if ((unsigned int)p < (unsigned int)base) {
			cprintf("Here");
			insert_loc = &(p->page_link);
		}
    }
    nr_free += n;	
	list_add_after(insert_loc, &(base->page_link));
```
* The algorithm can be improved by using better data structure to main the list of free block. An example would be to use a binary tree to organize the blocks, so that inserting a block takes O(logN) time rather than O(N)

# Task 2
This is accomplished by adding the following snippet of code in ```get_pte```
```
    pde_t *pdep = &pgdir[PDX(la)];			// (1) find page directory entry
    if (!(*pdep & PTE_P)) {				// (2) check if entry is not present
        struct Page *page = alloc_page();		// (3) check if creating is needed, then alloc page for page table
        if (page == NULL) {
            return NULL;
        }
        set_page_ref(page, 1);				// (4) set page reference
        uintptr_t pa = page2pa(page);			// (5) get linear address of page
        memset(KADDR(pa), 0, PGSIZE);			// (6) clear page content using memset
        *pdep = pa | PTE_U | PTE_W | PTE_P;		// (7) set page directory entry's permission
    }
    return &((pte_t *)KADDR(PDE_ADDR(*pdep)))[PTX(la)];		// (8) return page table entry
```
* PDE contains the following fields

| 31 .. 12 | 11 .. 8 | 7 .. 0 |
| --- | --- | --- |
| page table address | reserved | flags |

* PTE contains the following fields

31 .. 12 | 11 .. 9 | 8 .. 0
--- | --- | --- 
page address | reserved | flags
 
# Task 3
This is accomplished by adding the following snippet of code in ```page_remove_pte```
```
    if (*ptep & PTE_P) {				//(1) check if this page table entry is present
        struct Page *page = pte2page(*ptep);		//(2) find corresponding page to pte
        if (page_ref_dec(page) == 0) {			//(3) decrease page reference
            free_page(page);				//(4) and free this page when page reference reachs 0
        }
        *ptep = 0;					//(5) clear second page table entry
        tlb_invalidate(pgdir, la);			//(6) flush tlb
    }
```
