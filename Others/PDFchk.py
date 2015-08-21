from PyPDF2 import PdfFileReader
from nt import listdir
import time
import sys

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
        inputPdf = PdfFileReader(open(fileNameStr, "rb"))

        Identified = False
        try:
            for page in inputPdf.pages:
                if Identified == True:
                    break

                #re=page.get('/Resources')
                r=page['/Resources']['/ProcSet']
               # r=re.get('/ProcSet')

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
            
            #txt = page.extractText()
            #if txt != "":
            #    break

        #if txt =="":
        #    countImg+=1
        #else:
        #    countNimg+=1

        #docInfo = inputPdf.getDocumentInfo()
        #if docInfo.producer != None:
        #    countNimg+=1
        #elif docInfo.creator==None:
        #    countImg+=1
        #else: 
        #    countNimg+=1

        #control progress bar
        if barWidth>0 and (i+1.0)/float(m*1.0/toolbar_width) - barIndex>=1:
            for j in range(0,int((i+1.0)/float(m*1.0/toolbar_width) - barIndex)):
                sys.stdout.write("-")
                barIndex+=1
        elif barWidth==0:
            for j in range(int((i-1)*toolbar_width/m),int(i*toolbar_width/m)):
                sys.stdout.write("-")
        sys.stdout.flush()

    file_object = open('Text_List.txt', 'w')
    [file_object.writelines(x+'\n') for x in lstPdfText]
    file_object.close( )

    file_object = open('Img_List.txt', 'w')
    [file_object.writelines(x+'\n') for x in lstPdfImg]
    file_object.close( )

    file_object = open('Err_List.txt', 'w')
    [file_object.writelines(x+'\n') for x in lsfPdfErr]
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
    file_object.close( )

    sys.stdout.write('Type q to exit program:')
    while(True):
        exit = sys.stdin.readline(1)
        print exit
        if exit=="q":
            break
        else:
            sys.stdout.write('Type q to exit program:')


main()
