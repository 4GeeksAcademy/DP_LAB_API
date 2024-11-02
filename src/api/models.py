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
    billing_id = db.Column(db.Integer, db.ForeignKey('billing.id'), nullable=True)
    shipping_id = db.Column(db.Integer, db.ForeignKey('shipping.id'), nullable=True)
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
    parent_id = db.Column(db.Integer, nullable=False)
    number = db.Column(db.String(80), nullable=False)
    order_key = db.Column(db.String(80), nullable=False)
    created_via = db.Column(db.String(80), nullable=False)
    version = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(80), nullable=False, default='pending')
    currency = db.Column(db.String(3), nullable=False, default='EUR')
    date_modified = db.Column(db.DateTime, onupdate=func.now(), nullable=True)
    date_modified_gmt = db.Column(db.DateTime, onupdate=func.now(), nullable=True)
    discount_total = db.Column(db.String(80), nullable=False)
    discount_tax = db.Column(db.String(80), nullable=False)
    shipping_total = db.Column(db.String(80), nullable=False)
    shipping_tax = db.Column(db.String(80), nullable=True)
    cart_tax = db.Column(db.String(80), nullable=True)
    total = db.Column(db.String(80), nullable=False)
    total_tax = db.Column(db.String(80), nullable=False)
    prices_include_tax = db.Column(db.Boolean, default=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer_ip_address = db.Column(db.String(45), nullable=True)
    customer_user_agent = db.Column(db.String(255), nullable=True)
    customer_note = db.Column(db.Text, nullable=True)
    payment_method = db.Column(db.String(80), nullable=False)
    payment_method_title = db.Column(db.String(80), nullable=True)
    transaction_id = db.Column(db.String(80), nullable=True)
    date_paid = db.Column(db.DateTime, nullable=True)
    date_paid_gmt = db.Column(db.DateTime, nullable=True)
    date_completed = db.Column(db.DateTime, nullable=True)
    date_completed_gmt = db.Column(db.DateTime, nullable=True)
    cart_hash = db.Column(db.String(32), nullable=True)
    set_paid = db.Column(db.Boolean, default=False)

    billing_id = db.Column(db.Integer, db.ForeignKey('billing.id'), nullable=True)
    shipping_id = db.Column(db.Integer, db.ForeignKey('shipping.id'), nullable=True)
    billing = db.relationship('Billing', backref='orders', uselist=False)
    shipping = db.relationship('Shipping', backref='orders', uselist=False)

    line_items = db.relationship('LineItem', backref='order', lazy='dynamic')
    tax_lines = db.relationship('TaxLine', backref='order', lazy='dynamic')
    shipping_lines = db.relationship('ShippingLine', backref='order', lazy='dynamic')
    fee_lines = db.relationship('FeeLine', backref='order', lazy='dynamic')
    coupon_lines = db.relationship('CouponLine', backref='order', lazy='dynamic')
    refunds = db.relationship('Refund', backref='order', lazy='dynamic')

    def __repr__(self):
        return f'<Order {self.number}>'

    def serialize(self):
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "number": self.number,
            "order_key": self.order_key,
            "created_via": self.created_via,
            "version": self.version,
            "status": self.status,
            "currency": self.currency,
            "date_modified": self.date_modified,
            "date_modified_gmt": self.date_modified_gmt,
            "discount_total": self.discount_total,
            "discount_tax": self.discount_tax,
            "shipping_total": self.shipping_total,
            "shipping_tax": self.shipping_tax,
            "cart_tax": self.cart_tax,
            "total": self.total,
            "total_tax": self.total_tax,
            "prices_include_tax": self.prices_include_tax,
            "customer_id": self.customer_id,
            "customer_ip_address": self.customer_ip_address,
            "customer_user_agent": self.customer_user_agent,
            "customer_note": self.customer_note,
            "payment_method": self.payment_method,
            "payment_method_title": self.payment_method_title,
            "transaction_id": self.transaction_id,
            "date_paid": self.date_paid,
            "date_paid_gmt": self.date_paid_gmt,
            "date_completed": self.date_completed,
            "date_completed_gmt": self.date_completed_gmt,
            "cart_hash": self.cart_hash,
            "set_paid": self.set_paid,
            "billing": self.billing.serialize() if self.billing else None,
            "shipping": self.shipping.serialize() if self.shipping else None,
            "customer": self.customer.serialize() if self.customer else None,
            "line_items": [item.serialize() for item in self.line_items],
            "tax_lines": [tax.serialize() for tax in self.tax_lines],
            "shipping_lines": [shipping.serialize() for shipping in self.shipping_lines],
            "fee_lines": [fee.serialize() for fee in self.fee_lines],
            "coupon_lines": [coupon.serialize() for coupon in self.coupon_lines],
            "refunds": [refund.serialize() for refund in self.refunds]
        }

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=True)
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120), nullable=True)
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
    
class LineItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    variation_id = db.Column(db.Integer, nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    tax_class = db.Column(db.String(80), nullable=True)
    subtotal = db.Column(db.String(80), nullable=False)
    subtotal_tax = db.Column(db.String(80), nullable=False)
    total = db.Column(db.String(80), nullable=False)
    total_tax = db.Column(db.String(80), nullable=False)
    sku = db.Column(db.String(80), nullable=True)
    price = db.Column(db.String(80), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "name": self.name,
            "product_id": self.product_id,
            "variation_id": self.variation_id,
            "quantity": self.quantity,
            "tax_class": self.tax_class,
            "subtotal": self.subtotal,
            "subtotal_tax": self.subtotal_tax,
            "total": self.total,
            "total_tax": self.total_tax,
            "sku": self.sku,
            "price": self.price
        }
    
class TaxLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    rate_code = db.Column(db.String(80), nullable=False)
    rate_id = db.Column(db.Integer, nullable=False)
    label = db.Column(db.String(80), nullable=False)
    compound = db.Column(db.Boolean, nullable=False)
    tax_total = db.Column(db.String(80), nullable=False)
    shipping_tax_total = db.Column(db.String(80), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "rate_code": self.rate_code,
            "rate_id": self.rate_id,
            "label": self.label,
            "compound": self.compound,
            "tax_total": self.tax_total,
            "shipping_tax_total": self.shipping_tax_total
        }
    
class CouponLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    code = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.String(80), nullable=False)
    discount_tax = db.Column(db.String(80), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "code": self.code,
            "discount": self.discount,
            "discount_tax": self.discount_tax
        }

class ShippingLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    method_title = db.Column(db.String(80), nullable=False)
    method_id = db.Column(db.String(80), nullable=False)
    total = db.Column(db.String(80), nullable=False)
    total_tax = db.Column(db.String(80), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "method_title": self.method_title,
            "method_id": self.method_id,
            "total": self.total,
            "total_tax": self.total_tax
        }

class FeeLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    tax_class = db.Column(db.String(80), nullable=True)
    tax_status = db.Column(db.String(80), nullable=False)
    total = db.Column(db.String(80), nullable=False)
    total_tax = db.Column(db.String(80), nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "name": self.name,
            "tax_class": self.tax_class,
            "tax_status": self.tax_status,
            "total": self.total,
            "total_tax": self.total_tax
        }

class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    total = db.Column(db.String(80), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "reason": self.reason,
            "total": self.total
        }

class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=True)
    address_1 = db.Column(db.String(120), nullable=False)
    address_2 = db.Column(db.String(120), nullable=True)
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

