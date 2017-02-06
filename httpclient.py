#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse


def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):
    def __init__(self):
        self.socket = 0 
        self.code = 0
        self.header = ""
        self.body = ""
        
    def connect(self, host, port):
        if (port == None):
            port = 80
        #print(host)
        #print(port)
            
        #thanks to Jimbo(http://www.programmingforums.org/member4334.html) for the hint
        #http://www.programmingforums.org/post143159-3.html    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.socket.setblocking(30)
        # use sockets!
        return None

    def get_code(self, data):
        
        return int(data[0].split('\r\n')[0].split(' ')[1])

    def get_headers(self,data):
        return data[0]

    def get_body(self, data):
        return data[1]

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:            
            part = sock.recv(1024)
            check = str(part)
            #/r/n0/r/n so the client doesn't choke on google.com's reponse
            if (part and '/r/n0/r/n' not in check):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        body = ""
              
        o = urlparse(url)       
            
        #print(o)
        #print(o.geturl())
        #print(o.port)
     
       
        url = o.netloc.split(':',1)[0]
        #written by Ned Batchelder(http://stackoverflow.com/users/14343/ned-batchelder)
        #http://stackoverflow.com/questions/904746/how-to-remove-all-characters-after-a-specific-character-in-python
        
        path = o.path

        if(path==''):
            path='/'
            
        self.connect(url,o.port)
        requeststring = "GET "+path+" HTTP/1.1\r\n"
        requeststring = requeststring +"Host: "+url+"\r\n"
        requeststring = requeststring +"Accept: */*\r\n"
        #requeststring = requeststring +"Accept-Language: en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3\r\n"
        #requeststring = requeststring +"Connection: Keep-Alive\r\n"
        #requeststring = requeststring +"Accept-Encoding: gzip, deflate, br\r\n"
        #requeststring = requeststring +"DNT:1\r\n"
        #requeststring = requeststring +"Cookie: __utma=87648711.980831727.1462167756.1467126737.1475612062.3; __utmz=87648711.1475612062.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); _ga=GA1.2.980831727.1462167756; __unam=94c97c-1547001c3\r\n"
        #requeststring = requeststring +"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15019\r\n"
        requeststring = requeststring +"\r\n"
        #print(requeststring)
        
        self.socket.sendall(requeststring)
        chunk = self.recvall(self.socket).split('\r\n\r\n')
      
        code = self.get_code(chunk);
        body = self.get_body(chunk);
        #print(code)    
        #print(body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        
        code = 500
        body = ""


        o = urlparse(url)       
            
        #print(o)
        #print(o.geturl())
        #print(o.port)

        url = o.netloc.split(':',1)[0]
        #written by Ned Batchelder(http://stackoverflow.com/users/14343/ned-batchelder)
        #http://stackoverflow.com/questions/904746/how-to-remove-all-characters-after-a-specific-character-in-python
        
        path = o.path

        if(path==''):
            path='/'
        if(args == None):
            args = ''
        else:
            print(str(args))
        self.connect(url,o.port)
        requeststring = "POST "+path+" HTTP/1.1 \r\n"
        requeststring = requeststring +"Host: "+url+"\r\n"
        requeststring = requeststring +"Accept: */* \r\n"      
        requeststring = requeststring +"Content-Length: "+str(len(urllib.urlencode(args)))+" \r\n\r\n"
        requeststring = requeststring + urllib.urlencode(args) +" \r\n"
        #print(requeststring)
        self.socket.sendall(requeststring)
        chunk = self.recvall(self.socket).split('\r\n\r\n')
        #print("chunk is:"+str(chunk))
        #print("\r\n\r\n\r\n\r\n")   
        #print("chunk[0] is :"+chunk[0])
        #print("\r\n\r\n\r\n\r\n")
        if(len(chunk)>1):
            body = self.get_body(chunk);
            #print("chunk[1] is :"+chunk[1])
        code = self.get_code(chunk);
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    else:
        print client.command( sys.argv[1] )
