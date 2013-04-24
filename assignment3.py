#!/usr/bin/python
#This module solves the third python assignment of building a web crawler
from urllib import *
from urllib2 import *
from pymongo import Connection
import pymongo
import argparse
#import rest
import re
import urlparse
import time
url = "" 
f = ""
request = None 
dbname = "" 
coll = ""
verbose = ""
host = ""
crawl_count = 0
r = {"ModelNumber":"","Manufacturer":"","OperatingSystem":"","Talktime":"","Touch":"","SecondaryCamera":"","GPS":"","Thickness":""}
#Modelnumber
#Manufacturer
#Operating system
#Talktime
#Touch
#Secondary camera


class myLogger():
	f_name = ""
	f_handler = None
	def __init__(self, f_name):
		self.f_name = f_name
		self.f_handler = open(self.f_name,"a")
	def write(self, line):
		self.f_handler.write(line+"\n")
	def close(self):
		self.f_handler.close()


def getPage(url):
	try:
		page = None
		request = Request(url)
		page = urlopen(request)
		return page
	except URLError as e:
		raise Exception("error: Please connect to a network and try again")
	except IOError as e:
		raise Exception("error: Invalid URL")

def makeList(page):
	#print "Dummy makeList method"
	pageString = page.read()
	k=0
	model_manufacturer = ""
	model = ""
	manufacturer = ""
	os_type = ""
	android_os = False
	ios = False
	meego_os = False
	blackberry_os = False

	talktime = ""
	touch = ""
	secondary_camera = ""
	gps = ""
	thickness = ""
	temp = []
	pageList = pageString.split("\n")	
	
	#print pageList
	os_l = "<td class=\"ttl\"><a href=\"glossary.php3?term=os\">OS</a></td>\r"
	touch_l = "<td class=\"ttl\"><a href=\"glossary.php3?term=display-type\">Type</a></td>\r"
	talktime_l = "<td class=\"ttl\"><a href=\"glossary.php3?term=talk-time\">Talk time</a></td>\r"
	secondary_l = "<td class=\"ttl\"><a href=\"glossary.php3?term=video-call\">Secondary</a></td>\r"
	gps_l = "<td class=\"ttl\"><a href=\"glossary.php3?term=gps\">GPS</a></td>\r"
	thickness_l = "<td class=\"ttl\"><a href=# onClick=\"helpW('h_dimens.htm');\">Dimensions</a></td>\r"

	try:
		os_type = pageList[pageList.index(os_l)+1]	#retrieveing the os type
		os_type = re.sub('<[^<]+?>', '', os_type)
		os_type = os_type[:-1]	
		if re.findall("android", os_type.lower()) != []:
			os_type = "android"
		elif re.findall("blackberry", os_type.lower()) != []:
			os_type = "BBOS"
		elif re.findall("ios", os_type.lower()) != []:
			os_type = "ios"
		elif re.findall("symbian", os_type.lower()) != []:
			os_type = "symbian"
		elif re.findall("windows", os_type.lower()) != []:
			os_type = "windows phone"
		elif re.findall("bada", os_type.lower()) != []:
			os_type = "bada"
		elif re.findall("meego", os_type.lower()) != []:
			os_type = "meego"
		elif re.findall("linux", os_type.lower()) != []:
			os_type = "linux"
			
	except ValueError as e:
		os_type = "N/A"

	try:	
		talktime = pageList[pageList.index(talktime_l)+1]		#retrieveing the talktime
		talktime = re.sub('<[^>]+?>', '', talktime)
		talktime = talktime[:-1]
		talktime = talktime.split("/")
		if talktime == [''] or talktime == ['No official data']:
			talktime = "N/A"
		else:
		 	m = re.findall('\d+\sh', talktime[0].lower())
			if m != []:
				try:
					talktime = int(m[0][:-2])
				except ValueError as e:
				 	try:
				 		m = re.findall('\d+\sh', talktime[1].lower())
				 		if m != []:
				 			talktime = int(m[0][:-2])
				 			
				 	except ValueError as e:
				 			talktime = "N/A"
			else:
				try:

				 		m = re.findall('\d+\sh', talktime[1].lower())

				 		if m != []:
				 			talktime = int(m[0][:-2])
				except ValueError as e:
				 			talktime = "N/A"

	except ValueError as e:
		talktime = "N/A"
	try:
		touch = pageList[pageList.index(touch_l)+1]
		touch = re.sub('<[^>]+?>', '', touch)
	        if re.findall("touch",touch.lower()) != []:
        	        touch = True
	        else:
        	        touch = False
	except ValueError as e:
		touch = "N/A"


	try:
		gps = pageList[pageList.index(gps_l)+1]
		gps = re.sub('<[^>]+?>', '', gps)
		if re.findall("yes", gps.lower()) != []:
			gps = True
		else:
			gps = False
		
	except ValueError as e:
		gps = "N/A"
	model_manufacturer = re.sub('<[^<]+?>', '',pageList[96])
	temp = model_manufacturer.split(" ",1)
	manufacturer = temp[0]
	model = temp[1][:-1]

	try:
		secondary_camera = pageList[pageList.index(secondary_l)+1]
		secondary_camera = re.sub('<[^>]+?>', '', secondary_camera)
	        if re.findall("yes",secondary_camera.lower()) != []:
             		secondary_camera = True
        	else:
                	secondary_camera = False
	except ValueError as e:
		secondary_camera = "N/A"

	try:
		thickness = pageList[pageList.index(thickness_l)+1]
	        thickness = re.sub('<[^>]+?>', '', thickness)
		k = thickness.split("(")
		if len(k) == 2:	
			k = k[0].split("x")[2]
			k = re.findall("(.+\smm)",k)[0]
			k = k[:-3]
			thickness = float(k)
	 	else:	
	 		thickness = "N/A"
	except ValueError as e:
		thickness = "N/A"

	if talktime == ['']:	
		talktime = 'N/A'
	
	model = model.lower()
	manufacturer = manufacturer.lower()
	os_type = os_type.lower()
	
	rs = r = {"model_number":model,"manufacturer":manufacturer,"operating_system":os_type,"talktime":talktime,"touch":touch,"secondary_camera":secondary_camera,"gps":gps,"thickness":thickness}
	return [rs]

def printrs(rs):
	print rs
	print "----------------------------------------------------------------------------------------"

#---------------------------------------------------------------------------



def insertdb(data):
	"""
	data is a list of dict's which ll be inserted into db called dbname and a collection called dbname
	"""
	global host
	connection = Connection(host, 27017)
	db = connection[dbname]
	collection = db[coll]
	post_id=[]
	posts = db.coll
	post_id.append(posts.insert(data))
	if verbose:
		print 'inserted:',data
	connection.close()
	return post_id

def displaydb():
	"""
	displays all data inside db called file name 
	something similar to read db
	"""
	global host
	connection = Connection(host, 27017)
	db = connection[dbname]
	collection = db[coll]
	posts = db.coll
	if posts.count():
		for post in posts.find():
			for key in post:
				if key != '_id':
					print '%22s' %(str(key)),
			print 
			break;
		for post in posts.find():
			for key,val in post.iteritems():
				if key != '_id':
					print '%22s' % (str(val)),
			print 
	else:
		return 'no data'
	connection.close()







#-----------------------------------------------------------------------------




def init():
	parser = argparse.ArgumentParser()
	global verbose
	global f
	global dbname
	global coll
	global host
	parser.add_argument('-f', action='store',dest='file',type=str,default="http://",help="File containing list of urls")
	parser.add_argument('-v', action='store_true',dest='Verbose',default=False,help="Toggle verbose mode, default to off")	
	parser.add_argument('-d', action='store',dest='dbname',type=str,default="dev_db",help="Mongo DB, databse name")
	parser.add_argument('-c', action='store',dest='coll',type=str,default="all",help="Mongo DB, collection name")
	parser.add_argument('-n', action='store',dest='host',type=str,default='localhost',help="Hostname on which the mongo db server is running")
	parser.add_argument('--version', action='version',version="K-crawler version 1.0")
    	results = parser.parse_args()
    	if results.file:
    		f = results.file
	
  	else:
  		raise Exception("URL file not specified")

  	host = results.host
    	verbose = results.Verbose
    	if results.dbname:
    		dbname = results.dbname
    	if results.coll:
    		coll = results.coll

def crawl():
		rs = None
		page = None
		hostname = urlparse.urlunparse(urlparse.urlparse(url)[:2] + ("",) * 4)
		if hostname == "http://www.gsmarena.com":
			page = getPage(url)
			rs = makeList(page)

			if verbose:
				printrs(rs)
			insertdb(rs)
		else:
			print "Only specific pages from http://gsmarena.com are supported\nexample: http://www.gsmarena.com/samsung_galaxy_s_iv-5125.php"

if __name__ == "__main__":
	try:


			crawl_count = 0
			init()
			log = myLogger("crawl_log.txt")
			start_time = time.time()
			log.write("crawler started "+time.ctime())
			print "crawler started "+time.ctime()
			
			handler = open(f,"r")
			for line in handler:
				url = line
				log.write("Currently crawling through:"+url[:-1]+time.ctime())
				if verbose:
					print "Current page = ", url
				crawl()
				crawl_count += 1
			end_time = time.time()
			log.write("crawler terminated,"+time.ctime()+" total no. of pages crawled  "+str(crawl_count)+" total time taken "+str(end_time - start_time))

			print "crawler terminated,"+time.ctime()+" total no. of pages crawled  "+str(crawl_count)+" total time taken "+str(end_time - start_time)
			'''if verbose:
				displaydb()'''
			#db = dbHelper("dbname","coll")
			#insertCollection(rs,db)
			#retrieveCollection(db)
			handler.close()
			log.close()
	except IOError as e:
			print "error: "+f+" no such file exists"
	except KeyboardInterrupt as e:
		print "\nProgram interrupted"
		end_time = time.time()
		log.write("crawler terminated,"+time.ctime()+" total no. of pages crawled  "+str(crawl_count)+" total time taken "+str(end_time - start_time))
		log.close()
		print "crawler terminated,"+time.ctime()+" total no. of pages crawled  "+str(crawl_count)+" total time taken "+str(end_time - start_time)
		'''if verbose:
			displaydb()'''
	except Exception as e:
		print e #, type(e)
