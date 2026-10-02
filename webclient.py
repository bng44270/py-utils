#####################
#
# Simple HTTP/HTTPS client using python http.client classes
#
# Usage:
#
#     # You can import WebClientHTTP or WebClientHTTPS
#     # depending on your needs (they work the same)
#     from webclient import WebClientHTTPS
#     req = WebClientHTTPS
#     resp = req.get("https://ifconfig.co/json",isjson=True)
#     
# The resp variable will have the following structure:
#
#    {
#      "status" : <numeric-HTTP-status-code>,
#      "headers" : <HTTP-response-header-dictionary>,
#      "body" : <response-body>
#    }
#
# The get and post class methods allow the following optional arguments:
#
#    headers=<HTTP-request-header-dictionary>
#    binary=<boolean>
#    isjson=<boolean>
#
# The binary argument specifies whether the response body should be a byte array
# The isjson argument specifies whether the response body should be parsed as a JSON object
#
# NOTE:  if both binary and isjson are set to true (which should not happen) the body is returned as clear text
#
# The post method also allows an optional payload argument containing the string value for the HTTP POST body
#
#####################

from http.client import HTTPConnection, HTTPSConnection
import json
import re

class WebClientBase:
  def __init__(self,conn):
    self.ConnClass = conn
  
  def __get_resp(self,method,url,headers,payload=""):
    url_pattern = r'^(?P<protocol>[^:]+)://(?P<host>[^\/:]+):*(?P<port>[0-9]*)(?P<path>\/.*$)'
    urlparts = re.match(url_pattern,url)
    useport = int(urlparts['port']) if len(urlparts['port']) > 0 else self.ConnClass.default_port
    conn = self.ConnClass(urlparts['host'],useport)
    if len(payload) == 0:
      conn.request(method,urlparts['path'],headers=headers)
    else:
      conn.request(method,urlparts['path'],body=payload,headers=headers)
    return conn.getresponse()
  
  def __resp_to_obj(self,resp,binary,isjson):
    resp_obj = {}
    resp_obj['status'] = resp.status
    resp_obj['headers'] = {a[0]:a[1] for a in resp.getheaders()}
    resp_obj['body'] = self.__get_resp_body(resp,binary,isjson)
    return resp_obj
  
  def __get_resp_body(self,resp,binary,isjson):
    if binary and not sjson:
      return resp.read()
    elif isjson and not binary:
      d = resp.read().decode('ascii')
      return json.loads(d)
    else:
      return resp.read().decode('ascii')
  
  def get(self,url,headers={},binary=False,isjson=False):
    resp = self.__get_resp('GET',url,headers)
    return self.__resp_to_obj(resp,binary,isjson)
  
  def gettofile(self,url,headers={},file="",binary=False):
    resp = self.get(url,headers,binary)
    usefile = file if len(file) > 0 else re.sub(r'^.*\/([^\/]+)$',"\\1",url)
    mode = "wb" if binary else "w"
    if len(usefile) > 0:
      with open(usefile,mode) as f:
        f.write(resp['body'])
  
  def post(self,url,payload="",headers={},binary=False,isjson=False):
    resp = self.__get_resp('POST',url,headers,payload)
    return self.__resp_to_obj(resp,binary,isjson)


class WebClientHTTP(WebClientBase):
  def __init__(self):
    super().__init__(HTTPConnection)

class WebClientHTTPS(WebClientBase):
  def __init__(self):
    super().__init__(HTTPSConnection)
