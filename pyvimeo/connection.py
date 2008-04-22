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
	1. Generate an authorization URL for the user using:
		a. permissions (read, write, delete)
		b. api key
	2. Get a Frob to establish an application session after going to the url
	   from #1 to authorize the application for the user account.
	3. Once the user goes to that url and clicks accept, a call to getToken
	   will work.
	4. Once a valid token is received, it should be saved in the user's 
	   configuration file.
	"""
	auth_token = None
	
	def __init__(self):
		self.auth_token = config.AUTH_TOKEN
		self.auth_data = None
		self.__frob = None
		self.__auth_token_data = None
		
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
			self.auth_data = self.make_request(
			    method='vimeo.auth.checkToken', auth_token=self.auth_token)
			return 'stat' in self.auth_data and self.auth_data['stat'] == 'ok'
		return False
		
	@property
	def authenticated(self):
		return self.check_token()
		
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
		self.__auth_token_data = self.make_request(
		    method='vimeo.auth.getToken', frob=frob)
		if 'stat' in self.__auth_token_data and \
		    self.__auth_token_data['stat'] == 'ok':
			self.auth_token = self.__auth_token_data['auth']['token']
			config.save_user_option('User', 'auth_token', self.auth_token)
			return self.auth_token
						
	def get_auth_url(self, write_perm=False, delete_perm=False):
		"""
		Get the authenticate url for the the user to register the app with.
		"""
		perms = 'read'
		if write_perm:
			perms = 'write'
		if delete_perm:
			perms = 'delete'
		url = self.generate_url(url_base=config.AUTH_URL, perms=perms)
		return url
