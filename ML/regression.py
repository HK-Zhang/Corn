from numpy import *
import matplotlib.pyplot as plt
import sys
import random

def rssError(yArr,yHatArr):
    return ((yArr-yHatArr)**2).sum()

def regularize(xMat):#regularize by columns
    inMat = xMat.copy()
    inMeans = mean(inMat,0)   #calc mean then subtract it off
    inVar = var(inMat,0)      #calc variance of Xi then divide by it
    inMat = (inMat - inMeans)/inVar
    return inMat

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t')) - 1
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat = mat(xArr);yMat=mat(yArr).T
    xTx = xMat.T*xMat
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I*(xMat.T*yMat)
    return ws

def standRegresTest():
    xArr,yArr = loadDataSet(r'F:\PY\data\ex0.txt')
    xMat = mat(xArr);yMat=mat(yArr)
    ws = standRegres(xArr,yArr)
    yHat = xMat*ws

    print corrcoef(yHat.T,yMat)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0])

    xCopy=xMat.copy()
    xCopy.sort(0)
    yHat=xCopy*ws
    ax.plot(xCopy[:,1],yHat)

    plt.show()

def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye((m)))
    for j in range(m):                      #next 2 lines create weights matrix
        diffMat = testPoint - xMat[j,:]     #
        weights[j,j] = exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws

def lwlrTest(testArr,xArr,yArr,k=1.0):  #loops over all the data points and applies lwlr to each one
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArr[i],xArr,yArr,k)
    return yHat

def lwlrRegss():
    xArr,yArr = loadDataSet(r'F:\PY\data\ex0.txt')
    xMat = mat(xArr);yMat=mat(yArr)
    print yArr[0],lwlrTest(xMat[0],xArr,yArr,0.01)
    lwlrTestPlot(xArr,yArr,0.01)

def lwlrTestPlot(xArr,yArr,k=1.0):  #same thing as lwlrTest except it sorts X first
    yHat = zeros(shape(yArr))       #easier for plotting
    xMat = mat(xArr);yMat=mat(yArr)
    xCopy = mat(xArr)
    xCopy.sort(0)
    for i in range(shape(xArr)[0]):
        yHat[i] = lwlr(xCopy[i],xArr,yArr,k)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0])

    xCopy=xMat.copy()
    xCopy.sort(0)
    ax.plot(xCopy[:,1],yHat)

    plt.show()

def ridgeRegres(xMat,yMat,lam = 0.2):
    xTx = xMat.T*xMat
    denom = xTx + eye(shape(xMat)[1])*lam
    if linalg.det(denom) == 0.0:
        print "this matrix is singular, cannot do inverse"
        return
    ws = denom.I*(xMat.T*yMat)
    return ws

def ridgeTest(xArr,yArr):
    xMat = mat(xArr);yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat =yMat -yMean
    xMeans = mean(xMat,0)
    xVar = var(xMat,0)
    xMat = (xMat - xMeans)/xVar
    numTestpts = 30
    wMat = zeros((numTestpts,shape(xMat)[1]))
    for i in range(numTestpts):
        ws = ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

def ridgeSample():
    abX,abY = loadDataSet(r'F:\PY\data\abalone.txt')
    ridgeWeights = ridgeTest(abX,abY)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ridgeWeights)
    plt.show()

def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat = mat(xArr); yMat=mat(yArr).T
    yMean = mean(yMat,0)
    yMat = yMat - yMean
    xMat = regularize(xMat)
    m,n = shape(xMat)
    returnMat = zeros((numIt,n))
    ws=zeros((n,1)); wsTest = ws.copy(); wsMax = ws.copy()
    for i in range(numIt):
        #print ws.T
        lowestError = inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j]+=eps*sign
                yTest = xMat*wsTest
                rssE = rssError(yMat.A,yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws =wsMax.copy()
        returnMat[i,:] = ws.T
    return returnMat

def stageWiseSample():
    abX,abY = loadDataSet(r'F:\PY\data\abalone.txt')
    stageWeights = stageWise(abX,abY,0.001,5000)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(stageWeights)
    plt.show()

def abaloneSample():
    abX,abY = loadDataSet(r'F:\PY\data\abalone.txt')
    #yHat01 = lwlrTest(abX[0:99],abX[0:99],abY[0:99],0.1)
    #yHat1 = lwlrTest(abX[0:99],abX[0:99],abY[0:99],1)
    #yHat10 = lwlrTest(abX[0:99],abX[0:99],abY[0:99],10)

    yHat01 = lwlrTest(abX[100:199],abX[0:99],abY[0:99],0.1)
    yHat1 = lwlrTest(abX[100:199],abX[0:99],abY[0:99],1)
    yHat10 = lwlrTest(abX[100:199],abX[0:99],abY[0:99],10)
    print rssError(abY[100:199],yHat01.T),rssError(abY[100:199],yHat1.T),rssError(abY[100:199],yHat10.T)

    ws = standRegres(abX[0:99],abY[0:99])
    yHat = mat(abX[100:199])*ws
    print rssError(abY[100:199],yHat.T.A)

def corssbValidation(xArr,yArr,numVal=10):
    m=len(yArr)
    indexList = range(m)
    errorMat = zeros((numVal,30))
    for i in range(numVal):
        trainX=[]; trainY=[]
        testX=[]; testY=[]
        random.shuffle(indexList)
        for j in range(m):
            if j < m*0.9:
                trainX.append(xArr[indexList[j]])
                trainY.append(yArr[indexList[j]])
            else:
                testX.append(xArr[indexList[j]])
                testY.append(yArr[indexList[j]])
        wMat =ridgeTest(trainX,trainY)
        for k in range(30):
            matTestX = mat(testX); matTrainX= mat(trainX)
            meanTrain = mean(matTrainX,0)
            varTrain = var(matTrainX,0)
            matTestX = (matTestX-meanTrain)/varTrain
            yEst = matTestX * mat(wMat[k,:]).T+mean(trainY)
            errorMat[i,k]=rssError(yEst.T.A,array(testY))
    meanErrors = mean(errorMat,0)#calc avg performance of the different ridge weight vectors
    minMean = float(min(meanErrors))
    bestWeights = wMat[nonzero(meanErrors==minMean)]
    #can unregularize to get model
    #when we regularized we wrote Xreg = (x-meanX)/var(x)
    #we can now write in terms of x not Xreg:  x*w/var(x) - meanX/var(x) +meanY
    xMat = mat(xArr); yMat=mat(yArr).T
    meanX = mean(xMat,0); varX = var(xMat,0)
    unReg = bestWeights/varX
    print "the best model from Ridge Regression is:\n",unReg
    print "with constant term: ",-1*sum(multiply(meanX,unReg)) + mean(yMat)

def corssbValidationSample():
    abX,abY = loadDataSet(r'F:\PY\data\abalone.txt')
    corssbValidation(abX,abY,10)

def main():
    #standRegresTest()
    #lwlrRegss()
    #abaloneSample()
    #ridgeSample()
    #stageWiseSample()
    corssbValidationSample()
    

if __name__ == "__main__":
    main()