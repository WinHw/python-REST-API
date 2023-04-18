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
  if (request.headers.get('Content-Type') != "application/json"):
    return jsonify({
      'messsage' : 'Please send JSON request.'
    }), 400
  else:
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quantity = request.json['quantity']
    new_product = Product(name, description, price, quantity)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({
      'data' : product_schema.dump(new_product),
      'message' : 'Product storage succeed.'
    }), 201

# get all products endpoint
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  result = products_schema.dump(all_products)
  return jsonify({
    'data' : result,
    'message' : 'Product(s) retrieval succeed.'
  }), 200

# get single product endpoint
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  if (product):
    return jsonify({
      'data': product_schema.dump(product),
      'message': 'Product retrieval succeed.'
    }), 200
  else:
    return jsonify({
      'message' : 'There is no product based on id provided'
    }), 404

# update a product endpoint
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  if (request.headers.get('Content-Type') != "application/json"):
    return jsonify({
      'messsage' : 'Please send JSON request.'
    }), 400
  else:
    product = Product.query.get(id)
    if (product):
      product.name = request.json['name']
      product.description = request.json['description']
      product.price = request.json['price']
      product.quantity = request.json['quantity']
      db.session.commit()
      return jsonify({
        'data': product_schema.dump(product),
        'message': 'Product update succeed.'
      }), 200
    else:
      return jsonify({
        'message' : 'There is no product based on id provided'
      }), 404
      

# delete product endpoint
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  if (product):
    db.session.delete(product)
    db.session.commit()
    return jsonify({
      'data': product_schema.dump(product),
      'message': 'Product deletion succeed.'
    }), 200
  else:
    return jsonify({
      'message' : 'There is no product based on id provided'
    }), 404

# basic route
@app.route('/', methods=['GET'])
def get():
  return jsonify({ 'messages': "You are connected to Flask REST API." })

# run server
if __name__ == '__main__':
  app.run(debug=True)