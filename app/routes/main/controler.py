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
    
    def getallprodutos(self, vendedor_hash):
        from app.models import Produto
        produtos = Produto.query.filter_by(vendedor_id=vendedor_hash).all()
        return produtos
    
    def get_product(self,  product_hash):
        from app.models import Produto
        produto = Produto.query.filter_by(random_hash=product_hash).first()
        return produto
