from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session,current_app, jsonify
import os


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
    
    def get_categorias(self):
        from app.models import Categoria_loja
        categorias = Categoria_loja.query.all()
        categorias_list = []

        for categoria in categorias:
            categoria_id = str(categoria.id)
            
            categorias_list.append({'categoria_nome': categoria.nome_categoria, 'image_path': f'system_images/{categoria_id}.avif', 'id': categoria_id})
        return categorias_list
    
    def get_user_info(self, user_hash):
        from app.models import Comprador
        user = Comprador.query.filter_by(random_hash=user_hash).first()
        user_names_list = user.nome_completo.split(' ')
        first_name = user_names_list[0]
        return jsonify({'user_name':first_name , 'user_email': user.email, 'user_hash': user.random_hash, 'profile_image': user.profile_image_path})
            
    
    


    