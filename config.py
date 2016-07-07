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
OAUTH_KEY = "8907d3c7-b43c-4e52-864c-ba43e0a1f23f"
OAUTH_SECRET = "tgyDtZxV1Nw0uNX2ZUOK5pbvTt0j2ybK"
TARGET_URL = "dev.bbdn.local:8443"
#TARGET_URL = "ultra-integ.int.bbpd.io"
TOKEN = ""
LIMIT=10
OFFSET=0
COURSES_PATH = "/learn/api/public/v1/courses/?limit=%s&offset=%s" % (LIMIT, OFFSET)
COURSE_PATH = "/learn/api/public/v1/courses/"
USERS_PATH = "/learn/api/public/v1/users/?limit=%s&offset=%s" % (LIMIT, OFFSET)
USER_PATH = "/learn/api/public/v1/users/" 
COURSE_MEMBERSHIPS_PATH = '/learn/api/public/v1/courses/<courseId>/users?limit=%s&offset=%s' % (LIMIT, OFFSET)
USER_MEMBERSHIPS_PATH = '/learn/api/public/v1/users/<userId>/courses?limit=%s&offset=%s' % (LIMIT, OFFSET)



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