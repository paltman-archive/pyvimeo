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

from pyvimeo.connection import Connection

class User(Connection):
	def __init__(self, authenticate_user=False):
		super(User, self).__init__()
		
		self.__id           = None
		self.__username     = None
		self.__display_name = None
		self.__perms        = None
		
		if authenticate_user:
			if self.authenticated:
				self.__id           = self.auth_data['auth']['user']['id']
				self.__username     = self.auth_data['auth']['user']['username']
				self.__display_name = self.auth_data['auth']['user']['fullname']
				self.__perms        = self.auth_data['auth']['perms']
			else:
				raise Exception("Failed to Authenticate.")
			
	@property
	def id(self):
		return self.__id
		
	@property
	def username(self):
		return self.__username
		
	@property
	def display_name(self):
		return self.__display_name
		
	@property
	def perms(self):
		return self.__perms
		