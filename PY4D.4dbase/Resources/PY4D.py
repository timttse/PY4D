import imp, sys
import json
import os.path
from json import JSONEncoder
from collections import OrderedDict

try:
	import __builtin__
except(NameError,ImportError):
	import builtins

class PY4D:
	def __init__(self,pyVer="2",moduleName="",path="",func="",params={}):
		self.pyVer=pyVer
		self.moduleName=moduleName
		self.path=path
		self.func=func
		self.params=params


		## get array of valid 4D types
	def getValid4DTypes(self,n=True,s=True,b=True):
		numTypes=[int,float]
		if (self.pyVer=="2"):
			strTypes=[str,unicode]
		else:
			strTypes=[str,bytes]
		boolTypes=[bool]
		return (numTypes*n)+(strTypes*s)+(boolTypes*b)


	## get list type if all values are same, else return False
	## Python types: https://docs.python.org/2/library/types.html
	def getListType(self,seq):
	    iseq = iter(seq)
	    firstType = type(next(iseq))
	    numTypes=self.getValid4DTypes(True,False,False)
	    strTypes=self.getValid4DTypes(False,True,False)

	    if firstType in numTypes:
	    	return firstType if all( (type(x) in numTypes) for x in iseq ) else False

	    if firstType in strTypes:
	    	return firstType if all( (type(x) in strTypes) for x in iseq ) else False

	    return firstType if all( (type(x) is firstType) for x in iseq ) else False

	def evalMethod(self,module,func,params):
		try:
			methodToCall= getattr(module,func)
			p=[v for v in params.values()]
			return eval("methodToCall(*p)")
		except(AttributeError):
			exec(func)
			return None

	def evalBuiltIn(self,func,params):
		if (self.pyVer=="2"):
			return self.evalMethod(__builtin__,func,params)
		else:
			return self.evalMethod(builtins,func,params)

	def execute(self):
		moduleName=self.moduleName
		func=self.func
		path=self.path
		params=self.params

		if moduleName=="" and func!="":
			ret=self.evalBuiltIn(func,params)

		else:
			scriptFolder=os.path.abspath(os.path.join(path,os.pardir)) # script file's parent directory
			sys.path.insert(0,scriptFolder) # Add modules located at script location   
			foo = imp.load_source(moduleName,path)
			ret=self.evalMethod(foo,func,params)

		js=JSONEncoder()
		if(ret!=None):
			retType=type(ret)
			appendObjStr=''
			if retType==list or retType==tuple:
				listElemType=self.getListType(ret)

				if listElemType:  ## If all list elements are the same type
					appendObjStr='","ElemType":"'+str(listElemType)+'"'

					if listElemType in self.getValid4DTypes(False,True,False): ## if all list elements are of string or unicode type
						ret=[str(i) for i in ret]						  ## convert to string (if unicode)
				else:
					appendObjStr='"'

			else:
				appendObjStr='"'


			if (retType not in self.getValid4DTypes()):
				ret=str(ret)

			retTypeString=str(retType)
			resObj='{"Return":' + js.encode(ret)+', "Type":"'+retTypeString+appendObjStr+'}'
			print (resObj)

if __name__=="__main__":

	pyVer=sys.version[0]
	if (pyVer=='2'):
		args=raw_input()
		args=json.loads(args.decode('utf-8','ignore'),object_pairs_hook=OrderedDict)
	else:
		args=input()
		args=json.loads(args,object_pairs_hook=OrderedDict)

	moduleName=args["ModuleName"]
	path=args["Path"]
	func=args["Function"]
	if 'Parameters' in args: 
		params=args["Parameters"]
	else:
		params={}

	p=PY4D(pyVer,moduleName,path,func,params)
	p.execute()
	