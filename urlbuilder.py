###############################
# UrlBuilder - Build and rebuild URLs
#
# Usage:
#
# Rebuild existing URL
#
#   from urlbuilder import UrlBuilder
#   urlOrig = UrlBuilder("http://www.google.com/")
#   urlOrig.setPath("/maps")
#   urlOrig.addArgument("one","2")
#   str(urlOrig)
#
# Returns "http://www.google.com/maps?one=2"
#
# Build URL from scratch
#
#   from urlbuilder import UrlBuilder
#   urlNew = UrlBuilder()
#   urlNew.setProtocol("http")
#   urlNew.setHost("www.google.com")
#   urlNew.setPath("/")
#   str(urlNew)
#
# Returns "http://www.googlecom"
#
# Set URL Arguments:
#
#   urlNew.addArgument("one","1")
#   urlNew.addArgument("two",2)
#   str(urlNew)
#
# Returns "http://www.google.com/?one=1&two=2
#
# Set URL Anchor
#
#   urlNew.setAnchor("pagetop")
#   urlNew(url)
#
# Returns "http://www.google.com/?one=1&two=2#pagetop"
#
###############################
import re
from urllib.parse import unquote as url_decode

class UrlBuilder:
  def __init__(self,url=None):
    self.PROTO = ""
    self.HOST = ""
    self.PATH = ""
    self.ARGS = {}
    self.ANCHOR = ""

    if url:
      self.___parseurl(url)
  
  def setProtocol(self,p):
    self.PROTO = p
  
  def setHost(self,h):
    self.HOST = h
  
  def setPath(self,p):
    self.PATH = p
  
  def addArgument(self,n,v):
    self.ARGS[str(n)] = str(v)
  
  def removeArgument(self,n):
    newArgs = {k:v for (k,v) in self.ARGS.items() if k != str(n)}
    self.ARGS = newArgs
  
  def setAnchor(self,a):
    self.ANCHOR = a if a[0] == '#' else ("#" + a)
  
  def __str__(self):
    if self.___validurl():
      args = ("?" + "&".join([f"{k}={v}" for (k,v) in self.ARGS.items()])) if len(self.ARGS.items()) > 0 else ""
      url = f"{self.PROTO}://{self.HOST}{self.PATH}{args}{self.ANCHOR}"
      return url
    elif self.___validpath():
      args = ("?" + "&".join([f"{k}={v}" for (k,v) in self.ARGS.items()])) if len(self.ARGS.items()) > 0 else ""
      url = f"{self.PATH}{args}{self.ANCHOR}"
      return url
    else:
      return ""
  
  def ___validpath(self):
    return (len(self.PATH) > 0)
  
  def ___validurl(self):
    return (len(self.PROTO) > 0 and len(self.HOST) > 0 and len(self.PATH) > 0)
  
  def ___parseurl(self,url):
    # check for protocol, hostname, and path (required)
    urlmatch = re.match(r"^(?P<protocol>[^:]+):\/\/(?P<hostname>[^\/]+)(?P<path>[^?]+)",url)
    if urlmatch:
      self.PROTO = urlmatch.group("protocol")
      self.HOST = urlmatch.group("hostname")
      self.PATH = urlmatch.group("path")
    
      argmatch = re.match("^[^:]+:\/\/[^\/]+[^?]+(?P<args>[?][^#]+)",url)
      
      # check for URL arguments (optional)
      if argmatch:
        argstr = argmatch.group("args")
        if len(argstr):
          argname = [a.split("=")[0] for a in re.sub(r"^\?","",argmatch.group("args")).split("&")]
          argval = [url_decode(a.split("=")[1]) for a in re.sub(r"^\?","",argmatch.group("args")).split("&")]
          self.ARGS = {k:v for (k,v) in zip(argname,argval)}
      
      anchormatch = re.match(r"^[^:]+:\/\/[^\/]+[^?]+\?[^#]+(?P<anchor>#.*)$",url)
      
      # check for anchor (optional)
      if anchormatch:
        self.ANCHOR = anchormatch.group("anchor")
    else:
      pathmatch = re.match(r"^(?P<path>\/[^?]+)",url)
      
      if pathmatch:
        self.PATH = pathmatch.group("path")
        
        argmatch = re.match("^\/[^?]+(?P<args>[?][^#]+)",url)
        
        # check for URL arguments (optional)
        if argmatch:
          argstr = argmatch.group("args")
          if len(argstr):
            argname = [a.split("=")[0] for a in re.sub(r"^\?","",argmatch.group("args")).split("&")]
            argval = [url_decode(a.split("=")[1]) for a in re.sub(r"^\?","",argmatch.group("args")).split("&")]
            self.ARGS = {k:v for (k,v) in zip(argname,argval)}
        
        anchormatch = re.match(r"^\/[^?]+\?[^#]+(?P<anchor>#.*)$",url)
        
        # check for anchor (optional)
        if anchormatch:
          self.ANCHOR = anchormatch.group("anchor")
