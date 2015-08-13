from PyPDF2 import PdfFileReader
from nt import listdir
import time
import sys

toolbar_width = 50

# setup toolbar
sys.stdout.write("[Start:%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

def main():
    fileList = [x for x in listdir(r'.') if x.lower().endswith(".pdf")]
    m = len(fileList)
    countImg = 0; countNimg=0
    barWidth=int(m/toolbar_width)
    barIndex=0

    for i in range(m):
        fileNameStr = fileList[i]
        inputPdf = PdfFileReader(open(fileNameStr, "rb"))
        docInfo = inputPdf.getDocumentInfo()
        if docInfo.producer != None:
            countNimg+=1
        elif docInfo.creator==None:
            countImg+=1
        else: 
            countNimg+=1

        #control toolbar
        if barWidth>0 and (i+1.0)/float(m*1.0/toolbar_width) - barIndex>=1:
            for j in range(0,int((i+1.0)/float(m*1.0/toolbar_width) - barIndex)):
                sys.stdout.write("-")
                barIndex+=1
        elif barWidth==0:
            for j in range(int((i-1)*toolbar_width/m),int(i*toolbar_width/m)):
                sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("Done]\n")
    print 'Count of image pdf files:',countImg
    print 'Count of Non image pdf files:',countNimg
    sys.stdout.write('Type q to exit program:')
    while(True):
        exit = sys.stdin.readline(1)
        print exit
        if exit=="q":
            break
        else:
            sys.stdout.write('Type q to exit program:')


main()
