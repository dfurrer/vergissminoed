#!/usr/bin/env python

import os
import datetime
import copy
import socket

from database import Database

def main():
  hostname = socket.gethostname()
  if hostname == 'hpenvy':
    data_dir='c:\\hackathon\\vergissminoed\\server\\data'
  else:
    raise RuntimeError('Hostname %s has not been handled.' % hostname)

  if not os.path.exists(data_dir):
    raise RuntimeError("Data dir %s does not exist."%repr(data_dir))

  db = Database()
  db.load(data_dir)

  customerid =  db.customerids[3]
  purchase = db.pos[customerid][2]

  assert purchase['quantNorm'] == 1
  assert purchase['migrosEan'] == u'7616700197884'

  productid = purchase['migrosEan']
  product = db.products[productid]

  products_without_name = []
  for productid in db.productids:
    if db.products[productid]['name'] == 'Not_specified':
      products_without_name.append(productid)

  # customer model
  db.count_threshold = 2
  db.compute_all_customer_models()

  # find a customer with max number of purchases
  most_frequent_customer = None
  max_purchases_count = -1
  for (customerid, purchases) in db.pos.iteritems():
    if max_purchases_count < len(purchases):
      most_frequent_customer = customerid
      max_purchases_count = len(purchases)

  customerid = most_frequent_customer
  date_of_last_purchase = db.pos[customerid][-1]['date']

  print 'Most frequent customer: %s' % customerid
  print 'Date of last purchase: %s' % repr(date_of_last_purchase)

  print '\nSuggestions for the one week later:'
  one_week_later = date_of_last_purchase + datetime.timedelta(days = 7)
  suggestions = db.suggest(customerid, one_week_later)

  for suggestion in suggestions:
    suggestion['latest'] = suggestion['latest'].strftime('%Y-%m-%d')
    print repr(suggestion)

  print '\nSuggestions for the one month later:'
  one_month_later = date_of_last_purchase + datetime.timedelta(days = 30)
  suggestions = db.suggest(customerid, one_month_later)

  for suggestion in suggestions:
    suggestion['latest'] = suggestion['latest'].strftime('%Y-%m-%d')
    print repr(suggestion)

if __name__ == '__main__':
  main()
