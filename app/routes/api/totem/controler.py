from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session

class Controler:

    def get_vendedor_by_hash(self, user_hash):
        from app.models import Vendedor
        vendedor = Vendedor.query.filter_by(random_hash=user_hash).first()
        return vendedor
    
    def get_produtos_by_vendedor_hash(self, user_hash):
        from app.models import Produto
        produtos = Produto.query.filter_by(vendedor_id=user_hash).all()
        return produtos
    
    def get_vendedor_totem(self, totem_hash):
        from app.models import Totem
        totem = Totem.query.filter_by(random_hash=totem_hash).first()
        return totem
    

