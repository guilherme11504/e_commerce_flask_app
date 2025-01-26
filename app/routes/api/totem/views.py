# views.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.routes.api.totem.controler import Controler
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

totem_bp = Blueprint('totem_bp', __name__)
controler = Controler()

@totem_bp.route('/client_menu', methods=['GET'])
def client_menu():
    totem_hash = session.get('totem_hash')  # Exemplo de como você pode obter o vendedor_hash da sessão
    vendedor_token = controler.get_vendedor_totem(totem_hash)
    # Verificando se temos o random_hash do vendedor na sessão
    if not totem_hash:
        flash("Totem não autenticado.")
        return redirect(url_for('main_bp.login'))

    # Obtendo o vendedor e os produtos associados a ele
    vendedor = controler.get_vendedor_by_hash(vendedor_token.user_id)
    produtos = controler.get_produtos_by_vendedor_hash(vendedor_token.user_id)

    # Renderizando a página com as variáveis vendedor e produtos
    return render_template('client_menu.html', vendedor=vendedor, produtos=produtos)
