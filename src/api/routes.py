from flask import Flask, request, jsonify, Blueprint
from api.models import db, Customer, Order, LineItem, TaxLine, ShippingLine, FeeLine, CouponLine, Refund, Billing, Shipping, User
from flask_cors import CORS
from woocommerce import API
from dotenv import load_dotenv
import os

load_dotenv()

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api, resources={r"/api/*": {"origins": "*"}})

database_url = os.getenv('DATABASE_URL')
consumer_key = os.getenv('WC_CONSUMER_KEY')
consumer_secret = os.getenv('WC_CONSUMER_SECRET')

wcapi = API(
    url="https://piedrapapelytijeras.es",  
    consumer_key=consumer_key,  
    consumer_secret=consumer_secret, 
    version="wc/v3",
    timeout=30
)

@api.route("/import_customers", methods=["GET"])
def import_customers():
    try:
        response = wcapi.get("customers", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar clientes: {response.text}"}), 401
        
        wc_customers = response.json()

        if not isinstance(wc_customers, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_customer in wc_customers:
            existing_customer = Customer.query.filter_by(id=wc_customer["id"]).first()

            if existing_customer:
                existing_customer.email = wc_customer["email"]
                existing_customer.first_name = wc_customer["first_name"]
                existing_customer.last_name = wc_customer["last_name"]
                existing_customer.role = wc_customer["role"]
                existing_customer.username = wc_customer["username"]
                existing_customer.is_paying_customer = wc_customer["is_paying_customer"]
            else:
                new_customer = Customer(
                    id=wc_customer["id"],
                    email=wc_customer["email"],
                    first_name=wc_customer["first_name"],
                    last_name=wc_customer["last_name"],
                    role=wc_customer["role"],
                    username=wc_customer["username"],
                    password="default_password",
                    is_paying_customer=wc_customer["is_paying_customer"]
                )
                db.session.add(new_customer)

            billing_info = wc_customer.get("billing", {})
            if billing_info:
                billing = Billing.query.filter_by(id=existing_customer.billing_id).first() if existing_customer else None
                if billing:
                    billing.first_name = billing_info["first_name"]
                    billing.last_name = billing_info["last_name"]
                    billing.company = billing_info.get("company")
                    billing.address_1 = billing_info.get("address_1", "")
                    billing.address_2 = billing_info.get("address_2", "")
                    billing.city = billing_info.get("city", "")
                    billing.state = billing_info.get("state", "")
                    billing.postcode = billing_info.get("postcode", "")
                    billing.country = billing_info.get("country", "")
                    billing.email = billing_info.get("email", "")
                    billing.phone = billing_info.get("phone", "")
                else:
                    new_billing = Billing(
                        first_name=billing_info["first_name"],
                        last_name=billing_info["last_name"],
                        company=billing_info.get("company"),
                        address_1=billing_info.get("address_1", ""),
                        address_2=billing_info.get("address_2", ""),
                        city=billing_info.get("city", ""),
                        state=billing_info.get("state", ""),
                        postcode=billing_info.get("postcode", ""),
                        country=billing_info.get("country", ""),
                        email=billing_info.get("email", ""),
                        phone=billing_info.get("phone", "")
                    )
                    db.session.add(new_billing)
                    if existing_customer:
                        existing_customer.billing = new_billing
                    else:
                        new_customer.billing = new_billing

            shipping_info = wc_customer.get("shipping", {})
            if shipping_info:
                shipping = Shipping.query.filter_by(id=existing_customer.shipping_id).first() if existing_customer else None
                if shipping:
                    shipping.first_name = shipping_info["first_name"]
                    shipping.last_name = shipping_info["last_name"]
                    shipping.company = shipping_info.get("company")
                    shipping.address_1 = shipping_info.get("address_1", "")
                    shipping.address_2 = shipping_info.get("address_2", "")
                    shipping.city = shipping_info.get("city", "")
                    shipping.state = shipping_info.get("state", "")
                    shipping.postcode = shipping_info.get("postcode", "")
                    shipping.country = shipping_info.get("country", "")
                else:
                    new_shipping = Shipping(
                        first_name=shipping_info["first_name"],
                        last_name=shipping_info["last_name"],
                        company=shipping_info.get("company"),
                        address_1=shipping_info.get("address_1", ""),
                        address_2=shipping_info.get("address_2", ""),
                        city=shipping_info.get("city", ""),
                        state=shipping_info.get("state", ""),
                        postcode=shipping_info.get("postcode", ""),
                        country=shipping_info.get("country", "")
                    )
                    db.session.add(new_shipping)
                    if existing_customer:
                        existing_customer.shipping = new_shipping
                    else:
                        new_customer.shipping = new_shipping

        db.session.commit()
        return jsonify({"msg": "Clientes importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar clientes: {str(e)}"}), 500

@api.route("/import_orders", methods=["GET"])
def import_orders():
    try:
        response = wcapi.get("orders", params={"per_page": 100, "page": 1})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar órdenes: {response.text}"}), 401
        
        wc_orders = response.json()

        if not isinstance(wc_orders, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_order in wc_orders:
            customer_id = wc_order["customer_id"]
            customer = Customer.query.filter_by(id=customer_id).first()

            if not customer:
                # Si el cliente no existe, omitir la orden o crear un nuevo cliente
                continue

            existing_order = Order.query.filter_by(id=wc_order["id"]).first()

            billing_info = wc_order.get("billing", {})
            shipping_info = wc_order.get("shipping", {})

            if billing_info:
                billing = Billing.query.filter_by(
                    first_name=billing_info["first_name"],
                    last_name=billing_info["last_name"],
                    address_1=billing_info["address_1"]
                ).first()
                if not billing:
                    billing = Billing(
                        first_name=billing_info["first_name"],
                        last_name=billing_info["last_name"],
                        company=billing_info.get("company"),
                        address_1=billing_info.get("address_1", ""),
                        address_2=billing_info.get("address_2", ""),
                        city=billing_info.get("city", ""),
                        state=billing_info.get("state", ""),
                        postcode=billing_info.get("postcode", ""),
                        country=billing_info.get("country", ""),
                        email=billing_info.get("email", ""),
                        phone=billing_info.get("phone", "")
                    )
                    db.session.add(billing)

            if shipping_info:
                shipping = Shipping.query.filter_by(
                    first_name=shipping_info["first_name"],
                    last_name=shipping_info["last_name"],
                    address_1=shipping_info["address_1"]
                ).first()
                if not shipping:
                    shipping = Shipping(
                        first_name=shipping_info["first_name"],
                        last_name=shipping_info["last_name"],
                        company=shipping_info.get("company"),
                        address_1=shipping_info.get("address_1", ""),
                        address_2=shipping_info.get("address_2", ""),
                        city=shipping_info.get("city", ""),
                        state=shipping_info.get("state", ""),
                        postcode=shipping_info.get("postcode", ""),
                        country=shipping_info.get("country", "")
                    )
                    db.session.add(shipping)


            if existing_order:
                existing_order.number = wc_order["number"]
                existing_order.status = wc_order["status"]
                existing_order.total = wc_order["total"]
                existing_order.customer_id = wc_order["customer_id"]
                existing_order.billing = billing
                existing_order.shipping = shipping
            else:
                new_order = Order(
                    id=wc_order["id"],
                    number=wc_order["number"],
                    status=wc_order["status"],
                    total=wc_order["total"],
                    customer_id=wc_order["customer_id"],
                    billing=billing,
                    shipping=shipping
                )
                db.session.add(new_order)

        db.session.commit()
        return jsonify({"msg": "Órdenes importadas y actualizadas correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar órdenes: {str(e)}"}), 500
    
@api.route("/import_line_items", methods=["GET"])
def import_line_items():
    try:
        response = wcapi.get("line_items", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar line items: {response.text}"}), 401
        
        wc_line_items = response.json()

        if not isinstance(wc_line_items, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_line_item in wc_line_items:
            existing_line_item = LineItem.query.filter_by(id=wc_line_item["id"]).first()

            if existing_line_item:
                existing_line_item.name = wc_line_item["name"]
                existing_line_item.product_id = wc_line_item["product_id"]
                existing_line_item.variation_id = wc_line_item["variation_id"]
                existing_line_item.quantity = wc_line_item["quantity"]
                existing_line_item.tax_class = wc_line_item["tax_class"]
                existing_line_item.subtotal = wc_line_item["subtotal"]
                existing_line_item.subtotal_tax = wc_line_item["subtotal_tax"]
                existing_line_item.total = wc_line_item["total"]
                existing_line_item.total_tax = wc_line_item["total_tax"]
                existing_line_item.price = wc_line_item["price"]
            else:
                new_line_item = LineItem(
                    id=wc_line_item["id"],
                    name=wc_line_item["name"],
                    product_id=wc_line_item["product_id"],
                    variation_id=wc_line_item["variation_id"],
                    quantity=wc_line_item["quantity"],
                    tax_class=wc_line_item["tax_class"],
                    subtotal=wc_line_item["subtotal"],
                    subtotal_tax=wc_line_item["subtotal_tax"],
                    total=wc_line_item["total"],
                    total_tax=wc_line_item["total_tax"],
                    price=wc_line_item["price"]
                )
                db.session.add(new_line_item)

        db.session.commit()
        return jsonify({"msg": "Line items importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar line items: {str(e)}"}), 500

@api.route("/import_tax_lines", methods=["GET"])
def import_tax_lines():
    try:
        response = wcapi.get("tax_lines", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar tax lines: {response.text}"}), 401
        
        wc_tax_lines = response.json()

        if not isinstance(wc_tax_lines, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_tax_line in wc_tax_lines:
            existing_tax_line = TaxLine.query.filter_by(id=wc_tax_line["id"]).first()

            if existing_tax_line:
                existing_tax_line.rate_code = wc_tax_line["rate_code"]
                existing_tax_line.rate_id = wc_tax_line["rate_id"]
                existing_tax_line.label = wc_tax_line["label"]
                existing_tax_line.compound = wc_tax_line["compound"]
                existing_tax_line.tax_total = wc_tax_line["tax_total"]
                existing_tax_line.shipping_tax_total = wc_tax_line["shipping_tax_total"]
            else:
                new_tax_line = TaxLine(
                    id=wc_tax_line["id"],
                    rate_code=wc_tax_line["rate_code"],
                    rate_id=wc_tax_line["rate_id"],
                    label=wc_tax_line["label"],
                    compound=wc_tax_line["compound"],
                    tax_total=wc_tax_line["tax_total"],
                    shipping_tax_total=wc_tax_line["shipping_tax_total"]
                )
                db.session.add(new_tax_line)

        db.session.commit()
        return jsonify({"msg": "Tax lines importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar tax lines: {str(e)}"}), 500

@api.route("/import_shipping_lines", methods=["GET"])
def import_shipping_lines():
    try:
        response = wcapi.get("shipping_lines", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar shipping lines: {response.text}"}), 401
        
        wc_shipping_lines = response.json()

        if not isinstance(wc_shipping_lines, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_shipping_line in wc_shipping_lines:
            existing_shipping_line = ShippingLine.query.filter_by(id=wc_shipping_line["id"]).first()

            if existing_shipping_line:
                existing_shipping_line.method_title = wc_shipping_line["method_title"]
                existing_shipping_line.method_id = wc_shipping_line["method_id"]
                existing_shipping_line.total = wc_shipping_line["total"]
                existing_shipping_line.total_tax = wc_shipping_line["total_tax"]
            else:
                new_shipping_line = ShippingLine(
                    id=wc_shipping_line["id"],
                    method_title=wc_shipping_line["method_title"],
                    method_id=wc_shipping_line["method_id"],
                    total=wc_shipping_line["total"],
                    total_tax=wc_shipping_line["total_tax"]
                )
                db.session.add(new_shipping_line)

        db.session.commit()
        return jsonify({"msg": "Shipping lines importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar shipping lines: {str(e)}"}), 500

@api.route("/import_fee_lines", methods=["GET"])
def import_fee_lines():
    try:
        response = wcapi.get("fee_lines", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar fee lines: {response.text}"}), 401
        
        wc_fee_lines = response.json()

        if not isinstance(wc_fee_lines, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_fee_line in wc_fee_lines:
            existing_fee_line = FeeLine.query.filter_by(id=wc_fee_line["id"]).first()

            if existing_fee_line:
                existing_fee_line.name = wc_fee_line["name"]
                existing_fee_line.tax_class = wc_fee_line["tax_class"]
                existing_fee_line.tax_status = wc_fee_line["tax_status"]
                existing_fee_line.amount = wc_fee_line["amount"]
                existing_fee_line.total = wc_fee_line["total"]
                existing_fee_line.total_tax = wc_fee_line["total_tax"]
            else:
                new_fee_line = FeeLine(
                    id=wc_fee_line["id"],
                    name=wc_fee_line["name"],
                    tax_class=wc_fee_line["tax_class"],
                    tax_status=wc_fee_line["tax_status"],
                    amount=wc_fee_line["amount"],
                    total=wc_fee_line["total"],
                    total_tax=wc_fee_line["total_tax"]
                )
                db.session.add(new_fee_line)

        db.session.commit()
        return jsonify({"msg": "Fee lines importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar fee lines: {str(e)}"}), 500

@api.route("/import_coupon_lines", methods=["GET"])
def import_coupon_lines():
    try:
        response = wcapi.get("coupon_lines", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar coupon lines: {response.text}"}), 401
        
        wc_coupon_lines = response.json()

        if not isinstance(wc_coupon_lines, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_coupon_line in wc_coupon_lines:
            existing_coupon_line = CouponLine.query.filter_by(id=wc_coupon_line["id"]).first()

            if existing_coupon_line:
                existing_coupon_line.code = wc_coupon_line["code"]
                existing_coupon_line.discount = wc_coupon_line["discount"]
                existing_coupon_line.discount_tax = wc_coupon_line["discount_tax"]
            else:
                new_coupon_line = CouponLine(
                    id=wc_coupon_line["id"],
                    code=wc_coupon_line["code"],
                    discount=wc_coupon_line["discount"],
                    discount_tax=wc_coupon_line["discount_tax"]
                )
                db.session.add(new_coupon_line)

        db.session.commit()
        return jsonify({"msg": "Coupon lines importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar coupon lines: {str(e)}"}), 500

@api.route("/import_refunds", methods=["GET"])
def import_refunds():
    try:
        response = wcapi.get("refunds", params={"timeout": 30})
        
        if response.status_code != 200:
            return jsonify({"msg": f"Error al importar refunds: {response.text}"}), 401
        
        wc_refunds = response.json()

        if not isinstance(wc_refunds, list):
            return jsonify({"msg": "Error: formato de respuesta inesperado"}), 400

        for wc_refund in wc_refunds:
            existing_refund = Refund.query.filter_by(id=wc_refund["id"]).first()

            if existing_refund:
                existing_refund.reason = wc_refund["reason"]
                existing_refund.total = wc_refund["total"]
            else:
                new_refund = Refund(
                    id=wc_refund["id"],
                    reason=wc_refund["reason"],
                    total=wc_refund["total"]
                )
                db.session.add(new_refund)

        db.session.commit()
        return jsonify({"msg": "Refunds importados y actualizados correctamente"}), 200

    except Exception as e:
        return jsonify({"msg": f"Error al importar refunds: {str(e)}"}), 500

@api.route('/customers/<int:customer_id>', methods=['GET'])
def customer_detail(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        return jsonify(customer.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/api/orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([order.serialize() for order in orders]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@api.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 25, type=int)
        customers_query = Customer.query.paginate(page, limit, False)
        
        customers = customers_query.items
        total_pages = customers_query.pages
        
        return jsonify({
            "customers": [customer.serialize() for customer in customers],
            "totalPages": total_pages
        }), 200
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