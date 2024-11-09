# controller.py
from app import db
from flask import session
import random
import string

class Controler:

    def gerar_hash(self, tamanho=16):
        caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e dígitos
        hash_aleatorio = ''.join(random.choice(caracteres) for _ in range(tamanho))
        return hash_aleatorio

    def update_user_data(self, user_data):
        user_hash = session.get('user_hash')
        from app.models import Vendedor, Categoria
        user = Vendedor.query.filter_by(random_hash=user_hash).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.session.commit()
            return True
        return False

    def register_totem(self, totem_data):
        user_hash = session.get('user_hash')
        from app.models import Vendedor, Categoria, Totem
        user = Vendedor.query.filter_by(random_hash=user_hash).first()
        if user:
            new_totem = Totem(**totem_data, user_id=user.random_hash)  # Atribuindo o login do usuário ao totem
            db.session.add(new_totem)
            db.session.commit()
            return True
        return False
