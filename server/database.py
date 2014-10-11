import os
import re
import json
import datetime


class Database(object):
  def __init__(self):
    self.pos = {}
    self.products = {}
    self.prodarticles = {}
    self.re_json = re.compile(r'^([a-zA-Z_\-0-9]*)\.json$')
    self.customerids = []
    self.customerids_set = []
    self.productids = []

    # model
    self.count_threshold = 3
    self.customer_model = {}

  def load(self, data_dir):
    pos_dir = os.path.join(data_dir, 'pos')
    pos_filenames = os.listdir(pos_dir)

    for pos_filename in pos_filenames:
      customerid = self.re_json.sub(r'\1', pos_filename)
      with open(os.path.join(pos_dir , pos_filename), 'r') as f:
        text = f.read()
        self.pos[customerid] = json.loads(text)

  
    prodarticles_dir = os.path.join(data_dir, 'prodarticles')
    prodarticles_filenames = os.listdir(prodarticles_dir)
    for prodarticles_filename in prodarticles_filenames:
      productid = self.re_json.sub(r'\1', prodarticles_filename)
      prodarticles_path = os.path.join(prodarticles_dir, prodarticles_filename)

      with open(prodarticles_path, 'r') as f:
        text = f.read()
        if text.strip() != '':
          try:
            self.prodarticles[productid] = json.loads(text)
          except:
            print 'File % s could not be parsed.' % prodarticles_path
            raise

    products_dir = os.path.join(data_dir , 'products')
    products_filenames = os.listdir(products_dir)
    for products_filename in products_filenames:
      productid = self.re_json.sub(r'\1', products_filename)
      products_path = os.path.join(products_dir, products_filename)
      with open(products_path, 'r') as f:
        text = f.read()
        if text.strip() == '':
          self.products[productid] = {}
        else:
          try:
            self.products[productid] = json.loads(text)
          except:
            print 'File % s could not be parsed.' % products_path
            raise

    self.customerids = self.pos.keys()
    self.customerids_set = set(self.pos.keys())

    # parse dates
    for purchases in self.pos.itervalues():
      for purchase in purchases:
        datestr = purchase['rDate']
        purchase['date'] = datetime.datetime.strptime(purchase['rDate'], '%Y-%m-%dT%H:%MZ')
    
    for (productid, product) in self.products.iteritems():
      product['name'] = self._product_name(productid)

    for product in self.products.itervalues():
      assert 'name' in product

    self.productids = self.products.keys()

  def compute_all_customer_models(self):
    for customerid in self.customerids:
      self.compute_customer_model(customerid)

  def compute_customer_model(self, customerid):
    if customerid not in self.customerids_set:
      raise RuntimeError(
        'Customerid %s is not in the database.' % repr(customerid))

    self.customer_model[customerid] = {}

    product_models = {}

    for purchase in self.pos[customerid]:
      productid = purchase['migrosEan']
      quant = purchase['quantNorm']
      purchase_date = purchase['date']

      if productid not in product_models:
        product_models[productid] = {
          'count': 0,
          'earliest': purchase_date,
          'latest': purchase_date,
          'last_stock': 0,
          'sum_quant': 0
        }

      product_model = product_models[productid]

      product_model['count'] += 1
      product_model['sum_quant'] += quant

      if purchase_date < product_model['earliest']:
        product_model['earliest'] = purchase_date

      if purchase_date >= product_model['latest']:
        product_model['latest'] = purchase_date
        product_model['last_stock'] = quant

    morituri_product_models = []
    for (productid, product_model) in product_models.iteritems():
      if product_model['count'] <= self.count_threshold:
        morituri_product_models.append(productid)

    for productid in morituri_product_models:
      del product_models[productid]

    for (productid, product_model) in product_models.iteritems():
      assert product_model['last_stock'] > 0

      product_model['duration'] = (product_model['latest'] - \
                                   product_model['earliest']).days

      product_model['name'] = self.products[productid]['name']
      product_model['consumption_rate'] = float(product_model['sum_quant']) / \
                                           float(product_model['duration'])
      
      self.customer_model[customerid][productid] = product_model

  def suggest(self, customerid, date):
    if customerid not in self.customer_model:
      return []

    suggestions = []
    customer_model = self.customer_model[customerid]

    for (productid, product_model) in customer_model.iteritems():
      days = (date - product_model['latest']).days
      if days == 0:
        continue

      stock = float(product_model['last_stock']) - float(days) * product_model['consumption_rate']

      if stock <= 0.0:
        suggestions.append({
          'productid': productid, 
          'name': self.products[productid]['name'],
          'last_stock': product_model['last_stock'],
          'latest': product_model['latest'],
          'days': days,
          'stock': float('%.2f' % stock),
          'consumption_rate': float('%.2f' % product_model['consumption_rate'])
        })

    return suggestions

  def _product_name(self, productid):
    if productid not in self.products:
      raise RuntimeError(
        'Product with id % s is not in the database.' % repr(productid))
    product = self.products[productid]
    if 'name' in product:
      return product['name']
    else:
      return 'Not_specified'
