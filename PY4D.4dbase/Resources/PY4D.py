import imp, sys
import json
import os.path
from types import *
from json import JSONEncoder
from collections import OrderedDict

def loadBuiltIn():
	return imp.init_builtin("__builtin__")

## get array of valid 4D types
def getValid4DTypes(n=True,s=True,b=True):
	numTypes=[IntType,LongType,FloatType]
	strTypes=[StringType,UnicodeType]
	boolTypes=[BooleanType]
	return (numTypes*n)+(strTypes*s)+(boolTypes*b)


## get list type if all values are same, else return False
## Python types: https://docs.python.org/2/library/types.html
def getListType(seq):
    iseq = iter(seq)
    firstType = type(next(iseq))
    numTypes=getValid4DTypes(True,False,False)
    strTypes=getValid4DTypes(False,True,False)

    if firstType in numTypes:
    	return firstType if all( (type(x) in numTypes) for x in iseq ) else False

    if firstType in strTypes:
    	return firstType if all( (type(x) in strTypes) for x in iseq ) else False

    return firstType if all( (type(x) is firstType) for x in iseq ) else False

## checks if list elements are same type, and valid in 4D (string,boolean,numeric).
## If valid, return type, else return False
def getValidArray(seq):
	validTypes=getValid4DTypes()

	elemType=getListType(seq)
	return elemType if (elemType in validTypes) else False

def convertUnicodeToString(uStr):
	if type(x) == UnicodeType:
		return str(uStr)
	return uStr

def main(args):
	jsonData=json.loads(args.decode('utf-8','ignore'),object_pairs_hook=OrderedDict) # parse json

	moduleName=jsonData["ModuleName"]
	path=jsonData["Path"]
	func=jsonData["Function"]


	if 'Parameters' in jsonData: 
		params=jsonData["Parameters"]
	else:
		params={}

	if moduleName=="":
		foo = loadBuiltIn()
	else:

		scriptFolder=os.path.abspath(os.path.join(path,os.pardir)) # script file's parent directory
		sys.path.insert(0,scriptFolder) # Add modules located at script location                      
		foo = imp.load_source(moduleName,path)

	try:
		methodToCall= getattr(foo,func)
		p=[v for v in params.values()]
		execString="methodToCall(*p)"
		ret=eval(execString)
	except:
		ret=None

	js=JSONEncoder()
	if(ret!=None):
		retType=type(ret)
		appendObjStr=''
		if retType==ListType or retType==TupleType:
			listElemType=getListType(ret)

			if listElemType:  ## If all list elements are the same type
				appendObjStr='","ElemType":"'+str(listElemType)+'"'

				if listElemType in getValid4DTypes(False,True,False): ## if all list elements are of string or unicode type
					ret=[str(i) for i in ret]						  ## convert to string (if unicode)
			else:
				appendObjStr='"'

		else:
			appendObjStr='"'


		if (retType not in getValid4DTypes()):
			ret=str(ret)

		retTypeString=str(retType)
		resObj='{"Return":' + js.encode(ret)+', "Type":"'+retTypeString+appendObjStr+'}'
		print resObj

if __name__=="__main__":

	args = raw_input("") # get json input from 4D
	main(args)
	
