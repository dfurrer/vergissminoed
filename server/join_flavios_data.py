#!/usr/bin/env python

import os, sys, re,json
import datetime

def main():
  data_dir = os.path.join(os.path.split(__file__)[0], 'data')

  csv = []
  for i in range(1, 13):
    csv_path = os.path.join(
      data_dir, 'cumulus-sales-slip-overview-details (%d).csv' % i)
    
    with open(csv_path,'r') as f:
      lines = [line for line in f.read().split('\n') \
               if line.strip() != '']
      if i == 1:
        csv.extend(lines)
      else:
        csv.extend(lines[1:])

  pos = []
  for line in lines[1:]:
    parts=line.split(';')
    date=datetime.datetime.strptime(parts[0],'%d.%m.%y')
    time=datetime.datetime.strptime(parts[1],'%H:%M')

    pos.append({
      'name': parts[5],
      'rDate': date.strftime('%Y-%m-%dT') + time.strftime('%H:%MZ'),
      'quant': float(parts[6])
    })

  out_path=os.path.join(data_dir,'pos','flavio.json')
  with open(out_path,'w') as f:
    f.write(json.dumps(pos))

if __name__ == '__main__':
  main()
