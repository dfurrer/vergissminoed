#!/usr/bin/env python

import os, sys, re, json
import datetime

def main():
  data_dir = os.path.join(os.path.split(__file__)[0], 'data')

  csv = []
  for i in range(1, 13):
    csv_path = os.path.join(
      data_dir, 'cumulus-sales-slip-overview-details (%d).csv' % i)
    
    with open(csv_path, 'r') as f:
      lines = [line for line in f.read().split('\n') \
               if line.strip() != '']
      if i == 1:
        csv.extend(lines)
      else:
        csv.extend(lines[1: ])


  pos = []
  product_map = {}
  productid = 0
  for line in csv[1: ]:
    parts = line.split(';')
    date = datetime.datetime.strptime(parts[0], '%d.%m.%y')
    time = datetime.datetime.strptime(parts[1], '%H:%M')
    name = parts[5]
    
    purchase= {
      'name': name,
      'rDate': date.strftime('%Y-%m-%dT') + time.strftime('%H:%MZ'),
      'quantNorm': float(parts[6])
    }

    if purchase['quantNorm'] > 0.0:
      pos.append(purchase)

    if name not in product_map:
      product_map[name] = 'flavio_prod_%d' % productid
      productid += 1

    for purchase in pos:
      purchase['migrosEan'] = product_map[purchase['name']]

  for (name, productid) in product_map.iteritems():
    out_path = os.path.join(data_dir, 'products', '%s.json' % productid)
    with open(out_path, 'w') as f:
      f.write(json.dumps({'name': name}))

  out_path = os.path.join(data_dir, 'pos', 'flavio.json')
  with open(out_path, 'w') as f:
    json_strs = []
    for purchase in pos:
      json_strs.append(json.dumps(purchase))

    f.write('[\n  ' + ',\n  '.join(json_strs) + '\n]')

if __name__ == '__main__':
  main()
