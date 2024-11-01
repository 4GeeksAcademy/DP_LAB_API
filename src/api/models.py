from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), default="customer")
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_paying_customer = db.Column(db.Boolean, default=False)
    billing_id = db.Column(db.Integer, db.ForeignKey('billing.id'))
    shipping_id = db.Column(db.Integer, db.ForeignKey('shipping.id'))
    billing = db.relationship('Billing', backref='customer', uselist=False)
    shipping = db.relationship('Shipping', backref='customer', uselist=False)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "username": self.username,
            "is_paying_customer": self.is_paying_customer,
            "billing": self.billing.serialize() if self.billing else None,
            "shipping": self.shipping.serialize() if self.shipping else None,
            "orders": [order.serialize() for order in self.orders] if self.orders else []
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, unique=False, nullable=False)
    number = db.Column(db.String(80), unique=False, nullable=False)
    order_key = db.Column(db.String(80), unique=False, nullable=False)
    created_via = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.String(80), unique=False, nullable=False)
    date_created = db.Column(db.String(80), unique=False, nullable=False)
    discount_total = db.Column(db.String(80), unique=False, nullable=False)
    discount_tax = db.Column(db.String(80), unique=False, nullable=False)
    shipping_total = db.Column(db.String(80), unique=False, nullable=False)
    total = db.Column(db.String(80), unique=False, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    payment_method = db.Column(db.String(80), unique=False, nullable=False)
    total_tax = db.Column(db.String(80), unique=False, nullable=False)
   

    def __repr__(self):
        return f'<Order {self.number}>'

    def serialize(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "number": self.number,
            "order_key": self.order_key,
            "created_via": self.created_via,
            "status": self.status,
            "date_created": self.date_created,
            "discount_total": self.discount_total,
            "discount_tax": self.discount_tax,
            "shipping_total": self.shipping_total,
            "total": self.total,
            "customer_id": self.customer_id,
            "payment_method": self.payment_method,
            "total_tax": self.total_tax,
            "customer": self.customer.serialize() if self.customer else None
        }
class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120))
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "address_1": self.address_1,
            "address_2": self.address_2,
            "city": self.city,
            "state": self.state,
            "postcode": self.postcode,
            "country": self.country,
            "email": self.email,
            "phone": self.phone
        }

class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120))
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(3), nullable=False)

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "address_1": self.address_1,
            "address_2": self.address_2,
            "city": self.city,
            "state": self.state,
            "postcode": self.postcode,
            "country": self.country
        }
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
           
        }

