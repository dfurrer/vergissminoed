#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

import json, requests
import glob
from collections import defaultdict

base_url = 'http://api.autoidlabs.ch/'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #resp = requests.get(url=base_url + 'customerids')
        #customerids = json.loads(resp.text)
        self.response.write(json.dumps(
            {"2014-10-10": ["Milk", "Toilet paper", "Yoghurt", "Nespresso"]}))
        

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
