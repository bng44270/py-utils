###############################
# UrlBuilder - Build and rebuild URLs
#
# NOTE:  Also works without protocol and hostname
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
from urllib.parse import unquote as url_decode, quote as url_encode

class UrlBuilder(dict):
  def __init__(self,url=None):
    self['protocol'] = ""
    self['host'] = ""
    self['path'] = ""
    self['params'] = {}
    self['anchor'] = ""
    
    if url:
      self.___parseurl(url)
  
  def __str__(self):
    if self.___validurl():
      args = ("?" + "&".join([f"{k}={url_encode(v)}" for (k,v) in self['params'].items()])) if len(self['params'].items()) > 0 else ""
      url = f"{self['protocol']}://{self['host']}{self['path']}{args}{self['anchor']}"
      return url
    elif self.___validpath():
      args = ("?" + "&".join([f"{k}={url_encode(v)}" for (k,v) in self['params'].items()])) if len(self['params'].items()) > 0 else ""
      url = f"{self['path']}{args}{self['anchor']}"
      return url
    elif self.__validhost():
      url = f"{self['protocol']}://{self['host']}/"
      return url
    else:
      return ""
  
  def ___validpath(self):
    return (len(self['path']) > 0)
  
  def ___validurl(self):
    return (len(self['protocol']) > 0 and len(self['host']) > 0 and len(self['path']) > 0)
  
  def __validhost(self):
    return (len(self['protocol']) > 0 and len(self['host']) > 0)
  
  def ___parseurl(self,url):
    # check for protocol, hostname, and path (required)
    urlmatch = re.match(r"^(?P<protocol>[^:]+):\/\/(?P<hostname>[^\/]+)(?P<path>[^?]+)",url)
    if urlmatch:
      self['protocol'] = urlmatch.group("protocol")
      self['host'] = urlmatch.group("hostname")
      self['path'] = urlmatch.group("path")
    
      argmatch = re.match("^[^:]+:\/\/[^\/]+[^?]+(?P<args>[?][^#]+)",url)
      
      # check for URL arguments (optional)
      if argmatch:
        argstr = argmatch.group("args")
        if len(argstr):
          argname = [a.split("=")[0] for a in re.sub(r"^\?","",argmatch.group("args")).split("&")]
          argval = [url_decode(a.split("=")[1]) for a in re.sub(r"^\?","",argmatch.group("args")).split("&")]
          self['params'] = {k:v for (k,v) in zip(argname,argval)}
      
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
            self['params'] = {k:v for (k,v) in zip(argname,argval)}
        
        anchormatch = re.match(r"^\/[^?]+\?[^#]+(?P<anchor>#.*)$",url)
        
        # check for anchor (optional)
        if anchormatch:
          self['anchor'] = anchormatch.group("anchor")
