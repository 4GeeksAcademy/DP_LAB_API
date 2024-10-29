from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 


db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    billing = db.Column(db.String(120), nullable=False)  # Se puede cambiar a una relación si se desea
    shipping = db.Column(db.String(120), nullable=False)  # Se puede cambiar a una relación si se desea
    is_paying_customer = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)


    def __repr__(self):
        return f'<Customer {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "username": self.username,
            "billing": self.billing,
            "shipping": self.shipping,
            "is_paying_customer": self.is_paying_customer
            
        }