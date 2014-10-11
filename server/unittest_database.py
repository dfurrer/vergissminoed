#!/usr/bin/env python

from database import Database

def main():
  data_dir = './data'
  db = Database()
  db.load(data_dir)


  customerid =  db.customerids[3]
  purchase = db.pos[customerid][2]

  print purchase
  assert purchase['quantNorm'] == 1
  assert purchase['migrosEan'] == u'7616700197884'

  productid = purchase['migrosEan']
  product = db.products[productid]

  products_without_name = []
  for productid in db.productids:
    if db.products[productid]['name'] == 'Not_specified':
      products_without_name.append(productid)

if __name__ == '__main__':
  main()
