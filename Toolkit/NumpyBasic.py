import numpy as np
import sys

def dTypeTest():
    #Using dictionaries. Two fields named ‘gender’ and ‘age’:
    student=np.dtype({'names':['name', 'age', 'weight'],'formats':['S32', 'i','f']}, align=True)
    a=np.array([('zhang',65,123.5),('wang',23,122.5)],dtype=student)
    print a
    #Using array-scalar type:
    a=np.array([1,2],dtype=np.dtype(np.int16))
    print a

    #Structured type, one field name 'f1', containing int16:
    #a=np.array([1,2],dtype=np.dtype([('f1', np.int16)]))
    #http://docs.scipy.org/doc/numpy/reference/generated/numpy.dtype.html
    #http://numpy-discussion.10968.n7.nabble.com/Structured-array-inititialization-weirdness-td23335.html
    a=np.array([1,2]).view(np.dtype([('f1', np.int16)])) 
    print a
    a=np.array([1,2]).view(np.dtype([('f1', np.int32)])) 
    print a
    a=np.array([(1,),(2,)],dtype=np.dtype([('f1', np.int16)]))
    print a
    #below two lines of code is not working as [1,2] is not a list of tuple
    #a=np.array([1,2],dtype=np.dtype([('f1', np.int16)]))
    #a=np.array([(1),(2,)],dtype=np.dtype([('f1', np.int16)]))

    #Structured type, one field named ‘f1’, in itself containing a structured type with one field:
    dt=np.dtype([('f1', [('f1', np.int32)])])
    a=np.array([1,2]).view(dt) 
    print a
    a=np.array([((1,),),((2,),)],dtype=dt)
    print a
    #below two lines of code is not working as (1,) is not same as the structure of dtype declared
    #a=np.array([(1,),(2,)],dtype=dt)

    #Structured type, two fields: the first field contains an unsigned int, the second an int32
    dt=np.dtype([('f1', np.uint), ('f2', np.int32)])
    a=np.array([(1,2),(3,4)],dtype=dt)
    print a

    #Using array-protocol type strings:
    dt=np.dtype([('a','f8'),('b','S10')])
    a=np.array([(3.14,'pi'),(2.17,'e')],dtype=dt)
    print a

    #Using comma-separated field formats. The shape is (2,3):
    dt=np.dtype("i4, (2,3)f8")
    a=np.array([(1,[[1,2,3],[4,5,6]]),(2,[[4,5,6],[1,2,3]])],dtype=dt)
    print a

    #Using tuples. int is a fixed type, 3 the field’s shape. void is a flexible type, here of size 10
    dt=np.dtype([('hello',(np.int,3)),('world',np.void,10)])
    a=np.array([([1,2,3],'this is a')],dtype=dt)
    print a

def main():
    dTypeTest()

if __name__ == "__main__":
    main()