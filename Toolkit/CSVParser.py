import csv
import numpy as np
import sys

def csvReader1():
    with open(r"F:\PY\data\pokemon.csv") as f:
        data = csv.reader(f)
        for line in data:
            print "id: {0},typeTwo: {1},name: {2},type: {3}".format(line[0],line[1],line[2],line[3])

def csvReader2():
    data = np.genfromtxt(r"F:\PY\data\pokemon.csv",skip_header=1,dtype=None,delimiter=',')
    print data

if __name__ == "__main__":
    csvReader2()