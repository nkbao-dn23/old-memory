from pwn import *
r = remote('125.235.240.166',20103)
r.recvline()
r.recvline()
dem=0
for i in range(0,256):
    dem+=1
    print("i: ",dem)
    u = r.recvline()
    print(u)
    # for _ in u:
    #     print(_)
    char_set = []
    # for _ in u:
    # 	if(_=='*' or _=='/' or _=='+' or _=='-'):
    # 		print(_)
    # 		break
    # + : 0 ; - : 1 ; *: 2 ; / : 3

    for _ in u:
        if(chr(_)=='*' or chr(_)=='/' or chr(_)=='+' or chr(_)=='-'):
            # print(chr(_))
            if(chr(_)=='+'):
                char_set.append(0)
            if(chr(_)=='-'):
                char_set.append(1)
            if(chr(_)=='*'):
                char_set.append(2)
            if(chr(_)=='/'):
                char_set.append(3)
            break
    res1 = 0
    res2 = 0
    dau = 0
    ans = 0
    if(char_set[0]==0):
        kitu = '+'
        for _ in u:
            if(chr(_)==kitu):
                dau=1
            if(48<=_ and _<=57 and dau==0):
                res1 = res1*10 + (_-48)
            elif(48<=_ and _<=57 and dau==1):
                res2 = res2*10 + (_-48)
        ans = res1+res2  


    if(char_set[0]==1):
        kitu = '-'
        for _ in u:
            if(chr(_)==kitu):
                dau=1
            if(48<=_ and _<=57 and dau==0):
                res1 = res1*10 + (_-48)
            elif(48<=_ and _<=57 and dau==1):
                res2 = res2*10 + (_-48)
        ans = res1-res2 

    if(char_set[0]==2):
        kitu = '*'
        for _ in u:
            if(chr(_)==kitu):
                dau=1
            if(48<=_ and _<=57 and dau==0):
                res1 = res1*10 + (_-48)
            elif(48<=_ and _<=57 and dau==1):
                res2 = res2*10 + (_-48)
        ans = res1*res2 

    if(char_set[0]==3):
        kitu = '/'
        for _ in u:
            if(chr(_)==kitu):
                dau=1
            if(48<=_ and _<=57 and dau==0):
                res1 = res1*10 + (_-48)
            elif(48<=_ and _<=57 and dau==1):
                res2 = res2*10 + (_-48)
        ans = res1//res2 

    print("ans: ",ans)
    r.sendline(str(ans).encode())
    r.recvline()
    u = r.recvline()
    print(u)
r.interactive()
# u = r.recvline()
# print(u)
# u = r.recvline()
# print(r)
# u = r.recvline()
# print(r)
