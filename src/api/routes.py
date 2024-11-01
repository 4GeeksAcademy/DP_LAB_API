"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Customer, User, Billing, Shipping, Order
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from woocommerce import API
import requests
# import logging

load_dotenv()
# logging.basicConfig(level=logging.DEBUG)

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)
database_url = os.getenv('DATABASE_URL')
consumer_key = os.getenv('WC_CONSUMER_KEY')
consumer_secret = os.getenv('WC_CONSUMER_SECRET')
# # logging.debug(f"Consumer Key: {consumer_key}")
# # logging.debug(f"Consumer Secret: {consumer_secret}")

wcapi = API(
    url="https://imprimefotografia.es",  
    consumer_key=os.getenv('WC_CONSUMER_KEY'),  
    consumer_secret=os.getenv('WC_CONSUMER_SECRET'), 
    version="wc/v3"
)


@api.route('/import_customers', methods=['GET'])
def import_customers():
    try:
        response = wcapi.get("customers")

        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar customers: {response.text}"}), 400

        wc_customers = response.json()

        if not isinstance(wc_customers, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_customer in wc_customers:
            existing_customer = Customer.query.filter_by(email=wc_customer["email"]).first()

            if existing_customer:
                # Actualizar el cliente existente
                existing_customer.first_name = wc_customer.get("first_name", "")
                existing_customer.last_name = wc_customer.get("last_name", "")
                existing_customer.username = wc_customer.get("username", "")
                existing_customer.is_paying_customer = wc_customer.get("is_paying_customer", False)

                # Actualizar datos de facturación
                billing_data = wc_customer.get("billing", {})
                if existing_customer.billing:
                    existing_customer.billing.first_name = billing_data.get("first_name", "")
                    existing_customer.billing.last_name = billing_data.get("last_name", "")
                    existing_customer.billing.company = billing_data.get("company", "")
                    existing_customer.billing.address_1 = billing_data.get("address_1", "")
                    existing_customer.billing.address_2 = billing_data.get("address_2", "")
                    existing_customer.billing.city = billing_data.get("city", "")
                    existing_customer.billing.state = billing_data.get("state", "")
                    existing_customer.billing.postcode = billing_data.get("postcode", "")
                    existing_customer.billing.country = billing_data.get("country", "")
                    existing_customer.billing.email = billing_data.get("email", "")
                    existing_customer.billing.phone = billing_data.get("phone", "")
                else:
                    billing = Billing(
                        first_name=billing_data.get("first_name", ""),
                        last_name=billing_data.get("last_name", ""),
                        company=billing_data.get("company", ""),
                        address_1=billing_data.get("address_1", ""),
                        address_2=billing_data.get("address_2", ""),
                        city=billing_data.get("city", ""),
                        state=billing_data.get("state", ""),
                        postcode=billing_data.get("postcode", ""),
                        country=billing_data.get("country", ""),
                        email=billing_data.get("email", ""),
                        phone=billing_data.get("phone", "")
                    )
                    db.session.add(billing)
                    db.session.flush()
                    existing_customer.billing_id = billing.id

                # Actualizar datos de envío
                shipping_data = wc_customer.get("shipping", {})
                if existing_customer.shipping:
                    existing_customer.shipping.first_name = shipping_data.get("first_name", "")
                    existing_customer.shipping.last_name = shipping_data.get("last_name", "")
                    existing_customer.shipping.company = shipping_data.get("company", "")
                    existing_customer.shipping.address_1 = shipping_data.get("address_1", "")
                    existing_customer.shipping.address_2 = shipping_data.get("address_2", "")
                    existing_customer.shipping.city = shipping_data.get("city", "")
                    existing_customer.shipping.state = shipping_data.get("state", "")
                    existing_customer.shipping.postcode = shipping_data.get("postcode", "")
                    existing_customer.shipping.country = shipping_data.get("country", "")
                else:
                    shipping = Shipping(
                        first_name=shipping_data.get("first_name", ""),
                        last_name=shipping_data.get("last_name", ""),
                        company=shipping_data.get("company", ""),
                        address_1=shipping_data.get("address_1", ""),
                        address_2=shipping_data.get("address_2", ""),
                        city=shipping_data.get("city", ""),
                        state=shipping_data.get("state", ""),
                        postcode=shipping_data.get("postcode", ""),
                        country=shipping_data.get("country", "")
                    )
                    db.session.add(shipping)
                    db.session.flush()
                    existing_customer.shipping_id = shipping.id

            else:
                # Crear un nuevo cliente
                billing_data = wc_customer.get("billing", {})
                billing = Billing(
                    first_name=billing_data.get("first_name", ""),
                    last_name=billing_data.get("last_name", ""),
                    company=billing_data.get("company", ""),
                    address_1=billing_data.get("address_1", ""),
                    address_2=billing_data.get("address_2", ""),
                    city=billing_data.get("city", ""),
                    state=billing_data.get("state", ""),
                    postcode=billing_data.get("postcode", ""),
                    country=billing_data.get("country", ""),
                    email=billing_data.get("email", ""),
                    phone=billing_data.get("phone", "")
                )
                db.session.add(billing)
                db.session.flush()

                shipping_data = wc_customer.get("shipping", {})
                shipping = Shipping(
                    first_name=shipping_data.get("first_name", ""),
                    last_name=shipping_data.get("last_name", ""),
                    company=shipping_data.get("company", ""),
                    address_1=shipping_data.get("address_1", ""),
                    address_2=shipping_data.get("address_2", ""),
                    city=shipping_data.get("city", ""),
                    state=shipping_data.get("state", ""),
                    postcode=shipping_data.get("postcode", ""),
                    country=shipping_data.get("country", "")
                )
                db.session.add(shipping)
                db.session.flush()

                new_customer = Customer(
                    email=wc_customer["email"],
                    password="default_password",
                    first_name=wc_customer.get("first_name", ""),
                    last_name=wc_customer.get("last_name", ""),
                    role="customer",
                    username=wc_customer.get("username", ""),
                    billing_id=billing.id,
                    shipping_id=shipping.id,
                    is_paying_customer=wc_customer.get("is_paying_customer", False),
                )
                db.session.add(new_customer)

        db.session.commit()
        return jsonify({"msg": "Customers importados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar customers: {str(e)}"}), 500
    
@api.route('/customers', methods=['GET'])
def list_customers():
    try:
       
        customers = Customer.query.all()
        customers_serialized = [customer.serialize() for customer in customers]
        
        return jsonify(customers_serialized), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route("/login", methods=["POST"])   
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"msg": "No encuentro tu email"}), 401
    if email != user.email or password != user.password:
        return jsonify({"msg": "Email o usuario incorrecto"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)

# @api.route("/signup", methods=["POST"])
# def signup():
#     body = request.get_json()
#     user = User.query.filter_by(email=body["email"]).first()
    
#     if user is None:
#         user = User(email=body["email"], password=body["password"], is_active=False)
#         db.session.add(user)
#         db.session.commit()
#         response_body = {
#             "msg": "Usuario creado"
#         }
#         return jsonify(response_body), 200
#     else:
#         return jsonify({"msg": "Ya tenemos fichado un cliente con ese correo"}), 401

@api.route("/import_orders", methods=["GET"])
def import_orders():
    try:
        # Obtener órdenes de WooCommerce con un tiempo de espera aumentado
        response = wcapi.get("orders", timeout=30)  # Aumenta el tiempo de espera a 30 segundos
        
        # Verifica si la respuesta es exitosa
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar órdenes: {response.text}"}), 401
        
        wc_orders = response.json()

        # Verifica que wc_orders sea una lista
        if not isinstance(wc_orders, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_order in wc_orders:
            # Verificar si la orden ya existe en la base de datos
            existing_order = Order.query.filter_by(id=wc_order["id"]).first()

            if existing_order:
                # Actualizar la orden existente
                existing_order.parent_id = wc_order.get("parent_id", 0)
                existing_order.number = wc_order["number"]
                existing_order.order_key = wc_order["order_key"]
                existing_order.created_via = wc_order["created_via"]
                existing_order.status = wc_order["status"]
                existing_order.date_created = wc_order["date_created"]
                existing_order.discount_total = wc_order["discount_total"]
                existing_order.discount_tax = wc_order["discount_tax"]
                existing_order.shipping_total = wc_order["shipping_total"]
                existing_order.total = wc_order["total"]
                existing_order.customer_id = str(wc_order["customer_id"])
                existing_order.payment_method = wc_order["payment_method"]
                existing_order.total_tax = wc_order["total_tax"]
            else:
                # Crear y guardar la nueva orden en la base de datos
                new_order = Order(
                    id=wc_order["id"],
                    parent_id=wc_order.get("parent_id", 0),
                    number=wc_order["number"],
                    order_key=wc_order["order_key"],
                    created_via=wc_order["created_via"],
                    status=wc_order["status"],
                    date_created=wc_order["date_created"],
                    discount_total=wc_order["discount_total"],
                    discount_tax=wc_order["discount_tax"],
                    shipping_total=wc_order["shipping_total"],
                    total=wc_order["total"],
                    customer_id=str(wc_order["customer_id"]),
                    payment_method=wc_order["payment_method"],
                    total_tax=wc_order["total_tax"]
                )
                db.session.add(new_order)

        db.session.commit()
        return jsonify({"msg": "Órdenes importadas y actualizadas correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar órdenes: {str(e)}"}), 500
    


@api.route('/customers/<int:customer_id>', methods=['GET'])
def customer_detail(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify(customer.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@api.route('/api/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.serialize() for customer in customers]), 200
    
# @api.route("/orders", methods=["GET"])
# def get_orders():
#     orders = Order.query.all()
#     orders_serialized = [order.serialize() for order in orders]
#     return jsonify(orders_serialized), 200

