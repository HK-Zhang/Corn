import matplotlib.pyplot as plt
import numpy as np
import dateutil.parser as dparser
from pylab import *
import mlpy
from mlpy import KernelRidge
import sys
import operator


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

    targetValues = np.genfromtxt('F:\PY\data\stock.txt',
                         skip_header=1,
                         dtype=None,
                         delimiter='\t',
                         usecols=(1))
    mse = {}
    for i in range(20,50):
        trainingPoints = np.arange(i-1).reshape(-1, 1)
        testPoints = np.arange(i).reshape(-1, 1)

        #training kernel matrix
        knl = mlpy.kernel_gaussian(trainingPoints, trainingPoints, sigma=1)
        #testing kernel matrix
        knlTest = mlpy.kernel_gaussian(testPoints, trainingPoints, sigma=1)

        knlRidge = KernelRidge(lmb=0.01, kernel=None)
        err=0
        for j in range(1,6):
            knlRidge.learn(knl, targetValues[-(i+j-1):-j])
            resultPoints = knlRidge.pred(knlTest)
            err += (resultPoints[-1]-targetValues[-j])**2
            print i,resultPoints[-1],targetValues[-j]
        mse[i] = square(err/5)
        print mse[i]
    sortedMse = sorted(mse.iteritems(),key=operator.itemgetter(1),reverse=False)
    print sortedMse[0]

def KRRTest():
    np.random.seed(10)

    targetValues = np.genfromtxt('F:\PY\data\stock.txt',
                         skip_header=1,
                         dtype=None,
                         delimiter='\t',
                         usecols=(1))

    trainingPoints = np.arange(46).reshape(-1, 1)
    testPoints = np.arange(47).reshape(-1, 1)

    #training kernel matrix
    knl = mlpy.kernel_gaussian(trainingPoints, trainingPoints, sigma=1)
    #testing kernel matrix
    knlTest = mlpy.kernel_gaussian(testPoints, trainingPoints, sigma=1)

    knlRidge = KernelRidge(lmb=0.01, kernel=None)
    knlRidge.learn(knl, targetValues[-46:])
    resultPoints = knlRidge.pred(knlTest)

    print targetValues.size, resultPoints

    fig = plt.figure(1)
    plot1 = plt.plot(trainingPoints, targetValues[-46:], 'o')
    plot2 = plt.plot(testPoints, resultPoints)
    plt.show()

def KRRProTy():
    np.random.seed(10)

    targetValues = np.genfromtxt('F:\PY\data\stockPT.txt',
                         skip_header=1,
                         dtype=None,
                         delimiter='\t',
                         usecols=(1))

    trainingPoints = np.arange(targetValues.size).reshape(-1, 1)
    testPoints = np.arange(targetValues.size+1).reshape(-1, 1)

    #training kernel matrix
    knl = mlpy.kernel_gaussian(trainingPoints, trainingPoints, sigma=1)
    #testing kernel matrix
    knlTest = mlpy.kernel_gaussian(testPoints, trainingPoints, sigma=1)

    knlRidge = KernelRidge(lmb=0.01, kernel=None)
    knlRidge.learn(knl, targetValues)
    resultPoints = knlRidge.pred(knlTest)

    print targetValues.size, resultPoints

    fig = plt.figure(1)
    plot1 = plt.plot(trainingPoints, targetValues, 'o')
    plot2 = plt.plot(testPoints, resultPoints)
    plt.show()

def SmoothKRR():
    y = np.genfromtxt('F:\PY\data\stock.txt',
                         skip_header=1,
                         dtype=None,
                         delimiter='\t',
                         usecols=(1))


    targetValues = smooth(y, len(y))


    np.random.seed(10)

    trainingPoints = np.arange(28).reshape(-1, 1)
    testPoints = np.arange(29).reshape(-1, 1)


    knl = mlpy.kernel_gaussian(trainingPoints, trainingPoints, sigma=1)
    knlTest = mlpy.kernel_gaussian(testPoints, trainingPoints, sigma=1)

    knlRidge = mlpy.KernelRidge(lmb=0.01, kernel=None)
    knlRidge.learn(knl, targetValues)
    resultPoints = knlRidge.pred(knlTest)

    print resultPoints


    plt.step(trainingPoints, targetValues, 'o')
    plt.step(testPoints, resultPoints)
    plt.show()


def main():
    #SmoothKRR()
    #KRR()
    KRRTest()
    #KRRProTy()

if __name__ == "__main__":
    main()