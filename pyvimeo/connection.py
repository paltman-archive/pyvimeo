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

import hashlib
import simplejson
import urllib

from pyvimeo import config

class Connection(object):
	"""
	Represents a connection to the Vimeo API and takes care of things like
	signing requests, authenticating, etc.
	
	Authentication for a Vimeo app goes as follows:
	0. Check configuration for a valid token.
	1. Get a Frob to establish an application session
	2. Generate an authentication URL for the user using:
		a. the frob
		b. permissions (read, write, delete)
		c. api key
	3. Once the user goes to that url and clicks accept, a call to getToken
	   will work.
	4. Once a valid token is received, it should be saved in the user's 
	   configuration file.
	"""
	auth_token = None
	
	def __init__(self):
		self.auth_token = config.AUTH_TOKEN
		self.auth_data = None
		
	def __generate_sig(self, **kargs):
		sig = ''
		sorted_keys = kargs.keys()
		sorted_keys.sort()
		for key in sorted_keys:
			sig += "%s%s" % (key, kargs[key])
	
		return hashlib.md5("%s%s" % (config.SHARED_SECRET, sig)).hexdigest();
	
	def generate_url(self, url_base, **kargs):
		url = ''
		kargs['api_key'] = config.API_KEY
		kargs['format'] = 'json'
		kargs['nojsoncallback'] = 1
		kargs['api_sig'] = self.__generate_sig(**kargs)
		url = urllib.urlencode(kargs)
		return "%s?%s" %  (url_base, url)
		
	def make_request(self, method, **kargs):
		kargs['method'] = method
		url = self.generate_url(url_base=config.API_URL, **kargs)
		raw_data = urllib.urlopen(url).read()
		return simplejson.loads(raw_data)
		
	def check_token(self):
		if self.auth_token:
			self.auth_data = self.make_request(method='vimeo.auth.checkToken', auth_token=self.auth_token)
			return 'stat' in self.auth_data and self.auth_data['stat'] == 'ok'
		return False
		
	@property
	def authenticated(self):
		return self.check_token()


class Authentication(Connection):
	def __init__(self):
		super(Connection, self).__init__()
		self.__frob = None
		self.__auth_token_data = None
		
	def __get_frob(self):
		if self.__frob:
			return self.__frob
			
		frob_data = self.make_request(method='vimeo.auth.getFrob')
		if 'stat' in frob_data and frob_data['stat'] == 'ok':
			self.__frob = frob_data['frob']
			return self.__frob
			
	def get_token(self):
		"""
		Get and save to the user configuration file, the auth token.
		"""
		if self.auth_token:
			return self.auth_token
			
		frob = self.__get_frob()
		self.__auth_token_data = self.make_request(method='vimeo.auth.getToken', frob=frob)
		if 'stat' in self.__auth_token_data and self.__auth_token_data['stat'] == 'ok':
			self.auth_token = self.__auth_token_data['auth']['token']
			config.save_user_option('User', 'auth_token', self.auth_token)
			return self.auth_token
						
	def get_auth_url(self, write_perm=False, delete_perm=False):
		"""
		Get the authenticate url for the the user to register the app with.
		"""
		frob = self.__get_frob()
		perms = 'read'
		if write_perm:
			perms = 'write'
		if delete_perm:
			perms = 'delete'
		url = self.generate_url(url_base=config.AUTH_URL, perms=perms, frob=frob)
		return url
