﻿from numpy import *
import matplotlib
import matplotlib.pyplot as plt

import sys

def loadDataSet(fileName, delim='\t'):
    fr = open(fileName)
    stringArr = [line.strip().split(delim) for line in fr.readlines()]
    datArr= [map(float,line) for line in stringArr]
    return mat(datArr)

def pca(dataMat,topNfeat=9999999):
    meanVals = mean(dataMat,axis=0)
    meanRemoved = dataMat - meanVals
    covMat = cov(meanRemoved,rowvar=0)
    eigVals,eigVects = linalg.eig(mat(covMat))
    eigValInd = argsort(eigVals)
    eigValInd = eigValInd[:-(topNfeat+1):-1]
    redEigVects = eigVects[:,eigValInd]
    lowDDataMat=meanRemoved*redEigVects
    reconMat=(lowDDataMat*redEigVects.T)+meanVals
    #print redEigVects
    return lowDDataMat,reconMat

def replaceNanWithMean():
    datMat=loadDataSet(r'F:\PY\data\secom.data')
    numFeat = shape(datMat)[1]
    for i in range(numFeat):
        meanVal = mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i])
        datMat[nonzero(isnan(datMat[:,i].A))[0],i]=meanVal
    return datMat

def test():
    #datMat=replaceNanWithMean()
    dataMat=loadDataSet(r'F:\PY\data\testSetPca.txt')
    lowDmat,reconMat = pca(dataMat,1)
    #print dataMat[0:5,:],lowDmat[0:5,:],reconMat[0:5,:]
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90)
    ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
    plt.show()

def main():
    test()

if __name__ == "__main__":
    main()