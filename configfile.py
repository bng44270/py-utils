from re import sub as regex_sub
from os import path

typeof = lambda x : type(x).__name__

class ConfigFile(dict):
  """
    ConfigFile - extends Python dict object
    
    Usage:
    
      # Initialize object with no configuration file (must be configured with Read method)
      conf = ConfigFile()
      
      # Initialize object with a configuration file and read configuration
      conf = ConfigFile("/path/to/settings.conf")
      
    Configuration file format (uses key/value pairs):
    
      <KEY><space/tab><VALUE>
      # start lines with a hash to comment configuration file
    
  """
  def __init__(self,filename=""):    
    if len(filename) > 0:
      self.FILENAME = filename
      self.Read(filename)
  
  def Read(self,filename):
    """
      # Read data from configuration file
      conf.Read('/path/to/settings.conf')
    """
    if (path.exists(filename) or path.exists(self.FILENAME)) and (len(filename) > 0 or len(self.FILENAME) > 0):
      if filename and not self.FILENAME:
        self.FILENAME = filename
      with open(self.FILENAME,"r") as conffile:
        for line in conffile:
          if line[0] == '#' or len(line) == 0:
            continue
          else:
	          configkey = regex_sub('^([^ \t]+).*$','\\1',str(line)).strip()
	          configvalue = regex_sub('^[^ \t]+[ \t]+(.*)$','\\1',str(line)).strip()
	          self.Add(configkey,configvalue)
  
  def IsNew(self):
    """
      # Returns True if the configuration object is empty, False if the object contains data
      is_new_file = conf.IsNew()
    """
    if len(list(self.keys())) == 0:
      return True
    else:
      return False
  
  def Write(self):
    """
      # Write data in configuration object to the file set in the constructor or Read function
      conf.Write()
    """
    with open(self.FILENAME,"w") as thisfile:
      for (k,v) in self.items():
        if typeof(v) == 'list':
          for value in v:
            thisfile.write(f"{k}\t{value}\n")
        else:
          thisfile.write(f"{k}\t{v}\n")
  
  def Add(self,key,value):
    """
      # Add a new key/value pair to the configuration file (key = BINPATH, value = /usr/bin)
      conf.Add('BINPATH','/usr/bin')

      # If duplicate keys are found, the single value property is transformed into a list
      conf.Add('FIELD','name')
      conf.Add('FIELD','age')

      # conf['FIELD'] resolves to ['name','age']
    """
    if len(key) > 0 and len(value) > 0:
      if key in list(self.keys()):
        if typeof(self[key]) == 'list':
          self[key].append(value)
        else:
          orig = self[key]
          self[key] = []
          self[key].append(orig)
          self[key].append(value)
      else:
        self[key] = value
    else:
      raise Exception(f"Invalid key/value pair ({key}:{value})")
    
  def Get(self,key):
    """
      # Return the value of a provided key
      binary_file_path = conf.Get('BINPATH')
    """
    if self[key]:
      return self[key]
  
  def Remove(self,key):
    """
      # Remove an existing key from the object
      conf.Remove('BINPATH')
    """
    if self[key]:
      del self[key]
