# views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.routes.api.config.controler import Controler
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

config_bp = Blueprint('config_bp', __name__)
controler = Controler()

@config_bp.route('/config', methods=['GET', 'POST'])
def config():
    from app.models import Vendedor
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        user_data = {
            'nome_completo':nome, 'email':email
        }
        if controler.update_user_data(user_data):
            flash('Dados atualizados com sucesso!', 'success')
        else:
            flash('Erro ao atualizar dados!', 'danger')
    
    # Carregue os dados do usuário para exibir no formulário
    user_hash = session.get('user_hash')
    user = Vendedor.query.filter_by(random_hash=user_hash).first()
    
    return render_template('config.html', user=user)

@config_bp.route('/register_totem', methods=['GET', 'POST'])
def register_totem():
    if request.method == 'POST':
        senha = request.form['senha']
        cript_senha = generate_password_hash(senha)
        totem_data = {
            'name': request.form['name'],
            'senha': cript_senha,
            'random_hash':controler.gerar_hash()
        }
        if controler.register_totem(totem_data):
            flash('Totem cadastrado com sucesso!', 'success')
            return redirect(url_for('config_bp.config'))
        else:
            flash('Erro ao cadastrar totem!', 'danger')

    return render_template('register_totem.html')
