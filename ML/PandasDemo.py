import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
from pandas.tools.plotting import scatter_matrix

ts = pd.read_csv(r'F:\PY\data\Gold.csv',index_col=0,parse_dates=True)

def showPlot():
    #ts.plot()
    ts["2006":"2007"].plot(color = "green")
    plt.show()

def showPlotAdv():
    ts.truncate(after = "05/30/2003")
    #ts_res = ts.resample("A")
    #ts_res.plot(style="g--")
    ts_res = ts.resample("A",how =["mean",np.max,np.min])
    #ts_res.plot(subplots=True)
    ts_res.plot()
    plt.show()


def describeDF():
    wine = pd.read_csv(r'F:\PY\data\wine.csv',sep=";")
    print wine.head()
    print wine.describe()
    scatter_matrix(wine,alpha=0.2,figsize=(6,6),diagonal='kde')
    plt.show()

def AggregateDF():
    iris = pd.read_csv(r'F:\PY\data\iris.txt',sep=",")
    g = iris.groupby('name')
    for name,group in g:
        print name
    print iris.groupby('name').sum()
    print iris.groupby('name').describe()

def analyzeData():
    iris = pd.read_csv(r'F:\PY\data\iris.txt',sep=",")
    print iris.corr(method = 'spearman')
    print iris['SL'].corr(iris['PL'])
    print iris.corr()


def main():
    #showPlot()
    #showPlotAdv()
    #describeDF()
    #AggregateDF()
    analyzeData()

if __name__ == "__main__":
    main()