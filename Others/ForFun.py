def Filt(arr,func): 
    result = [] 
    for item in arr: 
        result.append(func(item)) 
    return result

def MyFilter(ele): 
    if ele < 0 : 
        return 0 
    return ele

def expr(x,n): 
    result = 1 
    for i in range(1,n+1): 
        result = result * x 
    return result

def expr2(num,n): 
    if n==0: 
        return 1 
    return num*expr(num,n-1)

def num_of_one(num):
    cnt = 0
    flag = 1
    while c_int(flag).value:
        if c_int(num & flag).value:
            cnt+=1
        flag = flag <<1
    return cnt

def num_of_one2(num):
    cnt = 0
    while c_int(num).value:
        cnt+=1
        num = (num -1) & num
    return cnt

def num_of_one3(num):
    if num>0:
        nbin=bin(num)
        return nbin.count('1')
    else:
        num=abs(num)
        nbin=bin(num-1)
        return 32 - nbin.count('1')

def num_of_one4(num):
    nbin = bin(num & 0xffffffff)
    return nbin.count('1')

def num_of_one5(num):
    counts = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]
    result = 0
    for i in range(0,32,4):
        result += counts[num >> i & 0xf]
    return result


def main():
    arr = [-5,3,5,11,-45,32] 
    func = MyFilter 
    print('%s' % (Filt(arr,func)))

def main2():
    arr = [-5,3,5,11,-45,32] 
    print('%s' % (map(lambda x : 0 if x<0 else x ,arr)))

def main1():
    print(expr2(2,5))

def main3():
    print(num_of_one5(1024))


if __name__ == '__main__': 
    main1()
