def add100(x):
    return x+100

hh = [11,22,33]
print map(add100,hh)

def abc(a, b, c):
    return a*10000 + b*100 + c
list1 = [11,22,33]
list2 = [44,55,66]
list3 = [77,88,99]
print map(abc,list1,list2,list3)
print map(None,list1)
print map(None,list1,list2,list3)