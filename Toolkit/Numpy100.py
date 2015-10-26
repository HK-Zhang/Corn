import numpy as np
import sys
import scipy
import scipy.spatial
from numpy.lib import stride_tricks

def showVersion():
    """Print the Numpy Version and Confingue"""
    print(np.__version__)
    np.__config__.show()

def creatNullVector():
    """Create a null vector of size 10 """
    z=np.zeros(10)
    z[5]=1
    print z

def createVectorRange():
    """Create a vector with values ranging from 10 to 49"""
    z=np.arange(10,50)
    print z

def createMatrix():
    """Create a 3*3 matrix with values ranging from 0 to 8"""
    z=np.arange(9).reshape(3,3)
    print z

def findIndicsNonZero():
    """find indics of non-zero element from a vector"""
    z=np.nonzero([0,1,2,0,4,0])
    print z

def createIdentityMatrix():
    """Create a 3*3 identity matrix"""
    z=np.eye(3)
    print z

def createMatrixDiagonal():
    """Create 5*5 matrix with values 1,2,3,4 just below the diagonal"""
    z=np.diag(1+np.arange(4),k=-1)
    print z

def createRandomArray():
    """Create a 3*3*3 array with random values"""
    z=np.random.random((3,3,3))
    print z

def createCheckerBoardMatrix():
    """Create a 8*8 matrix and fill it with a checkerboard pattern"""
    z=np.zeros((8,8),dtype=int)
    z[1::2,::2]=1
    z[::2,1::2]=1
    print z

def maxOfArray():
    """Create a 10*10 array with random values and find the maximum and minimum value"""
    z=np.random.random((10,10))
    zmax,zmin=z.max(),z.min()
    print zmax,zmin

def createMaxWithTile():
    """Create a checkerboard 8*8 matrix using tile function"""
    z=np.tile(np.array([[1,0],[0,1]]),(4,4))
    print z

def mormalizeMatrixMaxMin():
    """Normalize matrix with max-min approach"""
    z=np.random.random((10,10))
    zmax,zmin=z.max(),z.min()
    z=(z-zmin)/(zmax-zmin)
    print z

def realMatrixProduct():
    """multiply a 5*3 matrix by a 3*2 matrix("""
    z=np.dot(np.ones((5,3)),np.ones((3,2)))
    print z

def creatMatrixwithRawValue():
    """Create a 5*5 matrix with raw values ranging from 0 to 4"""
    z = np.zeros((5,5)) 
    z+=np.arange(5)
    print z

def createArrayByLinespace():
    """Create a vector of size 10 with raw value ranging from 0 to 1, both excluded"""
    z=np.linspace(0,1,12,endpoint=True)[1:-1]
    print z

def sortArray():
    """Create a random vector of size 10 and sort it"""
    z = np.random.random(10)
    z.sort()
    print z

def compareArray():
    """Consider two random array A and B. check if they are equal"""
    z1 = np.random.randint(0,2,5)
    z2 = np.random.randint(0,2,5)
    z= np.allclose(z1,z2)
    print z

def arrayMean():
    """Create a random vector of size 30 and find mean value"""
    z=np.random.random(30)
    m=z.mean()
    print m

def createImmutableArray():
    """Make a array immutable"""
    z=np.zeros(10)
    z.flags.writeable = False
    z[0]=1
    print z

def convertCoordinates():
    """Create a random 10*2 matrix representing cartesian coordinates, and convert them to polar coordinate"""
    z= np.random.random((10,2))
    x=z[:,0]
    y=z[:,1]
    z1 = np.sqrt(x**2+y**2)
    z2= np.arctan2(x,y)
    print z1,z2

def replaceMaxInArray():
    """create a random array of size 10 and replace the max vlaue by 0"""
    z = np.random.random(10)
    z[z.argmax()] = 0
    print z

def createStructuredArray():
    """create a structured array with x and y coordinate"""
    z = np.zeros((10,10),[('x',float),('y',float)])
    z['x'],z['y'] = np.meshgrid(np.linspace(0,1,10),np.linspace(0,1,10))
    print z


def scalaTypeValue():
    """Print the minimum and maximun represntable value for each numpy scalar type"""
    for dtype in [np.int8,np.int32,np.int64]:
        print np.iinfo(dtype).min,np.iinfo(dtype).max

    for dtype in [np.float32,np.float64]:
        print np.finfo(dtype).min,np.finfo(dtype).max

def createStructuredArray():
    """Create a strucured array representing position(x,y) and color(r,g,b)"""
    z = np.zeros(10,[('position',[('x',float,1),('y',float,1)]),('color',[('r',float,1),('g',float,1),('b',float,1)])])
    print z

def calP2PDist():
    """Consider a random vector with shape(10,2) coordinate. find point to point distance """
    z=np.random.random((10,2))
    x,y=np.atleast_2d(z[:,0]),np.atleast_2d(z[:,1])
    D=np.sqrt((x-x.T)**2+(y-y.T)**2)
    D=scipy.spatial.distance.cdist(z,z)
    print D

def createGaussianArray():
    """Generate a generic 2 D Gaussian like array"""
    X,Y = np.meshgrid(np.linspace(-1,1,10),np.linspace(-1,1,10))
    D=np.sqrt(X*X+Y*Y)
    sigma,mu=1.0,0.0
    G = np.exp(-( (D-mu)**2 / ( 2.0 * sigma**2 ) ) )
    print G

def subtractMeanOfEachRow():
    """subtract mean of each row of matrix"""
    x=np.random.rand(5,10)
    z=x-x.mean(axis=1,keepdims=True)
    z=x-x.mean(axis=1).reshape(-1,1)
    print z

def findNullColsof2DArray():
    """Tell if a 2D array has null column"""
    z = np.random.randint(0,3,(3,10))
    print (~z.any(axis=0)).any()

def findNearestValueInArray():
    """find the nearest value from a given value in a array"""
    Z=np.random.uniform(0,1,10)
    z=0.5
    m=Z[np.abs(Z-z).argmin()]
    print m

def readingFile():
    Z=np.genfromtxt('F:\PY\data\missing.txt',delimiter=',')
    print Z

def generate():
    for x in xrange(10):
        yield x

def createArrayFromIter():
    """Consider a generator function generate 10 integers and use it to build an array"""
    Z=np.fromiter(generate(),dtype=float,count=-1)
    print Z

def accumulateVactor():
    """Accumulate elements of array A to Array F based on an index list"""
    X=[1,2,3,4,5,6]
    I=[1,3,9,4,3,1]
    F=np.bincount(I,X)
    print F

def calculateUniqueColor():
    """Consider a image(m,h,3). compute the number of unique color"""
    m,h=16,16
    I=np.random.randint(0,2,(m,h,3)).astype(np.ubyte)
    F = I[...,0]*256*256 + I[...,1]*256 +I[...,2]
    n=len(np.unique(F))
    print n

def sumLastTwoIndexFourDArray():
    """Consider a four dimensions array, how to get a sum over the last two index at once"""
    A=np.random.randint(0,10,(3,4,3,4))
    sum = A.reshape(A.shape[:-2]+(-1,)).sum(axis=-1)
    print sum

def getMeanOfSubset():
    """Considering a one-dimensional vector D, how to compute means of subsets of D using a vector S of same size describing subset indices """
    D=np.random.uniform(0,1,100)
    S=np.random.randint(0,10,100)
    D_Sum=np.bincount(S,D)
    D_Count=np.bincount(S)
    D_Mean=D_Sum/D_Count
    print D_Mean

def getDiagonalOdDotProduct():
    """get the diagonal of a dot product """
    A=np.ones((3,3))
    B=np.ones((3,3))
    #slow
    print np.diag(np.dot(A,B))
    #fast
    print np.sum(A * B.T, axis=1)
    print np.einsum("ij,ji->i", A, B)

def createVectorWithConsecutiveZeros():
    """Consider a vector and build a new vector with consecutive zeros interleaved between each value"""
    z=np.array([1,2,3,4,5])
    nz=3
    z0=np.zeros(len(z)+(len(z)-1)*nz)
    z0[::nz+1]=z
    print z0


def swapRowsOfArray():
    """swap two rows of an array"""
    A=np.arange(25).reshape(5,5)
    A[[0.,1]]=A[[1,0]]
    print A

def stridTrick():
    """Consider a one-dimensional array Z, build a two-dimensional array whose first row is (Z[0],Z[1],Z[2]) and each subsequent row is shifted by 1 """
    A=np.arange(10)
    window =3
    shape=(A.size-window+1,window)
    strides=(A.itemsize,A.itemsize)
    Z=stride_tricks.as_strided(A,shape=shape,strides=strides)
    print Z
    
def Fun1():
    """Given an array C that is a bincount, how to produce an array A such that np.bincount(A) == C """
    C=np.bincount([1,1,2,3,4,4,6])
    A = np.repeat(np.arange(len(C)), C)
    print A

def moving_average(a,n):
    ret=np.cumsum(a,dtype=float)
    ret[n:]=ret[n:]-ret[:-n]
    return ret[n-1:]/n

def Fun2():
    """Compute average using a slide window over an array"""
    A=np.arange(25)
    print moving_average(A,3)

def negateVal():
    """negate a boolean, change the sign of a float inplace"""
    Z=np.random.randint(0,2,100)
    np.logical_not(Z,out=Z)
    print Z
    W=np.random.uniform(-1.0,1.0,100)
    np.negative(Z,out=Z)
    print Z

def ectractUnequalVal():
    """Consider a 10*3 matrix. extract rows with unequal values"""
    Z = np.random.randint(0,5,(10,3))
    E = np.logical_and.reduce(Z[:,1:] == Z[:,:-1], axis=1)
    U = Z[~E]
    print(Z)
    print(U)


def extractUniqueRow():
    """Given a two dimensional array, how to extract unique rows """
    Z=np.random.randint(0,2,(6,3))
    T = np.ascontiguousarray(Z).view(np.dtype((np.void, Z.dtype.itemsize * Z.shape[1])))
    _, idx = np.unique(T, return_index=True)
    uZ = Z[idx]
    print Z,uZ


def main():
    extractUniqueRow()

if __name__ == "__main__":
    main()