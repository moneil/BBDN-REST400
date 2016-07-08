"""
Configuration file for flask sample application
"""
import os


# enable CSRF
WTF_CSRF_ENABLED = True

# enable debug
DEBUG = True

# secret key for authentication
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "you-will-never-guess")

CERT_PATH = "./certs/dev.bbdn.local.pem"
#OAUTH_KEY = "your oauth key here"
#OAUTH_SECRET = "your oauth secret here"
#TARGET_URL = "dev.bbdn.local:8443"
TOKEN = ""
LIMIT=10
OFFSET=0
COURSES_PATH = "/learn/api/public/v1/courses/?limit=%s&offset=%s" % (LIMIT, OFFSET)
COURSE_PATH = "/learn/api/public/v1/courses/"
USERS_PATH = "/learn/api/public/v1/users/?limit=%s&offset=%s" % (LIMIT, OFFSET)
USER_PATH = "/learn/api/public/v1/users/" 
COURSE_MEMBERSHIPS_PATH = '/learn/api/public/v1/courses/<courseId>/users?limit=%s&offset=%s' % (LIMIT, OFFSET)
USER_MEMBERSHIPS_PATH = '/learn/api/public/v1/users/<userId>/courses?limit=%s&offset=%s' % (LIMIT, OFFSET)

#Heroku configs Comment out if not using Heroku Toolbelt or Heroku deployment
OAUTH_KEY = os.environ.get('APP_OAUTH_KEY', '')
OAUTH_SECRET = os.environ.get('APP_OAUTH_SECRET', '')
TARGET_URL = os.environ.get('APP_TARGET_URL', '')
      
# Sample client certificate example for 12 factor app
# You would want to store your entire pem in an environment variable
# with something like:
# ```
# export CONSUMER_KEY_CERT=$(cat <<EOF
# < paste cert here>
# EOF
# )
# ```

CONSUMER_KEY_PEM_FILE = os.path.abspath('consumer_key.pem')
with open(CONSUMER_KEY_PEM_FILE, 'w') as wfile:
    wfile.write(os.environ.get('CONSUMER_KEY_CERT', ''))

PYLTI_CONFIG = {
    "consumers": {
        "__consumer_key__": {
            "secret": os.environ.get("CONSUMER_KEY_SECRET", "__lti_secret__"),
            "cert": CONSUMER_KEY_PEM_FILE
        }
    }
}