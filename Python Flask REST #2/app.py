# import libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
# init app-2
base_dir = os.path.abspath(os.path.dirname(__file__))

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init marshmallow
ma = Marshmallow(app)

# product class/model
class Product(db.Model):
  # fields
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  quantity = db.Column(db.Integer)
  # constructor
  def __init__(self, name, description, price, quantity):
    self.name = name
    self.description = description
    self.price = price
    self.quantity = quantity

# product schema
class ProductSchema(ma.Schema):
  # fields control
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'quantity')

# init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# create a product endpoint
@app.route('/product', methods=['POST'])
def add_product():
  # retrieve request data/attributes
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  quantity = request.json['quantity']
  # new instance of product model/class
  new_product = Product(name, description, price, quantity)
  # store to database
  db.session.add(new_product)
  db.session.commit()
  # return response
  return product_schema.jsonify(new_product)

# get all products endpoint
@app.route('/product', methods=['GET'])
def get_products():
  # get the products from sqlite
  all_products = Product.query.all()
  # serialize them using schema
  result = products_schema.dump(all_products)
  # return json result
  return jsonify(result)

# get single product endpoint
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  # get the product by id from sqlite
  product = Product.query.get(id)
  # return serialized product as json
  return product_schema.jsonify(product)

# update a product endpoint
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  # get actual product instance by id from sqlite
  product = Product.query.get(id)
  # assign values from request to product instance
  product.name = request.json['name']
  product.description = request.json['description']
  product.price = request.json['price']
  product.quantity = request.json['quantity']
  # update to database
  db.session.commit()
  # return response
  return product_schema.jsonify(product)

# delete product endpoint
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  # get the product by id from sqlite
  product = Product.query.get(id)
  # delete the product instance
  db.session.delete(product)
  # save changes to database
  db.session.commit()
  # return serialized product as json
  return product_schema.jsonify(product)

# basic route
@app.route('/', methods=['GET'])
def get():
  return jsonify({ 'messages': "You are connected to Flask REST API." })

# run server
if __name__ == '__main__':
  app.run(debug=True)