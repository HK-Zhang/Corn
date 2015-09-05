import matplotlib.pyplot as plt
import numpy as np
import dateutil.parser as dparser
from pylab import *
import mlpy
from mlpy import KernelRidge
import sys


def matplotlibExample():
    x = np.linspace(10, 50, 100)

    y = np.cos(x)/x

    plt.step(x, y, 'co')
    plt.show()

def smooth(x,window_len):
    
        s=np.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        w = np.hamming(window_len)

        y=np.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]
    
def smoothTS():
    x = np.genfromtxt(r'F:\PY\data\Gold.csv', dtype='object', delimiter=',', skip_header=1,
                         usecols=(0), converters = {0: dparser.parse})

    y = np.genfromtxt('F:\PY\data\Gold.csv',
                         skip_header=1,
                         dtype=None,
                         delimiter=',',
                         usecols=(1))

    y2 = smooth(y, len(y))

    print(y2)

    plt.step(x, y2)
    plt.step(x, y, 'co')
    plt.show()

def KRR():
    np.random.seed(10)

    targetValues = np.genfromtxt('F:\PY\data\Gold.csv',
                         skip_header=1,
                         dtype=None,
                         delimiter=',',
                         usecols=(1))

    trainingPoints = np.arange(125).reshape(-1, 1)
    testPoints = np.arange(126).reshape(-1, 1)

    #training kernel matrix
    knl = mlpy.kernel_gaussian(trainingPoints, trainingPoints, sigma=1)
    #testing kernel matrix
    knlTest = mlpy.kernel_gaussian(testPoints, trainingPoints, sigma=1)

    knlRidge = KernelRidge(lmb=0.01, kernel=None)
    knlRidge.learn(knl, targetValues)
    resultPoints = knlRidge.pred(knlTest)

    print(resultPoints)

    fig = plt.figure(1)
    plot1 = plt.plot(trainingPoints, targetValues, 'o')
    plot2 = plt.plot(testPoints, resultPoints)
    plt.show()

def SmoothKRR():
    y = np.genfromtxt('F:\PY\data\Gold.csv',
                         skip_header=1,
                         dtype=None,
                         delimiter=',',
                         usecols=(1))


    targetValues = smooth(y, len(y))


    np.random.seed(10)

    trainingPoints = np.arange(125).reshape(-1, 1)
    testPoints = np.arange(126).reshape(-1, 1)


    knl = mlpy.kernel_gaussian(trainingPoints, trainingPoints, sigma=1)
    knlTest = mlpy.kernel_gaussian(testPoints, trainingPoints, sigma=1)

    knlRidge = mlpy.KernelRidge(lmb=0.01, kernel=None)
    knlRidge.learn(knl, targetValues)
    resultPoints = knlRidge.pred(knlTest)

    print(resultPoints)


    plt.step(trainingPoints, targetValues, 'o')
    plt.step(testPoints, resultPoints)
    plt.show()


def main():
    SmoothKRR()

if __name__ == "__main__":
    main()