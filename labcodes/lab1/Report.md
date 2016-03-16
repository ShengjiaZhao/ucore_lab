# Exercise 1

## 1.1 
makefile依次构造所依赖的文件，最后链接为ucore.img

## 1.2
512个字节的扇区，要求最后两个字节为0x55AA

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