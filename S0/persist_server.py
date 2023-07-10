import sys
import numpy as np
import math
import urllib.request, json 
from flask import Flask, jsonify, request



app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/home', methods = ['GET', 'POST'])
def home():
	if(request.method == 'GET'):

		data = "hello world"
		return jsonify({'data': data})


# A simple function to calculate the square of a number
# the number to be squared is sent in the URL when we use GET
# on the terminal type: curl http://127.0.0.1:5000 / home / 10
# this returns 100 (square of 10)
@app.route('/home/<int:num>', methods = ['GET'])
def disp(num):
	return jsonify({'data': num**2})






@app.route('/echorequest/', methods = ['GET'])
def echorequest():
	return jsonify(request.args)




class Pers_Store:
	def __init__(self,filename):
		self.pers_file_name=filename
		self.kv_sep=' @#SEP#@ '#try to find a better separator 
		self.del_str=' @#DEL#@ '
		self.stacksep=' $*STACKSEP*$ '
		self.STACK_TYPE =' $*STACK_TYPE$* '
		self.SET_TYPE=' #!SET_TYPE!# '
		self.setsep=' #!SET_SEP!# '
		self.setvalsep=' ###VALSEP### '
		self.kv_dict={}
		self.f_read=open(filename,'r') #create the file if not exist
		self.f_app = open(filename,'a')
		for line in self.f_read:
			line = line.rstrip("\r\n")
			l=line.split(self.kv_sep)
			self.kv_dict[l[0]]=l[1] #only string based keys and vals are supported. for other data types, we need to serialize the datatypes.
		self.f_read.close()



	def set(self,a,b):
		self.kv_dict[a]=b
		self.f_app.write(a+self.kv_sep+b+"\n")
		return
	

	

	def get(self,a):
		if a in self.kv_dict:
			return self.kv_dict[a]
		else:
			print("returning from original get")
			return None

	def delkey(self,a):
		if a in self.kv_dict:
			del self.kv_dict[a]
			self.f_app.write(a+self.kv_sep+self.del_str+"\n")
		else:
			return


	def save(self):
		self.f_app.close()
		self.f_app=open(self.pers_file_name,'a')
		return

	def shutdown(self):
		self.f_app.close()
		return

	def spush(self,lname,val):
		index = self.get(lname)
		if index == None:
			self.set(lname,self.STACK_TYPE)
			self.set(lname+self.stacksep+str(0),val)
			self.set(lname+self.stacksep+'top',lname+self.stacksep+str(0))
		else:
			t=self.get(lname+self.stacksep+'top')
			tv=int(t.split(self.stacksep)[-1])
			tv+=1
			tv = str(tv)
			self.set(lname+self.stacksep+tv,val)
			self.set(lname+self.stacksep+'top',lname+self.stacksep+tv)
		return

	def spop(self,lname):
		index = self.get(lname)
		if index==None:
			#print("returning from index=none")
			return None
		elif (index == self.STACK_TYPE):
			#print("get1")
			retkey=self.get(lname+self.stacksep+'top')
			tv=int(retkey.split(self.stacksep)[-1])
			if(tv<0):
				#print("returning from tv<0")
				return None
			else:	
				#print("get2")
				print(retkey)
				retval=self.get(retkey)
				if not(retval == None):
					self.delkey(retkey)
					tv-=1
					tv = str(tv)
					self.set(lname+self.stacksep+'top',lname+self.stacksep+tv)
				return retval
		else:
			print(f"{lname} is not a stack")
			return None
		return


	def sadd(self,set_name,val):
		index = self.get(set_name)
		if index == None:
			self.set(set_name,self.SET_TYPE)
			self.set(set_name+self.setsep,val)
		else:
			s=self.get(set_name+self.setsep)
			#latest_val=int(t.split(self.stacksep)[-1])
			#tv+=1
			#tv = str(tv)
			ss=s
			sslist=ss.split(self.setvalsep)
			if val in sslist:
				return
			else:
				self.set(set_name+self.setsep,s+self.setvalsep+val)
				#self.set(lname+self.stacksep+'top',lname+self.stacksep+tv)
		return

	def sismember(self,set_name,val):
		index=self.get(set_name)
		if index==None:
			return None
		elif index == self.SET_TYPE:
			vals=self.get(set_name+self.setsep)
			lvals=vals.split(self.setvalsep)
			if val in lvals:
				return 'yes'
			else:
				return 'no'


	def sunion(self,set1,set2):
		index1=self.get(set1)
		index2=self.get(set2)
		if index1==None or index2==None or index1!=self.SET_TYPE or index2!=self.SET_TYPE:
			return
		else:
			set1vals=self.get(set1+self.setsep)
			set2vals=self.get(set2+self.setsep)
			set1list=set1vals.split(self.setvalsep)
			set2list=set2vals.split(self.setvalsep)
			for i in set1list:
				if not (i in set2list):
					self.sadd('unionedset',i)
			for j in set2list:
				self.sadd('unionedset',j)
			fset=self.retset('unionedset')
		return str(fset)

	def sinter(self,set1,set2):
		index1=self.get(set1)
		index2=self.get(set2)
		if index1==None or index2==None or index1!=self.SET_TYPE or index2!=self.SET_TYPE:
			return
		else:
			set1vals=self.get(set1+self.setsep)
			set2vals=self.get(set2+self.setsep)
			set1list=set1vals.split(self.setvalsep)
			set2list=set2vals.split(self.setvalsep)
			for i in set1list:
				if i in set2list:
					self.sadd('intersectset',i)
			fset=self.retset('intersectset')
		return str(intersectset)

	def retset(self,setname):
		index=self.get(setname)
		if index == None or index!=self.SET_TYPE:
			return
		else:
			retvals=self.get(setname+self.setsep)
			return retvals





	### for debugging with small store ####
	def printkv(self):
		print(self.kv_dict)
		return


@app.route('/get/', methods = ['GET'])
def get():
	retval=PS.get(request.args['key'])
	return jsonify(retval)



@app.route('/set/', methods = ['GET'])
def set():
	#print(request.args)
	keyval=request.args['key']
	valval=request.args['val']
	PS.set(keyval,valval)
	return jsonify('status:ok')



@app.route('/spop/', methods = ['GET'])
def spop():
	retval=PS.spop(request.args['stackname'])
	return jsonify(retval)


@app.route('/spush/', methods = ['GET'])
def spush():
	#print(request.args)
	stackval=request.args['stackname']
	valval=request.args['val']
	PS.spush(stackval,valval)
	return jsonify('status:ok')


@app.route('/sadd/', methods = ['GET'])
def sadd():
	#print(request.args)
	setval=request.args['setname']
	valval=request.args['val']
	PS.sadd(setval,valval)
	return jsonify('status:ok')

@app.route('/sismember/', methods = ['GET'])
def sismember():
	retval=PS.sismember(request.args['setname'],request.args['val'])
	return jsonify(retval)

@app.route('/sunion/', methods = ['GET'])
def sunion():
	#print(request.args)
	set1=request.args['setname1']
	set2=request.args['setname2']
	retval=PS.sunion(set1,set2)
	return jsonify('retval')


@app.route('/sinter/', methods = ['GET'])
def sinter():
	#print(request.args)
	set1=request.args['setname1']
	set2=request.args['setname2']
	retval=PS.sinter(set1,set2)
	return jsonify('retval')

@app.route('/retset/', methods = ['GET'])
def retset():
	retval=PS.retset(request.args['setname'])
	return jsonify(retval)

@app.route('/save/', methods = ['GET'])
def save():
	PS.save()
	return 'saved'


@app.route('/shutdown/', methods = ['GET'])
def shutdown():
	PS.shutdown()
	return 'closed.'

def main():
	operation = " "
	PS = Pers_Store('Persistent_file.txt')
	## debugging ##
	PS.printkv()
	## end Debugging

	while 1:
		print("->>",end="")
		operation=input()
		op_seq=operation.split()
		if op_seq[0]=="get":
			val=PS.get(op_seq[1])
			print(val)
		elif op_seq[0]=="set":
			PS.set(op_seq[1],op_seq[2])
		elif op_seq[0]=="spush":
			PS.spush(op_seq[1],op_seq[2])
		elif op_seq[0]=="spop":
			val=PS.spop(op_seq[1])
			print(val)
		elif op_seq[0]=="delkey":
			PS.delkey(op_seq[1])
		elif op_seq[0]=="save":
			PS.save()
		elif op_seq[0]=="shutdown":
			PS.shutdown()
		elif op_seq[0]=="quit":
			return
		else:
			print("wrong operation")

if __name__ == '__main__':
	PS = Pers_Store('Persistent_file.txt')
	app.run(debug = True, host = "0.0.0.0", port=sys.argv[1])
	print("\n")


