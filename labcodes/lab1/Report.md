# Exercise 1

* 1.1 makefile builds a file based on the file it depends on. A file is build when all its dependencies have been built.
After all the source files have been built, the makefile links them into the final ucore.img

* 1.2 The last two bytes of the 512B sector must be 0x55AA

# Exercise 2

The process is as follows:

+ Add "break start" to the file gdbinit
+ Run in terminal "make debug"
+ Use the command "s" for single step statement-wise execution, and "si" for instruction-wise execution

# Exercise 3

+ A20 is un-set from low by the following code

``` 
seta20.1:
    inb $0x64, %al                                  # Wait for not busy(8042 input buffer empty).
    testb $0x2, %al
    jnz seta20.1

    movb $0xd1, %al                                 # 0xd1 -> port 0x64
    outb %al, $0x64                                 # 0xd1 means: write data to 8042's P2 port

seta20.2:
    inb $0x64, %al                                  # Wait for not busy(8042 input buffer empty).
    testb $0x2, %al
    jnz seta20.2

    movb $0xdf, %al                                 # 0xdf -> port 0x60
    outb %al, $0x60                                 # 0xdf = 11011111, means set P2's A20 bit(the 1 bit) to 1

```

+ The following code reserves a memory block for GDT table

```
.p2align 2                                          # force 4 byte alignment
gdt:
    SEG_NULLASM                                     # null seg
    SEG_ASM(STA_X|STA_R, 0x0, 0xffffffff)           # code seg for bootloader and kernel
    SEG_ASM(STA_W, 0x0, 0xffffffff)                 # data seg for bootloader and kernel

gdtdesc:
    .word 0x17                                      # sizeof(gdt) - 1
    .long gdt                                       # address gdt
```

+ Protected mode is turned on by the following code, with GDTR initialized

```
    lgdt gdtdesc
    movl %cr0, %eax
    orl $CR0_PE_ON, %eax
    movl %eax, %cr0
```

# Exercise 4

+ To read a sector from disk, the bootloader perform the following actions
    1. wait for the disk to be ready
    2. send read commands
    3. wait for the disk to complete the operation
    4. fetch the results
    
This is accomplished by the following code snippet

``` c
/* readsect - read a single sector at @secno into @dst */
static void
readsect(void *dst, uint32_t secno) {
    // wait for disk to be ready
    waitdisk();

    outb(0x1F2, 1);                         // count = 1
    outb(0x1F3, secno & 0xFF);
    outb(0x1F4, (secno >> 8) & 0xFF);
    outb(0x1F5, (secno >> 16) & 0xFF);
    outb(0x1F6, ((secno >> 24) & 0xF) | 0xE0);
    outb(0x1F7, 0x20);                      // cmd 0x20 - read sectors

    // wait for disk to be ready
    waitdisk();

    // read a sector
    insl(0x1F0, dst, SECTSIZE / 4);
}
```
+ To read an ELF file the bootloader first reads in the head of the ELF, and checks it validity

``` c
    // read the 1st page off disk
    readseg((uintptr_t)ELFHDR, SECTSIZE * 8, 0);

    // is this a valid ELF?
    if (ELFHDR->e_magic != ELF_MAGIC) {
        goto bad;
    }
```

then information about where in the memory the content of the ELF file should be loaded is extracted. The contents are read
and loaded to that location
``` c
    struct proghdr *ph, *eph;

    // load each program segment (ignores ph flags)
    ph = (struct proghdr *)((uintptr_t)ELFHDR + ELFHDR->e_phoff);
    eph = ph + ELFHDR->e_phnum;
    for (; ph < eph; ph ++) {
        readseg(ph->p_va & 0xFFFFFF, ph->p_memsz, ph->p_offset);
    }
```

Finally the program jumps to the entry point as indicated by the ELF header
``` c
    ((void (*)(void))(ELFHDR->e_entry & 0xFFFFFF))();
```

# Exercise 5

The only change is the addition of the following code snippet
``` c
    int i, j;
    uint32_t ebp = read_ebp();
    uint32_t eip = read_eip();

    for (i = 0; i < STACKFRAME_DEPTH; i++) {
        cprintf("ebp:0x%08x eip:0x%08x args:", ebp, eip);
        uint32_t *args = (uint32_t *)ebp + 2;
        for (j = 0; j < 4; j ++) {
            cprintf("0x%08x ", args[j]);
        }
        cprintf("\n");
        print_debuginfo(eip - 1);
        ebp = *((uint32_t *)ebp);
        eip = *((uint32_t *)ebp + 1);
        if (ebp == 0)
        	break;
    }
```

The last line is
``` ebp:0x00007bf8 eip:0x00007c4f args:0xc031fcfa 0xc08ed88e 0x64e4d08e 0xfa7502a8 ```
+ eip points to 0x7c4f, which is the address of bootmain
+ ebp points to 0x7bf8, which is the previous stack pointer position

# Exercise 6
