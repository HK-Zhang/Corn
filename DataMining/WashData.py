import csv
import time,datetime
import re
from schema import Schema, And, Use, Optional


class VarsGlobal:
	sourceFile='source.csv'
	targetFile='target.csv'
	issueFile='issue.csv'
	VarPatterns={'ORDER_STATUS':re.compile(r'^SHIPPED$|^IN PROGRESS$|^CANCELLED$|^IN PRODUCTION$|^READY$',re.I|re.M),'ORDER_LINE_STATUS':re.compile(r'^SHIPPED$|^IN PROGRESS$|^CANCELLED$|^IN PRODUCTION$|^READY$',re.I|re.M)}
	# for number range check e.g. 1000-4095 pattern = re.compile(r'^[1-4]\d(?<!4[1-9])\d\d(?<!409[6-9])$')
	VarsDate=['ORDER_RECEIVE_DATE','ORDER_LAST_UPDATE_DATE','ORDER_REQUESTED_DATE','ORDER_SCHEDULE_DATE','ORDER_PROMISED_DATE','SHIPMENT_SHIPPING_DATE','SHIPMENT_LAST_UPDATE_DATE']
	VarsInt=[]
	VarsStr=[]
	VarsFloat=[]
	VarNonEmpty=[]
	dateFormat='%Y-%m-%d'
	csvDiscriminator='|'
	csvQuotechar='"'
	
ROWData = []

gbl = VarsGlobal()


def _ValidateDate(dataVal):
    '''Verify date as per date format specified in VarsGlobal. Return True if input data pass validation or it is a blank string'''
    if _isNotBlankStr(dataVal)==False:
        return True
    try:
        time_format = datetime.datetime.strptime(dataVal.strip(), gbl.dateFormat)
        #time_format = time_format.strftime('%Y%m%d%H%M%S')
    except:
        return False
    return True


def _isNotBlankStr(dataVal):
	'''If it is a blank string, Retrun False'''
	if len(dataVal.strip())==0:
		return False
	else:
		return True

	
def _ValidateInt(dataVal):
	'''If it is not valid integer, Retrun False'''
	return dataVal.isalnum()
	
def _ValidateFloat(dataVal):
	'''If it is not valid float, Retrun False'''
	try:
		Schema(Use(float)).validate(dataVal)
	except:
		return False
		
	return True

def _ValidatePattern(dataVal,patternReg):
	'''If value doesn't pass pattern check, Retrun False'''
	if _isNotBlankStr(dataVal)==False:
		return True
	match=patternReg.match(dataVal.strip())
	if match:
		return True
	else:
		return False

def processBlankStr(dataRow,varsIndex):
	if len(varsIndex)==0: return True
	for i in varsIndex:
		if _isNotBlankStr(dataRow[i])==False:
			return False
	
	return True


	
def processInt(dataRow,varsIndex):
	if len(varsIndex)==0: return True
	for i in varsIndex:
		if _ValidateFloat(dataRow[i])==False:
			print("Invalid Int:",dataRow[i])
			return False
	
	return True
	
def processDate(dataRow,varsIndex):
	if len(varsIndex) == 0: return True
	
	for i in varsIndex:
		if _ValidateDate(dataRow[i]) == False: 
			print("Invalid Date:",dataRow[i])
			dataRow[i]='Invalid:'+dataRow[i]
			return False
		
	
	return True
	
	

def processFloat(dataRow,varsIndex):
	if len(varsIndex)==0: return True
	for i in varsIndex:
		if _ValidateInt(dataRow[i])==False:
			print("Invalid Float:",dataRow[i])
			return False
	
	return True
	
def processPattern(dataRow,varIndex,varsName):
	if len(varsName)==0: return True
	index=0
	for i in varIndex:
		if _ValidatePattern(dataRow[i],gbl.VarPatterns[varsName[index]])==False:
			print("Invalid Pattern:",dataRow[i])
			dataRow[i]='Invalid:'+dataRow[i]
			return False
		index=index+1
	
	return True
	
def readRecordFromFile():
	"""Read data from external csv and load data into a global variable RowData"""
	with open(gbl.sourceFile, newline='') as csvfile:
		rowReader = csv.reader(csvfile, delimiter=gbl.csvDiscriminator, quotechar=gbl.csvQuotechar)
		for row in rowReader:
			ROWData.append(row)
			
			
def processRecord():
	blankStrIndex=[]
	dateIndex=[]
	intIndex=[]
	floatIndex=[]
	patternIndex=[]
	patternName=[]

	"""Set up data validation requirement based on title and requirement array in VarsGlobal"""
	for i in range(len(ROWData[0])):
		if gbl.VarsDate.count(ROWData[0][i]) > 0:
			dateIndex.append(i)
		if gbl.VarsInt.count(ROWData[0][i]) > 0:
			intIndex.append(i)
		if gbl.VarsFloat.count(ROWData[0][i]) > 0:
			floatIndex.append(i)	
		if gbl.VarNonEmpty.count(ROWData[0][i]) > 0:
			blankStrIndex.append(i)	
		if list(gbl.VarPatterns.keys()).count(ROWData[0][i]) > 0:
			patternName.append(ROWData[0][i])
			patternIndex.append(i)	



	print('Number of columns:',len(ROWData[0]))
	
	
	with open(gbl.targetFile, 'w', newline='') as t, open(gbl.issueFile, 'w', newline='') as i:		
		writert = csv.writer(t, delimiter=gbl.csvDiscriminator, quotechar=gbl.csvQuotechar)
		writeri = csv.writer(i, delimiter=gbl.csvDiscriminator, quotechar=gbl.csvQuotechar)
		writert.writerow(ROWData[0])
		writeri.writerow(ROWData[0])
		
		for row in ROWData[1:]:
			#To check number of columns for data row and title
			if len(row) != len(ROWData[0]):
				row[0]='Missing Cloumn:'+row[0]
				writeri.writerow(row)
				print("Current Row's column number:",len(row))
				continue
			
			#To verify blank string
			isValid = processBlankStr(row,blankStrIndex)
			
			if isValid == False:
				writeri.writerow(row)
				print("Current Row has blank cell:")
				continue
			
			#To verify Date	
			isValid = processDate(row,dateIndex)
			
			if isValid == False:
				writeri.writerow(row)
				continue
			
			#To verify Integer			
			isValid = processInt(row,intIndex)
			
			if isValid == False:
				writeri.writerow(row)
				continue
			
			#To verify Float			
			isValid = processFloat(row,floatIndex)
			
			if isValid == False:
				writeri.writerow(row)
				continue

			#To verify Pattern			
			isValid = processPattern(row,patternIndex,patternName)
			
			if isValid == False:
				writeri.writerow(row)
				continue
			
			writert.writerow(row)
				
				
def Main():
	readRecordFromFile()
	processRecord()
	print('Done')

if __name__=="__main__":  
	Main()