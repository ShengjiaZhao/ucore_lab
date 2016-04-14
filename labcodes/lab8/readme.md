# Task 1
To perform reading, we perform the following
1. If the start offset is not aligned to the first block, we read in the incomplete part of the first block. Otherwise, we treat this either as a full block, or the last block
2. Read in all the full blocks in the middle
3. If the end address is not aligned to the last block, we read in the incomplete part of the last block 
This is accomplished with the following code
```
	// Read the first block, if offset is in the middle of the block
	blkoff = offset % SFS_BLKSIZE;			
	if (blkoff != 0) {			
		size = nblks > 0 ? SFS_BLKSIZE - blkoff : endpos - offset;
		if (sfs_bmap_load_nolock(sfs, sin, blkno, &ino))
			goto out;
		if (sfs_buf_op(sfs, buf, size, ino, blkoff))
			goto out;
		alen += size;
		buf = (char *)buf + size;
		blkno++;
	} else {					// Otherwise read this block either as a full block, or the last block
		nblks++;
	}
	
	// Read the full blocks 
	int read_count;
	for (read_count = 0; read_count < (int)nblks - 1; read_count++) {
		if (sfs_bmap_load_nolock(sfs, sin, blkno, &ino))
			goto out;
		if (sfs_block_op(sfs, buf, ino, 1))
			goto out;
		blkno++;
		alen += SFS_BLKSIZE;
		buf = (char *)buf + SFS_BLKSIZE;
	}

	// Read the final incomplete block, if it exists
	size = endpos % SFS_BLKSIZE;
    if(size != 0  &&  nblks > 0) {
        if(sfs_bmap_load_nolock(sfs, sin, blkno, &ino)) 
			goto out;
        if(sfs_buf_op(sfs, buf, size, ino, 0))   
			goto out;
        alen += size;
    }
```

# Task 2
The code is similar to lab6 and lab7, the major difference is that elf header, program header and program content are read from disk rather than ```binary```
```
	struct elfhdr elf_header;
	struct elfhdr *elf = &elf_header;
	load_icode_read(fd, (void *)elf, sizeof(struct elfhdr), 0);
    //(3.2) get the entry of the program section headers of the bianry program (ELF format)

	ph = kmalloc(sizeof(struct proghdr) * elf->e_phnum);
	load_icode_read(fd, (void *)ph, sizeof(struct proghdr) * elf->e_phnum, elf->e_phoff);
```
```
	load_icode_read(fd, (void *)(page2kva(page) + off), size, from);
```
To set up program arguments, first allocate the necessary storage, then copy the contents into the stack at the correct locations.
```
	// Allocate stack storage for actual arguments
	uint32_t argv_size = 0, i;
    for (i = 0; i < argc; i ++)
        argv_size += strnlen(kargv[i], EXEC_MAX_ARG_LEN + 1) + 1;
    uintptr_t stack_top = USTACKTOP - argv_size;
	stack_top = stack_top & 0xFFFFFFFC;				// Align stack top to 4 bytes boundaries
	uintptr_t content_ptr = stack_top;
	// Allocate stack storage for argument pointers
    stack_top -= argc * sizeof(char *);
    uintptr_t argv_ptr = stack_top;
	// Copy contents and pointers into the stack
    for (i = 0; i < argc; i ++) {
        ((char **)argv_ptr)[i] = strcpy(content_ptr, kargv[i]);
        content_ptr += strnlen(kargv[i], EXEC_MAX_ARG_LEN + 1) + 1;
    }
	// Allocate stack storage for argment count
    stack_top -= sizeof(int);
    *(int *)stack_top = argc;
```
