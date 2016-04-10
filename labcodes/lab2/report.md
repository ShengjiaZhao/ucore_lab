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
