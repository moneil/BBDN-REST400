"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import sys
from constants import *

requests.packages.urllib3.disable_warnings()

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
# May be removed if you migrated the cert as outlined in auth.py
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class Memberships():        

    def getCourseMemberships(self, url, key, secret, token):
        '''
        GET /learn/api/public/v1/courses/{courseId}/users
        returns a collection of all the memberships for a specific course
        '''

        print('[Membership:getCourseMemberships] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Membership:getCourseMemberships] authStr: ' + authStr)
        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production
        print ("[Membership:getCourseMemberships] URL: https://%s" % url)
        r = session.get("https://" + url, headers={'Authorization':authStr}, verify=False)

        if (r.status_code != 200): 
            print(r.text)
            r.raise_for_status()
        if r.text:
            parsed_json = json.loads(r.text)
        else:
            parsed_json = None
            print("NONE")
        
        return parsed_json

    def getUserMemberships(self, url, key, secret, token):
        #GET /learn/api/public/v1/users/{userId}/courses
        print('[Membership:readUserMemberships] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Membership:getUserMemberships] authStr: ' + authStr)
        session = requests.session()
        print("[Membership:getUserMemberships()] GET Request URL: https://%s" % url)
        print("[Membership:getUserMemberships()] JSON Payload: NONE REQUIRED")
        r = session.get("https://" + url, headers={'Authorization':authStr},  verify=False)
        print("[Membership:getUserMemberships()] STATUS CODE: " + str(r.status_code) )
        print("[Membership:getUserMemberships()] RESPONSE:")
        print 
        if r.text:
            parsed_json = json.loads(r.text)
        else:
            parsed_json = None
            print("NONE")

        return parsed_json

        

