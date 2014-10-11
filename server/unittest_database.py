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

  # customer model
  db.count_threshold = 2

  # find a customer with max number of purchases
  most_frequent_customer = None
  max_purchases_count = -1
  for (customerid, purchases) in db.pos.iteritems():
    if max_purchases_count < len(purchases):
      most_frequent_customer = customerid
      max_purchases_count = len(purchases)

  # analyze customer
  customerid = most_frequent_customer
  #customerid = 'flavio'
  date_of_last_purchase = db.pos[customerid][-1]['date']

  db.compute_customer_model(customerid)

  print 'Customer: %s' % customerid
  print 'Date of last purchase: %s' % repr(date_of_last_purchase)

  print '\nSuggestions for the one week later:'
  one_week_later = date_of_last_purchase + datetime.timedelta(days = 7)
  assert (one_week_later - date_of_last_purchase).days >= 6

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
