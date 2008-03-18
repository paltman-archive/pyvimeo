#!/usr/bin/python

# Copyright (c) 2008 Patrick Altman http://paltman.com
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
import ConfigParser
import os


SystemConfigPath = '/etc/pyvimeo.cfg'
UserConfigPath = '~/.pyvimeo'

class Config(ConfigParser.SafeConfigParser):
    def __init__(self, path=None, fp=None):
        ConfigParser.SafeConfigParser.__init__(self)
                                                      
        if path:
            self.read(path)
        elif fp:
            self.readfp(fp)
        else:
            self.read([SystemConfigPath, os.path.expanduser(UserConfigPath)])
            
    def get(self, section, name, default=None):
        try:
            val = ConfigParser.SafeConfigParser.get(self, section, name)
        except Exception, e:
            print str(e)
            val = default
        return val
  
    def getint(self, section, name, default=0):
        try:
            val = ConfigParser.SafeConfigParser.getint(self, section, name)
        except:
            val = int(default)
        return val
    
    def getfloat(self, section, name, default=0.0):
        try:
            val = ConfigParser.SafeConfigParser.getfloat(self, section, name)
        except:
            val = float(default)
        return val
    
    def getbool(self, section, name, default=False):
        if self.has_option(section, name):
            val = self.get(section, name)
            if val.lower() == 'true':
                val = True
            else:
                val = False
        else:
            val = default
        return val

config = Config()

config.API_KEY       = config.get('Credentials', 'api_key')
config.SHARED_SECRET = config.get('Credentials', 'shared_secret')
config.API_URL       = config.get('Urls', 'starndard_api_url', 'http://www.vimeo.com/api/rest/')
config.UPLOAD_URL    = config.get('Urls', 'upload_url', 'http://www.vimeo.com/services/upload/')
config.AUTH_URL      = config.get('Urls', 'auth_url', 'http://www.vimeo.com/services/auth/')
	

