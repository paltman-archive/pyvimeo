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
    
    def save_option(self, path, section, option, value):
        """
        Write the specified Section.Option to the config file specified by path.
        Replace any previous value.  If the path doesn't exist, create it.
        Also add the option the the in-memory config.
		
		Borrowed this code from the boto project. :-)  Thanks, Mitch.
        """
        config = ConfigParser.SafeConfigParser()
        config.read(path)
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)
        fp = open(path, 'w')
        config.write(fp)
        fp.close()
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, option, value)
    
    def save_user_option(self, section, option, value):
        self.save_option(os.path.expanduser(UserConfigPath), section, option, value)
    
    def save_system_option(self, section, option, value):
        self.save_option(SystemConfigPath, section, option, value)
    
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

API_KEY       = config.get('Credentials', 'api_key')
SHARED_SECRET = config.get('Credentials', 'shared_secret')
API_URL       = config.get('Urls', 'starndard_api_url', 'http://www.vimeo.com/api/rest/')
UPLOAD_URL    = config.get('Urls', 'upload_url', 'http://www.vimeo.com/services/upload/')
AUTH_URL      = config.get('Urls', 'auth_url', 'http://www.vimeo.com/services/auth/')
AUTH_TOKEN    = config.get('User', 'auth_token', None)