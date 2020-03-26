from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy  
from flask_marshmallow import Marshmallow 
import os

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#init db
db = SQLAlchemy(app)

#init Marshmallow
ma = Marshmallow(app)

#Customer Class/model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(6))
    income = db.Column(db.Float)

def __init__(self, name, age, gender, income):
    self.name = name
    self.age = age
    self.gender = gender
    self.income = income

#init schema

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'gender', 'income')

#init schema
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

#create a customer
@app.route('/customer', methods = ['POST'] ) 

def add_customer():
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    income = request.json['income']

    new_customer = Customer( name = name, age = age, gender = gender , income = income)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)
    #return 'Hi'

#Get all customers

@app.route('/customer', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result)

#Get a single customer
@app.route('/customer/<id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get(id)
    return customer_schema.jsonify(customer) 
 


#Update a customer
@app.route('/customer/<id>', methods = ['PUT'] ) 

def update_customer(id):
    customer = Customer.query.get(id)
    name = request.json['name']
    age = request.json['age']
    gender = request.json['gender']
    income = request.json['income']
     
    customer.name = name
    customer.age = age
    customer.gender = gender
    customer.income = income

    db.session.commit()

    return customer_schema.jsonify(customer)

#Delete a single customer
@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer) 
    



#Run Server
if __name__ == '__main__':
    app.run(debug=True)