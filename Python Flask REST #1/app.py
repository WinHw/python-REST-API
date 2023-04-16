# import libraries
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)
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

# basic route
@app.route('/', methods=['GET'])
def get():
  return jsonify({ 'messages': "This is basic route..." })

# run server
if __name__ == '__main__':
  app.run(debug=True)