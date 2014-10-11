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

import os, platform
import json, requests
import glob
from collections import defaultdict
import datetime

from database import Database

base_url = 'http://api.autoidlabs.ch/'

data_dir = os.path.join(os.path.split(__file__)[0], 'data')
db = Database()
hostname = None

def init():
  if not os.path.exists(data_dir):
    raise RuntimeError('Data dir %s does not exist.' % repr(data_dir))
  db.load(data_dir)

init()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        customerid = self.request.get('customerid')

        if customerid not in db.customerids_set:
          self.response.write(
            ('Customerid %s is not in the database. ' + \
            'Why don\'t you try with %s?') % (
              repr(customerid), '156290'))
          return

        db.compute_customer_model(customerid)
        date_of_last_purchase = datetime.datetime(2014, 9, 29, 0, 0)
        one_week_later = date_of_last_purchase + datetime.timedelta(days = 7)
        one_month_later = date_of_last_purchase + datetime.timedelta(days = 30)

        now = one_week_later 

        suggestions = db.suggest(customerid, now) 

        for suggestion in suggestions:
          suggestion['latest'] = suggestion['latest'].strftime('%Y-%m-%d')
        self.response.write(json.dumps(suggestions))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug = True)
