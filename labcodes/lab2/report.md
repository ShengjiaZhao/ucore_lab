The change to default_pmm.c is very simple, all that needs to be done is to change
'''		list_add_after(&free_list, &(base->page_link)); '''
to
''' 	list_add_after(list_prev(&free_list), &(base->page_link)); '''
the reason for this change is that the original version inserts the new block at the front of the list, which leads to failure of passing an assert. Inserting it at the back solves this problem.
