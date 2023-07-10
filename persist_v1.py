import sys
import numpy as np
import math

class Pers_Store:
	def __init__(self,filename):
		self.pers_file_name=filename
		self.kv_sep=' @#SEP#@ '#try to find a better separator 
		self.del_str='@#DEL#@'
		self.stacksep=' $*STACKSEP*$ '
		self.STACK_TYPE ='$*STACK_TYPE$*'
		self.kv_dict={}
		self.f_read=open(filename,'r') #create the file if not exist
		self.f_app = open(filename,'a')
		for line in self.f_read:
			line = line.rstrip("\r\n")
			l=line.split(self.kv_sep)
			if l[1]==self.del_str:
				if l[0] in self.kv_dict:
					del self.kv_dict[l[0]]
			else:
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
			self.set(lname,STACK_TYPE)
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
			print("returning from index=none")
			return None
		elif (index == self.STACK_TYPE):
			print("get1")
			retkey=self.get(lname+self.stacksep+'top')
			tv=int(retkey.split(self.stacksep)[-1])
			if(tv<0):
				print("returning from tv<0")
				return None
			else:	
				print("get2")
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



	### for debugging with small store ####
	def printkv(self):
		print(self.kv_dict)
		return

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

if __name__=="__main__":
	main()


