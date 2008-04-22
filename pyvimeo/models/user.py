from pyvimeo.connection import Connection

class User(Connection):
	"""
	Represents a Vimeo user, either authenticated as the calling user, or
	an unauthenticated user in the system.
	
	Supports the following Vimeo API methods:
		vimeo.people.findByUserName
		vimeo.people.findByEmail
		vimeo.people.getInfo
		vimeo.people.getPortraitUrl
		vimeo.people.addContact
		vimeo.people.removeContact
		vimeo.people.addSubscription
		vimeo.people.removeSubscription
		vimeo.contacts.getList
	"""
	def __init__(self, authenticate_user=False):
		super(User, self).__init__()
		
		self.__userdata = None
		self.__perms    = None
		
		if authenticate_user:
			if self.authenticated:
				self.__get_info(self.auth_data['auth']['user']['id'])
				self.__perms = self.auth_data['auth']['perms']
			else:
				raise Exception("Failed to Authenticate.")
	
	def __get_info(self, user_id):
		data = self.make_request('vimeo.people.getInfo', user_id=user_id)
		if 'stat' in data and data['stat'] == 'ok':
			self.__userdata = data['person']
	
	def load_user(self, user_id):
		self.__get_info(user_id)			
	
	@property
	def location(self):
		return self.__userdata['location']
	
	@property
	def url(self):
		return self.__userdata['url']
		
	@property
	def number_of_contacts(self):
		return int(self.__userdata['number_of_contacts'])
		
	@property
	def number_of_uploads(self):
		return int(self.__userdata['number_of_uploads'])
		
	@property
	def number_of_likes(self):
		return int(self.__userdata['number_of_likes'])
		
	@property
	def number_of_videos(self):
		return int(self.__userdata['number_of_videos'])
		
	@property
	def number_of_video_appearance(self):
		return int(self.__userdata['number_of_videos_appears_in'])
		
	@property
	def profile_url(self):
		return self.__userdata['profileurl']
		
	@property
	def videos_url(self):
		return self.__userdata['videosurl']
		
	@property
	def is_staff(self):
		return self.__userdata['is_staff'] == '1'
		
	@property
	def id(self):
		return self.__userdata['id']
		
	@property
	def username(self):
		return self.__userdata['username']
		
	@property
	def display_name(self):
		return self.__userdata['display_name']
		
	@property
	def perms(self):
		return self.__perms
		
	@staticmethod
	def find_by_username(username):
		c = Connection()
		data = c.make_request('vimeo.people.findByUserName', username=username)
		if 'stat' in data and data['stat'] == 'ok':
			u = User()
			u.load_user(data['user']['id'])
			return u
		
	@staticmethod
	def find_by_email(email):
		c = Connection()
		data = c.make_request('vimeo.people.findByEmail', find_email=email)
		if 'stat' in data and data['stat'] == 'ok':
			u = User()
			u.load_user(data['user']['id'])
			return u
		