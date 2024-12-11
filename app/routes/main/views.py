from flask import Blueprint, render_template, redirect, url_for, request, session,current_app, flash
from app.routes.main.controler import Controler
from app.models import *

controler = Controler()

main_bp =Blueprint('main_bp', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@main_bp.route('/totem_login', methods=['GET'])
def totem_login():
    return render_template('login_totem.html')

@main_bp.route('/select_option', methods=['GET'])
def select_option():
    return render_template('select_option.html')

@main_bp.route('/totem_home', methods=['GET'])
def totem_home():
    return render_template('totem_home.html')

@main_bp.route('/register', methods=['GET'])
def register():
    user_type = request.args.get('user_type')
    return render_template('register.html',user_type=user_type)

@main_bp.route('/main', methods=['GET'])
def main():
    return render_template('main.html')

@main_bp.route('/pedidos', methods=['GET'])
def pedidos():
    return render_template('pedidos.html')

@main_bp.route('/produtos', methods=['GET'])
def produtos():
    produtos = controler.getProdutos()
    return render_template('produtos.html', produtos=produtos)

@main_bp.route('/cadastrar_produto_page', methods=['GET'])
def cadastrar_produto_page():
    try:
        user_hash = session['user_hash']
        categorias = controler.getCategories()
        produtos = controler.getallprodutos(user_hash)
        return render_template('cadastro_produto.html', categorias=categorias,produtos=produtos)
    except:
        flash('Ocorreu um erro ao carregar a página')
        return render_template('produtos.html')

@main_bp.route('/cadastrar_categorias_page', methods=['GET'])
def cadastrar_categorias_page():
    try:
        categorias = controler.getCategories()
        return render_template('cadastro_categoria.html', categorias=categorias)
    except:
        flash('Ocorreu um erro ao carregar a página')
        return render_template('produtos.html')

@main_bp.route('/editar_produto_page', methods=['GET'])
def editar_produto_page():
    user_hash = session['user_hash']
    product_hash = request.args.get('product_hash')
    product = controler.get_product(product_hash)
    categorias = controler.getCategories()
    produtos = controler.getallprodutos(user_hash)
    return render_template('edit_product.html',produto=product,categorias=categorias,produtos=produtos)
