# views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.routes.api.config.controler import Controler
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
import requests
from dotenv import load_dotenv
import os

load_dotenv()

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

@config_bp.route('/callback', methods=['GET'])
def callback():
    from app import db
    from app.models import MP_token, Vendedor
    vendedor_hash = session.get('user_hash')
    code = request.args.get('code')
    client_id = os.getenv('APP_ID')
    client_secret = os.getenv('ACCESS_TOKEN')
    redirect_uri = os.getenv('REDIRECT_URI')

    vendedor = Vendedor.query.filter_by(random_hash=vendedor_hash).first()

    if not vendedor:
        flash('Vendedor não encontrado!', 'danger')
        return redirect(url_for('config_bp.config'))

    response = requests.post(
        'https://api.mercadopago.com/oauth/token',
        headers={
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded'
        },
        data={
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': client_id
        }
    )

    if response.status_code == 200:
        data = response.json()
        access_token = data.get('access_token')
        token_type = data.get('token_type')
        expires_in = data.get('expires_in')
        user_id = data.get('user_id')

        mp_token = MP_token(
            vendedor_id=vendedor.random_hash,
            access_token=access_token,
            public_key=token_type,
            refresh_token=token_type,
            expires_in=expires_in,
            user_id=user_id

        )

        db.session.add(mp_token)
        db.session.commit()

        flash('Token de acesso obtido com sucesso!', 'success')

        return redirect(url_for('config_bp.config'))
    else:
        flash('Erro ao obter token de acesso!', 'danger')

        return redirect(url_for('config_bp.config'))
