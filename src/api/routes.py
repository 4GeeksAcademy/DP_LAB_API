"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Customer
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager
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
consumer_key = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
consumer_secret = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')
# # logging.debug(f"Consumer Key: {consumer_key}")
# # logging.debug(f"Consumer Secret: {consumer_secret}")

wcapi = API(
    url="https://imprimefotografia.es",  # Cambia por la URL de tu tienda
    consumer_key=os.getenv('WOOCOMMERCE_CONSUMER_KEY'),  # Coloca tu consumer key
    consumer_secret=os.getenv('WOOCOMMERCE_CONSUMER_SECRET'),  # Coloca tu consumer secret
    version="wc/v3"
)


@api.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()  # Recibir datos del cliente en formato JSON
    
    # Validar que los datos requeridos estén presentes
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    # Crear el nuevo cliente
    customer = Customer(email=email, password=password, is_active=True)
    db.session.add(customer)
    db.session.commit()

    return jsonify({"message": "Customer created successfully", "customer": {"email": customer.email}}), 201

@api.route('/import_customers', methods=['GET'])
def import_customers():
    
    try:
        response = wcapi.get("customers")

        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar customers: {response.text}"}), 400

        wc_customers = response.json()
        print (wc_customers)

        # Verifica que wc_customers sea una lista
        if not isinstance(wc_customers, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_customer in wc_customers:
            
            existing_customer = Customer.query.filter_by(email=wc_customer["email"]).first()

            if not existing_customer:
                
                new_customer = Customer(
                    email=wc_customer["email"],
                    password="default_password",  # Debes manejar la contraseña de forma segura o ser consciente de cómo se van a gestionar.
                    first_name=wc_customer.get("first_name", ""),
                    last_name=wc_customer.get("last_name", ""),
                    role="customer",  # Puedes ajustar según sea necesario
                    username=wc_customer.get("username", ""),
                    billing=wc_customer.get("billing", {}).get("address_1", ""),
                    shipping=wc_customer.get("shipping", {}).get("address_1", ""),
                    is_paying_customer=True,  # Ajusta según tu lógica
                    is_active=True  # O cualquier otro valor según tu lógica
                )
                db.session.add(new_customer)

        db.session.commit()
        return jsonify({"msg": "Customers importados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar customers: {str(e)}"}), 500
    

# @api.route("/login", methods=["POST"])   
# def login():
#     email = request.json.get("email", None)
#     password = request.json.get("password", None)

#     user = User.query.filter_by(email=email).first()
    
#     if user is None:
#         return jsonify({"msg": "No encuentro tu email"}), 401
#     if email != user.email or password != user.password:
#         return jsonify({"msg": "Email o usuario incorrecto"}), 401

#     access_token = create_access_token(identity=email)
#     return jsonify(access_token=access_token)

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

# @api.route("/import_orders", methods=["GET"])
# def import_orders():
#     try:
#         # Obtener órdenes de WooCommerce
#         response = wcapi.get("orders")
        
#         # Verifica si la respuesta es exitosa
#         if response.status_code != 200:
#             return jsonify({"msg": f"Error al importar órdenes: {response.text}"}), 401
        
#         wc_orders = response.json()

#         # Verifica que wc_orders sea una lista
#         if not isinstance(wc_orders, list):
#             return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

#         for wc_order in wc_orders:
#             # Verificar si la orden ya existe en la base de datos
#             existing_order = Order.query.filter_by(id=wc_order["id"]).first()

#             if not existing_order:
#                 # Crear y guardar la orden en la base de datos
#                 new_order = Order(
#                     id=wc_order["id"],
#                     parent_id=wc_order.get("parent_id", 0),
#                     number=wc_order["number"],
#                     order_key=wc_order["order_key"],
#                     created_via=wc_order["created_via"],
#                     status=wc_order["status"],
#                     date_created=wc_order["date_created"],
#                     discount_total=wc_order["discount_total"],
#                     discount_tax=wc_order["discount_tax"],
#                     shipping_total=wc_order["shipping_total"],
#                     total=wc_order["total"],
#                     customer_id=str(wc_order["customer_id"]),
#                     payment_method=wc_order["payment_method"],
#                     total_tax=wc_order["total_tax"]
#                 )
#                 db.session.add(new_order)

#         db.session.commit()
#         return jsonify({"msg": "Órdenes importadas correctamente"}), 200

#     except Exception as e:
#         return jsonify({"msg": f"Error al importar órdenes: {str(e)}"}), 500

   
# @api.route("/orders", methods=["GET"])
# def get_orders():
#     orders = Order.query.all()
#     orders_serialized = [order.serialize() for order in orders]
#     return jsonify(orders_serialized), 200