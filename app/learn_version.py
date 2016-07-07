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

class LearnVersion():
    def __init__(self):
        self.VERSION = None

    def getLearnVersion(self, url, key, secret, token): 
        version_path = '/learn/api/public/v1/system/version'
        URL = 'https://' + url + version_path

        authStr = 'Bearer ' + token

        session = requests.session()
        #session.mount('https://', Tls1Adapter()) # remove for production

        print("[getLearnVersion] GET Request URL: %s" % URL)
        #r = requests.post(url, data=data, verify='/path/to/public_key.pem')
        r = session.get(URL, auth=(key, secret), headers={'Authorization':authStr}, verify=False)
        #r = session.post(OAUTH_URL, data=self.PAYLOAD, auth=(self.KEY, self.SECRET), verify=CERTPATH)

        print("[getLearnVersion] STATUS CODE: " + str(r.status_code))
        #strip quotes from result for better dumps
        r.raise_for_status()

        if r.text:
            res = json.loads(r.text)
            print("[getLearnVersion] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))
            parsed_json = json.loads(r.text)
            print ("[getLearnVersion] Parsed JSON: %s" % parsed_json)

        else:
            print("NONE")


        res = json.loads(r.text)
        print("[getLearnVersion] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))

        #if r.status_code == 200:
            #do nothing
        
    
        
        return parsed_json

