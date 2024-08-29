##############################################
#
# SatTle - load satellite TLE data from a URL
#          or a local file into a dictionary
#
# Usage:
#
#    # sats variable will be a dictionary containing TLE data
#    sats = SatTle(filespec="/path/to/tle.txt")
#
#    # noaa variable will be a dictionary containing TLE data loaded from the URL
#    noaa = SatTle(url='http://www.celestrak.com/NORAD/elements/noaa.txt')
#
##############################################
from re import match as regex_match
from os.path import exists as file_exists
from requests import get as http_get

class SatTle(list):
  def __init__(self,filespec=None,url=None):
    lines = []
    
    if url:
      resp = http_get(url)
      if resp.status_code == 200:
        lines = resp.text.splitlines()
    
    elif filespec:
      if file_exists(filespec):
        with open(filespec,'r') as f:
          lines = f.readlines()
      
    if len(lines) > 0:  
      idx = 0
      
      while True:
        d = {}
        
        title = self.__parsetitle(lines[idx])
        
        d['name'] = title
        
        idx = idx + 1
        
        line1 = self.__parseline1(lines[idx])
        
        for key in [a for a in line1.keys()]:
          d[key] = line1[key]
        
        idx = idx + 1
        
        line2 = self.__parseline2(lines[idx])
        
        for key in [a for a in line2.keys()]:
          d[key] = line2[key]
        
        self.append(d)
        
        idx = idx + 1
        
        if idx == len(lines):
          break
    else:
      raise Exception("No TLE data found")
  
  def __parsetitle(self,s):
    tle_title_pattern = r'^(?P<title>.+)$'
    title = regex_match(tle_title_pattern,s)
    return title['title'].strip() if title else False
  
  def __parseline1(self,s):
    tle_line1_pattern = r'^.[ \t]+(?P<satcat>.....)(?P<classification>.)[ \t]+(?P<launch_year>..)(?P<launch_number>...)(?P<piece_of_launch>...)[ \t]+(?P<epoch_year>..)(?P<epoch_day>............)[ \t]+(?P<first_derivative>..........)[ \t]+(?P<second_derivative>........)[ \t]+(?P<drag_term>........)[ \t]+(?P<ephemeris_type>.)[ \t]+(?P<set_number>....)(?P<checksum>.)$'
    line1 = regex_match(tle_line1_pattern,s)
    return line1.groupdict() if line1 else False
  
  def __parseline2(self,s):
    tle_line2_pattern = r'^.[ \t]+(?P<satcat>.....)[ \t]+(?P<inclination>........)[ \t]+(?P<right_ascension>........)[ \t]+(?P<eccentricity>.......)[ \t]+(?P<argument_of_perigee>........)[ \t]+(?P<mean_anomoly>........)[ \t]+(?P<mean_motion>...........)(?P<revolution>.....)(?P<checksum>.)$'
    line2 = regex_match(tle_line2_pattern,s)
    return line2.groupdict() if line2 else False
