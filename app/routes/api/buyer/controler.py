from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session,current_app


class Controler:

    def get_sellers(self):
        from app.models import Vendedor
        sellers = Vendedor.query.all()
        return sellers
    
    def get_seller(self, seller_hash):
        from app.models import Vendedor
        seller = Vendedor.query.filter_by(random_hash=seller_hash).first()
        return seller
    
    def get_products(self, seller_hash):
        from app.models import Produto
        products = Produto.query.filter_by(vendedor_id=seller_hash).all()
        return products
    
    


    