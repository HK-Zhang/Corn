import scipy as sp
import numpy as np
import sys

def Example1():
    a = sp.array([[1,2,3],[4,5,6]])
    b = sp.array([i*i for i in range(100) if i%2==1])
    c = b.tolist()
    print a,b,c

    a = sp.zeros(100)                      # a 100-element array of float zeros
    b = sp.zeros((2,8), int)               # a 2x8 array of int zeros
    c = sp.zeros((2,2,2), complex)         # a NxMxL array of complex zeros
    print a,b,c

    a = sp.ones(10, int)                   # a 10-element array of int ones
    b = sp.pi * sp.ones((5,5))          # a useful way to fill up an array with a specified value
    print a,b

    id = sp.eye(10,10, dtype=int)                           # 10x10 identity matrix (1's on diagonal)
    offdiag = sp.eye(10,10,1)+sp.eye(10,10,-1)     # off diagonal elements = 1
    print id,offdiag

    a = sp.array([[1,2,3],[4,5,6]])
    b = sp.transpose(a)                    # reverse dimensions of a (even for dim > 2)
    b = a.T                                   # equivalent to scipy.transpose(a)
    c = sp.swapaxes(a, 0, 1)       # swap specified axes
    print a,b,c

    a = sp.arange(1, 10, 1)      # like Python range, but with (potentially) real-valued arrays
    b = sp.linspace(1, 10, 11) # create array of equally-spaced points based on specifed number of points
    print a,b

    a = sp.random.random((100,100))        # 100x100 array of floats uniform on [0.,1.)
    b = sp.random.randint(0,10, (100,))    # 100 random ints uniform on [0, 10), i.e., not including the upper bound 10
    c = sp.random.standard_normal((5,5,5)) # zero-mean, unit-variance Gaussian random numbers in a 5x5x5 array
    print a,b,c

    elem = c[1,1,1]       # equiv. to a[i][j][k] but presumably more efficient
    print elem

    i = sp.array([0,1,2,1])                     # array of indices for the first axis
    j = sp.array([1,2,3,4])                     # array of indices for the second axis
    print a[i,j]                                         # return array([a[0,1], a[1,2], a[2,3], a[1,4]])
    c = sp.linspace(1, 10, 11)
    b = sp.array([True, False, True, False])
    print c[b]    
    last_elem = c[-1]     # the last element of the array
    print last_elem

    section = a[10:20, 30:40]         # 10x10 subblock starting at [10,30]
    print section

    asection = a[10:, 30:]            # missing stop index implies until end of array
    bsection = a[:10, :30]            # missing start index implies until start of array
    print asection,bsection

    x = a[:, 0]                       # get everything in the 0th column (missing start and stop)
    y = a[:, 1]                       # get everything in the 1st column
    print x,y

    s  = sp.sum(a)             # sum all elements in a, returning a scalar
    s0 = sp.sum(a, axis=0)     # sum elements along specified axis (=0), returning an array of remaining shape, e.g.,
    a  = sp.ones((10,20,30))
    a0 = sp.sum(a, axis=0)     # s0 has shape (20,30)
    print s,s0,a,a0

    a = sp.array([[1,2,3],[4,5,6]])
    m = sp.mean(a, axis=0)       # compute mean along the specified axis (over entire array if axis=None)
    s = sp.std(a, axis=0)        # compute standard deviation along the specified axis (over entire array if axis=None)
    print m,s

    s0 = sp.cumsum(a, axis=0)  # cumulatively sum over 0 axis, returning array with same shape as a
    s1 = sp.cumsum(a)          # cumulatively sum over 0 axis, returning 1D array of length shape[0]*shape[1]*...*shape[dim-1]
    print s0,s1

def Example2():
    a = sp.array([[-1,2,3],[4,-5,0]])
    print a
    #scipy.any(a): return True if any element of a is True 
    #scipy.all(a): return True if all elements of a are True 
    #scipy.alltrue(a, axis): perform logical_and along given axis of a 
    print sp.any(a),sp.all(a),sp.alltrue(a,axis=0),sp.alltrue(a,axis=1)
    #scipy.append(a, values, axis): append values to a along specified axis 
    print sp.append(a,[[7,8,9],[10,11,12]]),sp.append(a,[[7,8,9],[10,11,12]],axis=0),sp.append(a,[[7,8,9],[10,11,12]],axis=1)
    #scipy.concatenate((a1, a2, ...), axis): concatenate tuple of arrays along specified axis 
    print sp.concatenate((a,[[7,8,9],[10,11,12]])),sp.concatenate((a,[[7,8,9],[10,11,12]]),axis=0),sp.concatenate((a,[[7,8,9],[10,11,12]]),axis=1)
    #scipy.min(a, axis=None), scipy.max(a, axis=None): get min/max values of a along specified axis (global min/max if axis=None) 
    print np.min(a),np.max(a)
    #scipy.argmin(a, axis=None), scipy.argmax(a, axis=None): get indices of min/max of a along specified axis (global min/max if axis=None) 
    print sp.argmin(a),sp.argmin(a,axis=0),sp.argmin(a,axis=1)
    print sp.argmax(a),sp.argmax(a,axis=0),sp.argmax(a,axis=1)
    #scipy.reshape(a, newshape): reshape a to newshape (must conserve total number of elements)
    b=sp.reshape(a,(3,2)) 
    print b
    #scipy.matrix(a): create matrix from 2D array a (matrices implement matrix multiplication rather than element-wise multiplication) 
    m=sp.matrix(a)
    print m
    #scipy.histogram, scipy.histogram2d, scipy.histogramdd: 1-dimensional, 2-dimensional, and d-dimensional histograms, respectively 
    print sp.histogram([1, 2, 1], bins=[0, 1, 2, 3])
    print sp.histogram([[1, 2, 1], [1, 0, 1]], bins=[0,1,2,3])
    #scipy.round(a, decimals=0): round elements of matrix a to specified number of decimals 
    c=sp.array([[1.1,2.2,3.3],[4.5,6.6,6.7]])
    print np.round(c,decimals=0)
    #scipy.sign(a): return array of same shape as a, with -1 where a < 0, 0 where a = 0, and +1 where a > 0 
    print sp.sign(a)
    #a.tofile(fid, sep="", format="%s"): write a to specified file (fid), in either binary or ascii format depending on options 
    #scipy.fromfile(file=, dtype=float, count=-1, sep=''): read array from specified file (binary or ascii) 
    #scipy.unique(a): return sorted unique elements of array a 
    print sp.unique(a)
    #scipy.where(condition, x, y): return array with same shape as condition, where values from x are inserted in positions where condition is True, and values from y where condition is False 
    print sp.where([[2,3,4],[0,0,0]],1,-1)

def main():
    Example2()

if __name__ == "__main__":
    main()