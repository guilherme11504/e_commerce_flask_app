from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session


class Controler:
    def gerar_hash(self, tamanho=16):
        caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e dígitos
        hash_aleatorio = ''.join(random.choice(caracteres) for _ in range(tamanho))
        return hash_aleatorio

    def register_user(self, nome_completo, email, nome_usuario, senha, nome_food_truck):
        from app.models import Vendedor
        try:
            vendedor = Vendedor(nome_completo=nome_completo, email=email,nome_usuario=nome_usuario,senha_hash=generate_password_hash(senha), nome_food_truck=nome_food_truck, random_hash=self.gerar_hash())
            db.session.add(vendedor)
            db.session.commit()
            return True
        except Exception as e:
            print(f'erro ao registrar usuario')
            print(f'traceback:{e}')
            return False
        
    def login_user(self, email, senha):
        from app.models import Vendedor
        existing_user = Vendedor.query.filter_by(email=email).first()
        if not existing_user:
            return False
        check_pass = check_password_hash(existing_user.senha_hash, senha)
        if check_pass:
            session['user_hash'] = existing_user.random_hash
            return check_pass
        
    def login_totem(self, nome,senha):
        from app.models import Totem
        existing_user = Totem.query.filter_by(name=nome).first()
        if not existing_user:
            return False
        check_pass = check_password_hash(existing_user.senha, senha)
        if check_pass:
            session['totem_hash'] = existing_user.random_hash
            return check_pass
