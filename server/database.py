import os
import re
import json


class Database(object):
  def __init__(self):
    self.pos = {}
    self.products = {}
    self.prodarticles = {}
    self.re_json = re.compile(r'^([a-zA-Z_\-0-9]*)\.json$')
    self.customerids = []
    self.productids = []

  def load(self, data_dir):

    pos_dir = os.path.join(data_dir , 'pos')
    pos_filenames = os.listdir(pos_dir)

    for pos_filename in pos_filenames:
      customerid = self.re_json.sub(r'\1', pos_filename)
      with open(os.path.join(pos_dir , pos_filename), 'rt') as f:
        text = f.read()
        self.pos[customerid] = json.loads(text)

  
    prodarticles_dir = os.path.join(data_dir, 'prodarticles')
    prodarticles_filenames = os.listdir(prodarticles_dir)
    for prodarticles_filename in prodarticles_filenames:
      productid = self.re_json.sub(r'\1', prodarticles_filename)
      prodarticles_path = os.path.join(prodarticles_dir, prodarticles_filename)

      with open(prodarticles_path, 'rt') as f:
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
      with open(products_path, 'rt') as f:
        text = f.read()
        if text.strip() == '':
          self.products[productid]={}
        else:
          try:
            self.products[productid] = json.loads(text)
          except:
            print 'File % s could not be parsed.' % products_path
            raise

    self.customerids = self.pos.keys()
    
    for (productid, product) in self.products.iteritems():
      product['name'] = self._product_name(productid)

    for product in self.products.itervalues():
      assert 'name' in product

    self.productids=self.products.keys()


  def _product_name(self, productid):
    if productid not in self.products:
      raise RuntimeError(
        'Product with id % s is not in the database.'% repr(productid))
    product = self.products[productid]
    if 'name' in product:
      return product['name']
    else:
      return 'Not_specified'
