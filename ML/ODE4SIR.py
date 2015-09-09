import scipy
import scipy.integrate
import pylab as plt
import sys
import numpy as np

beta = 0.003
gamma = 0.1
sigma = 0.1

def SIR_model(X,t=0):
    r = scipy.array([-beta*X[0]*X[1],beta*X[0]*X[1] - gamma*X[1],gamma*X[1]])
    return r

def SIRS_model(X,t=0):
    r=scipy.array([-beta*X[0]*X[1]+sigma*X[2],beta*X[0]*X[1] - gamma*X[1],gamma*X[1]-sigma*X[2]])
    return r

def ODEModel():
    time = scipy.linspace(0,60,num = 100)
    parameters = scipy.array([255,1,0])
    #X=scipy.integrate.odeint(SIR_model,parameters,time)
    X=scipy.integrate.odeint(SIRS_model,parameters,time)
    print X

    plt.plot(range(0,100),X[:,0],'o',color = 'green',label='Susceptible')
    plt.plot(range(0,100),X[:,1],'x',color = 'red',label='Infected')
    plt.plot(range(0,100),X[:,2],'*',color = 'blue',label='Recover')
    plt.legend(loc="center right", ncol=1, shadow=True, fancybox=True)
    plt.show()

def PltRecordCAData():
    data = np.array([215,10,0,153,72,0,54,171,0,2,223,0,0,225,0,0,178,47,0,72,153,0,6,219,0,0,225,47,0,178,153,0,72,219,0,6,225,0,0])
    result = data.reshape(-1,3)
    length = len(result)
    plt.plot(range(0,length), result[:,0], marker = 'o', lw = 3, color = "green",label='Susceptible')
    plt.plot(range(0,length), result[:,1], marker = 'x', linestyle = '--',lw = 3, color = "red",label='Infected')
    plt.plot(range(0,length), result[:,2], marker = '*', linestyle = ':',lw = 3, color = "blue",label='Recover')
    plt.legend(loc="bottom", ncol=3, shadow=True, fancybox=True)
    plt.show()



def main():
    #ODEModel()
    PltRecordCAData()

if __name__ == "__main__":
    main()