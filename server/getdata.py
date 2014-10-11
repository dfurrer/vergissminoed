#!/usr/bin/env python 

import json
import requests
import glob
from collections import defaultdict
#from lxml import html
import time
import os.path

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
  for filename in glob.glob("data/pos/*.json"):
    data = open(filename, 'r').read()
    records = json.loads(data)
    for record in records:
      products_count[str(record['migrosEan'])] += 1
  sorted_products = sorted(products_count.iteritems(), key=lambda key_value: key_value[1], reverse=True)
  for i, (id, num) in enumerate(sorted_products):
    #resp = requests.get(url=base_url + 'prodarticles/' + str(id))
    #try:
    #  open('prodarticles/%s.json' % id, 'w').write(resp.text)  # Dump locally 
    #except UnicodeEncodeError as e:
    #  pass
    #product_data = json.loads(resp.text)
    #name = product_data['name'] if 'name' in product_data else 'unknown'
    #if name == 'unknown':
    cached_filename = str(int(id)) + '.html'
    if os.path.isfile(cached_filename): 
      data = open(cached_filename, 'r').read()
    else:
      page = requests.get('https://produkte.migros.ch/sortiment/supermarkt?q=' + id)
      i = page.text.find('data-itemtype="tpo"')
      i = page.text.rfind('href', 0, i)
      start = page.text.find('"', i)
      end = page.text.find('"', start + 1)
      product_rel_url = page.text[start+1:end]
      print product_rel_url
      page = requests.get('https://produkte.migros.ch' + product_rel_url)
      data = page.text
      #print data
      try:
        open(cached_filename, 'w').write(data)
      except UnicodeEncodeError as e:
        pass      

    start = data.find('class="product-name"') + 20
    end = data.find('<', start)
    name = data[start+1:end]

    #print '%s, %s, %s, %s' % (i, id, name, num)
    print '%s: "%s"' % (id, name)
    time.sleep(5)    


open_data() 
