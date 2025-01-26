from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import random
import string
from flask import session, current_app
import os


class Controler:
    def gerar_hash(self, tamanho=16):
        caracteres = string.ascii_letters + string.digits  # Letras maiúsculas, minúsculas e dígitos
        hash_aleatorio = ''.join(random.choice(caracteres) for _ in range(tamanho))
        return hash_aleatorio

    def register_user(self, nome_completo, email, senha, nome_loja, user_type, user_profile_picture, categoria_id):
        from app.models import Vendedor, Comprador
        try:
            random_hash = self.gerar_hash()
            if user_profile_picture:
                with current_app.app_context():
                    app = current_app._get_current_object()
                profile_picture_path = os.path.join(app.config['UPLOAD_USER_PROFILE_FOLDER'], f'{random_hash}.jpg')
                user_profile_picture.save(profile_picture_path)
                profile_image_path = f'user_images/{random_hash}.jpg'
            else:
                profile_image_path = 'user_images/default.jpg'
            
            if user_type == 'seller':
                # Usar diretamente o ID da categoria
                user = Vendedor(
                    nome_completo=nome_completo,
                    email=email,
                    senha_hash=generate_password_hash(senha),
                    nome_loja=nome_loja,
                    random_hash=random_hash,
                    profile_image_path=profile_image_path,
                    categoria_id=int(categoria_id)  # Certifique-se de que é um inteiro
                )
            elif user_type == 'buyer':
                user = Comprador(
                    nome_completo=nome_completo,
                    email=email,
                    senha_hash=generate_password_hash(senha),
                    random_hash=random_hash,
                    profile_image_path=profile_image_path
                )
            
            db.session.add(user)
            db.session.commit()
            return True
        except Exception as e:
            print('Erro ao registrar usuário')
            print(f'Traceback: {e}')
            return False

        
    def login_user(self, email, senha, user_type):
        from app.models import Vendedor, Comprador
        if user_type == 'seller':
            existing_user = Vendedor.query.filter_by(email=email).first()
        elif user_type == 'buyer':
            existing_user = Comprador.query.filter_by(email=email).first()
        if not existing_user:
            return False
        check_pass = check_password_hash(existing_user.senha_hash, senha)
        if check_pass:
            session['user_hash'] = existing_user.random_hash
            session['user_type'] = user_type
            return check_pass
        
    def login_totem(self, nome,senha):
        from app.models import Totem
        existing_user = Totem.query.filter_by(name=nome).first()
        if not existing_user:
            return False
        check_pass = check_password_hash(existing_user.senha, senha)
        if check_pass:
            session['user_type'] = 'totem'
            session['totem_seller_id'] = existing_user.user_id
            session['totem_hash'] = existing_user.random_hash
            return check_pass
