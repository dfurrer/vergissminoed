#!/usr/bin/env python 

import json, requests
import glob
from collections import defaultdict

base_url = 'http://api.autoidlabs.ch/'

def download_data():
  resp = requests.get(url=base_url + 'customerids')
  customerids = json.loads(resp.text)
  records = 0
  for customerid in customerids:
    print 'Customer %s' % customerid
    resp = requests.get(url=base_url + 'pos/' + str(customerid))
    customer_data = json.loads(data)
    open('customerids/%s.json' % customerid, 'w').write(resp.text)  # Dump locally
    print 'User records %s' % len(customer_data)
    records += len(customer_data)
    print 'Total records %s' % records
 
def open_data():
  products_count = defaultdict(int)
  for filename in glob.glob("customerids/*.json"):
    data = open(filename, 'r').read()
    records = json.loads(data)
    for record in records:
      products_count[str(record['migrosEan'])] += 1
  sorted_products = sorted(products_count.iteritems(), key=lambda key_value: key_value[1], reverse=True)
  for i, (id, num) in enumerate(sorted_products):
    resp = requests.get(url=base_url + 'prodarticles/' + str(id))
    try:
      open('prodarticles/%s.json' % id, 'w').write(resp.text)  # Dump locally 
    except UnicodeEncodeError as e:
      pass
    product_data = json.loads(resp.text)
    name = product_data['name'] if 'name' in product_data else 'unknown'
    print '%s, %s (%s): %s' % (i, id, name, num)
    


open_data() 
