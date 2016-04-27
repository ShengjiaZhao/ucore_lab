semaphore mutex=1,a,empty1=m,b,empty2=N,full1,full2=0;
cobegin
    process(A);
    process(B);
    process(C)
coend
// A物品入库
process A
begin
    while(TRUE)
    begin
    p(empty1);
    P(a);
    p(mutex);
    A物品入库;
    v(mutex);
    V(b);
    v(full1);
    end
end
// B物品入库：
process B
begin
    while(TRUE)
    begin
    p(empty2);
    P(b);
    p(mutex);
    B物品入库;
    v(mutex);
    V(a);
    p(full2);
    end
end
// process C
begin
    while(TRUE)
    begin
    p(full1);
    p(full2);
    p(a);
    P(b);
    组装;
    V(a);
    v(b);
    v(empty1);
    v(empty2);
    end
end

