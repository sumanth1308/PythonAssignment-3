import time
import json
import BaseHTTPServer
import cgi
import assignment3
import urllib
import argparse
from pymongo import Connection
HOST_NAME = '0.0.0.0' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8800 # Maybe set this to 9000.


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        f_name = urllib.unquote_plus(s.path)   
        if s.path == "/":
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                f = open("index.html","r")
                s.wfile.write(f.read())
                f.close()
        else:
            try:
                f = open(f_name[1:],"r")
                s.send_response(200)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write(f.read())
                f.close()
            except IOError as e:
                s.send_response(404)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write("ERROR 404: File not found, "+s.path+" doesn't exist on this server")
    def do_POST(self):
        # Parse the form data posted
        form_dictionary = {}
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        

        # Echo back information about what was posted in the form
        for field in form.keys():
            field_item = form[field]
            form_dictionary[field] = form[field].value
        try:
            k = list(form_dictionary["query"])
	    flag = 1
	    l = 0
            while l < len(k):
                	j = k[l]
                	if j == "$" and flag == 1:
                        	flag = 0
                        	k.insert(l,"\"")
                	if j == ":" and flag == 0:
                        	k.insert(l,"\"")
                       		flag = 1
                        l = l + 1
                

            query = ''.join(k)
            if query != "":
                query = query.lower()
                query = eval(query)
                #self.wfile.write("<h3 style=\"text-decoration:underline\">Result set</h3>")
                #self.wfile.write("<p style=\"font-size:20px text-decoration:underline\">Query:"+str(query)+"</p>")
                #print type(query)
                result = self.getResult(query)
                if result != []:
     		    for i in result:
			self.wfile.write(str(i)+'\n')
                else:
                    self.wfile.write("Null set"+'\n')

            else:
                self.wfile.write("Empty query"+'\n')
        except KeyError as e:
                self.wfile.write("Empty query"+'\n')                
        except SyntaxError as e:
            self.wfile.write("Syntax error in query"+'\n')
        return

    def getResult(self,query):
        """
        returns a list of database objects
        """
        l = []
        connection = Connection(host, 27017)
        db = connection[dbname]
        collection = db[coll]
        posts = db.coll
        if posts.count():
                for post in posts.find(query):
                    l.append(post)



        return l




def init():
    parser = argparse.ArgumentParser()
    global dbname
    global coll
    global host
    parser.add_argument('-d', action='store',dest='dbname',type=str,default="dev_db",help="Mongo DB, databse name")
    parser.add_argument('-c', action='store',dest='coll',type=str,default="all",help="Mongo DB, collection name")
    parser.add_argument('-n', action='store',dest='host',type=str,default='localhost',help="Hostname on which the mongo db server is running")
    parser.add_argument('--version', action='version',version="K-server version 1.0")
    results = parser.parse_args()
    host = results.host
    dbname = results.dbname
    coll = results.coll



if __name__ == '__main__':
    try:
	init()
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
        print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
    except Exception as e:
        print e
