from PyPDF2 import PdfFileReader
from nt import listdir
import os
import time
import sys
import shutil

toolbar_width = 50

# setup progress bar
sys.stdout.write("[Start:%s]" % (" " * toolbar_width))
sys.stdout.flush()
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

def main():
    fileList = [x for x in listdir(r'.') if x.lower().endswith(".pdf")]
    m = len(fileList)
    lstPdfImg=[];lstPdfText=[];lsfPdfErr=[]
    barWidth=int(m/toolbar_width)
    barIndex=0

    for i in range(m):
        fileNameStr = fileList[i]
        f=open(fileNameStr, "rb")
        inputPdf = PdfFileReader(f)

        Identified = False
        try:
            for page in inputPdf.pages:
                if Identified == True:
                    break

                r=page['/Resources']['/ProcSet']

                for i in range(len(r)):
                    if r[i]=="/Text":
                        Identified = True
                        break
        
            if Identified == True:
                lstPdfText.append(fileNameStr)
            else:
                lstPdfImg.append(fileNameStr)
        except:
            lsfPdfErr.append(fileNameStr)

        f.close()
           
        #control progress bar
        if barWidth>0 and (i+1.0)/float(m*1.0/toolbar_width) - barIndex>=1:
            for j in range(0,int((i+1.0)/float(m*1.0/toolbar_width) - barIndex)):
                sys.stdout.write("-")
                barIndex+=1
        elif barWidth==0:
            for j in range(int((i-1)*toolbar_width/m),int(i*toolbar_width/m)):
                sys.stdout.write("-")
        sys.stdout.flush()

    #output result
    file_object = open('Text_List.txt', 'w')
    for x in lstPdfText:
        file_object.writelines(x+'\n')
        if not os.path.exists(r'./TxtBasedPDF/'+x):
            os.rename('./'+x, './TxtBasedPDF/'+x) 
    file_object.close( )

    file_object = open('Img_List.txt', 'w')
    for x in lstPdfImg:
        file_object.writelines(x+'\n')
        if not os.path.exists(r'./ImgBasedPDF/'+x):
            os.rename('./'+x, './ImgBasedPDF/'+x) 
    file_object.close( )

    file_object = open('Err_List.txt', 'w')
    for x in lsfPdfErr:
        file_object.writelines(x+'\n')
        if not os.path.exists(r'./ErrorPDF/'+x):
            os.rename('./'+x, './ErrorPDF/'+x) 
    file_object.close( )

    sys.stdout.write("Done]\n")
    print 'Total pdf files:',len(fileList)
    print 'Image pdf files:',len(lstPdfImg)
    print 'Not only image pdf files:',len(lstPdfText)
    print 'Fail to read pdf files:',len(lsfPdfErr)

    file_object = open('Summary.txt', 'w')
    file_object.writelines('Total pdf files: %d \n' % len(fileList))
    file_object.writelines('Image pdf files:%d \n' % len(lstPdfImg))
    file_object.writelines('Not only image pdf files:%d \n' % len(lstPdfText))
    file_object.writelines('Fail to read pdf files:%d \n' % len(lsfPdfErr))
    file_object.close()

#steup folders
isExists=os.path.exists(r'.\ImgBasedPDF')
if not isExists:
    os.makedirs(r'.\ImgBasedPDF')

isExists=os.path.exists(r'.\TxtBasedPDF')
if not isExists:
    os.makedirs(r'.\TxtBasedPDF')

isExists=os.path.exists(r'.\ErrorPDF')
if not isExists:
    os.makedirs(r'.\ErrorPDF')

if __name__ == '__main__':
    main()

    #Exit program
    time1= time.time()
    #sys.stdout.write('Type q to exit program:')
    sys.stdout.write('Task is completed and will exit after 5 sec:')
    while(True):
        time2= time.time()
        if (time2-time1)>5:
            break
        #exit = sys.stdin.readline(1)
        #print exit
        #if exit=="q":
        #    break
        #else:
        #    sys.stdout.write('Type q to exit program:')
