Programming with python - Assignment 3
--------------------------------------

Topic: Building a device database, group 1
Website chosen: www.gsmarena.com

a. Files included:
	1. assignment3.py	#crawler source code
	2. crawl_log.txt	#crawler log
	3. server.py		#server
	4. index.html		#default page served
	5. long_list.txt	#specifies list of url to crawl through


b. Important notes:

	1. The crawler is designed to extract data only from specific pages of gsmarena.com, examples of which can be found in long_list.txt
	2. The usage of the respective modules can be found by specifying --help as the command line argument
	3. The crawler writes to a mongodb database, so make sure that the process "mongod" is running
	4. All the crawling performance details are logged into crawl_log.txt
	5. The server must be started only after the crawling is complete
	6. Normal mongodb json queries can be specified in the query box in the default index.html page
	7. The schema used is the same as in Assignment 1
	8. The server by default runs on port 8800
	9. The server implements a rest interface since any post request with a field named-"query" containing the query can gain access to the service
	10. The query set is returned as a json object
