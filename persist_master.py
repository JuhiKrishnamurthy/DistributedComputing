import sys
import numpy as np
import math
import urllib.request, json 
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

setvalseperator=' ###VALSEP### '

@app.route('/get/', methods = ['GET'])
def get():
	#retval=PS.get(request.args['keyname'])
	sid=getserver('get',request.args['key'],None,nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/get/?key='+request.args['key'])
	#return jsonify(str(retval))
	return retval.text



@app.route('/set/', methods = ['GET'])
def set():
	#print(request.args)
	sid=getserver('set',request.args['key'],request.args['val'],nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/set/?key='+request.args['key']+'&val='+request.args['val'])
	#return jsonify(str(retval))
	return retval.text



@app.route('/spop/', methods = ['GET'])
def spop():
	sid=getserver('spop',request.args['stackname'],None,nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/spop/?stackname='+request.args['stackname'])
	#return jsonify(str(retval))
	return retval.text


@app.route('/spush/', methods = ['GET'])
def spush():
	#print(request.args)
	sid=getserver('spush',request.args['stackname'],request.args['val'],nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/spush/?stackname='+request.args['stackname']+'&val='+request.args['val'])
	#return jsonify(str(retval))
	return retval.text



@app.route('/sadd/', methods = ['GET'])
def sadd():
	#print(request.args)
	sid=getserver('sadd',request.args['setname'],request.args['val'],nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/sadd/?setname='+request.args['setname']+'&val='+request.args['val'])
	#return jsonify(str(retval))
	return retval.text


@app.route('/sismember/', methods = ['GET'])
def sismember():
	#print(request.args)
	sid=getserver('sismember',request.args['setname'],request.args['val'],nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/sismember/?setname='+request.args['setname']+'&val='+request.args['val'])
	#return jsonify(str(retval))
	return retval.text



@app.route('/retset/', methods = ['GET'])
def retset():
	#print(request.args)
	sid=getserver('retset',request.args['setname'],None,nservers)
	url=hashval_url_dict[sid]
	retval=requests.get(url+'/retset/?setname='+request.args['setname'])
	#return jsonify(str(retval))
	return retval.text


@app.route('/sinter/', methods = ['GET'])
def sinter():
	#print(request.args)
	sname1 = request.args['setname1']
	sname2 = request.args['setname2']
	sid1=getserver('sinter',request.args['setname1'],None,nservers)
	sid2=getserver('sinter',request.args['setname2'],None,nservers)
	url1=hashval_url_dict[sid1]
	url2=hashval_url_dict[sid2]
	set1val=requests.get(url1+'/retset/?setname='+request.args['setname1'])
	set2val=requests.get(url2+'/retset/?setname='+request.args['setname2'])
	for i in set1val.text.split(setvalseperator):
		requests.get(url2+'/sadd/?setname='+sname1+'temp'+'&val='+i)
	requests.get(url2+'/save/')
	retvals=requests.get(url2+'/sinter/?setname1='+sname2+'&setname2='+sname1+'temp')
	#return jsonify(str(retval))
	return jsonify(retvals.text)


@app.route('/sunion/', methods = ['GET'])
def sunion():
	#print(request.args)
	sname1 = request.args['setname1']
	sname2 = request.args['setname2']
	sid1=getserver('sinter',request.args['setname1'],None,nservers)
	sid2=getserver('sinter',request.args['setname2'],None,nservers)
	url1=hashval_url_dict[sid1]
	url2=hashval_url_dict[sid2]
	set1val=requests.get(url1+'/retset/?setname='+request.args['setname1'])
	set2val=requests.get(url2+'/retset/?setname='+request.args['setname2'])
	for i in set1val.text.split(setvalseperator):
		requests.get(url2+'/sadd/?setname='+sname1+'temp'+'&val='+i)
	requests.get(url2+'/save/')
	retvals=requests.get(url2+'/sunion/?setname1='+sname2+'&setname2='+sname1+'temp')
	#return jsonify(str(retval))
	return jsonify(retvals.text)


@app.route('/save/', methods = ['GET'])
def save():
	for k in hashval_url_dict:
		cururl=hashval_url_dict[k]
		requests.get(cururl+'/save/')
	return('saved')


@app.route('/shutdown/', methods = ['GET'])
def shutdown():
	for k in hashval_url_dict:
		cururl=hashval_url_dict[k]
		requests.get(cururl+'/shutdown/')
	return('closed.')



def getserver(command,key,val,nservers):
	hashedkey = hash(key)
	serverid=hashedkey%nservers
	return serverid



if __name__ == '__main__':

	nservers=0
	dictsep=' ^%DICTSEP%^ '
	hashval_url_dict={}
	master_file=open('Master_file.txt','r')
	for line in master_file:
		line=line.rstrip('\r\n')
		items=line.split(dictsep)
		hashval_url_dict[int(items[0])]=items[1]
	nservers=len(hashval_url_dict)
	app.run(debug = True, host = "0.0.0.0", port=sys.argv[1])
	print("\n")