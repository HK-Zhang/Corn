from numpy import *
import sys
from Tkinter import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def loadDataSet(fileName):
    dataMat = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat

def binSplitDataSet(dataSet,feature,value):
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:][0]
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:][0]
    return mat0,mat1

def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1])*shape(dataSet)[0]

def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    feat,val = chooseBestSplit(dataSet,leafType,errType,ops)
    if feat == None: return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet,feat,val)
    retTree['left'] = createTree(lSet,leafType,errType,ops)
    retTree['right'] = createTree(rSet,leafType,errType,ops)
    return retTree


def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    tolS=ops[0]; tolN = ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
        return None, leafType(dataSet)
    m,n = shape(dataSet)
    S= errType(dataSet)
    bestS= inf; bestIndex = 0; bestValue = 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if (shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN) : continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if(S-bestS)<tolS:
        return None,leafType(dataSet)
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if (shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
        return None,leafType(dataSet)
    return bestIndex,bestValue

def regTreeSample():
    myDat = loadDataSet(r'F:\PY\data\ex00.txt')
    myDat = mat(myDat)
    print createTree(myDat)

def isTree(obj):
    return (type(obj).__name__=='dict')

def getMean(tree):
    if isTree(tree['right']):tree['right']=getMean(tree['right'])
    if isTree(tree['left']):tree['left']=getMean(tree['left'])
    return (tree['right']+tree['left'])/2.0

def prune(tree,testData):
    if shape(testData)[0]==0: return getMean(tree)
    if (isTree(tree['right']) or isTree(tree['left'])):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']): tree['left']=prune(tree['left'],lSet)
    if isTree(tree['right']): tree['right']=prune(tree['right'],rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge = sum(power(lSet[:,-1]-tree['left'],2))+sum(power(rSet[:,-1]-tree['right'],2))
        treeMean = (tree['right']+tree['left'])/2.0
        errorMerge = sum(power(testData[:,-1]-treeMean,2))
        if errorMerge < errorNoMerge:
            print "merging"
            return treeMean
        else: return tree
    else: return tree

def pruneSample():
    myDat = loadDataSet(r'F:\PY\data\ex2.txt')
    myDat = mat(myDat)
    myTree=createTree(myDat)
    myDatTest = loadDataSet(r'F:\PY\data\ex2test.txt')
    myDatTest = mat(myDatTest)
    myTree2 = prune(myTree,myDatTest)
    print myTree2

def linearSolve(dataSet):
    m,n=shape(dataSet)
    X = mat(ones((m,n))); Y=mat(ones((m,1)))
    X[:,1:n]=dataSet[:,0:n-1];Y=dataSet[:,-1]
    xTx = X.T*X
    if linalg.det(xTx) ==0.0:
        raise NameError('This mateix is singular, cannot do inverse, try increasing the second value of ops')
    ws = xTx.I*(X.T*Y)
    return ws,X,Y

def modelLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X*ws
    return sum(power(Y-yHat,2))

def regTreeEval(model,inDat):
    return float(model)

def modelTreeEval(model,inDat):
    n=shape(inDat)[1]
    X=mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

def treeForeCast(tree,inData,modelEval=regTreeEval):
    if not isTree(tree): return modelEval(tree,inData)
    if inData[tree['spInd']]>tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData,modelEval)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData,modelEval)
        else:
            return modelEval(tree['right'],inData)

def createForecast(tree,testData,modelEval=regTreeEval):
    m=len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat


def regTreeSample():
    myDat = loadDataSet(r'F:\PY\data\ex2.txt')
    myDat = mat(myDat)
    myTree=createTree(myDat,modelLeaf,modelErr,(1,10))
    print myTree


def modelRegTree():
    trainmat=mat(loadDataSet(r'F:\PY\data\bikeSpeedVsIq_train.txt'))
    testmat=mat(loadDataSet(r'F:\PY\data\bikeSpeedVsIq_test.txt'))
    mytree= createTree(trainmat,ops=(1,20))
    yHat=createForecast(mytree,testmat[:,0])
    print corrcoef(yHat,testmat[:,1],rowvar=0)[0,1]

    mytree= createTree(trainmat,modelLeaf,modelErr,ops=(1,20))
    yHat=createForecast(mytree,testmat[:,0],modelTreeEval)
    print corrcoef(yHat,testmat[:,1],rowvar=0)[0,1]


def guiTest(): 
    def reDraw(tolS,tolN):
        reDraw.f.clf()        # clear the figure
        reDraw.a = reDraw.f.add_subplot(111)
        if chkBtnVar.get():
            if tolN < 2: tolN = 2
            myTree=createTree(reDraw.rawDat, modelLeaf,modelErr, (tolS,tolN))
            yHat = createForecast(myTree, reDraw.testDat, modelTreeEval)
        else:
            myTree=createTree(reDraw.rawDat, ops=(tolS,tolN))
            yHat = createForecast(myTree, reDraw.testDat)
        reDraw.a.scatter(reDraw.rawDat[:,0], reDraw.rawDat[:,1], s=5) #use scatter for data set
        reDraw.a.plot(reDraw.testDat, yHat, linewidth=2.0) #use plot for yHat
        reDraw.canvas.show()
    
    def getInputs():
        try: tolN = int(tolNentry.get())
        except: 
            tolN = 10 
            print "enter Integer for tolN"
            tolNentry.delete(0, END)
            tolNentry.insert(0,'10')
        try: tolS = float(tolSentry.get())
        except: 
            tolS = 1.0 
            print "enter Float for tolS"
            tolSentry.delete(0, END)
            tolSentry.insert(0,'1.0')
        return tolN,tolS

    def drawNewTree():
        tolN,tolS = getInputs()#get values from Entry boxes
        reDraw(tolS,tolN)

    root=Tk()

    reDraw.f = Figure(figsize=(5,4), dpi=100) #create canvas
    reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
    reDraw.canvas.show()
    reDraw.canvas.get_tk_widget().grid(row=0, columnspan=3)

    Label(root, text="tolN").grid(row=1, column=0)
    tolNentry = Entry(root)
    tolNentry.grid(row=1, column=1)
    tolNentry.insert(0,'10')
    Label(root, text="tolS").grid(row=2, column=0)
    tolSentry = Entry(root)
    tolSentry.grid(row=2, column=1)
    tolSentry.insert(0,'1.0')
    Button(root, text="ReDraw", command=drawNewTree).grid(row=1, column=2, rowspan=3)
    chkBtnVar = IntVar()
    chkBtn = Checkbutton(root, text="Model Tree", variable = chkBtnVar)
    chkBtn.grid(row=3, column=0, columnspan=2)

    reDraw.rawDat=mat(loadDataSet(r'F:\PY\data\bikeSpeedVsIq_train.txt'))
    reDraw.testDat=mat(loadDataSet(r'F:\PY\data\bikeSpeedVsIq_test.txt'))[:,0]

    #reDraw.rawDat = mat(loadDataSet(r'F:\PY\data\sine.txt'))
    #reDraw.testDat = arange(min(reDraw.rawDat[:,0]),max(reDraw.rawDat[:,0]),0.01)
    reDraw(1.0, 10)
               
    root.mainloop()

def main():
    #regTreeSample()
    #pruneSample()
    #regTreeSample()
    #modelRegTree()
    guiTest()

if __name__ == "__main__":
    main()