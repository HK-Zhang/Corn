import numpy as np
import sys

def main():
    A=np.array([1,2,3,4,5,6,7,8,9,0])
    B=A.copy()
    print A
    print 'same as print A,',A[:]
    print 'same as print A,',A[::1]
    print 'reverse A,',A[::-1]
    print 'print all elements with 2 interval,',A[::2]
    print 'print elements from the 4th element with 2 interval,',A[3::2]
    print 'print elements from the last 4th element with 2 interval,',A[-3::2]
    print 'print elements from the 2nd to 5th element with 2 interval,',A[1:4:2]
    print 'reverse print all elements with 2 interval,',A[::-2]
    print 'reverse print elements from the 4th element with 2 interval,',A[3::-2]
    print 'reverse print elements from the last 4th element with 2 interval,',A[-3::-2]
    #print A[a:b:c]: a and b determine range of slide. c determine the interval and direction (forth or reverse)
    print A[:-3:-1]
    print A[:3:1]
    print A[:3:-1]
    print A[:-3:1]
    print A[-3::-1]
    C=A[::-1]
    C[0]=10
    print 'A is also changed as how does c change,',A
    B[9]=0
    print 'A will not be affected when B change,',A
    print 'array slide from second element to the last one,',A[1:]
    print 'array slide from last second element to the first one,',A[:-1]



if __name__ == "__main__":
    main()