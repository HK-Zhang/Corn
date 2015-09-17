import sys
import nt
from nt import listdir
import datetime
import random
import csv
import shutil
import time
import os

FolderName="MissingBoxNumbers"
LogFile = r"./"+datetime.datetime.now().strftime('%y%m%d%H%M%S')+".log.csv"

def mkdir():
    isExists=os.path.exists(r"./"+FolderName)
    if not isExists:
        os.makedirs(r"./"+FolderName)

def getFileName():
    return "COL"+datetime.datetime.now().strftime('%y%m%d%H%M%S')+"_"+str(random.randint(0,1000))+".csv"

def main():
    fileList = [x for x in listdir(r'.') if (x.lower().endswith(".csv") and not(x.lower().endswith(".log.csv")))]
    missingBoxfileList = [x for x in listdir(r'.') if x.lower().endswith(".txt")]
    m = len(fileList)
    n = len(missingBoxfileList)

    missingBoxNums = []

    for i in range(n):
        boxNums=[line.strip() for line in open(missingBoxfileList[i],'rU').readlines()]
        missingBoxNums.extend(boxNums)
    missingBoxNums=set(missingBoxNums)


    with open(LogFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(('box number','old file name','new file name'))

        for i in range(m):
            boxNums=[line.strip().split(';')[11] for line in open(fileList[i],'rU').readlines()]
            boxNums = set(boxNums)
            outputMissingBox = list(missingBoxNums & boxNums)
            
            if len(outputMissingBox)>0:
                mkdir()
                print 'Missing:',fileList[i]
                newFile = getFileName()
                shutil.copyfile(fileList[i], "./"+FolderName+"/"+newFile)

                for item in outputMissingBox:
                    writer.writerow((item,fileList[i],newFile))
            else:
                print 'No Missing:',fileList[i]


if __name__ == '__main__':
    main()
    #Exit program
    time1= time.time()
    #sys.stdout.write('Type q to exit program:')
    sys.stdout.write('Task is completed and will exit after 1 min:')
    while(True):
        time2= time.time()
        if (time2-time1)>60:
            break
