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

class Users():
    def __init__(self):
        self.users_Path = '/learn/api/public/v1/users/' #create(POST)/get(GET)
        self.user_Path = '/learn/api/public/v1/users/externalId:'
        self.users_Path_Params = "?limit=20&offset=0"

    def getUsers(self, url, key, secret, token): 
        '''
        Returns a Collection of Users
        '''
        URL = 'https://' + url
        print('[Users:getUsers()] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Users:getUsers()] authStr: ' + authStr)
        session = requests.session()
        #session.mount('https://', Tls1Adapter()) # remove for production
        print("[Users:getUsers()] GET Request URL: %s" % URL)
  
        r = session.get(URL, headers={'Authorization':authStr}, verify=False)
        
        print("[Users:getUsers()]: " + str(r.status_code))
        r.raise_for_status()

        if r.text:
            parsed_json = json.loads(r.text)
        else:
            parsed_json = None
            print("NONE")
        
        return parsed_json

    def getUser(self, url, key, secret, token):
        # returns a single user
        print('[Users:getUser()] token: ' + token)
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token
        print('[Users:getUser()] authStr: ' + authStr)
        session = requests.session()

        print("[Users:getUser()] GET Request URL: https://%s" % url)
        
        r = session.get("https://" + url, headers={'Authorization':authStr},  verify=False)

        print("[Users:getUser()] STATUS CODE: " + str(r.status_code) )
        print("[Users:getUser()] RESPONSE:")
        if r.text:
            res = json.loads(r.text)
            parsed_json = json.loads(r.text)
            print(json.dumps(res,indent=4, separators=(',', ': ')))
        else:
            print("NONE")

        return parsed_json


