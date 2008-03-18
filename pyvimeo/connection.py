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
	
	>>> c = Connection()
	>>> c.authenticated
	False
	>>> None == c.authed_user
	True
	"""
	def __init__(self):
		self.__authenticated = False
		self.__auth_token = None
		self.__auth_token_data = None
		self.__authed_user = None
		self.__frob = None
		
	def __generate_sig(self, **args):
		sig = ''
		sorted_keys = args.keys()
		sorted_keys.sort()
		for key in sorted_keys:
			sig += "%s%s" % (key, sorted_keys[key])
	
		return hashlib.md5("%s%S" % (config.SHARED_SECRET, sig)).hexdigest();
	
	def __generate_url(self, url_base, **args):
		url = ''
		args['api_key'] = config.API_KEY
		args['format'] = 'json'
		args['nojsancallback'] = 1
		sig = self.__generate_sig(args)
		
		for key in args.keys():
			url += "%s=%s&" % (key, urllib.urlencode(args[key]))
		
		return "%s?%sapi_sig=%s" %  (url_base, url, sig)
		
	def make_request(self, method, **kargs):
		# TODO: From the API Sandbox, it appears that all calls use the api/rest
		#       url.  If this is not try, then filter on the method name to 
		#       select the appropriate base_url.
		kargs['method'] = method
		url = self.__generate_url(url_base=config.API_URL, kargs)
		raw_data = urllib.urlopen(url).read()
		return simplejson.loads(raw_data)
		
	def __get_frob(self):
		if self.__frob:
			return self.__frob
	
		frob_data = self.make_request(method='vimeo.auth.getFrob')
		if 'stat' in frob_data and frob_data['stat'] == 'ok':
			self.__frob = frob_data['frob']
			return self.__frob
		
		return None
		
	def __get_token(self):
		if self.__auth_token:
			return self.__auth_token
			
		self.__get_frob()
		self.__auth_token_data = self.make_request(method='vimeo.auth.getToken', frob=self._frob)
		if 'stat' in self.__auth_token_data and self.__auth_token_data['stat'] == 'ok':
			self.__auth_token = self.__auth_token_data['auth']['token']
			return self.__auth_token
		
		return None
		
	def __check_token(self):
		if self.__auth_token:
			self.__auth_token_data = self.make_request(method='vimeo.auth.checkToken', auth_token=self.__auth_token)
			return 'stat' in self.__auth_token_data and self.__auth_token_data['stat'] == 'ok'
		return False
	
	def authenticate(self):
		"""
		Authenticates the user based on the configured api key and shared
		secret.
		
		>>> c = Connection()
		>>> c.authenticate()
		>>> c.authenticated
		True
		>>> None == c.authed_user
		False
		"""
		self.__get_token()
		if self.__check_token():
			self.__authenticated = True
			self.__authed_user = User(auth_token_data=self.__auth_token_data)
			
	@property
	def authed_user(self):
		return self.__authed_user
		
	@property
	def authenticated(self):
		return self.__authenticated
		
	def get_user(username):
		"""
		Get a User object via an Email Address. 
		
		>>> c = Connection()
		>>> user = c.get_user(username='ted')
		>>> user.id
		151542
		>>> user.username
		ted
		>>> user.display_name
		Ted!
		"""
		pass
		
	def get_user_by_email(email):
		"""
		Get a User object with a username.
		
		>>> c = Connection()
		>>> user = c.get_user_by_email(email='paltman@gmail.com')
		>>> user.id
		332546
		>>> user.username
		altman
		>>> user.display_name
		Patrick Altman
		"""
		pass
		