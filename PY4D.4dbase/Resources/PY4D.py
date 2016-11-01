import imp, sys
import json
import os.path
# from types import *
from json import JSONEncoder
from collections import OrderedDict

try:
	import __builtin__
except(NameError,ImportError):
	import builtins
# import builtins

## get array of valid 4D types
def getValid4DTypes(n=True,s=True,b=True):
	numTypes=[int,float]
	strTypes=[str,bytes,unicode]
	boolTypes=[bool]
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

def evalMethod(module,func,params):
	try:
		methodToCall= getattr(module,func)
		p=[v for v in params.values()]
		execString="methodToCall(*p)"
		return eval(execString)
	except(AttributeError):
		exec(func)
		return None

def evalBuiltIn(pyVer,func,params):
	if (pyVer=="2"):
		return evalMethod(__builtin__,func,params)
	else:
		return evalMethod(builtins,func,params)

def main(args,pyVer):
	# args=json.loads(args.decode('utf-8','ignore'),object_pairs_hook=OrderedDict) # parse json
	args=json.loads(args.decode('utf-8','ignore'),object_pairs_hook=OrderedDict)
	# args=json.loads(args,object_pairs_hook=OrderedDict)

	moduleName=args["ModuleName"]
	path=args["Path"]
	func=args["Function"]
	if 'Parameters' in args: 
		params=args["Parameters"]
	else:
		params={}

	if moduleName=="" and func!="":
		# ret=evalBuiltIn(func,params)
		ret=evalBuiltIn(pyVer,func,params)

	else:

		scriptFolder=os.path.abspath(os.path.join(path,os.pardir)) # script file's parent directory
		sys.path.insert(0,scriptFolder) # Add modules located at script location   
		foo = imp.load_source(moduleName,path)
		ret=evalMethod(foo,func,params)

	js=JSONEncoder()
	if(ret!=None):
		retType=type(ret)
		appendObjStr=''
		if retType==list or retType==tuple:
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
		print (resObj)

if __name__=="__main__":

	pyVer=sys.version[0]
	if (pyVer=='2'):
		args=raw_input()
	else:
		args=input()

	main(args,pyVer)
	