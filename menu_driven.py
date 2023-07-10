import sys
from persist_master import *
def main():
	ch = 0
	while 1:
		print("CHOOSE FUNCTIONALITY:")
		print("1. Add key value pair in hash table.")
		print("2. Get the value of a key from hash table")
		#print("3. Remove a key from hash table")
		print("3. Push an element into stack.")
		print("4. Pop an element from stack")
		print("5. Add an element into a set.")
		print("6. check if element belongs to a set")
		#print("8. intersection of sets")
		#print("9. union of sets")
		print("7. see the values in a set")
		print("8. Save")
		print("9. ShutDown")
		ch = int(input())
		if ch == 1:
			key=input("enter key")
			val=input("enter value")
			url="http://localhost:8000/set/?key="+key+"&val="+val
			print("url for your request is: ")
			print(url)
		elif ch == 2:
			key=input("enter key")
			url="http://localhost:8000/get/?key="+key
			print("url for your request is: ")
			print(url)
		#elif ch == 3:
			#write code
		elif ch == 3:
			stackname=input("enter stack name")
			val=input("enter value")
			url="http://localhost:8000/spush/?stackname="+stackname+"&val="+val
			print("url for your request is: ")
			print(url)
		elif ch == 4:
			stackname=input("enter stackname")
			url="http://localhost:8000/spop/?stackname="+stackname
			print("url for your request is: ")
			print(url)

		elif ch == 5:
			setname=input("enter setname")
			val=input("enter value")
			url=url="http://localhost:8000/sadd/?setname="+setname+"&val="+val
			print(url)

		elif ch == 6:
			setname=input("enter setname")
			val=input("enter value")
			url=url="http://localhost:8000/sismember/?setname="+setname+"&val="+val
			print(url)

		# elif ch == 8:
		# 	setname1=input("enter setname1")
		# 	setname2=input("enter setname2")
		# 	url=url="http://localhost:8000/sinter/?setname1="+setname1+"&setname2="+setname2
		# 	print(url)

		# elif ch == 9:
		# 	setname1=input("enter setname1")
		# 	setname2=input("enter setname2")
		# 	url=url="http://localhost:8000/sunion/?setname1="+setname1+"&setname2="+setname2
		# 	print(url)

		elif ch == 7:
			setname=input("enter setname")
			url=url="http://localhost:8000/retset/?setname="+setname
			print(url)

		elif ch == 8:
			url="http://localhost:8000/save/"
			print("url for your request is: ")
			print(url)
		elif ch == 9:
			url="http://localhost:8000/shutdown/"
			print("url for your request is: ")
			print(url)
			return
		else:
			print("Wrong operation")

if __name__ == "__main__":
	main()

