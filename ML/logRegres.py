import sys
from numpy import *


def loadDataSet():
    dataMat = []; labelMat = []
    fr = open(r'F:\PY\data\testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMatIn,lableMatIn):
    dataMatrix = mat(dataMatIn)
    labelMat = mat(lableMatIn).transpose()
    m,n =shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weight = ones((n,1))
    for k in range(maxCycles):
        h=sigmoid(dataMatrix*weight)
        error = (labelMat - h)
        weight = weight + alpha * dataMatrix.transpose()*error
    return weight


def ploatBestFit(wei):
    import matplotlib.pyplot as plt
    #wei=weight.getA() #Return self as an ndarray object.
    dataMat,labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []; ycord1 =[]
    xcord2 = []; ycord2 = []
    for i in range(n):
        if int(labelMat[i])==1:
            xcord1.append(dataArr[i,1]); ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]); ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x= arange(-3.0,3.0,0.1)
    y=(-wei[0]-wei[1]*x)/wei[2]
    ax.plot(x,y)
    plt.xlabel('X1'); plt.ylabel('X2')
    plt.show()

def stocGradAscent0(dataMatrix,classLabels):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    weightsHistory=zeros((500*m,n))
    for j in range(500):
        for i in range(m):
            h = sigmoid(sum(dataMatrix[i]*weights))
            error = classLabels[i] - h
            weights = weights + alpha * error * dataMatrix[i]
            weightsHistory[j*m + i,:] = weights
    return weights,weightsHistory

def stocGradAscent1(dataMatrix,classLabels,numIter=40):
    m,n = shape(dataMatrix)
    alpha = 0.4
    weights = ones(n)
    weightsHistory=zeros((numIter*m,n))
    for j in range(numIter):
        dataIndex = range(m)
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.01
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabels[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            weightsHistory[j*m + i,:] = weights
            del(dataIndex[randIndex])
    return weights,weightsHistory

def performanceCheck():
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    dataMat,labelMat=loadDataSet()
    dataArr = array(dataMat)
    dataArr = array(dataMat)
    weight,myHist = stocGradAscent0(dataArr,labelMat)
    weight,myHist2 = stocGradAscent1(dataArr,labelMat)
    n = shape(dataArr)[0] #number of points to create
    xcord1 = []; ycord1 = []
    xcord2 = []; ycord2 = []

    markers =[]
    colors =[]

    fig = plt.figure()
    ax = fig.add_subplot(311)
    type1 = ax.plot(myHist[:,0])
    #type2= ax.plot(myHist2[:,0],c='red')
    plt.ylabel('X0')
    ax = fig.add_subplot(312)
    type1 = ax.plot(myHist[:,1])
    #type2= ax.plot(myHist2[:,1],c='red')
    plt.ylabel('X1')
    ax = fig.add_subplot(313)
    type1 = ax.plot(myHist[:,2])
    #type2= ax.plot(myHist2[:,2],c='red')
    plt.xlabel('iteration')
    plt.ylabel('X2')
    plt.show()

def classifyVector(inX,weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest():
    frTrain = open(r'F:\PY\data\horseColicTraining.txt')
    frTest = open(r'F:\PY\data\horseColicTest.txt')
    trainingSet = []; trainingLabels =[]
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights,myhist = stocGradAscent1(array(trainingSet),trainingLabels,500)
    errorCount = 0; numTestVec =0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr),trainWeights))!= int(currLine[21]):
            errorCount +=1
    errorRate = (float(errorCount)/numTestVec)
    print "the error rate of this test is : %f" % errorRate
    return errorRate

def multiTest():
    numTests=10; errorSum=0.0
    for k in range(numTests):
        errorSum +=colicTest()
    print "after %d iterations the average error rate is: %f" % (numTests,errorSum/float(numTests))



def main():
    dataArr,lableMat=loadDataSet()
    #weight,weighthist = stocGradAscent1(array(dataArr),lableMat)
    #weight = gradAscent(dataArr,lableMat)
    #ploatBestFit(weight)
    #performanceCheck()
    multiTest()

if __name__ == "__main__":
    main()