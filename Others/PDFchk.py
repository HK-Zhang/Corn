from PyPDF2 import PdfFileReader
inputPdf = PdfFileReader(open(r"p1.pdf", "rb"))
docInfo = inputPdf.getDocumentInfo()

if docInfo.producer != None:
    print 'Produced by '+docInfo.producer
elif docInfo.creator==None: 
    print 'image' 
else: 
    print 'Converted from '+docInfo.creator
