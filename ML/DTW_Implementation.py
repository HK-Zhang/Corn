from PIL import Image
from numpy import array
import mlpy
from collections import OrderedDict
import sys
import os
from nt import listdir

data = {}

def classifyImg():
    fileList = [x for x in listdir(r'F:\PY\data\Img') if x.lower().endswith(".jpg")]
    m = len(fileList)
    
    for fn in range(m):
        img = Image.open(r'F:\PY\data\Img\{0}'.format(fileList[fn]))
        arr = array(img)
        list = []
        if arr.ndim==2:
            print fileList[fn]
            continue;
        for n in arr: list.append(n[0][0])
        for n in arr: list.append(n[0][1])
        for n in arr: list.append(n[0][2])
        
        data[fileList[fn]] = list
    reference = data['007_0025.jpg']
    result = {}

    for x,y in data.items():
        dist = mlpy.dtw_std(reference,y,dist_only=True)
        result[x]=dist

    sortedRes = OrderedDict(sorted(result.items(),key=lambda x:x[1]))


    for a,b in sortedRes.items():
        print("{0} - {1}".format(a,b))
        i=i+1
        if i==10:
            break




def main():
   classifyImg()


if __name__ == "__main__":
    main()