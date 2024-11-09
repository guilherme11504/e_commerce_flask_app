from app import db
import random
import string
from flask import session


class Controler:

    def getProdutos(self):
        from app.models import Produto, Vendedor, Categoria
        user_hash = session['user_hash']
        produtos = db.session.query(Produto, Categoria).join(Categoria, Produto.categoria_id == Categoria.id).filter(Produto.vendedor_id == user_hash).all()
        return produtos
    
    def getCategories(self):
        from app.models import Produto, Vendedor, Categoria
        user_hash = session['user_hash']
        categorias = Categoria.query.filter_by(vendedor_id=user_hash).all()
        return categorias
