import matplotlib
import matplotlib.pyplot as plt
import sys
import numpy as np
import mlpy
import matplotlib.cm as cm

def getData():
    lists=[line.strip().split(',') for line in open(r'F:\PY\data\wine.txt','r').readlines()]
    return [list(l[1:14] for l in lists)],[l[0] for l in lists]

def PlotWineFeatures():
    matrix, labels = getData()
    matrix = matrix[0]
    xaxis1 = []; yaxis1 = []
    xaxis2 = []; yaxis2 = []
    xaxis3 = []; yaxis3 = []

    x = 0
    y = 1



    for n,elem in enumerate(matrix):
        if int(labels[n]) == 1:
            xaxis1.append(matrix[n][x])
            yaxis1.append(matrix[n][y])
        if int(labels[n]) == 2:
            xaxis2.append(matrix[n][x])
            yaxis2.append(matrix[n][y])
        if int(labels[n]) == 3:
            xaxis3.append(matrix[n][x])
            yaxis3.append(matrix[n][y])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    type1 = ax.scatter(xaxis1,yaxis1,s=50,c='white')
    type2 = ax.scatter(xaxis2,yaxis2,s=50,c='red')
    type3 = ax.scatter(xaxis3,yaxis3,s=50,c='darkred')

    ax.set_title('Wine Feature', fontsize=14)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.legend([type1,type2,type3],['Class 1','Class 2','Class 3'],loc=1)
    ax.grid(True,linestyle='-',color = '0.80')

    plt.show()

def pcaSvm():
    wine = np.loadtxt(r'F:\PY\data\wine.txt', delimiter=',')
    x,y = wine[:,1:4],wine[:,0].astype(np.int)
    print x.shape, y.shape

    pca=mlpy.PCA()
    pca.learn(x)

    z = pca.transform(x,k=2)
    print z.shape

    fig1 = plt.figure(1)
    title = plt.title('PCA on wine dataset')
    plot = plt.scatter(z[:,0],z[:,1],c = y, s = 90, cmap =cm.Reds)
    labx = plt.xlabel('First component')
    laby = plt.ylabel('Second component')
    plt.show()

    svm = mlpy.LibSvm(kernel_type='rbf',gamma=20)
    svm.learn(z,y)

    xmin, xmax = z[:,0].min()-0.1, z[:,0].max()+0.1
    ymin, ymax = z[:,1].min()-0.1, z[:,1].max()+0.1
    xx, yy = np.meshgrid(np.arange(xmin, xmax, 0.01), np.arange(ymin, ymax, 0.01))
    grid = np.c_[xx.ravel(), yy.ravel()]

    result = svm.pred(grid)

    fig2 = plt.figure(2)
    title = plt.title("SVM (rbf kernel) on PCA")
    plot1 = plt.pcolormesh(xx, yy, result.reshape(xx.shape), cmap = cm.Greys_r)
    plot2 = plt.scatter(z[:, 0], z[:, 1], c=y, s=90, cmap = cm.Reds)
    labx = plt.xlabel("First component")
    laby = plt.ylabel("Second component")
    limx = plt.xlim(xmin, xmax)
    limy = plt.ylim(ymin, ymax)
    plt.show()


def main():
    #PlotWineFeatures()
    pcaSvm()

if __name__ == "__main__":
    main()