  
import os
from flask_admin import Admin
from .models import db, Customer, User, Order, Billing, Shipping, LineItem, TaxLine, CouponLine, ShippingLine, FeeLine, Refund
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Customer, db.session))
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Billing, db.session))
    admin.add_view(ModelView(Order, db.session))
    admin.add_view(ModelView(Shipping, db.session))
    admin.add_view(ModelView(LineItem, db.session))
    admin.add_view(ModelView(TaxLine, db.session))
    admin.add_view(ModelView(CouponLine, db.session))
    admin.add_view(ModelView(ShippingLine, db.session))
    admin.add_view(ModelView(FeeLine, db.session))
    admin.add_view(ModelView(Refund, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))