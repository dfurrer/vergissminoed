# -*- coding: latin-1 -*-

import os
import re
import json
import datetime
import copy
import urllib2

product_names_backfill = {
"7610200035196": "Valflora Milch UHT",
"7617012070261": "Züribieter Vollmilch",
"7613269012146": "Creme zum Kochen",
"7616700018332": "Semmeli",
"7610632984741": "Bio Gurken",
"7616700223910": "Gourmetbrötli",
"7617027551762": "Bio Rispentomaten",
"7617027539036": "Äpfel Gala",
"7610200035202": "Valflora Milch UHT",
"7617027159074": "Kochbutter",
"7610632994122": "Eisbergsalat",
"7610632993613": "Salatgarten Kopfsalat",
"7617027659239": "Kult Ice Tea Zitrone",
"7612300010165": "Floralp Vorzugsbutter",
"7610200380265": "Milch halbentrahmt laktosefrei aha! 1l",
"7617027198455": "Lyoner",
"7617027555975": "Karotten",
"7617027557580": "Zwiebeln",
"7610200388346": "Kartoffeln Amandine",
"7610029037166": "Kult Ice Tea Zitrone",
"7610029014266": "Kult Ice Tea Zitrone",
"7617027541602": "Birnen Williams",
"7617027576994": "Bio Sauerhalbrahm",
"7610632986776": "Kohlrabi",
"7617027552370": "Peperoni rot",
"7617027953184": "M-Budget Nektarinen",
"7617027554763": "Bio Zucchetti",
"7617027633185": "Champignons geschnitten",
"7617300722278": "M-Budget Butter",
"7610200243430": "M-Budget Vollmilch",
"7610200010186": "Gelvite Gelierzucker",
"7610632070444": "Erdbeeren",
"7617027862196": "Bio Rahm past",
"7610200337467": "M-Budget Mineral ohne Co2",
"7610200379351": "Bio Joghurt Erdbeer",
"7610632961407": "Bio Eisbergsalat",
"7613269007234": "M-Budget geschälte Tomaten",
"7610145641308": "M-Classic Senf halb-scharf",
"7613312021422": "Bio Bratbutter",
"7617027617963": "Kalbsbratwurst past Terrasuisse",
"7617027577274": "M-Classic Joghurt Apfel/Mango",
"7617027011853": "Patissier Hefe Getrocknet",
"7616600709866": "M-Budget Rahmquark",
"7617027577144": "M-Classic Joghurt Heidelbeer",
"7617067003221": "Winzerkäse",
"8710496976940": "Hagelslag Schokoladen Streusel",
"7610200307729": "Schweizer Eier Freilandhaltung 53g+",
"22074737": "Valflora Saucenhalbrahm",
"7616600706285": "Bio Himbeerjoghurt",
"7616600711371": "Bifidus Classic",
"7617027556798": "Lauch grün",
"7613312025406": "Eimalzin Milchschokolade",
"7617027577182": "M-Classic Joghurt Birchermüesli",
"7610200040374": "M-Classic HOLL-Rapsöl",
"7617027814287": "Eier einzeln Freilandhaltung 63+",
"7617027804875": "Salat Eier CH Bodenhaltung 6 Stück",
"7610632991428": "Cherrytomaten am Zweig",
"7616600710879": "Passion Joghurt Mango",
"7617027731652": "M-Classic Schweizer Rapsöl",
"7616600710855": "Passion Joghurt Waldbeeren",
"7617027961028": "Joghurt Hazal",
"5000488105339": "Bachblüten Rescue Remedy Tropfen 10 ml",
"7617027552301": "Peperoni grün",
"7610200290335": "Bio Chnöpflimehl",
"7617027823890": "Züribieter Crème Fraîche Nature",
"7617027632133": "Anna&#039;s Best Salade Mégamix",
"7617027577090": "M-Classic Joghurt Classic Nature",
"7610169013327": "Bio Roggenschrotbrot in Scheiben",
"7617027556880": "Blumenkohl",
"7617027953467": "M-Budget Peperoni",
"7613269287247": "M-Classic Joghurt Erdb./Heidelb./Himb.",
"7616700003505": "Tessiner Brot Terrasuisse",
"7613269310006": "Kult Ice Tea Zitrone",
"7613269194156": "M-Budget Salzstangen",
"7616700219982": "Baguette hell",
"7610200232977": "Ostschweizer Eier Bodenhaltung 53+",
"7617067004235": "Emmentaler mild",
"7610200010094": "Kondensmilch gezuckert",
"7617027004022": "Lotus Lütticher Waffeln",
"7617027556538": "Stangensellerie",
"7613269228806": "Kult Ice Tea Zitrone",
"3228020481426": "Président Camembert L&#039;original",
"7613269431923": "Alnatura Roggen Vollkornbrot",
"7610632990971": "Bio Karotten",
"7616700103717": "M-Budget Toast Helles Weizenbrot",
"7616700197884": "Léger Proteinbrot",
"7610632993224": "Kult Ice Tea Zitrone",
"7617027885317": "Coca-Cola",
"7610200313737": "Bio Schweizer Eier Freilandhaltung",
"7617067005751": "Bündner Bergkäse kräftig",
"7610200050847": "M-Classic Maiskörner ungesalzen",
"7610200016966": "M-Classic Schweizer Eier Bodenhaltung",
"7610200069535": "Cherrytomaten"}

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

    # pull with api
    self.api_url = (
      'http://private-anon-df4ab668f-hackzurich2014.apiary-proxy.com')

  def load(self, data_dir):
    pos_dir = os.path.join(data_dir, 'pos')
    pos_filenames = os.listdir(pos_dir)

    for pos_filename in pos_filenames:
      customerid = self.re_json.sub(r'\1', pos_filename)
      with open(os.path.join(pos_dir , pos_filename), 'r') as f:
        if pos_filename == 'flavio.json':
          continue

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

    # sets and lists
    self.customerids = self.pos.keys()
    self.customerids_set = set(self.pos.keys())
    self.productids = self.products.keys()

    # parse dates
    for customerid in self.customerids_set:
      self._parse_purchase_dates(customerid)
    
    # set product names
    for (productid, product) in self.products.iteritems():
      product['name'] = self._product_name(productid)


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
    suggestions = []
    customer_model = self.customer_model[customerid]

    for (productid, product_model) in customer_model.iteritems():
      days = (date - product_model['latest']).days
      if days == 0:
        continue

      stock = float(product_model['last_stock']) - float(days) * product_model['consumption_rate']

      if stock <= 0.0:
        suggestion = copy.copy(product_model)
        suggestion['productid'] = productid
        suggestion['days'] = days
        suggestion['stock'] = stock

        suggestions.append(suggestion)

    def inv_cmp_on_count(me, other):
      return other['count'] - me['count']

    suggestions.sort(inv_cmp_on_count)

    return suggestions

  def _parse_purchase_dates(self, customerid):
    for purchase in self.pos[customerid]:
      if 'date' not in purchase:
        datestr = purchase['rDate']
        purchase['date'] = datetime.datetime.strptime(purchase['rDate'], '%Y-%m-%dT%H:%MZ')



  def pull_pos(self, customerid):
    response = urllib2.urlopen('%s/pos/%s' % (self.api_url, customerid))
    purchases = json.load(response)   
    self.pos[customerid] = purchases
    self._parse_purchase_dates(customerid)

  def _product_name(self, productid):
    if productid not in self.products:
      raise RuntimeError(
        'Product with id % s is not in the database.' % repr(productid))
    product = self.products[productid]
    if 'name' in product:
      return product['name']
    else:
      if productid in product_names_backfill:
        return product_names_backfill[productid]
      return productid
