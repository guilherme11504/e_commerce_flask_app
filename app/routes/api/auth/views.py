from flask import Blueprint, request
from app.routes.api.auth.controler import Controler
from flask import render_template, redirect, url_for, session,flash

controler = Controler()

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register_user', methods=['POST'])
def register_user():
    print(request.form.to_dict())
    user_profile_picture = request.files.get('profile_picture')
    user_type = request.form.get('user_type')
    nome_completo = request.form.get('nome_completo')
    email = request.form.get('email')
    senha = request.form.get('senha')
    nome_loja = request.form.get('nome_loja', None)
    categoria_id = request.form.get('categorias_select', None)  # Apenas o ID da categoria
    
    # Passando categoria_id
    result = controler.register_user(nome_completo, email, senha, nome_loja, user_type, user_profile_picture, categoria_id)
    
    if not result:
        error_message = 'Erro ao registrar usuario, tente novamente'
        return render_template('register.html', error_message=error_message)
    return redirect('login')


@auth_bp.route('/login_user', methods=['POST'])
def login_user():
    user_type = request.form.get('user_type')
    email = request.form.get('email')
    senha = request.form.get('senha')
    result = controler.login_user(email,senha,user_type)
    if not result:
        flash('Email e(ou) senha incorretos, Tente novamente')
        return render_template('login.html')
    if user_type == 'seller':
        return redirect('main')
    elif user_type == 'buyer':
        return redirect('buyer_home')

@auth_bp.route('/login_totem', methods=['POST'])
def login_totem():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    result = controler.login_totem(nome, senha)
    if not result:
        flash('Nome de usuario e(ou) senha incorretos, Tente novamente')
        return render_template('login_totem.html')
    return redirect('totem_home')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    #LIMPA TUDO DA SESSÃO
    session.clear()
    return render_template('index.html')



